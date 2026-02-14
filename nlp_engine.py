"""
NLP-Powered Chatbot Engine
Implements semantic similarity using embeddings for better query understanding
Phase 2: Advanced NLP integration with transformer models
"""

import json
import pickle
import os
import numpy as np
from typing import List, Dict, Tuple, Optional


class NLPChatbot:
    """
    NLP-powered chatbot using semantic embeddings for intelligent matching.
    Uses sentence transformers for semantic similarity.
    """
    
    def __init__(self, faqs: List[Dict[str, str]], 
                 model_name: str = "all-MiniLM-L6-v2",
                 threshold: float = 0.5,
                 cache_embeddings: bool = True):
        """
        Initialize the NLP chatbot.
        
        Args:
            faqs: List of FAQ dictionaries
            model_name: Name of the sentence transformer model
            threshold: Minimum similarity score for a match
            cache_embeddings: Whether to cache embeddings to disk
        """
        self.faqs = faqs
        self.threshold = threshold
        self.model_name = model_name
        self.cache_file = f"embeddings_{model_name.replace('/', '_')}.pkl"
        self.conversation_history = []
        
        # Initialize model and embeddings
        self.model = None
        self.faq_embeddings = None
        self._initialize_model()
        
        if cache_embeddings and os.path.exists(self.cache_file):
            self._load_cached_embeddings()
        else:
            self._generate_embeddings()
            if cache_embeddings:
                self._cache_embeddings()
    
    def _initialize_model(self) -> None:
        """Initialize the sentence transformer model."""
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print("✓ Model loaded successfully!")
        except ImportError:
            print("ERROR: sentence-transformers not installed.")
            print("Install it with: pip install sentence-transformers")
            raise
        except Exception as e:
            print(f"ERROR loading model: {e}")
            raise
    
    def _generate_embeddings(self) -> None:
        """Generate embeddings for all FAQ questions."""
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        print(f"Generating embeddings for {len(self.faqs)} FAQs...")
        questions = [faq['question'] for faq in self.faqs]
        self.faq_embeddings = self.model.encode(questions, show_progress_bar=True)
        print("✓ Embeddings generated!")
    
    def _cache_embeddings(self) -> None:
        """Cache embeddings to disk."""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.faq_embeddings, f)
            print(f"✓ Embeddings cached to {self.cache_file}")
        except Exception as e:
            print(f"Warning: Could not cache embeddings: {e}")
    
    def _load_cached_embeddings(self) -> None:
        """Load embeddings from cache."""
        try:
            with open(self.cache_file, 'rb') as f:
                self.faq_embeddings = pickle.load(f)
            print(f"✓ Loaded embeddings from cache ({self.cache_file})")
        except Exception as e:
            print(f"Warning: Could not load cached embeddings: {e}")
            print("Generating new embeddings...")
            self._generate_embeddings()
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_best_match(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """
        Find best matching FAQs using semantic similarity.
        
        Args:
            query: User query
            top_k: Number of top matches to return
            
        Returns:
            List of (faq, similarity_score) tuples
        """
        if self.model is None or self.faq_embeddings is None:
            raise RuntimeError("Model or embeddings not initialized")
        
        # Encode the query
        query_embedding = self.model.encode([query])[0]
        
        # Calculate similarities with all FAQs
        similarities = []
        for i, faq_embedding in enumerate(self.faq_embeddings):
            similarity = self._cosine_similarity(query_embedding, faq_embedding)
            similarities.append((self.faqs[i], similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def get_response(self, query: str, return_confidence: bool = False) -> str:
        """
        Get chatbot response using semantic matching.
        
        Args:
            query: User query
            return_confidence: Whether to include confidence in response
            
        Returns:
            Chatbot response
        """
        if not query.strip():
            return "I didn't catch that. Could you please ask a question?"
        
        # Find best matches
        matches = self.find_best_match(query, top_k=3)
        
        if not matches:
            return self._get_fallback_response()
        
        best_match, score = matches[0]
        
        # Log interaction
        self.conversation_history.append({
            'query': query,
            'response': best_match['answer'],
            'score': float(score),
            'method': 'semantic'
        })
        
        # Check confidence threshold
        if score < self.threshold:
            similar_questions = [m[0]['question'] for m in matches[:2]]
            return self._get_fallback_response(similar_questions)
        
        response = best_match['answer']
        
        if return_confidence:
            response += f"\n\n(Confidence: {score:.2%})"
        
        return response
    
    def _get_fallback_response(self, similar_questions: Optional[List[str]] = None) -> str:
        """Generate fallback response."""
        response = "I'm not completely sure about that. "
        
        if similar_questions:
            response += "Perhaps you're asking about:\n"
            for i, q in enumerate(similar_questions, 1):
                response += f"{i}. {q}\n"
            response += "\nPlease rephrase or select one of these questions."
        else:
            response += "Could you rephrase your question?"
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
    
    def add_faq_dynamically(self, question: str, answer: str, category: str = 'general') -> None:
        """
        Add a new FAQ and update embeddings.
        
        Args:
            question: New question
            answer: New answer
            category: Category for the FAQ
        """
        new_faq = {
            'question': question,
            'answer': answer,
            'category': category
        }
        self.faqs.append(new_faq)
        
        # Generate embedding for new question
        new_embedding = self.model.encode([question])[0]
        self.faq_embeddings = np.vstack([self.faq_embeddings, new_embedding])
        
        print(f"✓ Added new FAQ: '{question}'")


class HybridChatbot:
    """
    Hybrid chatbot combining rule-based and NLP approaches.
    Uses both methods and picks the best result.
    """
    
    def __init__(self, rule_based_bot, nlp_bot, 
                 rule_weight: float = 0.3, 
                 nlp_weight: float = 0.7):
        """
        Initialize hybrid chatbot.
        
        Args:
            rule_based_bot: RuleBasedChatbot instance
            nlp_bot: NLPChatbot instance
            rule_weight: Weight for rule-based score
            nlp_weight: Weight for NLP score
        """
        self.rule_bot = rule_based_bot
        self.nlp_bot = nlp_bot
        self.rule_weight = rule_weight
        self.nlp_weight = nlp_weight
        self.conversation_history = []
    
    def get_response(self, query: str, return_confidence: bool = False) -> str:
        """
        Get response using hybrid approach.
        
        Args:
            query: User query
            return_confidence: Whether to include confidence
            
        Returns:
            Best response from either method
        """
        # Get results from both methods
        rule_matches = self.rule_bot.find_best_match(query, top_k=1)
        nlp_matches = self.nlp_bot.find_best_match(query, top_k=1)
        
        rule_score = rule_matches[0][1] if rule_matches else 0
        nlp_score = nlp_matches[0][1] if nlp_matches else 0
        
        # Calculate weighted scores
        rule_weighted = rule_score * self.rule_weight
        nlp_weighted = nlp_score * self.nlp_weight
        
        # Pick the best method
        if rule_weighted > nlp_weighted and rule_matches:
            best_match = rule_matches[0][0]
            final_score = rule_score
            method = 'rule-based'
        elif nlp_matches:
            best_match = nlp_matches[0][0]
            final_score = nlp_score
            method = 'semantic'
        else:
            return "I couldn't find a good answer. Please rephrase your question."
        
        # Log interaction
        self.conversation_history.append({
            'query': query,
            'response': best_match['answer'],
            'score': float(final_score),
            'method': method
        })
        
        response = best_match['answer']
        
        if return_confidence:
            response += f"\n\n(Confidence: {final_score:.2%}, Method: {method})"
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history


if __name__ == "__main__":
    print("NLP Chatbot Engine - Ready for integration")
    print("Requires: sentence-transformers, transformers, torch")
    print("\nInstall with:")
    print("pip install sentence-transformers transformers torch")
