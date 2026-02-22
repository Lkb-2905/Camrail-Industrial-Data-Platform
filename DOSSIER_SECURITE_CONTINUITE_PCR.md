🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ CIDP PCR : Industrial Data Platform (Sécurité E2E)
![Sécurité](https://img.shields.io/badge/Plan-Continuité-red) ![SQL](https://img.shields.io/badge/SQL-Intégrité-blue) ![Qualité](https://img.shields.io/badge/Qualité-ITIL-yellow)

**Version:** 1.0.0 Stable | **Date:** Février 2026  
**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Contact:** gaetanbrunel.kamenitchouatcheu@et.esiea.fr  

🚀 [Démarrage Rapide](#-démarrage-rapide) • 📚 [Documentation](#-guide-dutilisation) • 🎯 [Fonctionnalités](#-fonctionnalités-clés) • 🔧 [Installation](#-installation-rapide)

---

## 📋 TABLE DES MATIÈRES
1. [Vue d'ensemble du projet](#-vue-densemble-du-projet)
2. [Architecture Technique (Menaces)](#️-architecture-technique)
3. [Stack Technologique & PCA](#️-stack-technologique)
4. [Fonctionnalités Clés (Reprise)](#-fonctionnalités-clés)
5. [Démarrage Rapide](#-démarrage-rapide)
6. [Guide d'Utilisation](#-guide-dutilisation)
7. [Qualité & Best Practices](#-qualité--best-practices)
8. [Roadmap & Évolutions](#️-roadmap--évolutions)

---

## 🎯 VUE D'ENSEMBLE DU PROJET

### Contexte & Objectifs
Ce document définit la stratégie complète de résilience opérationnelle et le **Plan de Continuité d'Activité (PCA)** de l'usine End-to-End **CIDP**.
Si l'Orchestrateur Python Maître s'effondre pendant un run de nuit à 2h00 AM, tout le site est paralysé à l'aube.

Il illustre de A à Z les compétences absolues suivantes :

✅ **Architecture de Continuité :** Le script bloque l'IA en cas de données tronquées par un appel API externe mort.
✅ **Data Science Sécurisée :** Prévention du "Data Poisoning" (Base de données falsifiée par l'ETL).
✅ **Automatisation d'Urgence :** Lancement du Cold Restart.
✅ **Data Reliability :** Garantie de la cohérence de log avec `Loguru`.

### Pourquoi ce projet ?
| Aspect | Démonstration |
| --- | --- |
| **Scalabilité** | Architecture résiliente End-to-End face aux goulets réseau. |
| **Maintenabilité** | Centralisation du monitoring asynchrone pour faciliter l'astreinte N2. |
| **Sécurité** | Tolérance aux faiblesses réseaux via Fail-Safe SQL. |

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Flux de Données Détaillé (BIA)
| Menace Identifiée | Probabilité | Impact Métier | Sévérité |
| --- | --- | --- | --- |
| **API Capteurs Injoignable** | Élevée (3/5) | Extraction asynchrone stoppée, métriques `NaN`, chaîne Data Science non déclenchée. | 🟠 Majeur |
| **Panne de Mémoire Vive RAM** | Moyenne (2/5) | Crash du Serveur lors de l'assemblage Pandas. | 🟠 Majeur |
| **Base SQLite Verrouillée** | Faible (1/5) | Impossible d'insérer l'ETL (Data Warehouse Lock). | 🔴 Critique |
| **Data Drift (Modèle Biaisé)** | Très Faible | L'IA calcule des faux positifs sur la télémétrie. | 🔴 Critique |

---

## 🛠️ STACK TECHNOLOGIQUE

### Stratégies de Continuité (PCA)
* **Failover-by-Design** : L'orchestrateur attrape les exceptions levées par l'ETL (`try-except`). Il coupe l'exécution logicielle (`sys.exit(1)`) **AVANT** l'entraînement de l'Intelligence Artificielle. Le Dashboard PowerBI n'affichera donc aucune fausse probabilité de casse de train.

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Procédures de Reprise (PRA)
**Reprise et Cold Reboot Global**
Lors d'une crise asynchrone complète, purger tous les processus mémoires Python et restaurer la DB à froid.

### 🛡️ Sécurité & Robustesse
| Aspect | Implémentation |
| --- | --- |
| **Résilience** | SQLAlchemy sécurise les accès fichiers SQLite par pool d'horloge (time out). |

---

## 🚀 DÉMARRAGE RAPIDE

### Installation Express (Reprise Cold Reboot)
```powershell
# 1. Kill et Vérification des verrous (Locks) Python asynchrones
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue

# 2. Back-up immédiat du Data Warehouse avant intervention
Copy-Item "database/industrial_dwh.sqlite" "database/industrial_dwh_SAFE.sqlite" -ErrorAction SilentlyContinue

# 3. Lancement d'Hivernage (Reborn)
cd "C:\chemin\vers\Camrail-Industrial-Data-Platform"
.\env\Scripts\activate
python run_industrial_platform.py

Write-Host "🚀 Processus global de l'usine relancé. Le DWH est sécurisé."
```

---

## 📖 GUIDE D'UTILISATION

### Scénario d'Astreinte (Contacts)
* **Responsable Technique :** Kameni Tchouatcheu (Ext. 06.XX.XX.XX.XX)
* **Ingénierie Master Data :** support-data-science@camrail.net
* **Procédure :** Lancer le script de PRA (Cold Reboot).

---

## ✨ QUALITÉ & BEST PRACTICES

### Standards Tests E2E (MCO)
* **Failures Scénarios :** Les Tests de corruption métier (Lever une Exception purement artificielle dans `extract.py`) sont menés chaque trimestre pour s'assurer que le script s'interrompt convenablement en amont de `model.fit()`.

### Métriques d'Excellence
✅ **Performance :** L'arrêt du programme en cas de crise protège instantanément la BDD en `O(1)`.

---

## 🗺️ ROADMAP & ÉVOLUTIONS

**Version Actuelle : 1.0.0 ✅**
* PCA/PRA opérationnel par scripts centralisés et architecture découplée.

**Version 2.0.0 🚧**
* Ajout de bascules de réseau vers des Clusters secondaires (Azure) pour résilience SQL suprême.

---

## 🤝 CONTRIBUTION
*Interdit. (Lecture seule pour la cellule de crise ITSM et la Direction des Données Industrielles)*.

---

## 📄 LICENCE
Ce projet est Confidentiel. Réservé à un usage académique ESIEA et professionnel au sein du Groupe Bolloré / Camrail.

## 👨‍💻 AUTEUR
**KAMENI TCHOUATCHEU GAETAN BRUNEL**  
Ingénieur Logiciel & Data Scientist en devenir | Étudiant ESIEA  

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
