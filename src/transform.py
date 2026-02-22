import pandas as pd
from loguru import logger
import sqlite3
import os
from .extract import extract_sensor_data, extract_maintenance_data

logger.add("logs/transform.log", rotation="10 MB")

def transform_and_load():
    """Transformation métiers (Feature Engineering) et chargement SQL."""
    try:
        df_sensors = extract_sensor_data()
        df_maint = extract_maintenance_data()
        
        logger.info("⚙️ [TRANSFORM] Nettoyage et jointure des données télémétriques.")
        
        # Exemple de transformation industrielle basique
        df_merged = pd.merge(df_sensors, df_maint, on="loco_id", how="left")
        
        # Feature Engineering : Risque Machine
        df_merged["critical_risk"] = ((df_merged["vibration"] > 3.0) & (df_merged["temperature"] > 60.0)).astype(int)
        
        # Enregistrement dans le Data Warehouse
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, "data", "industrial_dwh.db")
        
        with sqlite3.connect(db_path) as conn:
            df_merged.to_sql("sensor_metrics", conn, if_exists="replace", index=False)
            logger.info(f"✅ [LOAD] Succès : Données fusionnées insérées dans {db_path}.")
            
    except Exception as e:
        logger.error(f"❌ [TRANSFORM/LOAD] Erreur fatale dans le pipeline ETL : {e}")
        raise

if __name__ == "__main__":
    transform_and_load()
