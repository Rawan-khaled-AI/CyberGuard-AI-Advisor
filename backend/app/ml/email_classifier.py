import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

MODEL_NAME = "rawankhaled46/cyberguard-email-phishing-model"

tokenizer = None
model = None


def load_email_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        print("Loading email phishing model from Hugging Face...")
        tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()

    return tokenizer, model


def predict_email_phishing(text: str) -> dict:
    tokenizer, model = load_email_model()

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
        "confidence": float(confidence),
        "model_available": True,
        "source": "huggingface",
    }