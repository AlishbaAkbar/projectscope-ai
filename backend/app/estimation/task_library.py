"""
Task Library with baseline hours and adjustments
"""

from typing import Dict, List, Optional


class TaskLibrary:
    """Central repository for task baselines"""
    
    def __init__(self):
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict:
        """Load all tasks with baseline hours"""
        return {
            # AUTHENTICATION
            "auth_design": {
                "title": "Design authentication flows",
                "role": "UI/UX Designer",
                "base_hours": 8,
                "description": "Design login, registration, password reset screens"
            },
            "auth_backend": {
                "title": "Implement JWT authentication",
                "role": "Backend Developer",
                "base_hours": 12,
                "description": "Set up JWT tokens, refresh tokens, middleware"
            },
            "auth_frontend": {
                "title": "Build authentication UI",
                "role": "Frontend Developer",
                "base_hours": 10,
                "description": "Create login, register, reset password pages"
            },
            "auth_security": {
                "title": "Implement security best practices",
                "role": "Security Engineer",
                "base_hours": 6,
                "description": "Rate limiting, password hashing, session management"
            },
            "auth_testing": {
                "title": "Test authentication flows",
                "role": "QA Engineer",
                "base_hours": 6,
                "description": "Test login, registration, password reset, session expiry"
            },
            
            # PRODUCT CATALOG
            "product_design": {
                "title": "Design product catalog",
                "role": "UI/UX Designer",
                "base_hours": 12,
                "description": "Design product listing, detail pages, categories"
            },
            "product_backend": {
                "title": "Build product API",
                "role": "Backend Developer",
                "base_hours": 16,
                "description": "CRUD operations, filtering, sorting, pagination"
            },
            "product_frontend": {
                "title": "Build product pages",
                "role": "Frontend Developer",
                "base_hours": 14,
                "description": "Create product list, detail, category pages"
            },
            "product_admin": {
                "title": "Build admin product management",
                "role": "Full-Stack Developer",
                "base_hours": 10,
                "description": "Admin interface for product CRUD"
            },
            "product_testing": {
                "title": "Test product catalog",
                "role": "QA Engineer",
                "base_hours": 8,
                "description": "Test CRUD operations, search, filtering"
            },
            
            # CART
            "cart_design": {
                "title": "Design shopping cart",
                "role": "UI/UX Designer",
                "base_hours": 8,
                "description": "Design cart page and checkout flow"
            },
            "cart_backend": {
                "title": "Build cart API",
                "role": "Backend Developer",
                "base_hours": 10,
                "description": "Add, remove, update, checkout endpoints"
            },
            "cart_frontend": {
                "title": "Build cart interface",
                "role": "Frontend Developer",
                "base_hours": 10,
                "description": "Create cart page, mini-cart, checkout flow"
            },
            "cart_testing": {
                "title": "Test cart functionality",
                "role": "QA Engineer",
                "base_hours": 6,
                "description": "Test add, remove, update, checkout"
            },
            
            # PAYMENT
            "payment_design": {
                "title": "Design payment flows",
                "role": "UI/UX Designer",
                "base_hours": 10,
                "description": "Design payment page, confirmation screens"
            },
            "payment_business": {
                "title": "Select payment provider",
                "role": "CEO/Business Owner",
                "base_hours": 4,
                "description": "Research and select payment gateway"
            },
            "payment_backend": {
                "title": "Integrate payment gateway",
                "role": "Backend Developer",
                "base_hours": 16,
                "description": "Payment processing, webhooks, refunds"
            },
            "payment_frontend": {
                "title": "Build payment UI",
                "role": "Frontend Developer",
                "base_hours": 10,
                "description": "Checkout form, payment confirmation"
            },
            "payment_security": {
                "title": "Implement payment security",
                "role": "Security Engineer",
                "base_hours": 8,
                "description": "PCI compliance, tokenization, secure webhooks"
            },
            "payment_testing": {
                "title": "Test payment processing",
                "role": "QA Engineer",
                "base_hours": 10,
                "description": "Test success, failure, refund scenarios"
            },
            
            # ORDER MANAGEMENT
            "order_design": {
                "title": "Design order management",
                "role": "UI/UX Designer",
                "base_hours": 8,
                "description": "Design order history, detail, tracking pages"
            },
            "order_backend": {
                "title": "Build order management API",
                "role": "Backend Developer",
                "base_hours": 12,
                "description": "Order creation, tracking, status endpoints"
            },
            "order_frontend": {
                "title": "Build order interface",
                "role": "Frontend Developer",
                "base_hours": 10,
                "description": "Order history, detail, tracking pages"
            },
            "order_testing": {
                "title": "Test order management",
                "role": "QA Engineer",
                "base_hours": 6,
                "description": "Test order creation, tracking, status updates"
            },
            
            # ADMIN PANEL
            "admin_design": {
                "title": "Design admin dashboard",
                "role": "UI/UX Designer",
                "base_hours": 12,
                "description": "Design admin dashboard layout and management pages"
            },
            "admin_backend": {
                "title": "Build admin APIs",
                "role": "Backend Developer",
                "base_hours": 16,
                "description": "Admin-specific endpoints and permissions"
            },
            "admin_frontend": {
                "title": "Build admin dashboard",
                "role": "Frontend Developer",
                "base_hours": 16,
                "description": "Admin dashboard with analytics and management tools"
            },
            "admin_testing": {
                "title": "Test admin panel",
                "role": "QA Engineer",
                "base_hours": 8,
                "description": "Test admin permissions, CRUD operations"
            },
        }
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a single task by ID"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_role(self, role_name: str) -> List[Dict]:
        """Get all tasks for a specific role"""
        return [
            task for task in self.tasks.values()
            if task.get("role") == role_name
        ]
    
    def get_tasks_by_feature(self, feature_name: str) -> List[Dict]:
        """Get all tasks for a specific feature"""
        prefix = feature_name.lower().replace("_", "")
        return [
            task for task_id, task in self.tasks.items()
            if task_id.startswith(prefix)
        ]
    
    def get_all_tasks(self) -> Dict:
        """Get all tasks"""
        return self.tasks