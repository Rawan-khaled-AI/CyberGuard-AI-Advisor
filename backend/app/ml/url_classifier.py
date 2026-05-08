import joblib
import pandas as pd

from app.ml.url_feature_extractor import FEATURE_COLUMNS, extract_url_features

MODEL_PATH = "app/ml_models/url_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_url_risk(url: str) -> dict:
    features = extract_url_features(url)
    x = pd.DataFrame([features], columns=FEATURE_COLUMNS)

    prediction = int(model.predict(x)[0])
    probabilities = model.predict_proba(x)[0]

    legitimate_confidence = float(probabilities[0])
    phishing_confidence = float(probabilities[1])

    return {
        "prediction": "Phishing URL" if prediction == 1 else "Legitimate URL",
        "legitimate_confidence": round(legitimate_confidence, 4),
        "phishing_confidence": round(phishing_confidence, 4),
    }