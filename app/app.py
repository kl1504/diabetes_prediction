from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # nécessaire pour que index.html puisse appeler l'API

pipeline = joblib.load("pipeline.joblib")

FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age",
]

@app.route("/")
def home():
    return "Bienvenue sur l'API de prédiction du diabète !"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data], columns=FEATURES)
    # Les 0 impossibles deviennent NaN, comme à l'entraînement
    cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    df[cols] = df[cols].replace(0, np.nan)

    prediction = int(pipeline.predict(df)[0])
    proba = float(pipeline.predict_proba(df)[0][1])

    return jsonify({
        "prediction": prediction,
        "probability": round(proba, 3),
        "result": "Diabète probable" if prediction == 1 else "Diabète peu probable",
    })

if __name__ == "__main__":
    app.run(debug=True)
    
