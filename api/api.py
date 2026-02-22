from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
from loguru import logger

app = Flask(__name__)

# Chargement du modèle en mémoire Cache (Production)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "data", "model.joblib")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes / Docker Compose"""
    return jsonify({"status": "healthy", "service": "Camrail Predictive API"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    """Exposition API du modèle IA pour le Dashboard UI et Power BI."""
    try:
        data = request.get_json()
        df_input = pd.DataFrame([data])
        
        if not os.path.exists(model_path):
            return jsonify({"error": "Modèle non entraîné. Lancez le DAG."}), 503
            
        model = joblib.load(model_path)
        features = df_input[['flow_rate', 'pressure', 'vibration', 'temperature']]
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0][1]
        
        logger.info(f"API Request - Prediction: {prediction} | Proba: {proba:.2f}")
        
        return jsonify({
            "critical_risk": int(prediction),
            "risk_probability": round(float(proba), 4),
            "loco_id": data.get("loco_id", "UNKNOWN")
        })
        
    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    logger.info("🚀 Démarrage de l'API Flask (Industrial AI API)")
    app.run(host="0.0.0.0", port=5000, debug=False)
