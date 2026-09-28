import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def test_regression_baseline_meets_r2_quality_threshold():
    features = np.arange(100, dtype=float).reshape(-1, 1)
    actual = 12 + 2.5 * features.ravel()
    model = LinearRegression().fit(features[:80], actual[:80])
    assert r2_score(actual[80:], model.predict(features[80:])) > 0.7
