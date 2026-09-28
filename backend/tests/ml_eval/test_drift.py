import numpy as np


def _population_stability_index(reference, current, bins=5):
    edges = np.histogram_bin_edges(np.concatenate([reference, current]), bins=bins)
    expected = np.histogram(reference, bins=edges)[0] / len(reference)
    observed = np.histogram(current, bins=edges)[0] / len(current)
    epsilon = 1e-6
    expected = np.clip(expected, epsilon, None)
    observed = np.clip(observed, epsilon, None)
    return float(np.sum((observed - expected) * np.log(observed / expected)))


def test_drift_metric_increases_for_shifted_effort_distribution():
    reference = np.linspace(10, 100, 200)
    stable = reference + 0.01
    shifted = reference + 80
    assert _population_stability_index(reference, stable) < 0.1
    assert _population_stability_index(reference, shifted) > 0.2
