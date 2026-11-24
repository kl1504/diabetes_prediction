from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent
PUBLIC = BASE / "public"

# Le modèle est cherché à côté de app.py, puis dans ../models (en local)
MODEL_PATH = BASE / "pipeline.joblib"
if not MODEL_PATH.exists():
    MODEL_PATH = BASE.parent / "models" / "pipeline.joblib"

FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age",
]
ZERO_AS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

app = Flask(__name__)
pipeline = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return send_from_directory(PUBLIC, "index.html")


@app.route("/script.js")
def script():
    return send_from_directory(PUBLIC, "script.js")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_PATH.name})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Corps JSON invalide."}), 400

    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Champs manquants : {', '.join(missing)}"}), 400

    try:
        df = pd.DataFrame([{f: float(data[f]) for f in FEATURES}], columns=FEATURES)
    except (TypeError, ValueError):
        return jsonify({"error": "Toutes les valeurs doivent être numériques."}), 400

    # Les 0 impossibles deviennent NaN, comme à l'entraînement
    df[ZERO_AS_MISSING] = df[ZERO_AS_MISSING].replace(0, np.nan)

    try:
        prediction = int(pipeline.predict(df)[0])
        probability = float(pipeline.predict_proba(df)[0][1])
    except Exception as exc:
        return jsonify({"error": f"Erreur du modèle : {exc}"}), 500

    return jsonify({
        "prediction": prediction,
        "probability": round(probability, 3),
        "result": "Diabète probable" if prediction == 1 else "Diabète peu probable",
    })


if __name__ == "__main__":
    app.run(debug=True)
