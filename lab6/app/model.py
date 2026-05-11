from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / "models" / "iris_model.joblib"
CLASS_NAMES = ["setosa", "versicolor", "virginica"]


def train_and_save_model():
    iris = load_iris()

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )

    model.fit(iris.data, iris.target)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        return train_and_save_model()

    return joblib.load(MODEL_PATH)


def predict_iris(features: list[float]) -> dict:
    model = load_model()

    data = np.array([features], dtype=float)
    predicted_class = int(model.predict(data)[0])

    probabilities = model.predict_proba(data)[0]
    probability = float(probabilities[predicted_class])

    return {
        "predicted_class": predicted_class,
        "predicted_name": CLASS_NAMES[predicted_class],
        "probability": round(probability, 4),
    }
