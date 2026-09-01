import logging
from typing import Any, Dict
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ProjectScopeException(Exception):
    """Base exception for ProjectScope AI"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class EntityNotFoundException(ProjectScopeException):
    """Raised when a requested resource is not found"""
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"entity": entity_name, "id": str(entity_id)}
        )


class LLMProviderException(ProjectScopeException):
    """Raised when an external LLM provider call fails"""
    def __init__(self, message: str, provider: str = "unknown", details: Any = None):
        super().__init__(
            message=f"LLM Provider ({provider}) error: {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class LLMValidationException(ProjectScopeException):
    """Raised when LLM response fails Pydantic schema validation after retries"""
    def __init__(self, message: str, raw_output: str = "", details: Any = None):
        super().__init__(
            message=f"Requirement analysis output validation failed: {message}",
            status_code=422,
            details={"raw_output_snippet": raw_output[:300] if raw_output else None, "errors": details}
        )


class InvalidInputException(ProjectScopeException):
    """Raised when client input is invalid or underspecified"""
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProjectScopeException)
    async def projectscope_exception_handler(request: Request, exc: ProjectScopeException):
        logger.error(f"ProjectScopeException: {exc.message} (status: {exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "details": exc.details,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"RequestValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": "Request payload validation failed.",
                "details": exc.errors(),
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        logger.warning(f"Pydantic ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": "Data validation failed.",
                "details": exc.errors(),
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception during request {request.url.path}: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "An unexpected internal server error occurred.",
                "details": str(exc) if app.debug else None,
            }
        )
