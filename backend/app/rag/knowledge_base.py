"""
Phase 19: Knowledge Base
Stores approved project knowledge, templates, and policies
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


@dataclass
class KnowledgeDocument:
    """Single knowledge document"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str] = field(default_factory=list)
    source: str = "internal"
    version: str = "1.0"
    created_at: str = ""
    updated_at: str = ""


class KnowledgeBase:
    """
    Manages approved knowledge documents for RAG
    """
    
    def __init__(self):
        self.documents: Dict[str, KnowledgeDocument] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_default_knowledge()
    
    def _load_default_knowledge(self):
        """Load default knowledge documents"""
        
        # Project Templates
        self.add_document(KnowledgeDocument(
            id="template_ecommerce",
            title="E-commerce Project Template",
            content="""
            E-commerce projects typically include:
            - User authentication (login, registration, password reset)
            - Product catalog with search and filtering
            - Shopping cart and checkout flow
            - Payment gateway integration (Stripe, PayPal)
            - Order management and tracking
            - Admin dashboard for product management
            - Email notifications for orders
            
            Typical timeline: 8-12 weeks
            Typical team: 1 designer, 2 developers, 1 QA
            Typical cost range: $15,000 - $50,000
            """,
            category="template",
            tags=["ecommerce", "web", "payment", "cart"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="template_saas",
            title="SaaS Platform Template",
            content="""
            SaaS projects typically include:
            - Multi-tenant architecture
            - User authentication and role management
            - Subscription billing and payments
            - Admin dashboard with analytics
            - API for integrations
            - Email notifications and alerts
            
            Typical timeline: 12-20 weeks
            Typical team: 1 designer, 3 developers, 1 QA, 1 DevOps
            Typical cost range: $40,000 - $150,000
            """,
            category="template",
            tags=["saas", "subscription", "multi-tenant"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="template_mobile",
            title="Mobile App Template",
            content="""
            Mobile app projects typically include:
            - Native or cross-platform development
            - User authentication and profiles
            - Push notifications
            - Offline capabilities
            - App store submission and approval
            
            Typical timeline: 10-16 weeks
            Typical team: 1 designer, 2 mobile developers, 1 QA
            Typical cost range: $25,000 - $80,000
            """,
            category="template",
            tags=["mobile", "ios", "android", "app"]
        ))
        
        # Estimation Policies
        self.add_document(KnowledgeDocument(
            id="policy_estimation",
            title="Estimation Policy",
            content="""
            Estimation Guidelines:
            - Always provide min/expected/max ranges (±20%)
            - Use 8-hour working days, Monday-Friday
            - Include 15-20% buffer for unknowns
            - Complexity scores 1-10 (5+ is high)
            - Payment integration adds 30% complexity
            - Mobile adds 50% complexity
            - Real-time features add 40% complexity
            
            Confidence Levels:
            - High: >80% (well-understood requirements)
            - Medium: 60-80% (some unknowns)
            - Low: <60% (many unknowns)
            """,
            category="policy",
            tags=["estimation", "guidelines", "confidence"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="policy_risk",
            title="Risk Assessment Policy",
            content="""
            Risk Assessment Guidelines:
            - All projects have inherent risks
            - Security risks are HIGH for payment/user data
            - Compliance risks for GDPR/PCI
            - Technical risks for complex features
            - Schedule risks for tight timelines
            - Always provide mitigation strategies
            
            Risk Levels:
            - CRITICAL: Immediate action required
            - HIGH: Address within sprint
            - MEDIUM: Monitor and plan
            - LOW: Acceptable
            """,
            category="policy",
            tags=["risk", "assessment", "mitigation"]
        ))
        
        # Technology Guidance
        self.add_document(KnowledgeDocument(
            id="tech_stack_web",
            title="Recommended Web Stack",
            content="""
            Recommended Web Technology Stack:
            - Frontend: React/Next.js with TypeScript
            - Backend: Python FastAPI or Node.js Express
            - Database: PostgreSQL or MySQL
            - Cache: Redis
            - Queue: Celery or Bull
            - Deployment: Docker + AWS/GCP
            - CI/CD: GitHub Actions
            
            For e-commerce: Add Stripe, Elasticsearch
            For real-time: Add WebSockets, Redis Pub/Sub
            """,
            category="technology",
            tags=["web", "stack", "react", "fastapi"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="tech_stack_mobile",
            title="Recommended Mobile Stack",
            content="""
            Recommended Mobile Technology Stack:
            - Cross-platform: React Native or Flutter
            - Native iOS: Swift + SwiftUI
            - Native Android: Kotlin + Jetpack Compose
            - Backend: Same as web (FastAPI/Node)
            - Push: Firebase Cloud Messaging
            - Analytics: Firebase or Mixpanel
            
            For e-commerce mobile: Add Stripe SDK
            """,
            category="technology",
            tags=["mobile", "react-native", "flutter", "ios", "android"]
        ))
        
        # Feature Definitions
        self.add_document(KnowledgeDocument(
            id="feature_auth",
            title="Authentication Feature Guide",
            content="""
            Authentication Implementation:
            - JWT tokens with refresh mechanism
            - Password hashing (bcrypt/argon2)
            - Email verification
            - Password reset flow
            - Rate limiting for login attempts
            - Optional: Social login (Google, Facebook)
            - Optional: Two-factor authentication
            
            Estimated hours: 20-40 (depending on complexity)
            Roles involved: Backend, Frontend, Security, QA
            """,
            category="feature",
            tags=["auth", "login", "jwt", "security"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="feature_payment",
            title="Payment Integration Guide",
            content="""
            Payment Integration:
            - Stripe or PayPal recommended
            - PCI compliance required
            - Webhook handling for events
            - Refund and dispute handling
            - Multiple currency support (optional)
            - Subscription support (optional)
            
            Estimated hours: 40-80 (depending on complexity)
            Roles involved: Backend, Frontend, Security, QA, Business
            Risks: Security, Compliance, Integration
            """,
            category="feature",
            tags=["payment", "stripe", "paypal", "pci"]
        ))
        
        self.add_document(KnowledgeDocument(
            id="feature_realtime",
            title="Real-time Features Guide",
            content="""
            Real-time Implementation:
            - WebSockets for live updates
            - Redis Pub/Sub for scaling
            - Socket.io or native WebSockets
            - Connection management
            - Fallback to polling
            
            Estimated hours: 30-60
            Roles involved: Backend, Frontend, DevOps, QA
            Risks: Scalability, Technical
            """,
            category="feature",
            tags=["realtime", "websocket", "socket"]
        ))
        
        # Update categories
        self._update_categories()
    
    def _update_categories(self):
        """Update category index"""
        self.categories = {}
        for doc in self.documents.values():
            if doc.category not in self.categories:
                self.categories[doc.category] = []
            self.categories[doc.category].append(doc.id)
    
    def add_document(self, document: KnowledgeDocument):
        """Add a document to knowledge base"""
        if not document.created_at:
            document.created_at = datetime.now().isoformat()
        document.updated_at = datetime.now().isoformat()
        
        self.documents[document.id] = document
        
        if document.category not in self.categories:
            self.categories[document.category] = []
        if document.id not in self.categories[document.category]:
            self.categories[document.category].append(document.id)
    
    def get_document(self, doc_id: str) -> Optional[KnowledgeDocument]:
        """Get document by ID"""
        return self.documents.get(doc_id)
    
    def get_documents_by_category(self, category: str) -> List[KnowledgeDocument]:
        """Get all documents in a category"""
        doc_ids = self.categories.get(category, [])
        return [self.documents[doc_id] for doc_id in doc_ids if doc_id in self.documents]
    
    def get_documents_by_tags(self, tags: List[str]) -> List[KnowledgeDocument]:
        """Get documents matching any tag"""
        results = []
        for doc in self.documents.values():
            if any(tag in doc.tags for tag in tags):
                results.append(doc)
        return results
    
    def search(self, query: str) -> List[KnowledgeDocument]:
        """Simple text search in knowledge base"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents.values():
            if (query_lower in doc.title.lower() or 
                query_lower in doc.content.lower() or
                any(query_lower in tag.lower() for tag in doc.tags)):
                results.append(doc)
        
        return results
    
    def get_all_documents(self) -> List[KnowledgeDocument]:
        """Get all documents"""
        return list(self.documents.values())
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "total_documents": len(self.documents),
            "categories": {cat: len(docs) for cat, docs in self.categories.items()},
            "total_tags": len(set(tag for doc in self.documents.values() for tag in doc.tags))
        }