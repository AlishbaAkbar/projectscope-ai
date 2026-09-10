"""
Phase 19: Vector Store
Simple vector store for RAG (using TF-IDF for now, can be replaced with embeddings)
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from pathlib import Path


class VectorStore:
    """
    Simple vector store for document retrieval
    Uses TF-IDF for now, can be upgraded to embeddings later
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.documents = []
        self.vectors = None
        self.is_fitted = False
    
    def add_documents(self, documents: List[Dict]):
        """
        Add documents to vector store
        
        Args:
            documents: List of dicts with 'id', 'content', 'title', 'metadata'
        """
        self.documents = documents
        
        # Extract content for vectorization
        texts = [doc.get("content", "") for doc in documents]
        
        if texts:
            self.vectors = self.vectorizer.fit_transform(texts)
            self.is_fitted = True
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of documents with similarity scores
        """
        if not self.is_fitted or not self.documents:
            return []
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                doc = self.documents[idx].copy()
                doc["similarity"] = round(float(similarities[idx]), 4)
                results.append(doc)
        
        return results
    
    def save(self, filepath: str = "ml/models/vector_store.pkl"):
        """Save vector store to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        joblib.dump({
            "vectorizer": self.vectorizer,
            "documents": self.documents,
            "vectors": self.vectors,
            "is_fitted": self.is_fitted
        }, filepath)
        print(f"✅ Vector store saved to {filepath}")
    
    def load(self, filepath: str = "ml/models/vector_store.pkl"):
        """Load vector store from file"""
        if not Path(filepath).exists():
            print(f"⚠️ Vector store not found at {filepath}")
            return False
        
        data = joblib.load(filepath)
        self.vectorizer = data["vectorizer"]
        self.documents = data["documents"]
        self.vectors = data["vectors"]
        self.is_fitted = data["is_fitted"]
        print(f"✅ Vector store loaded from {filepath}")
        return True
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            "total_documents": len(self.documents),
            "is_fitted": self.is_fitted,
            "vector_dimensions": self.vectors.shape[1] if self.vectors is not None else 0
        }