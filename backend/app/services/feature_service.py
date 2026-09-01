import re
from typing import Dict, List, Set

# Canonical feature keys and their keyword/alias mappings
FEATURE_DICTIONARY: Dict[str, List[str]] = {
    "AUTHENTICATION": [
        "login",
        "log in",
        "sign in",
        "signin",
        "sign up",
        "signup",
        "register",
        "registration",
        "authentication",
        "user auth",
        "account login",
        "sso",
        "oauth",
        "jwt",
        "mfa",
        "two-factor",
        "password reset",
    ],
    "USER_PROFILE": [
        "profile",
        "user profile",
        "account management",
        "user settings",
        "preferences",
        "user account",
        "patient profile",
        "customer profile",
    ],
    "ADMIN_PANEL": [
        "admin",
        "admin panel",
        "admin dashboard",
        "backoffice",
        "back office",
        "management portal",
        "moderation",
        "system administration",
        "management console",
        "superadmin",
    ],
    "PAYMENT": [
        "payment",
        "checkout",
        "billing",
        "stripe",
        "paypal",
        "subscription",
        "pricing",
        "invoice",
        "invoicing",
        "transactions",
        "wallet",
        "payout",
    ],
    "SEARCH": [
        "search",
        "filtering",
        "filter",
        "catalog search",
        "lookup",
        "query",
        "find",
        "faceted search",
        "doctor search",
        "product search",
    ],
    "NOTIFICATIONS": [
        "notification",
        "notifications",
        "alert",
        "alerts",
        "push notification",
        "push notifications",
        "sms",
        "email alert",
        "email alerts",
        "reminders",
        "messaging alert",
    ],
    "LIVE_TRACKING": [
        "live tracking",
        "real-time tracking",
        "realtime tracking",
        "tracking",
        "gps",
        "gps tracking",
        "vehicle tracking",
        "route tracking",
        "map tracking",
        "location tracking",
        "telemetry",
    ],
    "BOOKING": [
        "booking",
        "appointment",
        "appointments",
        "reservation",
        "reservations",
        "scheduling",
        "schedule",
        "calendar",
        "slot booking",
    ],
    "REPORTING": [
        "report",
        "reporting",
        "analytics",
        "metrics",
        "insights",
        "issue reporting",
        "incident reporting",
        "delay reporting",
        "breakdown reporting",
        "dashboard analytics",
    ],
    "COMMUNICATION": [
        "chat",
        "messaging",
        "direct message",
        "in-app messaging",
        "forum",
        "comments",
        "discussion",
        "teleconsultation",
    ],
    "CONTENT_MANAGEMENT": [
        "content management",
        "catalog",
        "menu",
        "menus",
        "dishes",
        "inventory",
        "products",
        "listings",
        "cms",
    ],
    "ORDER_MANAGEMENT": [
        "order",
        "orders",
        "order management",
        "order tracking",
        "order dispatch",
        "fulfillment",
        "cart management",
    ],
    "REVIEWS_RATINGS": [
        "review",
        "reviews",
        "rating",
        "ratings",
        "feedback",
        "star rating",
        "testimonials",
    ],
}


class FeatureService:
    """Service to normalize and categorize feature names"""

    @classmethod
    def normalize_name(cls, raw_name: str) -> str:
        """
        Normalize a raw feature name into a canonical feature key.
        Matches against dictionary synonyms or produces a clean uppercase slug.
        """
        if not raw_name:
            return "GENERAL_FEATURE"

        clean_text = raw_name.lower().strip()
        clean_normalized = re.sub(r"[^a-z0-9\s_-]", "", clean_text)
        tokens = set(re.split(r"[\s_-]+", clean_normalized))

        # Check for exact matches and alias matches in dictionary
        for canonical_key, aliases in FEATURE_DICTIONARY.items():
            for alias in aliases:
                alias_clean = alias.lower()
                # Check direct substring or token match
                if alias_clean in clean_text or alias_clean.replace(" ", "_") in clean_text:
                    return canonical_key
                alias_tokens = set(alias_clean.split())
                if alias_tokens.issubset(tokens):
                    return canonical_key

        # Fallback: Convert to clean uppercase identifier
        slug = re.sub(r"[\s-]+", "_", clean_normalized).strip("_").upper()
        return slug if slug else "CUSTOM_FEATURE"

    @classmethod
    def get_known_features(cls) -> List[str]:
        return list(FEATURE_DICTIONARY.keys())
