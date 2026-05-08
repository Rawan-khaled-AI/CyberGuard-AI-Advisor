from pathlib import Path

MODEL_PATH = Path("app/ml_models/email_phishing_distilbert")


def predict_email_phishing(text: str) -> dict:
    if not MODEL_PATH.exists():
        return {
            "label": "unknown",
            "confidence": 0.0,
            "model_available": False,
            "note": "Email ML model is not available in deployment. Using rule-based analysis only.",
        }

    from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
    import torch

    tokenizer = DistilBertTokenizerFast.from_pretrained(str(MODEL_PATH))
    model = DistilBertForSequenceClassification.from_pretrained(str(MODEL_PATH))
    model.eval()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()

    label = "phishing" if predicted_class == 1 else "safe"

    return {
        "label": label,
        "confidence": confidence,
        "model_available": True,
    }