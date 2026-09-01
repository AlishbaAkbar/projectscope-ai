import json
from typing import Optional
from app.ai.providers.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Deterministic Mock LLM Provider for testing and offline local development.
    Analyzes prompt text for domain keywords to return authentic structured analysis JSON.
    """

    def __init__(self, **kwargs):
        pass

    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.generate(prompt, system_prompt)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        text = prompt.lower()

        if any(w in text for w in ["bus", "transport", "vehicle", "route", "driver", "transit"]):
            response_data = {
                "project_type": "transportation",
                "users": ["student", "driver", "transport_admin"],
                "requirements": [
                    {
                        "text": "Students should be able to view available bus schedules and routes.",
                        "category": "functional",
                        "confidence": 0.96
                    },
                    {
                        "text": "Students should be able to track assigned buses in real-time on a map.",
                        "category": "functional",
                        "confidence": 0.94
                    },
                    {
                        "text": "Students should receive push notifications when their bus is approaching.",
                        "category": "functional",
                        "confidence": 0.91
                    },
                    {
                        "text": "Users should be able to report transit delays, breakdowns, or route incidents.",
                        "category": "functional",
                        "confidence": 0.89
                    },
                    {
                        "text": "The platform must ensure location updates latency remains under 3 seconds.",
                        "category": "non_functional",
                        "confidence": 0.88
                    },
                    {
                        "text": "Drivers and students must securely authenticate using university credentials.",
                        "category": "functional",
                        "confidence": 0.95
                    }
                ],
                "features": [
                    {
                        "name": "authentication",
                        "description": "User login, signup, and campus SSO integration",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.95
                    },
                    {
                        "name": "live_tracking",
                        "description": "Real-time GPS vehicle location tracking and route mapping",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.96
                    },
                    {
                        "name": "notifications",
                        "description": "Automated push and SMS arrival and delay notifications",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.92
                    },
                    {
                        "name": "reporting",
                        "description": "Incident, breakdown, and delay reporting workflow",
                        "priority": "medium",
                        "complexity": "medium",
                        "confidence": 0.90
                    },
                    {
                        "name": "admin_panel",
                        "description": "Fleet management, route creation, and dispatch console",
                        "priority": "high",
                        "complexity": "high",
                        "confidence": 0.93
                    }
                ],
                "missing_information": [
                    "Required map and routing API provider (Google Maps vs Mapbox vs OpenStreetMap) is not specified.",
                    "Hardware source for driver GPS telemetry (dedicated GPS tracker vs driver mobile app) is not defined.",
                    "Expected peak student concurrency is not stated."
                ],
                "assumptions": [
                    "Students will primarily access the service via Mobile and Web browsers.",
                    "GPS coordinates will be broadcast via WebSockets or MQTT."
                ]
            }

        elif any(w in text for w in ["shop", "ecommerce", "e-commerce", "cart", "product", "checkout", "store"]):
            response_data = {
                "project_type": "e-commerce",
                "users": ["customer", "merchant", "store_admin"],
                "requirements": [
                    {
                        "text": "Customers must be able to search, filter, and view product catalogs.",
                        "category": "functional",
                        "confidence": 0.98
                    },
                    {
                        "text": "Customers must be able to add products to cart and complete checkout securely.",
                        "category": "functional",
                        "confidence": 0.97
                    },
                    {
                        "text": "System must process payments via card, digital wallets, and local gateways.",
                        "category": "functional",
                        "confidence": 0.95
                    },
                    {
                        "text": "Merchants must be able to manage inventory, product listings, and pricing.",
                        "category": "functional",
                        "confidence": 0.94
                    },
                    {
                        "text": "Payment gateway interactions must comply with PCI-DSS standards.",
                        "category": "non_functional",
                        "confidence": 0.92
                    }
                ],
                "features": [
                    {
                        "name": "authentication",
                        "description": "Customer and seller login with email, password, and social auth",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.95
                    },
                    {
                        "name": "search",
                        "description": "Catalog search, multi-faceted filtering, and sorting",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.94
                    },
                    {
                        "name": "payment",
                        "description": "Secure checkout and payment gateway processing",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.97
                    },
                    {
                        "name": "order_management",
                        "description": "Order placement, tracking, fulfillment, and status updates",
                        "priority": "high",
                        "complexity": "high",
                        "confidence": 0.93
                    },
                    {
                        "name": "admin_panel",
                        "description": "Catalog and inventory management dashboard",
                        "priority": "medium",
                        "complexity": "medium",
                        "confidence": 0.90
                    }
                ],
                "missing_information": [
                    "Target payment provider (Stripe, PayPal, Adyen) is not designated.",
                    "International tax and shipping calculation rules are unspecified."
                ],
                "assumptions": [
                    "The system will be responsive on both desktop and mobile web.",
                    "Inventory levels are updated in near real-time upon order placement."
                ]
            }

        elif any(w in text for w in ["food", "restaurant", "meal", "dish", "dining"]):
            response_data = {
                "project_type": "food_delivery",
                "users": ["customer", "restaurant_partner", "courier", "platform_admin"],
                "requirements": [
                    {
                        "text": "Customers can browse nearby restaurants and customize menu items.",
                        "category": "functional",
                        "confidence": 0.96
                    },
                    {
                        "text": "Customers can place orders and track delivery rider live on GPS map.",
                        "category": "functional",
                        "confidence": 0.95
                    },
                    {
                        "text": "Restaurants can accept/reject incoming orders and update preparation times.",
                        "category": "functional",
                        "confidence": 0.93
                    },
                    {
                        "text": "Couriers receive delivery requests and turn-by-turn navigation.",
                        "category": "functional",
                        "confidence": 0.91
                    }
                ],
                "features": [
                    {
                        "name": "authentication",
                        "description": "Multi-role login and registration for customers, restaurants, and riders",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.95
                    },
                    {
                        "name": "content_management",
                        "description": "Restaurant menus, dish modifiers, and availability toggling",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.92
                    },
                    {
                        "name": "payment",
                        "description": "Order billing and split payout management",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.95
                    },
                    {
                        "name": "live_tracking",
                        "description": "Real-time rider GPS tracking and estimated time of arrival",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.96
                    },
                    {
                        "name": "notifications",
                        "description": "Status alerts for order acceptance, cooking, and delivery",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.91
                    }
                ],
                "missing_information": [
                    "Delivery dispatch algorithm rules (manual vs automated batching) are not defined.",
                    "Commission rate structure is unspecified."
                ],
                "assumptions": [
                    "Riders will use an iOS/Android mobile app with active GPS permissions.",
                    "Restaurants receive orders via a tablet app or web portal."
                ]
            }

        elif any(w in text for w in ["health", "doctor", "appointment", "clinic", "hospital", "patient", "medical"]):
            response_data = {
                "project_type": "healthcare",
                "users": ["patient", "doctor", "receptionist", "medical_admin"],
                "requirements": [
                    {
                        "text": "Patients can search doctors by specialty, location, and availability.",
                        "category": "functional",
                        "confidence": 0.97
                    },
                    {
                        "text": "Patients can book, reschedule, and cancel clinic appointments.",
                        "category": "functional",
                        "confidence": 0.96
                    },
                    {
                        "text": "Doctors can manage their consultation calendar and review patient history.",
                        "category": "functional",
                        "confidence": 0.94
                    },
                    {
                        "text": "All patient health records must adhere to HIPAA / GDPR compliance.",
                        "category": "non_functional",
                        "confidence": 0.98
                    }
                ],
                "features": [
                    {
                        "name": "authentication",
                        "description": "Secure role-based login with MFA for healthcare staff and patients",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.97
                    },
                    {
                        "name": "booking",
                        "description": "Doctor schedule calendar and appointment slot reservation",
                        "priority": "critical",
                        "complexity": "high",
                        "confidence": 0.96
                    },
                    {
                        "name": "user_profile",
                        "description": "Patient medical profile, insurance details, and history",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.92
                    },
                    {
                        "name": "notifications",
                        "description": "Automated SMS and email reminders for upcoming consultations",
                        "priority": "medium",
                        "complexity": "low",
                        "confidence": 0.90
                    },
                    {
                        "name": "admin_panel",
                        "description": "Clinic workflow, staff roster, and audit log management",
                        "priority": "high",
                        "complexity": "high",
                        "confidence": 0.93
                    }
                ],
                "missing_information": [
                    "Whether telemedicine/video consultations are required is not clarified.",
                    "Electronic Health Record (EHR) third-party integration protocol is unspecified."
                ],
                "assumptions": [
                    "All patient data is encrypted at rest and in transit.",
                    "Appointment slots are calculated based on doctor working hours."
                ]
            }

        else:
            # Generic SaaS application analysis fallback
            response_data = {
                "project_type": "saas_application",
                "users": ["end_user", "team_member", "workspace_admin"],
                "requirements": [
                    {
                        "text": "Users must be able to sign up, log in, and manage their organization profile.",
                        "category": "functional",
                        "confidence": 0.95
                    },
                    {
                        "text": "Users must be able to access core workflow features described in the project scope.",
                        "category": "functional",
                        "confidence": 0.92
                    },
                    {
                        "text": "The application must provide an intuitive web dashboard and reporting views.",
                        "category": "functional",
                        "confidence": 0.90
                    },
                    {
                        "text": "The platform must achieve 99.9% uptime and low latency for standard queries.",
                        "category": "non_functional",
                        "confidence": 0.88
                    }
                ],
                "features": [
                    {
                        "name": "authentication",
                        "description": "Secure user registration, authentication, and session handling",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.95
                    },
                    {
                        "name": "user_profile",
                        "description": "User preferences, account details, and workspace settings",
                        "priority": "medium",
                        "complexity": "low",
                        "confidence": 0.91
                    },
                    {
                        "name": "reporting",
                        "description": "Analytical dashboard and usage reporting",
                        "priority": "high",
                        "complexity": "medium",
                        "confidence": 0.90
                    },
                    {
                        "name": "admin_panel",
                        "description": "System administration, user roles, and access management",
                        "priority": "medium",
                        "complexity": "medium",
                        "confidence": 0.89
                    }
                ],
                "missing_information": [
                    "Specific business logic rules and third-party integrations require clarification.",
                    "Expected storage capacity and user volume are not specified."
                ],
                "assumptions": [
                    "The system will be hosted on cloud infrastructure with relational database backing.",
                    "Access is managed through standard role-based access control (RBAC)."
                ]
            }

        return json.dumps(response_data)
