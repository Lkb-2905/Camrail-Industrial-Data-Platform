import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Camrail Live Monitor", layout="wide", page_icon="🚂")

st.title("🏭 Camrail Industrial Data Platform")
st.subheader("Monitoring en Temps Réel et Maintenance Prédictive AI")

# Simuler des entrées manuelles
st.sidebar.header("🔬 Outil de Test Manuel (API)")
loco_id = st.sidebar.text_input("Identifiant Locomotive", value="LOCO_001")
flow_rate = st.sidebar.slider("Débit d'Huile (L/min)", 200, 800, 500)
pressure = st.sidebar.slider("Pression (Bar)", 1.0, 10.0, 5.0)
vibration = st.sidebar.slider("Vibrations (mm/s)", 0.5, 15.0, 2.0)
temperature = st.sidebar.slider("Température (°C)", 20.0, 120.0, 45.0)

if st.sidebar.button("⚙️ Lancer la Prédiction AI"):
    url = "http://localhost:5000/predict"
    payload = {
        "loco_id": loco_id,
        "flow_rate": flow_rate,
        "pressure": pressure,
        "vibration": vibration,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            res = response.json()
            risk = res.get("critical_risk", 0)
            proba = res.get("risk_probability", 0.0)
            
            if risk == 1:
                st.error(f"🚨 DANGER DÉTECTÉ POUR {loco_id}. Probabilité Réseau de Neurones : {proba * 100}%")
            else:
                st.success(f"✅ STATUT NOMINAL POUR {loco_id}. Probabilité Risque : {proba * 100}%")
        else:
            st.warning(f"⚠️ Erreur Serveur API: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ ERREUR 503 : API IA hors ligne. Veuillez démarrer l'API sur le port 5000 via Docker ou bash.")

st.markdown("---")
st.markdown("### 📊 Architecture Enterprise Deployée")
st.image("https://img.shields.io/badge/Streamlit-App-red", use_column_width=False)
st.write("Le présent dashboard attaque l'API Flask de Machine Learning. Il est synchronisé avec les DAGs Apache Airflow qui rafraîchissent l'entrainement IA toutes les nuits.")
