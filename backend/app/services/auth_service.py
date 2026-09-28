"""
Phase 22-23: Authentication Service
Handles user registration, login, token refresh, password change,
session management, with audit logging support.

NO SELF-IMPORT — imports only models, schemas, and core security.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from app.models.user import User, RefreshToken
from app.models.project import Organization
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.schemas.auth import UserRegisterRequest, UserLoginRequest


class AuthService:
    """Authentication & authorization business logic"""

    def __init__(self, db: Session):
        self.db = db

    # ============================================
    # REGISTRATION
    # ============================================

    def register(self, data: UserRegisterRequest) -> Dict[str, Any]:
        """Register a new user (and organization if needed)"""

        # 1. Check for duplicate email
        existing = self.db.query(User).filter(User.email == data.email).first()
        if existing:
            raise ValueError("Email already registered")

        # 2. Get or create organization
        org = self._resolve_organization(data)

        # 3. Create user
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            organization_id=org.id,
            role="owner" if data.organization_name else "member",
            is_active=True,
            is_verified=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # 4. Issue tokens
        return self._generate_auth_response(user, org)

    def _resolve_organization(self, data: UserRegisterRequest) -> Organization:
        """Return existing org or create a new one based on request"""
        # Case A: explicit organization_id provided
        if getattr(data, "organization_id", None):
            org = (
                self.db.query(Organization)
                .filter(Organization.id == data.organization_id)
                .first()
            )
            if not org:
                raise ValueError("Organization not found")
            return org

        # Case B: organization_name provided → create if not exists
        if getattr(data, "organization_name", None):
            org = (
                self.db.query(Organization)
                .filter(Organization.name == data.organization_name)
                .first()
            )
            if not org:
                org = Organization(
                    name=data.organization_name,
                    plan="free",
                    slug=self._slugify(data.organization_name),
                )
                self.db.add(org)
                self.db.commit()
                self.db.refresh(org)
            return org

        # Case C: fallback to first existing org or create default
        org = self.db.query(Organization).first()
        if not org:
            org = Organization(
                name="Default Organization",
                plan="free",
                slug="default",
            )
            self.db.add(org)
            self.db.commit()
            self.db.refresh(org)
        return org

    @staticmethod
    def _slugify(name: str) -> str:
        """Very small slugger for org names"""
        return (
            name.lower()
            .strip()
            .replace(" ", "-")
            .replace("_", "-")[:80]
        )

    # ============================================
    # LOGIN
    # ============================================

    def login(self, data: UserLoginRequest) -> Dict[str, Any]:
        """Authenticate with email + password"""
        user = self.db.query(User).filter(User.email == data.email).first()

        # Do not leak which of email/password is wrong
        if not user:
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        if user.deleted_at:
            raise ValueError("Account has been deleted")

        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        org = (
            self.db.query(Organization)
            .filter(Organization.id == user.organization_id)
            .first()
        )
        if not org:
            raise ValueError("Organization not found for user")

        return self._generate_auth_response(user, org)

    # ============================================
    # TOKEN REFRESH
    # ============================================

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Issue a new access token using a valid refresh token"""
        record = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token,
                RefreshToken.revoked == False,  # noqa: E712
            )
            .first()
        )
        if not record:
            raise ValueError("Invalid refresh token")

        # Handle timezone-naive DB values
        expires = record.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)

        if expires < datetime.now(timezone.utc):
            raise ValueError("Refresh token expired")

        user = (
            self.db.query(User)
            .filter(User.id == record.user_id, User.is_active == True)  # noqa: E712
            .first()
        )
        if not user or user.deleted_at:
            raise ValueError("User not found or inactive")

        access_token = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    # ============================================
    # LOGOUT
    # ============================================

    def logout(self, refresh_token: str) -> bool:
        """Revoke a single refresh token"""
        record = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == refresh_token)
            .first()
        )
        if not record:
            return False
        record.revoked = True
        self.db.commit()
        return True

    def logout_all(self, user_id: int) -> int:
        """Revoke all refresh tokens for a user"""
        count = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,  # noqa: E712
            )
            .update({"revoked": True})
        )
        self.db.commit()
        return int(count or 0)

    # ============================================
    # CHANGE PASSWORD
    # ============================================

    def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str,
    ) -> bool:
        """Change password and revoke all sessions"""
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")

        # Optionally enforce strength here again
        user.password_hash = hash_password(new_password)
        self.db.commit()

        # Invalidate all existing sessions
        self.logout_all(user.id)
        return True

    # ============================================
    # INTERNAL HELPERS
    # ============================================

    def _generate_auth_response(
        self,
        user: User,
        org: Organization,
    ) -> Dict[str, Any]:
        """Create access + refresh tokens and persist refresh token"""
        access_token = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
        )

        refresh_data = create_refresh_token(user.id)

        # Persist refresh token
        record = RefreshToken(
            user_id=user.id,
            token=refresh_data["token"],
            expires_at=refresh_data["expires_at"],
        )
        self.db.add(record)
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_data["token"],
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user,
            "organization": org,
        }