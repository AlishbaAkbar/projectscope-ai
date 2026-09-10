"""
Phase 19: Retriever
Retrieves relevant knowledge for RAG-enhanced explanations
"""

from typing import Dict, List, Optional
from app.rag.knowledge_base import KnowledgeBase, KnowledgeDocument
from app.rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves relevant knowledge for project analysis
    """
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.vector_store = VectorStore()
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize vector store with knowledge base documents"""
        documents = self.knowledge_base.get_all_documents()
        
        docs_for_vector = []
        for doc in documents:
            docs_for_vector.append({
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "category": doc.category,
                "tags": doc.tags,
                "source": doc.source
            })
        
        self.vector_store.add_documents(docs_for_vector)
        print(f"✅ Initialized vector store with {len(docs_for_vector)} documents")
    
    def retrieve_for_project(self, 
                             features: List[str],
                             complexity_score: float,
                             risk_level: str,
                             top_k: int = 5) -> Dict:
        """
        Retrieve relevant knowledge for a project
        
        Args:
            features: List of feature names
            complexity_score: Project complexity score
            risk_level: Project risk level
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with retrieved knowledge
        """
        # Build query from project context
        query_parts = []
        
        # Add feature-specific queries
        for feature in features:
            query_parts.append(feature.lower().replace("_", " "))
        
        # Add complexity context
        if complexity_score > 20:
            query_parts.append("complex project estimation")
        
        # Add risk context
        if risk_level in ["CRITICAL", "HIGH"]:
            query_parts.append("high risk mitigation")
        
        query = " ".join(query_parts)
        
        # Search vector store
        results = self.vector_store.search(query, top_k=top_k)
        
        # Organize results by category
        organized = {
            "templates": [],
            "policies": [],
            "technology": [],
            "features": [],
            "other": []
        }
        
        for result in results:
            category = result.get("category", "other")
            if category == "template":
                organized["templates"].append(result)
            elif category == "policy":
                organized["policies"].append(result)
            elif category == "technology":
                organized["technology"].append(result)
            elif category == "feature":
                organized["features"].append(result)
            else:
                organized["other"].append(result)
        
        return {
            "query": query,
            "total_results": len(results),
            "results": organized,
            "raw_results": results
        }
    
    def retrieve_for_feature(self, feature_name: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve knowledge for a specific feature
        
        Args:
            feature_name: Name of the feature
            top_k: Number of results
            
        Returns:
            List of relevant documents
        """
        query = feature_name.lower().replace("_", " ")
        return self.vector_store.search(query, top_k=top_k)
    
    def get_knowledge_for_explanation(self, 
                                      features: List[str],
                                      complexity_score: float,
                                      risk_level: str) -> Dict:
        """
        Get knowledge formatted for explanation engine
        
        Args:
            features: List of feature names
            complexity_score: Complexity score
            risk_level: Risk level
            
        Returns:
            Dict with knowledge snippets for explanations
        """
        retrieved = self.retrieve_for_project(
            features=features,
            complexity_score=complexity_score,
            risk_level=risk_level,
            top_k=5
        )
        
        # Format for explanation
        knowledge = {
            "templates": [],
            "policies": [],
            "technology": [],
            "features": [],
            "snippets": []
        }
        
        for result in retrieved.get("raw_results", []):
            snippet = {
                "title": result.get("title", ""),
                "content": result.get("content", "")[:500],  # Limit length
                "category": result.get("category", ""),
                "similarity": result.get("similarity", 0)
            }
            
            category = result.get("category", "other")
            if category == "template":
                knowledge["templates"].append(snippet)
            elif category == "policy":
                knowledge["policies"].append(snippet)
            elif category == "technology":
                knowledge["technology"].append(snippet)
            elif category == "feature":
                knowledge["features"].append(snippet)
            
            knowledge["snippets"].append(snippet)
        
        return knowledge
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return self.knowledge_base.get_stats()
    
    def get_all_knowledge(self) -> List[Dict]:
        """Get all knowledge documents"""
        docs = self.knowledge_base.get_all_documents()
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "category": doc.category,
                "tags": doc.tags
            }
            for doc in docs
        ]