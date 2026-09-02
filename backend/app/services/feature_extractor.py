import json
import re
from typing import List, Dict, Set, Optional
from pathlib import Path
from difflib import SequenceMatcher

from app.models.feature import Feature
from app.models.project import Requirement 
from app.schemas.features import FeatureCreate

class FeatureExtractor:
    """Extracts and normalizes features from requirements"""
    
    def __init__(self):
        self.mapping_path = Path(__file__).parent.parent / "data" / "feature_mapping.json"
        self.feature_map = self._load_mapping()
        self.canonical_map = self._build_canonical_map()
        
    def _load_mapping(self) -> Dict:
        """Load feature mapping data"""
        with open(self.mapping_path) as f:
            return json.load(f)["feature_normalization"]
    
    def _build_canonical_map(self) -> Dict[str, Dict]:
        """Build reverse mapping from synonyms to canonical features"""
        reverse_map = {}
        for feature_id, data in self.feature_map.items():
            for synonym in data["synonyms"]:
                reverse_map[synonym.lower()] = {
                    "canonical_id": data["canonical_id"],
                    "complexity": data["complexity"],
                    "dependencies": data["dependencies"]
                }
        return reverse_map
    
    def extract_features(self, requirements: List[Requirement]) -> List[Feature]:
        """
        Extract and normalize features from requirements
        
        Args:
            requirements: List of Requirement objects
            
        Returns:
            List of normalized Feature objects
        """
        # Step 1: Extract all feature mentions
        raw_features = self._extract_feature_mentions(requirements)
        
        # Step 2: Normalize to canonical features
        normalized_features = self._normalize_features(raw_features)
        
        # Step 3: Resolve dependencies
        resolved_features = self._resolve_dependencies(normalized_features)
        
        # Step 4: Calculate priorities and complexities
        final_features = self._enrich_features(resolved_features)
        
        return final_features
    
    def _extract_feature_mentions(self, requirements: List[Requirement]) -> List[str]:
        """Extract raw feature mentions from requirement texts"""
        mentions = []
        
        for req in requirements:
            text = req.text.lower()
            
            # Check each synonym against the text
            for synonym in self.canonical_map.keys():
                if synonym in text:
                    mentions.append(synonym)
                    
            # Also extract using regex for phrases
            for pattern in self._get_patterns():
                if re.search(pattern, text):
                    # Find matching feature
                    for feature_id, data in self.feature_map.items():
                        for syn in data["synonyms"]:
                            if re.search(rf'\b{syn}\b', text):
                                mentions.append(syn)
        
        return list(set(mentions))  # Remove duplicates
    
    def _get_patterns(self) -> List[str]:
        """Get regex patterns for common feature phrases"""
        return [
            r'users? can',
            r'customers? can',
            r'admin(s?) can',
            r'allows? users?',
            r'enables? users?',
            r'feature(s?) includes?',
            r'support(s?) for',
            r'with (a|an) ',
            r'need(s?) to',
            r'require(s?) '
        ]
    
    def _normalize_features(self, raw_mentions: List[str]) -> List[Dict]:
        """Normalize raw mentions to canonical features"""
        normalized = {}
        
        for mention in raw_mentions:
            # Exact match
            if mention in self.canonical_map:
                feature_data = self.canonical_map[mention]
                feature_id = feature_data["canonical_id"]
                
                if feature_id not in normalized:
                    normalized[feature_id] = {
                        "canonical_id": feature_id,
                        "matches": [],
                        "complexity": feature_data["complexity"],
                        "dependencies": feature_data["dependencies"]
                    }
                normalized[feature_id]["matches"].append(mention)
            else:
                # Fuzzy match for near-matches
                best_match = self._fuzzy_match(mention)
                if best_match:
                    feature_data = self.canonical_map[best_match]
                    feature_id = feature_data["canonical_id"]
                    
                    if feature_id not in normalized:
                        normalized[feature_id] = {
                            "canonical_id": feature_id,
                            "matches": [],
                            "complexity": feature_data["complexity"],
                            "dependencies": feature_data["dependencies"]
                        }
                    normalized[feature_id]["matches"].append(mention)
        
        return list(normalized.values())
    
    def _fuzzy_match(self, term: str, threshold: float = 0.7) -> Optional[str]:
        """Find best fuzzy match for a term"""
        best_match = None
        best_score = 0
        
        for canonical_term in self.canonical_map.keys():
            score = SequenceMatcher(None, term.lower(), canonical_term.lower()).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = canonical_term
        
        return best_match
    
    def _resolve_dependencies(self, features: List[Dict]) -> List[Dict]:
        """Resolve feature dependencies"""
        resolved = []
        feature_ids = {f["canonical_id"] for f in features}
        
        for feature in features:
            # Check if all dependencies exist
            missing_deps = [dep for dep in feature["dependencies"] if dep not in feature_ids]
            
            if missing_deps:
                # Add missing dependencies as auto-discovered features
                for dep in missing_deps:
                    if dep in self.feature_map:
                        # Find the feature data
                        for feature_id, data in self.feature_map.items():
                            if data["canonical_id"] == dep:
                                resolved.append({
                                    "canonical_id": dep,
                                    "matches": ["auto_discovered"],
                                    "complexity": data["complexity"],
                                    "dependencies": data["dependencies"],
                                    "auto_discovered": True
                                })
            
            resolved.append(feature)
        
        return resolved
    
    def _enrich_features(self, features: List[Dict]) -> List[Feature]:
        """Add priority, confidence, and description"""
        enriched = []
        
        for idx, feature_data in enumerate(features):
            # Determine priority based on dependencies and complexity
            priority = self._calculate_priority(feature_data, idx, len(features))
            
            # Create Feature model
            feature = Feature(
                canonical_name=feature_data["canonical_id"],
                description=self._generate_description(feature_data),
                priority=priority,
                complexity=feature_data["complexity"],
                confidence=0.9 if not feature_data.get("auto_discovered") else 0.6,
                dependencies=feature_data["dependencies"],
                source_requirement_ids=[]  # Will be set by caller
            )
            enriched.append(feature)
        
        return enriched
    
    def _calculate_priority(self, feature_data: Dict, index: int, total: int) -> str:
        """Calculate feature priority"""
        # High priority if many dependencies depend on it
        depends_on_count = 0
        for f in self.feature_map.values():
            if feature_data["canonical_id"] in f["dependencies"]:
                depends_on_count += 1
        
        if depends_on_count > 2 or feature_data["complexity"] >= 5:
            return "HIGH"
        elif depends_on_count > 0 or feature_data["complexity"] >= 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_description(self, feature_data: Dict) -> str:
        """Generate a human-readable description"""
        canonical_id = feature_data["canonical_id"]
        matches = feature_data.get("matches", [])
        
        # Get original phrase
        original_phrase = matches[0] if matches else canonical_id.lower()
        
        descriptions = {
            "AUTHENTICATION": f"User authentication and account management based on: {original_phrase}",
            "USER_MANAGEMENT": f"User profile and account management for: {original_phrase}",
            "PRODUCT_CATALOG": f"Product catalog and inventory management for: {original_phrase}",
            "SEARCH": f"Search functionality for products: {original_phrase}",
            "CART": f"Shopping cart functionality: {original_phrase}",
            "PAYMENT": f"Payment processing and checkout: {original_phrase}",
            "ORDER_MANAGEMENT": f"Order management and tracking: {original_phrase}",
            "ADMIN_PANEL": f"Administration dashboard and management: {original_phrase}",
            "MOBILE_APP": f"Mobile application support: {original_phrase}",
            "REAL_TIME": f"Real-time functionality and live updates: {original_phrase}",
            "REVIEWS": f"Product reviews and ratings: {original_phrase}",
            "NOTIFICATIONS": f"Notification system: {original_phrase}",
            "ANALYTICS": f"Analytics and reporting: {original_phrase}"
        }
        
        return descriptions.get(canonical_id, f"Feature: {canonical_id} ({original_phrase})")