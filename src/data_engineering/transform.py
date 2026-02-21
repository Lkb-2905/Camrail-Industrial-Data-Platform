import pandas as pd
from loguru import logger

def transform_data(df_raw):
    """Data Processing - Nettoyage et Feature Engineering."""
    logger.info("⚙️ [ETL] Transformation et Lissage des Signaux (Rolling Means)...")
    
    df = df_raw.copy()
    
    # Remplir les valeurs nulles fictives éventuelles
    df = df.dropna()
    
    # Feature Engineering : Moyenne glissante par pompe sur 3 heures
    df_sorted = df.sort_values(by=['pump_id', 'timestamp'])
    
    df_sorted['vibration_rolling_mean'] = df_sorted.groupby('pump_id')['vibration'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    df_sorted['pressure_rolling_mean'] = df_sorted.groupby('pump_id')['pressure'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    
    logger.info("✅ [ETL] Features métiers créées avec succès.")
    return df_sorted
