"""
Logger Module
Handles logging of user queries, responses, and analytics
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class ChatLogger:
    """
    Logs conversations and provides analytics.
    """
    
    def __init__(self, log_file: str = "chat_logs.jsonl"):
        """
        Initialize the logger.
        
        Args:
            log_file: Path to the log file (JSONL format)
        """
        self.log_file = log_file
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
    
    def log_interaction(self, query: str, response: str, 
                       score: float = 0.0, 
                       method: str = "unknown",
                       category: str = "general") -> None:
        """
        Log a single interaction.
        
        Args:
            query: User query
            response: Bot response
            score: Confidence score
            method: Method used (rule-based/semantic/hybrid)
            category: FAQ category
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'query': query,
            'response': response,
            'score': score,
            'method': method,
            'category': category
        }
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve recent log entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of log entries
        """
        if not os.path.exists(self.log_file):
            return []
        
        logs = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
            
            # Return most recent entries
            return logs[-limit:]
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get analytics from logged interactions.
        
        Returns:
            Dictionary with analytics data
        """
        logs = self.get_logs(limit=10000)  # Get all logs
        
        if not logs:
            return {
                'total_interactions': 0,
                'message': 'No logs available'
            }
        
        # Calculate analytics
        total = len(logs)
        avg_score = sum(log.get('score', 0) for log in logs) / total if total > 0 else 0
        
        # Count methods used
        methods = {}
        for log in logs:
            method = log.get('method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        # Count categories
        categories = {}
        for log in logs:
            category = log.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        # Low confidence interactions (potential improvements needed)
        low_confidence = [log for log in logs if log.get('score', 0) < 0.5]
        
        # Most common queries
        query_counts = {}
        for log in logs:
            query = log.get('query', '').lower()
            query_counts[query] = query_counts.get(query, 0) + 1
        
        top_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        analytics = {
            'total_interactions': total,
            'average_confidence': avg_score,
            'methods_used': methods,
            'categories': categories,
            'low_confidence_count': len(low_confidence),
            'low_confidence_percentage': (len(low_confidence) / total * 100) if total > 0 else 0,
            'top_queries': [{'query': q, 'count': c} for q, c in top_queries],
            'session_count': len(set(log.get('session_id') for log in logs))
        }
        
        return analytics
    
    def export_analytics_report(self, output_file: str = "analytics_report.json") -> None:
        """
        Export analytics to a JSON file.
        
        Args:
            output_file: Path for the output file
        """
        analytics = self.get_analytics()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analytics, f, indent=2)
            print(f"✓ Analytics report exported to {output_file}")
        except Exception as e:
            print(f"Error exporting analytics: {e}")
    
    def print_analytics(self) -> None:
        """Print analytics to console."""
        analytics = self.get_analytics()
        
        print("\n" + "="*60)
        print("CHATBOT ANALYTICS")
        print("="*60)
        print(f"Total Interactions: {analytics.get('total_interactions', 0)}")
        print(f"Average Confidence: {analytics.get('average_confidence', 0):.2%}")
        print(f"Sessions: {analytics.get('session_count', 0)}")
        
        print(f"\nLow Confidence Interactions: {analytics.get('low_confidence_count', 0)} "
              f"({analytics.get('low_confidence_percentage', 0):.1f}%)")
        
        print("\nMethods Used:")
        for method, count in analytics.get('methods_used', {}).items():
            print(f"  - {method}: {count}")
        
        print("\nTop Queries:")
        for item in analytics.get('top_queries', [])[:5]:
            print(f"  - \"{item['query']}\": {item['count']} times")
        
        print("\nCategories:")
        for category, count in analytics.get('categories', {}).items():
            print(f"  - {category}: {count}")
        
        print("="*60)
    
    def get_unanswered_queries(self, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Get queries that received low-confidence responses.
        
        Args:
            threshold: Confidence threshold
            
        Returns:
            List of low-confidence interactions
        """
        logs = self.get_logs(limit=10000)
        return [log for log in logs if log.get('score', 0) < threshold]
    
    def export_unanswered_queries(self, output_file: str = "unanswered_queries.json",
                                 threshold: float = 0.5) -> None:
        """
        Export unanswered/low-confidence queries for review.
        
        Args:
            output_file: Output file path
            threshold: Confidence threshold
        """
        unanswered = self.get_unanswered_queries(threshold)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(unanswered, f, indent=2)
            print(f"✓ Exported {len(unanswered)} low-confidence queries to {output_file}")
        except Exception as e:
            print(f"Error exporting queries: {e}")


if __name__ == "__main__":
    # Test the logger
    logger = ChatLogger("test_logs.jsonl")
    
    # Log some test interactions
    logger.log_interaction(
        query="How do I reset my password?",
        response="Click 'Forgot Password' on the login page.",
        score=0.95,
        method="semantic",
        category="account"
    )
    
    logger.log_interaction(
        query="business hours?",
        response="We're open 9-5 Monday-Friday.",
        score=0.45,
        method="rule-based",
        category="general"
    )
    
    # Print analytics
    logger.print_analytics()
    
    # Clean up test file
    if os.path.exists("test_logs.jsonl"):
        os.remove("test_logs.jsonl")
