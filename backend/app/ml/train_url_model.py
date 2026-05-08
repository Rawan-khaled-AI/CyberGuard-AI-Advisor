import pandas as pd
import joblib

from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from app.ml.url_feature_extractor import FEATURE_COLUMNS

dataset = load_dataset("pirocheto/phishing-url")

train_df = dataset["train"].to_pandas()
test_df = dataset["test"].to_pandas()

df = pd.concat([train_df, test_df], ignore_index=True)

print("Dataset loaded:", df.shape)

df["label"] = df["status"].apply(lambda x: 1 if x == "phishing" else 0)

X = df[FEATURE_COLUMNS]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

joblib.dump(model, "app/ml_models/url_model.pkl")

print("\nURL Model v2 saved successfully!")