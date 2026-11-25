# Diabetes Prediction

Machine learning project based on Pima Indians dataset to predict the likehood based on clinical and diagnostic features.

## Overview

This project trains classification models on patient health metrics (such as glucose levels, BMI, insulin, blood pressure, and age) to predict diabetes risk (`Outcome`: `1` for positive, `0` for negative).


## Dataset

Typical implementations use tabular clinical datasets such as the Pima Indians Diabetes dataset (`diabetes.csv`) with features including:
- `Pregnancies`
- `Glucose`
- `BloodPressure`
- `SkinThickness`
- `Insulin`
- `BMI`
- `DiabetesPedigreeFunction`
- `Age`
- `Outcome` (target)


## Installation

```bash
git clone https://github.com/kl1504/diabetes_prediction.git
cd diabetes_prediction
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

**1. Train the model** by running the notebook:

```bash
cd notebooks
jupyter lab
```
**2. Run the app:**

```bash
cd app
python app.py
```

## Limitations

This is an educational project, not a medical tool. The dataset is small (768 patients) and limited to women of Pima Indian heritage, so the model should not be used for real diagnosis.
