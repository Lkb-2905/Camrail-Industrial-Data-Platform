import pandas as pd
from loguru import logger
import sqlite3
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

logger.add("logs/training.log", rotation="10 MB")

def train_model():
    """Entraînement du modèle Machine Learning de Maintenance Prédictive."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, "data", "industrial_dwh.db")
        
        logger.info("🧠 [TRAIN] Extraction des features depuis le Data Warehouse...")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT flow_rate, pressure, vibration, temperature, critical_risk FROM sensor_metrics", conn)
            
        if df.empty:
            logger.warning("⚠️ [TRAIN] Le DWH est vide. Impossible de lancer l'entraînement.")
            return
            
        X = df[['flow_rate', 'pressure', 'vibration', 'temperature']]
        y = df['critical_risk']
        
        if len(y.unique()) < 2:
            logger.warning("⚠️ [TRAIN] Classes insuffisantes pour apprendre. Utilisation données mockées.")
            # Injection de faux positifs pour éviter crash (car le csv est très petit)
            X.loc[len(X)] = [400, 3.2, 5.5, 65.8]
            y.loc[len(y)] = 1
            
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logger.info("🧠 [TRAIN] Algorithme Random Forest en cours de calcul...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        model_path = os.path.join(base_dir, "data", "model.joblib")
        joblib.dump(model, model_path)
        logger.info(f"✅ [TRAIN] Succès : Modèle IA sauvegardé en production ({model_path}).")
        
    except Exception as e:
        logger.error(f"❌ [TRAIN] Échec de l'entraînement du modèle IA : {e}")
        raise

if __name__ == "__main__":
    train_model()
