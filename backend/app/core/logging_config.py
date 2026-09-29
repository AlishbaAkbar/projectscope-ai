"""
Phase 26: Structured Logging Configuration
Uses structlog for JSON logs with correlation IDs.
"""

import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Optional
import structlog

from app.core.config import settings


# Context variable for request ID (async-safe)
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
user_id_var: ContextVar[Optional[int]] = ContextVar("user_id", default=None)
org_id_var: ContextVar[Optional[int]] = ContextVar("org_id", default=None)


def get_request_id() -> str:
    """Get or create request ID for current context"""
    rid = request_id_var.get()
    if not rid:
        rid = str(uuid.uuid4())[:8]
        request_id_var.set(rid)
    return rid


def set_request_id(request_id: str):
    """Set request ID in context"""
    request_id_var.set(request_id)


def set_user_context(user_id: int, org_id: int):
    """Set user context in logs"""
    user_id_var.set(user_id)
    org_id_var.set(org_id)


def add_context(logger, method_name, event_dict):
    """Add context variables to every log entry"""
    event_dict["request_id"] = request_id_var.get() or "-"
    event_dict["user_id"] = user_id_var.get()
    event_dict["org_id"] = org_id_var.get()
    event_dict["env"] = settings.APP_ENV
    return event_dict


def configure_logging():
    """Configure structlog for structured JSON logs"""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            add_context,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if not settings.DEBUG else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if not settings.DEBUG else logging.DEBUG
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


# Global logger
logger = configure_logging()