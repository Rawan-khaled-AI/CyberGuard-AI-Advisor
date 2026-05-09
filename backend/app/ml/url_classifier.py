import joblib
from huggingface_hub import hf_hub_download

MODEL_REPO = "rawankhaled46/cyberguard-url-model"

model = None


def load_url_model():
    global model

    if model is None:
        print("Loading URL model from Hugging Face...")

        model_path = hf_hub_download(
            repo_id=MODEL_REPO,
            filename="url_model.pkl",
            repo_type="model",
        )

        model = joblib.load(model_path)

    return model


def predict_url_risk(features: dict) -> dict:
    model = load_url_model()

    expected_features = list(features.values())[:20]
    feature_values = [expected_features]

    raw_prediction = int(model.predict(feature_values)[0])
    prediction = "phishing" if raw_prediction == 1 else "safe"

    return {
        "prediction": prediction,
        "confidence": 1.0,
        "model_available": True,
        "source": "huggingface",
    }