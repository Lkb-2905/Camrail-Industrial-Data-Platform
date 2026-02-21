import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from loguru import logger

def train_and_predict(engine):
    """Lecture depuis la Base SQL, Apprentissage et Prédiction."""
    logger.info("🧠 [IA] Lancement du Moteur de Data Science...")
    
    # 1. Extraction propre de la BDD pour alimenter l'IA
    logger.info("🔎 [IA] Fetch des features depuis 'fact_telemetry_features'...")
    df = pd.read_sql_query('SELECT * FROM fact_telemetry_features', con=engine)
    
    # Préparation des Features pour Scikit-Learn
    features = [
        'flow_rate', 'pressure', 'vibration', 'temperature',
        'vibration_rolling_mean', 'pressure_rolling_mean'
    ]
    
    X = df[features]
    y = df['failure']
    
    # Entraînement de Sécurité
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    logger.info("🌲 [IA] Apprentissage du modèle Random Forest sur classes déséquilibrées...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # Mémorisation & Sauvegarde du Modèle (.joblib)
    os.makedirs('data_science/models', exist_ok=True)
    joblib.dump(model, 'data_science/models/rf_failure_predict.joblib')
    
    # 2. Inférence (Calcul des Probabilités pour toutes les machines Maintentant)
    logger.info("⚡ [IA] Génération des prédictions à haut risque pour Power BI...")
    
    probabilities = model.predict_proba(X)[:, 1]  # Probabilité d'avoir la classe "1" (Panne)
    predictions = model.predict(X)
    
    # 3. Création du Datamart Final (La table PowerBI parfaite)
    df_powerbi = df[['timestamp', 'pump_id', 'flow_rate', 'pressure', 'vibration', 'temperature']].copy()
    
    df_powerbi['ai_risk_score_percent'] = np.round(probabilities * 100, 2)
    df_powerbi['ai_predicted_failure'] = predictions
    
    logger.info("💾 [IA] Écriture des nouvelles prévisions dans le Data Warehouse (Table: ai_telemetry_predictions)...")
    df_powerbi.to_sql('ai_telemetry_predictions', con=engine, index=False, if_exists='replace')
    
    logger.info("✅ [IA] Modèle ré-entraîné et prédictions sauvegardées dans le SQL.")
    return True
