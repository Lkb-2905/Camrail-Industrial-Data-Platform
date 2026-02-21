import pandas as pd
from sqlalchemy import create_engine
from loguru import logger
import os

def load_to_warehouse(df_processed, db_path="database/industrial_dwh.sqlite"):
    """Écriture Transactionnelle SQL SQLite structurant la Donnée pour l'IA et Power BI."""
    logger.info(f"💾 [ETL] Connexion au Data Warehouse ({db_path})...")
    
    # Créer le dossier database s'il n'existe pas
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    engine = create_engine(f'sqlite:///{db_path}')
    
    try:
        # Load Table Facts
        df_processed.to_sql(
            'fact_telemetry_features', 
            con=engine, 
            index=False, 
            if_exists='replace' # Replace car c'est un projet de démo (sinon "append")
        )
        logger.info(f"✅ [ETL] {len(df_processed)} lignes chargées dans la table 'fact_telemetry_features'.")
        return engine
    except Exception as e:
        logger.error(f"❌ [ETL] Erreur lors de l'insertion SQL : {e}")
        raise
