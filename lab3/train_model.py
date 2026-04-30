import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from mlflow.models import infer_signature


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    df = pd.read_csv("df_clear.csv")

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge())
    ])

    params = {
        "model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0],
        "model__fit_intercept": [True, False],
        "model__solver": ["auto", "svd", "cholesky", "lsqr"]
    }

    mlflow.set_experiment("ridge diabetes")

    with mlflow.start_run():
        clf = GridSearchCV(pipe, params, cv=3, n_jobs=4)
        clf.fit(X_train, y_train)

        best = clf.best_estimator_
        y_pred = best.predict(X_val)

        rmse, mae, r2 = eval_metrics(y_val, y_pred)

        mlflow.log_param("alpha", best.named_steps["model"].alpha)
        mlflow.log_param("fit_intercept", best.named_steps["model"].fit_intercept)
        mlflow.log_param("solver", best.named_steps["model"].solver)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        signature = infer_signature(X_train, best.predict(X_train))
        mlflow.sklearn.log_model(best, "model", signature=signature)

        with open("ridge_diabetes.pkl", "wb") as file:
            joblib.dump(best, file)

    dfruns = mlflow.search_runs()
    path2model = (
        dfruns.sort_values("metrics.r2", ascending=False)
        .iloc[0]["artifact_uri"]
        .replace("file://", "")
        + "/model"
    )

    print(path2model)
