"""
Mock AI Provider — analyzes project description and generates
requirements based on keywords in the text.
"""

import json
import re
from typing import Dict, Any, Optional
from app.ai.providers.base import BaseProvider


class MockLLMProvider(BaseProvider):
    """
    Offline mock provider that extracts requirements from description text.
    Uses keyword matching to generate project-specific requirements.
    """

    def __init__(self, **kwargs):
        pass

    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.generate(prompt, system_prompt)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return json.dumps(self.analyze_requirements(prompt))

    @staticmethod
    def _detect_project_type(description: str) -> str:
        ordered_domains = (
            ("healthcare", ("health", "doctor", "appointment", "clinic", "hospital", "patient", "medical")),
            ("transportation", ("bus", "transport", "vehicle", "route", "driver", "transit")),
            ("food_delivery", ("food", "restaurant", "meal", "dish", "dining")),
            ("e-commerce", ("shop", "ecommerce", "e-commerce", "cart", "product", "checkout", "store")),
        )
        for project_type, keywords in ordered_domains:
            if any(keyword in description for keyword in keywords):
                return project_type
        return "saas"
    
    # Keyword → (feature, category) mapping
    FEATURE_KEYWORDS = {
        # Authentication
        "login": ("AUTHENTICATION", "functional"),
        "signup": ("AUTHENTICATION", "functional"),
        "sign up": ("AUTHENTICATION", "functional"),
        "register": ("AUTHENTICATION", "functional"),
        "password": ("AUTHENTICATION", "functional"),
        "authentication": ("AUTHENTICATION", "functional"),
        "mfa": ("AUTHENTICATION", "technical"),
        "2fa": ("AUTHENTICATION", "technical"),
        "oauth": ("AUTHENTICATION", "technical"),
        "social login": ("AUTHENTICATION", "functional"),
        
        # Product catalog
        "product": ("PRODUCT_CATALOG", "functional"),
        "catalog": ("PRODUCT_CATALOG", "functional"),
        "inventory": ("PRODUCT_CATALOG", "functional"),
        "listing": ("PRODUCT_CATALOG", "functional"),
        
        # Cart & Checkout
        "cart": ("CART", "functional"),
        "basket": ("CART", "functional"),
        "checkout": ("CART", "functional"),
        
        # Payment
        "payment": ("PAYMENT", "functional"),
        "stripe": ("PAYMENT", "technical"),
        "paypal": ("PAYMENT", "technical"),
        "billing": ("PAYMENT", "functional"),
        "invoice": ("PAYMENT", "functional"),
        "subscription": ("PAYMENT", "functional"),
        "pricing": ("PAYMENT", "functional"),
        
        # Search
        "search": ("SEARCH", "functional"),
        "filter": ("SEARCH", "functional"),
        "sort": ("SEARCH", "functional"),
        
        # Orders
        "order": ("ORDER_MANAGEMENT", "functional"),
        "tracking": ("ORDER_MANAGEMENT", "functional"),
        "shipment": ("ORDER_MANAGEMENT", "functional"),
        "delivery": ("ORDER_MANAGEMENT", "functional"),
        
        # Admin
        "admin": ("ADMIN_PANEL", "functional"),
        "dashboard": ("ADMIN_PANEL", "functional"),
        "management": ("ADMIN_PANEL", "functional"),
        "staff": ("ADMIN_PANEL", "functional"),
        
        # Mobile
        "mobile": ("MOBILE_APP", "functional"),
        "ios": ("MOBILE_APP", "functional"),
        "android": ("MOBILE_APP", "functional"),
        "app": ("MOBILE_APP", "functional"),
        
        # Real-time
        "real-time": ("REAL_TIME", "technical"),
        "realtime": ("REAL_TIME", "technical"),
        "live": ("REAL_TIME", "functional"),
        "chat": ("REAL_TIME", "functional"),
        "websocket": ("REAL_TIME", "technical"),
        "notification": ("NOTIFICATIONS", "functional"),
        "reminder": ("NOTIFICATIONS", "functional"),
        "email": ("NOTIFICATIONS", "functional"),
        "sms": ("NOTIFICATIONS", "functional"),
        
        # Video
        "video": ("VIDEO_CONFERENCE", "functional"),
        "call": ("VIDEO_CONFERENCE", "functional"),
        "consultation": ("VIDEO_CONFERENCE", "functional"),
        
        # Scheduling
        "appointment": ("APPOINTMENT_SCHEDULING", "functional"),
        "scheduling": ("APPOINTMENT_SCHEDULING", "functional"),
        "calendar": ("APPOINTMENT_SCHEDULING", "functional"),
        "booking": ("APPOINTMENT_SCHEDULING", "functional"),
        
        # Records
        "record": ("RECORDS_MANAGEMENT", "functional"),
        "ehr": ("RECORDS_MANAGEMENT", "technical"),
        "history": ("RECORDS_MANAGEMENT", "functional"),
        "medical": ("RECORDS_MANAGEMENT", "functional"),
        "patient": ("RECORDS_MANAGEMENT", "functional"),
        
        # Prescriptions
        "prescription": ("PRESCRIPTION_MANAGEMENT", "functional"),
        "pharmacy": ("PRESCRIPTION_MANAGEMENT", "functional"),
        "medication": ("PRESCRIPTION_MANAGEMENT", "functional"),
        
        # Reports
        "report": ("REPORTS", "functional"),
        "analytics": ("ANALYTICS", "functional"),
        "insight": ("ANALYTICS", "functional"),
        "chart": ("ANALYTICS", "functional"),
        
        # Reviews
        "review": ("REVIEWS", "functional"),
        "rating": ("REVIEWS", "functional"),
        "feedback": ("REVIEWS", "functional"),
        
        # Content
        "blog": ("CONTENT_MANAGEMENT", "functional"),
        "post": ("CONTENT_MANAGEMENT", "functional"),
        "article": ("CONTENT_MANAGEMENT", "functional"),
        "forum": ("CONTENT_MANAGEMENT", "functional"),
        "discussion": ("CONTENT_MANAGEMENT", "functional"),
        
        # Learning
        "course": ("LEARNING_MANAGEMENT", "functional"),
        "lesson": ("LEARNING_MANAGEMENT", "functional"),
        "student": ("LEARNING_MANAGEMENT", "functional"),
        "quiz": ("LEARNING_MANAGEMENT", "functional"),
        "certificate": ("LEARNING_MANAGEMENT", "functional"),
        
        # Compliance
        "hipaa": ("COMPLIANCE", "technical"),
        "gdpr": ("COMPLIANCE", "technical"),
        "pci": ("COMPLIANCE", "technical"),
        "compliance": ("COMPLIANCE", "technical"),
        "audit": ("COMPLIANCE", "technical"),
        
        # Security
        "security": ("SECURITY", "technical"),
        "encryption": ("SECURITY", "technical"),
        "secure": ("SECURITY", "technical"),
        
        # Other
        "progress": ("PROGRESS_TRACKING", "functional"),
        "recommendation": ("RECOMMENDATIONS", "functional"),
        "integration": ("EXTERNAL_INTEGRATIONS", "technical"),
        "api": ("API_INTEGRATION", "technical"),
    }
    
    # Non-functional requirements patterns
    NFR_PATTERNS = [
        (r"responsive|mobile-friendly|adaptive", "NON_FUNCTIONAL", "The system must be responsive and mobile-friendly", "non_functional"),
        (r"scalable|scalability|load", "NON_FUNCTIONAL", "The system must be scalable under load", "non_functional"),
        (r"secure|encrypt|safety", "NON_FUNCTIONAL", "The system must ensure data security and encryption", "non_functional"),
        (r"fast|performance|<(\d+)\s*(ms|s|seconds)|latency", "NON_FUNCTIONAL", "The system must meet performance SLAs", "non_functional"),
        (r"available|uptime|reliable", "NON_FUNCTIONAL", "The system must ensure high availability", "non_functional"),
    ]
    
    def analyze_requirements(self, project_description: str) -> Dict[str, Any]:
        """Extract requirements from project description using keyword matching"""

        description_match = re.search(
            r'Project Description:\s*"""(.*?)"""',
            project_description,
            re.IGNORECASE | re.DOTALL,
        )
        source_text = description_match.group(1) if description_match else project_description
        description = source_text.lower()
        project_type = self._detect_project_type(description)
        detected_features = set()
        requirements = []
        
        # 1. Detect features from keywords
        for keyword, (feature, category) in self.FEATURE_KEYWORDS.items():
            if keyword in description:
                detected_features.add(feature)
        
        # 2. Generate requirements for detected features
        feature_reqs = {
            "AUTHENTICATION": ("Users can register and login securely", "functional"),
            "PRODUCT_CATALOG": ("System provides a searchable product catalog", "functional"),
            "CART": ("Users can add products to a shopping cart", "functional"),
            "PAYMENT": ("System processes online payments securely", "functional"),
            "SEARCH": ("Users can search and filter items", "functional"),
            "ORDER_MANAGEMENT": ("Users can track orders and view history", "functional"),
            "ADMIN_PANEL": ("Administrators manage system via dashboard", "functional"),
            "MOBILE_APP": ("System supports mobile application access", "functional"),
            "REAL_TIME": ("System provides real-time updates and live features", "technical"),
            "NOTIFICATIONS": ("System sends email/SMS notifications", "functional"),
            "VIDEO_CONFERENCE": ("Users can conduct video consultations", "functional"),
            "APPOINTMENT_SCHEDULING": ("Users can schedule appointments via calendar", "functional"),
            "RECORDS_MANAGEMENT": ("System stores and manages user records securely", "functional"),
            "PRESCRIPTION_MANAGEMENT": ("System manages prescriptions and pharmacy integration", "functional"),
            "REPORTS": ("System generates reports for administrators", "functional"),
            "ANALYTICS": ("System provides analytics and insights", "functional"),
            "REVIEWS": ("Users can leave reviews and ratings", "functional"),
            "CONTENT_MANAGEMENT": ("System supports content publishing and management", "functional"),
            "LEARNING_MANAGEMENT": ("System supports courses, lessons, and student progress", "functional"),
            "COMPLIANCE": ("System ensures regulatory compliance (HIPAA/GDPR/PCI)", "technical"),
            "SECURITY": ("System implements security best practices", "technical"),
            "PROGRESS_TRACKING": ("System tracks user progress over time", "functional"),
            "RECOMMENDATIONS": ("System provides personalized recommendations", "functional"),
            "EXTERNAL_INTEGRATIONS": ("System integrates with external services", "technical"),
            "API_INTEGRATION": ("System provides/exposes REST APIs", "technical"),
        }
        
        for feature in detected_features:
            if feature in feature_reqs:
                text, category = feature_reqs[feature]
                requirements.append({
                    "text": text,
                    "category": category,
                    "feature": feature,
                    "confidence": 0.9,
                })
        
        # 3. Detect non-functional requirements
        for pattern, _, text, category in self.NFR_PATTERNS:
            if re.search(pattern, description):
                requirements.append({
                    "text": text,
                    "category": category,
                    "feature": "NON_FUNCTIONAL",
                    "confidence": 0.85,
                })
        
        # 4. If nothing detected, use fallback
        if not requirements:
            requirements = []

        missing_information = []
        if not requirements:
            missing_information.append("What primary actions should users be able to perform?")
        if project_type == "healthcare" and not any(
            keyword in description for keyword in ("hipaa", "privacy", "compliance", "regulation")
        ):
            missing_information.append("What healthcare privacy and regulatory requirements apply?")

        personas = (
            ("patient", ("patient",)),
            ("doctor", ("doctor", "physician", "clinician")),
            ("admin", ("admin", "administrator")),
            ("student", ("student",)),
            ("driver", ("driver",)),
            ("restaurant staff", ("restaurant",)),
            ("customer", ("customer", "shopper", "buyer")),
        )
        users = [
            persona
            for persona, keywords in personas
            if any(keyword in description for keyword in keywords)
        ]

        # 5. Build final response
        return {
            "project_type": project_type,
            "users": users,
            "requirements": requirements,
            "features": [
                {
                    "canonical_name": feat,
                    "description": feature_reqs.get(feat, ("Feature", "functional"))[0],
                    "priority": "HIGH",
                    "complexity": 3 if feat in ["CART", "SEARCH", "REVIEWS"] else 4,
                    "confidence": 0.9,
                }
                for feat in sorted(detected_features)
            ],
            "missing_information": missing_information,
            "assumptions": [
                "Project scope remains stable",
                "Required resources are available",
            ],
            "total_estimated_hours": 0,
        }
    
MockProvider = MockLLMProvider