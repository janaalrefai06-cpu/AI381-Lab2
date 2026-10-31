
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "churn_v2.csv"
MODEL_PATH = BASE_DIR / "model.joblib"

NUMERIC = ["tenure_months", "monthly_fee", "support_calls"]
CATEGORICAL = ["contract", "internet_service"]


def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[NUMERIC + CATEGORICAL]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = Pipeline([
        ("prep", ColumnTransformer([
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ])),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]

    f1 = f1_score(y_test, probabilities > 0.5)
    auc = roc_auc_score(y_test, probabilities)

    joblib.dump(model, MODEL_PATH)

    print(f"F1: {f1:.3f}")
    print(f"AUC: {auc:.3f}")
    print(f"Model saved to: {MODEL_PATH}")

    return model


if __name__ == "__main__":
    train_model()
