import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

MODEL_NAME = "rawankhaled46/cyberguard-email-phishing-model"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()


def predict_email_phishing(text: str) -> dict:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()

    label = "phishing" if predicted_class == 1 else "safe"

    return {
        "label": label,
        "prediction": label,
        "confidence": confidence,
        "model_available": True,
        "source": "huggingface",
    }