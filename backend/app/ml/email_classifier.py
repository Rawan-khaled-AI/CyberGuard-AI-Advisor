import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

MODEL_PATH = "app/ml_models/email_phishing_distilbert"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()


def predict_email_phishing(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]

    safe_confidence = float(probs[0])
    phishing_confidence = float(probs[1])

    prediction = "Phishing Email" if phishing_confidence >= safe_confidence else "Safe Email"

    return {
        "prediction": prediction,
        "safe_confidence": round(safe_confidence, 4),
        "phishing_confidence": round(phishing_confidence, 4),
    }