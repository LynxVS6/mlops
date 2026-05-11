from app.model import load_model, predict_iris


def test_model_loads():
    model = load_model()
    assert model is not None


def test_predict_known_setosa():
    result = predict_iris([5.1, 3.5, 1.4, 0.2])

    assert result["predicted_class"] == 0
    assert result["predicted_name"] == "setosa"
    assert 0 <= result["probability"] <= 1


def test_predict_known_virginica():
    result = predict_iris([6.5, 3.0, 5.2, 2.0])

    assert result["predicted_class"] == 2
    assert result["predicted_name"] == "virginica"
    assert 0 <= result["probability"] <= 1
