# Industrial Data Platform

![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white) ![Airflow](https://img.shields.io/badge/Orchestration-Airflow-E43921?logo=apache-airflow&logoColor=white) ![Flask](https://img.shields.io/badge/API-Flask-000000?logo=flask&logoColor=white) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![Azure](https://img.shields.io/badge/Cloud-Azure-0089D6?logo=microsoft-azure&logoColor=white)

## Objectif

Pipeline industriel "Production-Ready" permettant :
* **L'ingestion des données capteurs** en provenance d'un Data Lake (référentiel GMAO et signaux thermiques réels).
* **Le stockage structuré** dans un Data Warehouse via processus ETL robuste.
* **La prédiction de maintenance** via Machine Learning (RandomForest), déployée et orchestrée.

## Stack Technologique

* **Python** (Pandas, Scikit-Learn, Loguru)
* **SQL** (SQLite Data Warehouse)
* **Power BI & Streamlit** (Visualisation / Dashboard)
* **Flask** (API REST d'Intelligence Artificielle)
* **Apache Airflow** (Orchestration des DAGs MLOps)
* **Docker** (Containerisation)
* **GitHub Actions** (CI/CD Pipeline)

## Architecture

![Architecture](https://img.shields.io/badge/Architecture-End--to--End-green)

```mermaid
graph TD
    subgraph Data Sources
        S1[Sensors CSV]
        S2[Maintenance ERP]
    end

    subgraph Data Engineering (Airflow DAG)
        E[extract.py]
        T[transform.py<br>Feature Engineering]
        L[(SQL DWH)]
    end

    subgraph MLOps
        M[train.py<br>RandomForest]
        J[model.joblib]
    end

    subgraph Deployment
        A[Flask API<br>/predict]
        D[Streamlit UI<br>Monitor]
        PB[Power BI]
    end

    S1 --> E
    S2 --> E
    E --> T
    T --> L
    L --> M
    M --> J
    J --> A
    A --> D
    A --> PB

    style S1 fill:#eee,color:#333
    style S2 fill:#eee,color:#333
    style L fill:#4fc3f7,color:#000
    style J fill:#fdd835,color:#000
    style A fill:#4caf50,color:#fff
    style D fill:#ff5252,color:#fff
    style PB fill:#fbc02d,color:#000
```

## Structure du Répértoire
```text
camrail-platform/
├── data/                  # Sources ETL / DB SQLite (Data Lake)
├── src/                   # Core Python Logic (ETL & ML)
│   ├── extract.py         
│   ├── transform.py       
│   └── train.py           
├── api/                   # Couche d'Exposition (Flask)
│   └── api.py             
├── dashboard/             # Application Web (Streamlit)
│   └── app.py             
├── dags/                  # Orchestration Airflow
│   └── camrail_pipeline.py
├── logs/                  # Logs applicatifs (Loguru)
├── Dockerfile             # Container Azure Ready
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation système
```

## Démarrer le projet

### Étape 1 : Pipeline ETL & ML
```bash
python src/extract.py
python src/transform.py
python src/train.py
```

### Étape 2 : Lancement Serveur API
```bash
python api/api.py
```

### Étape 3 : Frontend Applicatif (Monitoring)
Ouvrez un second terminal :
```bash
streamlit run dashboard/app.py
```
