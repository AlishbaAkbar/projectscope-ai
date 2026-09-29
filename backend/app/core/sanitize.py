"""
Phase 23: Input Sanitization
Prevents XSS, SQL injection, and prompt injection
"""

import re
from typing import Optional

import bleach

# ============================================
# HTML SANITIZATION
# ============================================

def sanitize_html(text: str) -> str:
    """Remove dangerous HTML/script tags"""
    if not text:
        return ""

    allowed_tags = ["p", "br", "strong", "em", "u", "ul", "ol", "li"]
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes={},
        strip=True,
    )


def sanitize_text(text: str) -> str:
    """Remove HTML entirely, keep plain text"""
    if not text:
        return ""
    return bleach.clean(text, tags=[], strip=True)


# ============================================
# PROMPT INJECTION DEFENSE
# ============================================

# Patterns that indicate prompt injection attempts
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"forget\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"new\s+instructions?:",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?(system\s+)?prompt",
    r"show\s+me\s+(your\s+)?(system\s+)?prompt",
    r"print\s+(your\s+)?(system\s+)?prompt",
    r"ignore\s+the\s+above",
    r"override\s+(your\s+)?instructions?",
    r"developer\s+mode",
    r"jailbreak",
    r"DAN\s+mode",
]

INJECTION_REGEX = re.compile(
    "|".join(f"({p})" for p in INJECTION_PATTERNS),
    re.IGNORECASE,
)


def detect_prompt_injection(text: str) -> bool:
    """Returns True if prompt injection is detected"""
    if not text:
        return False
    return bool(INJECTION_REGEX.search(text))


def sanitize_prompt(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user text before sending to LLM.
    - Removes control characters
    - Caps length
    - Neutralizes common injection patterns
    """
    if not text:
        return ""

    # Remove control chars (except newline/tab)
    text = "".join(c for c in text if c >= " " or c in "\n\t")

    # Cap length
    if len(text) > max_length:
        text = text[:max_length]

    # Neutralize injection patterns by escaping them
    text = INJECTION_REGEX.sub(
        lambda m: "[REDACTED-INSTRUCTION]",
        text,
    )

    return text.strip()


# ============================================
# GENERAL INPUT VALIDATION
# ============================================

def validate_email(email: str) -> bool:
    """Basic email format validation"""
    if not email or len(email) > 255:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_no_sql_injection(text: str) -> bool:
    """Check for common SQL injection patterns"""
    if not text:
        return True
    dangerous = [
        r";\s*drop\s+table",
        r";\s*delete\s+from",
        r"union\s+select",
        r"--\s*$",
        r"/\*.*\*/",
    ]
    for pattern in dangerous:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True
