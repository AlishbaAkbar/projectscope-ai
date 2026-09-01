from typing import Dict, List
from app.schemas.tasks import TaskBase

# Deterministic task library templates for canonical features
CANONICAL_TASK_TEMPLATES: Dict[str, List[dict]] = {
    "AUTHENTICATION": [
        {
            "title": "Create User Authentication UI",
            "description": "Implement responsive login, registration, password recovery forms, and authentication state management.",
            "category": "Frontend",
            "estimated_hours": 8.0,
        },
        {
            "title": "Implement Authentication & Token API",
            "description": "Create secure login, register, token refresh, and logout endpoints with JWT/OAuth validation.",
            "category": "Backend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Design User & Credentials Database Schema",
            "description": "Create users, roles, password hashes, and session tables with unique constraints and indices.",
            "category": "Database",
            "estimated_hours": 4.0,
        },
        {
            "title": "Write Authentication Security & Flow Tests",
            "description": "Develop unit and integration tests covering password hashing, invalid credentials, token expiration, and CSRF protection.",
            "category": "QA",
            "estimated_hours": 6.0,
        },
    ],
    "LIVE_TRACKING": [
        {
            "title": "Build Real-time Map & Tracking UI",
            "description": "Render interactive map container with live moving markers, route polyline overlays, and ETA widgets.",
            "category": "Frontend",
            "estimated_hours": 14.0,
        },
        {
            "title": "Implement Real-time Telemetry & Location API",
            "description": "Build WebSocket or SSE endpoints to ingest, broadcast, and stream low-latency GPS coordinate updates.",
            "category": "Backend",
            "estimated_hours": 16.0,
        },
        {
            "title": "Create Geospatial Telemetry Data Model",
            "description": "Design spatial indices, vehicle location history, and active session cache (Redis / PostGIS).",
            "category": "Database",
            "estimated_hours": 6.0,
        },
        {
            "title": "Integrate Mapping & Routing Provider",
            "description": "Connect external maps/directions API (Google Maps, Mapbox, or OpenStreetMap) for route calculation.",
            "category": "Integration",
            "estimated_hours": 8.0,
        },
        {
            "title": "Test Telemetry Latency & Disconnection Scenarios",
            "description": "Perform end-to-end tests for socket reconnections, packet drops, and high-frequency GPS updates.",
            "category": "QA",
            "estimated_hours": 6.0,
        },
    ],
    "PAYMENT": [
        {
            "title": "Build Checkout & Payment Method UI",
            "description": "Develop order summary, credit card input form (Stripe Elements / SDK), and payment status confirmation screen.",
            "category": "Frontend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Create Payment Intent & Webhook API",
            "description": "Implement server-side payment creation, charge capture, refund handling, and asynchronous webhook verification.",
            "category": "Backend",
            "estimated_hours": 14.0,
        },
        {
            "title": "Design Transactions & Invoicing Schema",
            "description": "Model transaction logs, payment states (pending, succeeded, failed), invoices, and audit trail tables.",
            "category": "Database",
            "estimated_hours": 6.0,
        },
        {
            "title": "Integrate Payment Gateway SDK",
            "description": "Configure payment provider client (Stripe/PayPal), sandbox credentials, and webhook secrets.",
            "category": "Integration",
            "estimated_hours": 6.0,
        },
        {
            "title": "Test Idempotency & Failed Payment Handling",
            "description": "Execute automated test suites for double-charge prevention, declined cards, and webhook replay protection.",
            "category": "QA",
            "estimated_hours": 8.0,
        },
    ],
    "NOTIFICATIONS": [
        {
            "title": "Build In-App Notification Center UI",
            "description": "Implement notification bell dropdown, badge count, notification history list, and toast alerts.",
            "category": "Frontend",
            "estimated_hours": 6.0,
        },
        {
            "title": "Create Notification Dispatch Service",
            "description": "Build asynchronous worker queue to dispatch push notifications, emails, and SMS based on system triggers.",
            "category": "Backend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Model Notification Logs & Preferences Schema",
            "description": "Create notification templates, delivery log records, and user notification opt-in preferences.",
            "category": "Database",
            "estimated_hours": 4.0,
        },
        {
            "title": "Integrate Push/SMS Delivery Provider",
            "description": "Connect external delivery gateway (Firebase Cloud Messaging, Twilio, SendGrid/Resend).",
            "category": "Integration",
            "estimated_hours": 6.0,
        },
        {
            "title": "Test Multi-Channel Notification Delivery",
            "description": "Verify template formatting, rate limits, unsubscribe handling, and deliverability status tracking.",
            "category": "QA",
            "estimated_hours": 4.0,
        },
    ],
    "SEARCH": [
        {
            "title": "Build Search & Filter Interface",
            "description": "Develop auto-complete search bar, faceted filter sidebar, sorting dropdowns, and paginated results grid.",
            "category": "Frontend",
            "estimated_hours": 8.0,
        },
        {
            "title": "Implement Search & Query API",
            "description": "Build high-performance search endpoint with full-text indexing, fuzzy search, and multi-field filtering.",
            "category": "Backend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Optimize Database Indexes for Querying",
            "description": "Create Gin/trigram indexes, composite search indices, or search engine synchronization pipeline.",
            "category": "Database",
            "estimated_hours": 6.0,
        },
        {
            "title": "Test Search Relevance & Boundary Filters",
            "description": "Validate empty queries, special character sanitization, pagination limits, and large-dataset performance.",
            "category": "QA",
            "estimated_hours": 4.0,
        },
    ],
    "BOOKING": [
        {
            "title": "Build Interactive Booking Calendar UI",
            "description": "Create responsive date/time slot picker, booking confirmation modal, and appointment management view.",
            "category": "Frontend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Develop Booking & Slot Reservation API",
            "description": "Build endpoints for available slot calculation, double-booking collision prevention, and booking lifecycle (book/cancel/reschedule).",
            "category": "Backend",
            "estimated_hours": 12.0,
        },
        {
            "title": "Design Appointment & Availability Schema",
            "description": "Model recurring availability rules, exceptions, reserved time slots, and status history with foreign keys.",
            "category": "Database",
            "estimated_hours": 6.0,
        },
        {
            "title": "Test Concurrent Booking Race Conditions",
            "description": "Conduct stress and concurrency tests to ensure two users cannot book the same slot simultaneously.",
            "category": "QA",
            "estimated_hours": 6.0,
        },
    ],
    "ADMIN_PANEL": [
        {
            "title": "Create Admin Management Dashboard UI",
            "description": "Implement metrics overview cards, data tables with bulk actions, and administrative configuration forms.",
            "category": "Frontend",
            "estimated_hours": 12.0,
        },
        {
            "title": "Implement Admin Management API",
            "description": "Create secure admin endpoints protected by RBAC for user moderation, system metrics, and audit logging.",
            "category": "Backend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Create Audit Trail & System Config Schema",
            "description": "Design audit logs table tracking operator ID, action performed, IP address, and timestamp.",
            "category": "Database",
            "estimated_hours": 4.0,
        },
        {
            "title": "Test Role-Based Access Controls",
            "description": "Verify unauthorized users and standard accounts cannot access administrative routes or actions.",
            "category": "QA",
            "estimated_hours": 4.0,
        },
    ],
    "REPORTING": [
        {
            "title": "Build Incident & Issue Submission UI",
            "description": "Create issue reporting forms with category selection, description input, attachment uploads, and status tracker.",
            "category": "Frontend",
            "estimated_hours": 6.0,
        },
        {
            "title": "Create Issue Reporting & Status API",
            "description": "Implement endpoints to create, assign, update, and resolve reported incidents with triage workflows.",
            "category": "Backend",
            "estimated_hours": 8.0,
        },
        {
            "title": "Design Reports & Incident Schema",
            "description": "Model report categories, severities, status enum, attachments, and resolution timestamps.",
            "category": "Database",
            "estimated_hours": 4.0,
        },
        {
            "title": "Test Report Submission & Triage Flows",
            "description": "Test validation on required report fields, attachment size limits, and resolution state machine.",
            "category": "QA",
            "estimated_hours": 4.0,
        },
    ],
    "USER_PROFILE": [
        {
            "title": "Build User Profile & Settings UI",
            "description": "Create profile editing screen, avatar upload, password change modal, and preference toggles.",
            "category": "Frontend",
            "estimated_hours": 6.0,
        },
        {
            "title": "Create Profile Management API",
            "description": "Implement GET and PUT profile endpoints with input sanitization and image upload processing.",
            "category": "Backend",
            "estimated_hours": 6.0,
        },
        {
            "title": "Design Profile & Preferences Schema",
            "description": "Model user bio, metadata, localized settings, and avatar storage references.",
            "category": "Database",
            "estimated_hours": 3.0,
        },
        {
            "title": "Test Profile Updates & Input Validation",
            "description": "Verify field length limits, email uniqueness checks, and secure image MIME type validation.",
            "category": "QA",
            "estimated_hours": 3.0,
        },
    ],
    "ORDER_MANAGEMENT": [
        {
            "title": "Build Order Placement & History UI",
            "description": "Develop cart review, active order tracking timeline, and past order history views.",
            "category": "Frontend",
            "estimated_hours": 10.0,
        },
        {
            "title": "Implement Order Lifecycle & Fulfillment API",
            "description": "Create state machine endpoints for placing, accepting, preparing, dispatching, and completing orders.",
            "category": "Backend",
            "estimated_hours": 12.0,
        },
        {
            "title": "Design Order & Order Items Database Schema",
            "description": "Model orders, line items, pricing snapshots, fulfillment statuses, and historical tracking.",
            "category": "Database",
            "estimated_hours": 6.0,
        },
        {
            "title": "Test Order State Transitions & Edge Cases",
            "description": "Verify invalid state transitions are blocked and total prices are strictly calculated server-side.",
            "category": "QA",
            "estimated_hours": 6.0,
        },
    ],
}


