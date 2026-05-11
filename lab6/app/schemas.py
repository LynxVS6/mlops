from pydantic import BaseModel, Field


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Длина чашелистика")
    sepal_width: float = Field(..., gt=0, description="Ширина чашелистика")
    petal_length: float = Field(..., gt=0, description="Длина лепестка")
    petal_width: float = Field(..., gt=0, description="Ширина лепестка")

    def to_model_input(self) -> list[float]:
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width,
        ]


class PredictionResponse(BaseModel):
    predicted_class: int
    predicted_name: str
    probability: float
    saved_id: int | None = None
