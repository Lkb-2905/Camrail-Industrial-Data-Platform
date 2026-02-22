🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
⚡ CIDP PCR : Industrial Data Platform (Sécurité E2E)
Gestion Crise Logistique SQL Résilience License

Version: 1.0.0 Stable | Date: Février 2026
Auteur: KAMENI TCHOUATCHEU GAETAN BRUNEL
Contact: gaetanbrunel.kamenitchouatcheu@et.esiea.fr

🚀 Démarrage Rapide • 📚 Documentation • 🎯 Fonctionnalités • 🔧 Installation

📋 TABLE DES MATIÈRES
Vue d'ensemble du projet
Architecture Technique
Stratégies de Continuité (PCA)
Procédures de Reprise (PRA)
Maintenance (MCO)
Annexe Technique

🎯 VUE D'ENSEMBLE DU PROJET
Contexte et Enjeux Critiques
Ce plan définit la stratégie de résilience de la Plateforme (E2E-IDP). L'incapacité de l'orchestrateur de nuit paralyse le site. Le PCR assure la fiabilité des flux ETL et l'intégrité de l'IA (éviter le Data Poisoning).

🏗️ ARCHITECTURE TECHNIQUE
Analyse d'Impact Métier (BIA)
Menace Identifiée | Probabilité | Impact Métier | Sévérité
--- | --- | --- | ---
API Capteurs Injoignable | Élevée (3/5) | Extraction asynchrone stoppée. | 🟠 Majeur
Panne de Mémoire Vive | Moyenne (2/5) | Crash du Serveur lors de l'assemblage Pandas. | 🟠 Majeur
Base SQLite Verrouillée | Faible (1/5) | Impossible d'insérer l'ETL. | 🔴 Critique

🛠️ STACK TECHNOLOGIQUE
Stratégies de Continuité (PCA)
Code structuré "Failover-by-Design". L'Orchestrateur Python Maître s'arrête `sys.exit(1)` net si l'ETL crashe, protégeant le SQL d'un entraînement ML corrompu.

🎯 FONCTIONNALITÉS CLÉS
Procédures de Reprise (PRA)
En cas de crash manuel.

🚀 DÉMARRAGE RAPIDE
```powershell
# 1. Kill et Vérification des verrous (Locks) Python asynchrones
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue

# 2. Back-up immédiat du Data Warehouse avant intervention
Copy-Item "database/industrial_dwh.sqlite" "database/industrial_dwh_SAFE.sqlite" -ErrorAction SilentlyContinue

# 3. Lancement d'Hivernage (Reborn)
cd "C:\chemin\vers\Camrail-Industrial-Data-Platform"
.\env\Scripts\activate
python run_industrial_platform.py
Write-Host "🚀 Processus d'usine redemarré."
```

📖 GUIDE D'UTILISATION
Maintenance & Tests (MCO)
"Corruption ETL Test" et "Deadlock DataBase Test" pratiqués trimestriellement.

✨ QUALITÉ & BEST PRACTICES
Supervision
Monitoring strict avec `loguru`, centralisant les comportements asynchrones End-to-End.

🗺️ ROADMAP & ÉVOLUTIONS
Des bascules réseau redondantes pour Azure (ou AWS) dans la V2.0.

🤝 CONTRIBUTION
Révisions annuelles recommandées.

📄 LICENCE
Confidentiel Camrail / Bolloré Logistics.

👨💻 AUTEUR
KAMENI TCHOUATCHEU GAETAN BRUNEL
Ingénieur Logiciel & Data | Étudiant ESIEA

📧 Email : gaetanbrunel.kamenitchouatcheu@et.esiea.fr
🐙 GitHub : @Lkb-2905

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