class TaskService:
    """Service to generate deterministic baseline tasks for features"""

    @classmethod
    def generate_tasks_for_feature(
        cls,
        normalized_key: str,
        feature_name: str,
        description: str
    ) -> List[TaskBase]:
        """
        Generate a list of baseline development tasks for a feature.
        Uses canonical templates if available, otherwise generates a clean full-stack baseline.
        """
        if normalized_key in CANONICAL_TASK_TEMPLATES:
            templates = CANONICAL_TASK_TEMPLATES[normalized_key]
            return [
                TaskBase(
                    title=t["title"],
                    description=t["description"],
                    category=t["category"],
                    estimated_hours=t["estimated_hours"]
                )
                for t in templates
            ]

        # Generic baseline for custom/unmatched features
        formatted_name = feature_name.replace("_", " ").title()
        return [
            TaskBase(
                title=f"Build {formatted_name} User Interface",
                description=f"Create interactive frontend views and user flows for {formatted_name.lower()} ({description}).",
                category="Frontend",
                estimated_hours=8.0,
            ),
            TaskBase(
                title=f"Implement {formatted_name} Business Logic & API",
                description=f"Develop backend REST endpoints, validation, and domain service for {formatted_name.lower()}.",
                category="Backend",
                estimated_hours=10.0,
            ),
            TaskBase(
                title=f"Design {formatted_name} Data Persistence Schema",
                description=f"Model database tables, relations, and indices required to support {formatted_name.lower()}.",
                category="Database",
                estimated_hours=4.0,
            ),
            TaskBase(
                title=f"Write Test Suite for {formatted_name}",
                description=f"Implement unit tests, integration tests, and edge-case validation for {formatted_name.lower()}.",
                category="QA",
                estimated_hours=5.0,
            ),
        ]
