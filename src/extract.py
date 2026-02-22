import pandas as pd
from loguru import logger
import os

logger.add("logs/extraction.log", rotation="10 MB")

def extract_sensor_data() -> pd.DataFrame:
    """Extraction des données réelles depuis le datalake ou stockage local."""
    logger.info("📡 [EXTRACT] Début de l'ingestion des capteurs IoT.")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sensors_path = os.path.join(base_dir, "data", "sensors.csv")
    
    try:
        df_sensors = pd.read_csv(sensors_path)
        logger.info(f"✅ [EXTRACT] Succès : {len(df_sensors)} enregistrements télémétriques ingérés.")
        return df_sensors
    except Exception as e:
        logger.error(f"❌ [EXTRACT] Échec critique de l'ingestion de sensors.csv : {e}")
        raise

def extract_maintenance_data() -> pd.DataFrame:
    """Extraction des données de l'ERP de maintenance (GMAO)."""
    logger.info("📡 [EXTRACT] Connexion à la base GMAO Maintenance.")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    maintenance_path = os.path.join(base_dir, "data", "maintenance.csv")
    
    try:
        df_maint = pd.read_csv(maintenance_path)
        logger.info(f"✅ [EXTRACT] Succès : Référentiel maintenance chargé.")
        return df_maint
    except Exception as e:
        logger.error(f"❌ [EXTRACT] Impossible de charger le référentiel maintenance : {e}")
        raise

if __name__ == "__main__":
    extract_sensor_data()
    extract_maintenance_data()
