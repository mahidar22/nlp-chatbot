"""
Rule-Based Chatbot Engine
Implements keyword matching and basic similarity for FAQ matching
"""

import re
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher


class RuleBasedChatbot:
    """
    Rule-based chatbot using keyword matching and string similarity.
    Phase 1 implementation with no ML dependencies.
    """
    
    def __init__(self, faqs: List[Dict[str, str]], threshold: float = 0.4):
        """
        Initialize the rule-based chatbot.
        
        Args:
            faqs: List of FAQ dictionaries with 'question' and 'answer' keys
            threshold: Minimum similarity score to consider a match (0-1)
        """
        self.faqs = faqs
        self.threshold = threshold
        self.conversation_history = []
        
        # Build keyword index for faster lookup
        self.keyword_index = self._build_keyword_index()
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text: lowercase, remove punctuation, extra spaces.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation except for important chars
        text = re.sub(r'[^\w\s\?]', ' ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_keywords(self, text: str) -> set:
        """
        Extract keywords from text (remove common stop words).
        
        Args:
            text: Input text
            
        Returns:
            Set of keywords
        """
        # Common stop words to ignore
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'i', 'you', 'can', 'do', 'how',
            'what', 'when', 'where', 'which', 'who', 'why', 'my', 'me'
        }
        
        words = self._preprocess_text(text).split()
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        return keywords
    
    def _build_keyword_index(self) -> Dict[str, List[int]]:
        """
        Build an index mapping keywords to FAQ indices for fast lookup.
        
        Returns:
            Dictionary mapping keywords to list of FAQ indices
        """
        index = {}
        for i, faq in enumerate(self.faqs):
            keywords = self._extract_keywords(faq['question'])
            for keyword in keywords:
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(i)
        return index
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using SequenceMatcher.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        text1 = self._preprocess_text(text1)
        text2 = self._preprocess_text(text2)
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _keyword_match_score(self, query: str, faq_question: str) -> float:
        """
        Calculate keyword match score between query and FAQ question.
        
        Args:
            query: User query
            faq_question: FAQ question to compare
            
        Returns:
            Score between 0 and 1
        """
        query_keywords = self._extract_keywords(query)
        faq_keywords = self._extract_keywords(faq_question)
        
        if not query_keywords:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = query_keywords & faq_keywords
        union = query_keywords | faq_keywords
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _get_candidate_faqs(self, query: str) -> List[int]:
        """
        Get candidate FAQ indices using keyword index.
        
        Args:
            query: User query
            
        Returns:
            List of FAQ indices that share keywords with query
        """
        query_keywords = self._extract_keywords(query)
        candidates = set()
        
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                candidates.update(self.keyword_index[keyword])
        
        # If no keyword matches, return all FAQs
        return list(candidates) if candidates else list(range(len(self.faqs)))
    
    def find_best_match(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """
        Find the best matching FAQ(s) for a query.
        
        Args:
            query: User query
            top_k: Number of top matches to return
            
        Returns:
            List of tuples (faq_dict, score) sorted by score
        """
        # Get candidate FAQs
        candidate_indices = self._get_candidate_faqs(query)
        
        # Score each candidate
        matches = []
        for idx in candidate_indices:
            faq = self.faqs[idx]
            
            # Combine keyword matching and string similarity
            keyword_score = self._keyword_match_score(query, faq['question'])
            similarity_score = self._calculate_similarity(query, faq['question'])
            
            # Weighted combination (60% keywords, 40% similarity)
            combined_score = 0.6 * keyword_score + 0.4 * similarity_score
            
            matches.append((faq, combined_score))
        
        # Sort by score and return top k
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_k]
    
    def get_response(self, query: str, return_confidence: bool = False) -> str:
        """
        Get chatbot response for a query.
        
        Args:
            query: User query
            return_confidence: Whether to include confidence score in response
            
        Returns:
            Chatbot response
        """
        # Handle empty query
        if not query.strip():
            return "I didn't catch that. Could you please rephrase your question?"
        
        # Find best matches
        matches = self.find_best_match(query, top_k=3)
        
        if not matches:
            return self._get_fallback_response()
        
        best_match, score = matches[0]
        
        # Log the interaction
        self.conversation_history.append({
            'query': query,
            'response': best_match['answer'],
            'score': score
        })
        
        # Check if confidence is above threshold
        if score < self.threshold:
            return self._get_fallback_response(similar_questions=[m[0]['question'] for m in matches[:2]])
        
        # Return the answer
        response = best_match['answer']
        
        if return_confidence:
            response += f"\n\n(Confidence: {score:.2%})"
        
        return response
    
    def _get_fallback_response(self, similar_questions: Optional[List[str]] = None) -> str:
        """
        Generate fallback response when no good match is found.
        
        Args:
            similar_questions: List of potentially similar questions
            
        Returns:
            Fallback response
        """
        response = "I'm not quite sure about that. "
        
        if similar_questions:
            response += "Did you mean to ask about:\n"
            for i, q in enumerate(similar_questions, 1):
                response += f"{i}. {q}\n"
            response += "\nPlease rephrase your question or try one of these."
        else:
            response += "Could you please rephrase your question or try asking something else?"
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []


if __name__ == "__main__":
    # Test the rule-based chatbot with sample data
    sample_faqs = [
        {
            "question": "How do I reset my password?",
            "answer": "To reset your password, click on 'Forgot Password' on the login page and follow the instructions.",
            "category": "account"
        },
        {
            "question": "What are your business hours?",
            "answer": "We are open Monday to Friday, 9 AM to 6 PM EST.",
            "category": "general"
        },
        {
            "question": "How can I contact customer support?",
            "answer": "You can reach our customer support via email at support@example.com or call us at 1-800-SUPPORT.",
            "category": "support"
        }
    ]
    
    chatbot = RuleBasedChatbot(sample_faqs)
    
    test_queries = [
        "how to reset password",
        "forgot my password",
        "business hours",
        "contact support team"
    ]
    
    print("Testing Rule-Based Chatbot:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = chatbot.get_response(query, return_confidence=True)
        print(f"Response: {response}")
        print("-" * 60)
