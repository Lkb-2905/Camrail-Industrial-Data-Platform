🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
⚡ CIDP : Camrail Industrial Data Platform End-to-End
Python SQLite Scikit-Learn PowerBI License

Version: 1.0.0 Stable | Date: Février 2026
Auteur: KAMENI TCHOUATCHEU GAETAN BRUNEL
Contact: gaetanbrunel.kamenitchouatcheu@et.esiea.fr

🚀 Démarrage Rapide • 📚 Documentation • 🎯 Fonctionnalités • 🔧 Installation

📋 TABLE DES MATIÈRES
Vue d'ensemble du projet
Architecture Technique
Stack Technologique
Fonctionnalités Clés
Démarrage Rapide
Guide d'Utilisation
Qualité & Best Practices
Roadmap & Évolutions

🎯 VUE D'ENSEMBLE DU PROJET
Contexte & Objectifs
Ce projet démontre la mise en œuvre d'une architecture de données de bout en bout unifiant l'Ingénierie de Données (ETL) et la Data Science (IA). Il s'inscrit dans le contexte critique de la logistique ferroviaire de fret (Camrail - Bolloré Logistics), illustrant un profil "Full-Stack Data".

✅ Ingénierie des Données : Orchestration d'un pipeline ETL vers un SQL Data Warehouse.
✅ IA Connectée SGBD : Algorithme Random Forest se connectant au SQL pour scorer les machines.
✅ Architecture Hexagonale : Isolation stricte ETL vs Modélisation.
✅ Automatisation IT : Orchestrateur global `run_industrial_platform.py` pour un Scheduler.

Pourquoi ce projet ?
Aspect | Démonstration
--- | ---
Gouvernance | Création d'une Source Unique de Vérité (SSOT) en SQL.
Bout en Bout | Autonomie de la captation physique jusqu'à l'IA et au Dashboard.
Maintenabilité | ETL et Machine Learning cloisonnés.
Business Value | KPI calculés renforçant la maintenance prescriptive.

🏗️ ARCHITECTURE TECHNIQUE
Diagramme de Flux
Flux de Données Détaillé
1. Data Engineering : Simulation IoT, Extraction, Feature Engineering, Loading (SSOT DB).
2. Data Science : Le script ML s'entraîne depuis le SQL et insère ses scores prédictifs (`ai_telemetry_predictions`).
3. Restitution : Power BI interroge le DB SQLite final.

🛠️ STACK TECHNOLOGIQUE
Technologies Core
Composant | Technologie | Version | Justification Technique
--- | --- | --- | ---
Langage | Python | 3.12+ | Ecosystème souverain complet.
SGBD | SQLite | - | SQL universel portable et puissant.
Data Processing | Pandas / SQLAlchemy | Latest | Pipeline et ORM robuste.
Machine Learning | Scikit-Learn | Latest | Random Forest interprétable.

🎯 FONCTIONNALITÉS CLÉS
🚀 Fonctionnalités Principales
Orchestrateur Centralisé
Le script pilote dépendances et crons. Il sécurise le flux (erreur ETL = arrêt ML).
IA Nativement Interconnectée
Requêtes SQL directes, écriture des probabilités de pannes pour l'alerte temps réel.

🛡️ Sécurité & Robustesse
Validation : Isolation en blocs try/except pour sécuriser la donnée.

🚀 DÉMARRAGE RAPIDE
Prérequis
Python (v3.12+)

Installation Rapide
```bash
# 1. Naviguer dans le dossier du projet
cd Camrail-Industrial-Data-Platform

# 2. Créer l'environnement
python -m venv env
.\env\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'usine numérique E2E
python run_industrial_platform.py
```

📖 GUIDE D'UTILISATION
Analyse des Résultats
Ouvrez le fichier `database/industrial_dwh.sqlite`. La table `ai_telemetry_predictions` est fraîchement calculée. Connectez vos rapports BI en ODBC.

📸 Aperçu de l'Exécution
![Exécution de l'Usine Numérique E2E](execution_screenshot.png)

✨ QUALITÉ & BEST Practices
Standards de Code
SSOT : Unique source de vérité base de données SQL. Loguru pour historiser l'exécution.

🗺️ ROADMAP & ÉVOLUTIONS
Version Actuelle : 1.0.0 ✅
Environnement bout en bout en local, ML connecté SQLite.

🤝 CONTRIBUTION
Les contributions sont les bienvenues.

📄 LICENCE
Ce projet est développé dans un cadre académique et professionnel. Droits réservés.

👨💻 AUTEUR
KAMENI TCHOUATCHEU GAETAN BRUNEL
Ingénieur Logiciel & Data | Étudiant ESIEA

📧 Email : gaetanbrunel.kamenitchouatcheu@et.esiea.fr
🐙 GitHub : @Lkb-2905

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
