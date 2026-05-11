from contextlib import asynccontextmanager

from fastapi import FastAPI, Query

from app.database import init_db, list_predictions, save_prediction
from app.model import load_model, predict_iris
from app.schemas import IrisFeatures, PredictionResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    init_db()
    yield


app = FastAPI(
    title="Iris ML Service",
    description="FastAPI-сервис для ML-модели классификации ирисов",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Iris ML Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
    prediction = predict_iris(features.to_model_input())
    saved_id = save_prediction(features, prediction)

    return {
        **prediction,
        "saved_id": saved_id,
    }


@app.get("/history")
def history(limit: int = Query(default=10, ge=1, le=100)):
    return list_predictions(limit)
