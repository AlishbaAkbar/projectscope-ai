"""
Phase 22: Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.rate_limit import limiter
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    ChangePasswordRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


# ============================================
# REGISTER
# ============================================

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """Register a new user"""
    service = AuthService(db)
    try:
        result = service.register(data)
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ============================================
# LOGIN
# ============================================

@router.post("/login", response_model=AuthResponse)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def login(
    request: Request,
    data: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """Login with email & password"""
    service = AuthService(db)
    try:
        result = service.login(data)
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# ============================================
# REFRESH
# ============================================

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """Refresh access token using refresh token"""
    service = AuthService(db)
    try:
        return TokenResponse(**service.refresh_access_token(data.refresh_token))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# ============================================
# LOGOUT
# ============================================

@router.post("/logout")
async def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """Logout by revoking refresh token"""
    service = AuthService(db)
    service.logout(data.refresh_token)
    return {"message": "Logged out successfully"}


@router.post("/logout-all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Logout from all devices"""
    service = AuthService(db)
    count = service.logout_all(current_user.id)
    return {"message": f"Revoked {count} sessions"}


# ============================================
# CURRENT USER
# ============================================

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user


# ============================================
# CHANGE PASSWORD
# ============================================

@router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password for current user"""
    service = AuthService(db)
    try:
        service.change_password(current_user, data.old_password, data.new_password)
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ============================================
# ACCOUNT DELETION
# ============================================

@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Soft-delete user account.
    All projects become inaccessible (kept for audit).
    """
    from datetime import datetime, timezone

    current_user.deleted_at = datetime.now(timezone.utc)
    current_user.is_active = False

    # Revoke all tokens
    service = AuthService(db)
    service.logout_all(current_user.id)

    db.commit()
    return None
