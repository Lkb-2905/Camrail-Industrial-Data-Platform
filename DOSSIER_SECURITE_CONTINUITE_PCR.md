🔰 DOSSIER DE SÉCURITÉ ET CONTINUITÉ (PCR/PRA)
⚡ E2E-IDP : Camrail Industrial Data Platform (End-to-End)
Gestion de Crise • Continuité Logistique • Intégrité Base de Données • Résilience IA

Classification: Confidentiel (Interne Camrail / Bolloré Logistics) | Version: 1.0.0
Responsable: KAMENI TCHOUATCHEU GAETAN BRUNEL

🔍 Analyse BIA • 🛡️ Stratégies PCA • 🔄 Procédures PRA • 📝 Maintenance MCO

---

## 📋 TABLE DES MATIÈRES
1. [Contexte & Enjeux Critiques](#-contexte-et-enjeux-critiques)
2. [Analyse d'Impact Métier (BIA)](#-analyse-dimpact-métier-bia)
3. [Stratégies de Continuité (PCA)](#️-stratégies-de-continuité-pca)
4. [Procédures de Reprise (PRA)](#-procédures-de-reprise-pra)
5. [Maintenance & Tests (MCO)](#-maintenance--tests-mco)
6. [Annexe Technique](#-annexe-technique)

---

## 🚨 CONTEXTE ET ENJEUX CRITIQUES
Ce plan définit la stratégie de résilience opérationnelle globale de la **Plateforme Industrielle (E2E-IDP)**.
En tant qu'architecture End-to-End (combinant Data Engineering, Base de données SQL, et Serveur de Machine Learning algorithmique), la surface de risque s'étend et la gravité croît. Si l'Orchestrateur Python Maître s'effondre pendant un run de nuit à 2h00 AM, tout le site est paralysé à l'aube.

**Objectifs du PCR :**
* **Fiabilité des Flux ETL :** Assurer que la collecte des données massives par lots ne bloque pas (Deadlocks Base d'Écriture).
* **Intégrité IA :** Assurer que des données corrompues de l'ETL ne viennent pas "empoisonner" *(Data Poisoning)* le modèle Random Forest enchaîné juste derrière.
* **Tolérance à la Panne (Graceful Degradation) :** Pouvoir servir les anciens indicateurs (J-1) au Power BI du gestionnaire si la chaîne matinale échoue.

---

## 🔍 ANALYSE D'IMPACT MÉTIER (BIA)

### Cartographie des Risques Unifiés (ETL + IA)
| Menace Identifiée | Probabilité | Impact Métier | Sévérité |
| :--- | :--- | :--- | :--- |
| **API Capteurs Injoignable (ETL_Fail)** | Élevée (3/5) | Extraction asynchrone stoppée, métriques `NaN`, chaîne Data Science non déclenchée. | 🟠 Majeur |
| **Panne de Mémoire Vive (RAM OutOfMemory DS)** | Moyenne (2/5) | Crash du Serveur lors du `model.fit()` ou lors de l'assemblage Pandas. | 🟠 Majeur |
| **Base SQLite Verrouillée (Lock DWH)** | Faible (1/5) | Impossible de Load l'ETL ou les prédictions IA dans la base de données. | 🔴 Critique |
| **Corrélation Fallacieuse Modèle (Data Drift)**| Très Faible | L'Orchestrateur accomplit sa tâche avec succès mais l'IA renvoie de mauvaises cotes à 100%. | 🔴 Critique |

### Métriques de Performance (SLA)
* **RTO (Recovery Time Objective) : < 30 minutes.**
  Le pipeline doit pouvoir redémarrer proprement si un verrou de process Python est abattu.
* **RPO (Recovery Point Objective) : Temps des Signaux Capteurs.**
  Chagrin limité par run.

---

## 🛡️ STRATÉGIES DE CONTINUITÉ (PCA)
Le système a été écrit avec du code structuré "Failover-by-Design".

### 1. Isolation Hermétique des Run (Safety Net Global)
Dans l'orchestrateur `run_industrial_platform.py`, le passage de la `Phase 1 Data Engineering` à la `Phase 2 Data Science` inclut une validation contextuelle `try-except` de bloc.
* ⚡ **Mode Nominal :** L'ETL insère dans SQLite. Une fois clos, l'IA reprend la main et lie la base de données pour insérer les tableaux de scores.
* 🚨 **Incident Détecté :** Le script d'Extraction ou Transformation `KeyError` au milieu du Batch.
* 🔄 **Basculement Auto :** L'orchestrateur attrape l'erreur, logue un `CRITICAL_ERROR` coloré dans `.log`, et coupe l'exécution proprement via `sys.exit(1)`. L'IA ne s'entraînera donc **PAS** sur une table SQL avariée ou mi-chargée, les décisionnels (Power BI) resteront sur le tableau SQL intact de la veille J-1.

### 2. Le Maintien Transactionnel SQL (SQL Load)
Les données traitées de Pandas transitent vers la base de données via `df_processed.to_sql("...", engine, if_exists="replace")`. Ceci assure que SQLite met l'opération entièrement en tampon. Si une mini-coupure électrique ou serveur interrompt ce petit laps de temps, SQLAlchemy reverte le buffer, conservant la SSOT ("Single source of truth") du Data Warehouse intacte.

---

## 🔄 PROCÉDURES DE REPRISE (PRA)
En cas de crash de l'architecture nécessitant un redémarrage manuel d'urgence (Crash VM pendant la nuit par exemple).

### 4.1. Protocole de Reprise Manuelle Batch "GLOBAL REBOOT" (PowerShell)
Si le Directeur signale que Power BI n'a pas bougé depuis 24h, et vérification par logue :

```powershell
# SCRIPT DE REPRISE ARCHITECTURE GLOBALE E2E (E2E-IDP)

# 1. Kill et Vérification des verrous (Locks) Python asynchrones
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Write-Host "✅ Nettoyage Processus Suspendus Applicatif Python (ETL+IA)."

# 2. Back-up immédiat du Data Warehouse avant intervention
Copy-Item "database/industrial_dwh.sqlite" "database/industrial_dwh_SAFE.sqlite" -ErrorAction SilentlyContinue
Write-Host "✅ Sandbox Data Warehouse sécurisée."

# 3. Lancement d'Hivernage (Reborn)
cd "C:\chemin\vers\Camrail-Industrial-Data-Platform"
.\env\Scripts\activate
# Exécution du Master
python run_industrial_platform.py
Write-Host "🚀 Processus d'usine redemarré. Vérifier la console d'historique des Logs Loguru pour les alertes."
```

### 4.2. Stratégie de Sauvegarde (Backup)
* **Code Source & Configuration :** Maintenu et tracé scrupuleusement sous `Git/GitHub` (GitHub repos : Camrail-Industrial-Data-Platform).
* **Base Données Warehouse (SGBD) :** Les fichiers `.sqlite` et modèles `.joblib` doivent faire l'objet de plans de capture disque (Snapshot SAN) par le DSI une fois par semaine.

---

## 📝 MAINTENANCE & TESTS (MCO)
S'assurer de la solidité du pipeline complet sous charge.

### Scénarios de Test (Réalisés chaque trimestre)
1. **"Corruption ETL Test" :**
   * *Action :* Dans `extract.py`, lever intentionnellement un `Exception("Crash Simulé API Météo/IOT")`.
   * *Attendu :* L'orchestrateur logue l'erreur, abandonne `Phase 1`, et n'exécute JAMAIS `Phase 2` et ne modifie PAS `industrial_dwh.sqlite`. Les clients (Power BI) ne remarquent rien d'autre que l'absence de nouvelle donnée matinale fraîche.
2. **"Deadlock DataBase Test" :**
   * *Action :* Ouvrir manuellement `industrial_dwh.sqlite` avec DBBrowser for SQLite, commencer une modification de la table des faits, ne pas la relâcher (Commit DB Locké) et lancer le Master Python Master.
   * *Attendu :* SQLAlchemy gère le Timeout sur la tentative de Load (`load.py`) et lève le message approprié sans provoquer d'écran bleu système.

---

## 🔧 ANNEXE TECHNIQUE
### Contacts d'Astreinte
* **Responsable Technique :** Kameni Tchouatcheu (Ext. 06.XX.XX.XX.XX)
* **Ingénierie & Architecture Data :** support-data-science@camrail.net

### Versions Validées en Production (Stack Fixée)
* **Python Environnement :** 3.12.x
* **Numpy :** STRICTEMENT 1.26.0 (Évitant de casser l'interpénétration Pandas C-Headers)
* **Scikit-Learn/Joblib :** STRICTEMENT Ancres respectives, 1.3.1 et 1.3.2 (Binarisation algorithmes IA).
* **SQLAlchemy :** 2.0+

*Ce document est la propriété de la Direction Logistique Ferroviaire (Data Department). Dernière mise à jour : Février 2026 par G.B.K.T.*
