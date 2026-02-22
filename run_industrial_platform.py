from loguru import logger
import time
import sys
import os

from src.data_engineering.extract import extract_sensor_data
from src.data_engineering.transform import transform_data
from src.data_engineering.load import load_to_warehouse
from src.data_science.train_and_predict import train_and_predict

def main_orchestrator():
    """Point d'entrée principal - Le Planificateur de Production"""
    logger.add("logs/platform_execution.log", rotation="2 MB")
    
    logger.info("=" * 60)
    logger.info("🚀 DÉMARRAGE DU PIPELINE INDUSTRIAL PLATFORM (CAMRAIL / BOLLORÉ LOGISTICS)")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    try:
        # Phase 1: DE (Data Engineering ETL)
        logger.info("\n--- PHASE 1: DATA ENGINEERING ---")
        raw_dataframe = extract_sensor_data(num_records=10000) # Extrait 10.000 lignes
        clean_dataframe = transform_data(raw_dataframe)
        
        # Le connecteur SQL (engine) est retourné par l'ETL pour être réutilisé (Connexion partagée)
        db_engine = load_to_warehouse(clean_dataframe, db_path="database/industrial_dwh.sqlite")
        
        # Phase 2: DS (Data Science IA)
        logger.info("\n--- PHASE 2: DATA SCIENCE ---")
        train_and_predict(db_engine)
        
        duration = round(time.time() - start_time, 2)
        logger.info("=" * 60)
        logger.info(f"✨ EXÉCUTION TERMINÉE AVEC SUCCÈS. Temps total: {duration} sec.")
        logger.info("📊 Les données SQLite sont prêtes pour Power BI !")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Échec Critique du Pipeline (Arrêt) : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # S'assurer que les dossiers existent
    os.makedirs("logs", exist_ok=True)
    os.makedirs("database", exist_ok=True)
    os.makedirs("data_science/models", exist_ok=True)
    
    main_orchestrator()
