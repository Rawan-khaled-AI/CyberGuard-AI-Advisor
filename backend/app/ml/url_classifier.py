from pathlib import Path
import joblib

MODEL_PATH = Path("app/ml_models/url_model.pkl")

model = None

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)


def predict_url_risk(features: dict) -> dict:
    if model is None:
        return {
            "prediction": "unknown",
            "confidence": 0.0,
            "model_available": False,
            "note": "URL ML model is not available in deployment. Using rule-based analysis only.",
        }

    feature_values = [list(features.values())]

    prediction = model.predict(feature_values)[0]

    confidence = 1.0

    return {
        "prediction": prediction,
        "confidence": confidence,
        "model_available": True,
    }