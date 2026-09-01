import pytest
from app.services.feature_service import FeatureService


def test_authentication_normalization_variants():
    assert FeatureService.normalize_name("login") == "AUTHENTICATION"
    assert FeatureService.normalize_name("sign in") == "AUTHENTICATION"
    assert FeatureService.normalize_name("user authentication") == "AUTHENTICATION"
    assert FeatureService.normalize_name("Account Login") == "AUTHENTICATION"
    assert FeatureService.normalize_name("signup and registration") == "AUTHENTICATION"
    assert FeatureService.normalize_name("jwt auth") == "AUTHENTICATION"


def test_live_tracking_normalization_variants():
    assert FeatureService.normalize_name("live tracking") == "LIVE_TRACKING"
    assert FeatureService.normalize_name("real-time tracking") == "LIVE_TRACKING"
    assert FeatureService.normalize_name("vehicle gps tracking") == "LIVE_TRACKING"
    assert FeatureService.normalize_name("route tracking") == "LIVE_TRACKING"


def test_other_canonical_features():
    assert FeatureService.normalize_name("stripe payment") == "PAYMENT"
    assert FeatureService.normalize_name("checkout and billing") == "PAYMENT"
    assert FeatureService.normalize_name("push notifications") == "NOTIFICATIONS"
    assert FeatureService.normalize_name("doctor appointment booking") == "BOOKING"
    assert FeatureService.normalize_name("admin dashboard") == "ADMIN_PANEL"
    assert FeatureService.normalize_name("incident reporting") == "REPORTING"
    assert FeatureService.normalize_name("product search and filtering") == "SEARCH"


def test_custom_unknown_feature_fallback():
    assert FeatureService.normalize_name("iot sensor sync") == "IOT_SENSOR_SYNC"
    assert FeatureService.normalize_name("quantum key distribution") == "QUANTUM_KEY_DISTRIBUTION"
    assert FeatureService.normalize_name("") == "GENERAL_FEATURE"
