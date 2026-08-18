import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = ["age", "job", "marital", "education", "balance", "housing", "loan", "campaign"]
NUMERIC_FEATURES = ["age", "balance", "campaign"]
CATEGORICAL_FEATURES = ["job", "marital", "education", "housing", "loan"]


def train_and_save() -> None:
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "bank.csv", sep=";")
    df.columns = [column.strip('"').lower() for column in df.columns]
    X, y = df[FEATURES], df["y"].str.strip().str.lower()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    preprocessor = ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    metrics = {
        "model": "LogisticRegression",
        "features": FEATURES,
        "excluded_features": ["duration"],
        "rows": len(df),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, pos_label="yes", zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, pos_label="yes", zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, predictions, pos_label="yes", zero_division=0)), 4),
    }
    models = root / "models"
    models.mkdir(exist_ok=True)
    joblib.dump(pipeline, models / "bank_marketing_pipeline.joblib")
    (models / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    train_and_save()
