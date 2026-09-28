import numpy as np


def test_confidence_calibration_error_is_low_for_well_calibrated_predictions():
    predicted_confidence = np.asarray([0.2, 0.4, 0.6, 0.8])
    observed_accuracy = np.asarray([0.2, 0.4, 0.6, 0.8])
    expected_calibration_error = float(np.mean(np.abs(predicted_confidence - observed_accuracy)))
    assert expected_calibration_error == 0
