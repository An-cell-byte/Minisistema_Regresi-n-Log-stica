from pathlib import Path

import joblib
import pandas as pd

FEATURE_ORDER = [
    "age", "job", "marital", "education", "balance", "housing", "loan", "campaign"
]
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "bank_marketing_pipeline.joblib"
_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No existe el modelo en {MODEL_PATH}. Ejecuta: python training/train.py"
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(payload: dict) -> dict:
    model = get_model()
    sample = pd.DataFrame([{key: payload[key] for key in FEATURE_ORDER}], columns=FEATURE_ORDER)
    predicted = str(model.predict(sample)[0])
    probabilities = model.predict_proba(sample)[0]
    yes_index = list(model.classes_).index("yes")
    probability = float(probabilities[yes_index])
    return {
        "prediction": predicted,
        "probability": round(probability, 4),
        "classification": "Potencialmente interesado" if predicted == "yes" else "Baja propensión",
    }
