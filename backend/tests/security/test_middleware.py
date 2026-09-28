from app.core.audit import AuditService
from app.core.config import settings
from app.models.audit import AuditLog


def test_security_headers_are_added_to_responses(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "content-security-policy" in response.headers


def test_request_size_limit_rejects_oversized_declared_body(client):
    response = client.post(
        "/api/v1/auth/login",
        content=b"",
        headers={"Content-Length": str((settings.MAX_REQUEST_SIZE_MB + 1) * 1024 * 1024)},
    )
    assert response.status_code == 413


def test_audit_service_persists_log_entries(db, user, organization):
    AuditService(db).log(
        action="test.operation",
        user_id=user.id,
        organization_id=organization.id,
        resource_type="test",
        resource_id=42,
    )
    entry = db.query(AuditLog).filter(AuditLog.action == "test.operation").one()
    assert entry.user_id == user.id
    assert entry.organization_id == organization.id
    assert entry.resource_id == 42


def test_audit_service_respects_disabled_setting(db, monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_AUDIT_LOG", False)
    AuditService(db).log(action="disabled.operation")
    assert db.query(AuditLog).count() == 0
