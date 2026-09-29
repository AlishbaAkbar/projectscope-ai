"""
Phase 23: Audit Service
"""

import logging
from typing import Any, Dict, Optional

from fastapi import Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    """Handles audit logging"""

    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        action: str,
        user_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        request: Optional[Request] = None,
    ):
        """Create an audit log entry"""
        if not settings.ENABLE_AUDIT_LOG:
            return

        ip_address = None
        user_agent = None

        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent", "")[:500]

        log = AuditLog(
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message,
        )

        try:
            self.db.add(log)
            self.db.commit()
        except Exception:
            self.db.rollback()
            logger.exception("Audit log persistence failed")

    # ============================================
    # SPECIFIC AUDIT HELPERS
    # ============================================

    def log_auth_success(self, user_id: int, org_id: int, email: str, request: Request):
        self.log(
            action="auth.login.success",
            user_id=user_id,
            organization_id=org_id,
            resource_type="auth",
            details={"email": email},
            request=request,
        )

    def log_auth_failure(self, email: str, request: Request, reason: str):
        self.log(
            action="auth.login.failure",
            resource_type="auth",
            details={"email": email, "reason": reason},
            status="failure",
            request=request,
        )

    def log_register(self, user_id: int, org_id: int, email: str, request: Request):
        self.log(
            action="auth.register",
            user_id=user_id,
            organization_id=org_id,
            resource_type="user",
            resource_id=user_id,
            details={"email": email},
            request=request,
        )

    def log_project_created(self, user_id: int, org_id: int, project_id: int, name: str, request: Request):
        self.log(
            action="project.create",
            user_id=user_id,
            organization_id=org_id,
            resource_type="project",
            resource_id=project_id,
            details={"name": name},
            request=request,
        )

    def log_project_deleted(self, user_id: int, org_id: int, project_id: int, request: Request):
        self.log(
            action="project.delete",
            user_id=user_id,
            organization_id=org_id,
            resource_type="project",
            resource_id=project_id,
            request=request,
        )

    def log_access_denied(self, user_id: int, org_id: int, resource_type: str, resource_id: int, request: Request):
        self.log(
            action="access.denied",
            user_id=user_id,
            organization_id=org_id,
            resource_type=resource_type,
            resource_id=resource_id,
            status="denied",
            request=request,
        )

    def log_account_deleted(self, user_id: int, request: Request):
        self.log(
            action="account.delete",
            user_id=user_id,
            resource_type="user",
            resource_id=user_id,
            request=request,
        )
