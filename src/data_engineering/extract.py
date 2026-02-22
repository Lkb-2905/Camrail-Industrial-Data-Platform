import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from loguru import logger

def extract_sensor_data(num_records=5000):
    """Extraction simulée d'une API d'usines logistiques (Data Engineering Phase)."""
    logger.info("📡 [ETL] Connexion aux capteurs industriels (Simulation API)...")
    
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(num_records)]
    
    # Simulation des capteurs
    locomotives = [f"LOCO_{str(i).zfill(3)}" for i in range(1, 6)]
    loco_ids = np.random.choice(locomotives, num_records)
    
    # Métriques normales
    flow_rates = np.random.normal(500, 50, num_records)
    pressures = np.random.normal(5.0, 0.5, num_records)
    vibrations = np.random.normal(2.0, 0.3, num_records)
    temperatures = np.random.normal(45.0, 5.0, num_records)
    
    # Injection des anomalies (Bruit Métier)
    failures = np.zeros(num_records, dtype=int)
    num_failures = int(num_records * 0.05)
    failure_indices = np.random.choice(num_records, num_failures, replace=False)
    
    for idx in failure_indices:
        failures[idx] = 1
        pressures[idx] *= 0.6  # Chute de pression
        vibrations[idx] *= 2.5 # Forte vibration
        temperatures[idx] += 20.0 # Surchauffe
    
    df_raw = pd.DataFrame({
        'timestamp': dates,
        'loco_id': loco_ids,
        'flow_rate': flow_rates,
        'pressure': pressures,
        'vibration': vibrations,
        'temperature': temperatures,
        'failure': failures
    })
    
    logger.info(f"✅ [ETL] {num_records} lignes télémétriques extraites avec succès.")
    return df_raw
