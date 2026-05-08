import torch
import numpy as np
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "app/ml_models/email_phishing_distilbert"


def encode_label(email_type: str) -> int:
    if email_type == "Phishing Email":
        return 1
    return 0


def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        preds,
        average="binary",
        zero_division=0,
    )

    acc = accuracy_score(labels, preds)

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {
            key: torch.tensor(value[idx])
            for key, value in self.encodings.items()
        }
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("=" * 50)
    print("Device:", device)

    if device == "cuda":
        print("GPU:", torch.cuda.get_device_name(0))
    print("=" * 50)

    dataset = load_dataset("zefang-liu/phishing-email-dataset")["train"]

    dataset = dataset.map(
        lambda row: {
            
            "text": str(row["Email Text"]) if row["Email Text"] is not None else "",
            "label": encode_label(row["Email Type"]),
        }
    )

    dataset = dataset.filter(
        lambda row: row["text"] is not None and len(row["text"].strip()) > 0
    )

    dataset = dataset.train_test_split(
        test_size=0.2,
        seed=42,
    )

    train_data = dataset["train"]
    val_data = dataset["test"]

    print("Train size:", len(train_data))
    print("Validation size:", len(val_data))

    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    train_encodings = tokenizer(
        list(train_data["text"]),
        truncation=True,
        padding=True,
        max_length=256,
    )

    val_encodings = tokenizer(
        list(val_data["text"]),
        truncation=True,
        padding=True,
        max_length=256,
    )
    
    train_dataset = EmailDataset(train_encodings, train_data["label"])
    val_dataset = EmailDataset(val_encodings, val_data["label"])

    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
    )

    training_args = TrainingArguments(
        output_dir="app/ml_models/training_outputs",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        learning_rate=2e-5,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=1)],
    )

    trainer.train()

    metrics = trainer.evaluate()
    print("Final Evaluation Metrics:")
    print(metrics)

    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("=" * 50)
    print(f"Model saved to: {OUTPUT_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()