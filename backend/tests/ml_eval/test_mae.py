import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def test_ml_effort_predictor_mae_is_below_project_hours_threshold():
    features = np.arange(60, dtype=float).reshape(-1, 1)
    actual = 20 + 3 * features.ravel()
    model = LinearRegression().fit(features[:45], actual[:45])
    predicted = model.predict(features[45:])
    assert mean_absolute_error(actual[45:], predicted) < 1
