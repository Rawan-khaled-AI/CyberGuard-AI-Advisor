import joblib
from huggingface_hub import hf_hub_download

MODEL_REPO = "rawankhaled46/cyberguard-url-model"

model = None

try:
    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename="url_model.pkl",
        repo_type="model",
    )

    model = joblib.load(model_path)

    print("URL model loaded from Hugging Face")

except Exception as e:
    print(f"Failed to load URL model: {e}")


def predict_url_risk(features: dict) -> dict:
    if model is None:
        return {
            "prediction": "unknown",
            "confidence": 0.0,
            "model_available": False,
            "note": "URL ML model is not available in deployment. Using rule-based analysis only.",
        }

    expected_features = list(features.values())[:20]

    feature_values = [expected_features]

    raw_prediction = int(model.predict(feature_values)[0])

    prediction = "phishing" if raw_prediction == 1 else "safe"

    confidence = float(1.0)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "model_available": True,
        "source": "huggingface",
    }
    