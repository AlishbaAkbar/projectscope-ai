import numpy as np

from app.ml.predictor import MLPredictor


class IdentityScaler:
    def transform(self, values):
        return np.asarray(values)


class FixedEstimator:
    def predict(self, values):
        assert values.shape == (1, 2)
        return np.asarray([42.5])


def test_predictor_maps_project_features_and_returns_hours():
    predictor = MLPredictor()
    predictor.model = FixedEstimator()
    predictor.preprocessor = {"scaler": IdentityScaler()}
    predictor.feature_columns = ["num_features", "num_tasks"]
    predictor.model_name = "test-estimator"
    predictor.is_loaded = True

    result = predictor.predict_from_project({"num_features": 3, "num_tasks": 7})
    assert result["predicted_hours"] == 42.5
    assert result["confidence"] == 0.75
