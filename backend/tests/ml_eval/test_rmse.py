import numpy as np
from sklearn.metrics import mean_squared_error


def test_rmse_is_zero_for_exact_predictions():
    actual = np.asarray([10.0, 20.0, 30.0])
    predicted = actual.copy()
    assert np.sqrt(mean_squared_error(actual, predicted)) == 0
