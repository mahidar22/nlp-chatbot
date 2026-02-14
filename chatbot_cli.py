#!/usr/bin/env python3
"""
Command-Line Interface for FAQ Chatbot
Provides an interactive terminal-based chat interface
"""

import sys
import os
from typing import Optional

# Import modules
from data_loader import DataLoader
from rule_based_engine import RuleBasedChatbot
from logger import ChatLogger

# Try to import NLP engine (optional)
try:
    from nlp_engine import NLPChatbot, HybridChatbot
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


class ChatbotCLI:
    """
    Command-line interface for the chatbot.
    """
    
    def __init__(self, mode: str = 'rule', threshold: float = 0.4):
        """
        Initialize the CLI.
        
        Args:
            mode: Chatbot mode ('rule', 'nlp', or 'hybrid')
            threshold: Confidence threshold
        """
        self.mode = mode
        self.threshold = threshold
        self.loader = DataLoader()
        self.logger = ChatLogger()
        self.chatbot = None
        
        # Load data
        self._load_data()
        
        # Initialize chatbot
        self._initialize_chatbot()
    
    def _load_data(self) -> None:
        """Load FAQ data from cache or download."""
        print("\n" + "="*60)
        print("FAQ CHATBOT - INITIALIZING")
        print("="*60)
        
        # Try to load from cache first
        if self.loader.load_from_cache():
            return
        
        # If cache doesn't exist, try to download
        print("\nCache not found. Attempting to download dataset...")
        if not self.loader.load_from_huggingface():
            print("\n" + "!"*60)
            print("ERROR: Could not load FAQ data!")
            print("!"*60)
            print("\nPlease run the following command first:")
            print("  python data_loader.py")
            print("\nOr ensure you have internet connection and 'datasets' library installed:")
            print("  pip install datasets")
            sys.exit(1)
    
    def _initialize_chatbot(self) -> None:
        """Initialize the chatbot based on selected mode."""
        faqs = self.loader.get_all_faqs()
        
        if not faqs:
            print("ERROR: No FAQs loaded!")
            sys.exit(1)
        
        print(f"\nLoaded {len(faqs)} FAQs")
        print(f"Mode: {self.mode.upper()}")
        
        if self.mode == 'rule':
            self.chatbot = RuleBasedChatbot(faqs, threshold=self.threshold)
            print("✓ Rule-based chatbot initialized")
            
        elif self.mode == 'nlp':
            if not NLP_AVAILABLE:
                print("\n" + "!"*60)
                print("ERROR: NLP mode requires additional libraries!")
                print("!"*60)
                print("\nPlease install:")
                print("  pip install sentence-transformers transformers torch")
                print("\nFalling back to rule-based mode...")
                self.mode = 'rule'
                self.chatbot = RuleBasedChatbot(faqs, threshold=self.threshold)
            else:
                print("Initializing NLP chatbot (this may take a moment)...")
                self.chatbot = NLPChatbot(faqs, threshold=self.threshold)
                print("✓ NLP chatbot initialized")
                
        elif self.mode == 'hybrid':
            if not NLP_AVAILABLE:
                print("\nWARNING: Hybrid mode requires NLP libraries. Using rule-based only.")
                self.mode = 'rule'
                self.chatbot = RuleBasedChatbot(faqs, threshold=self.threshold)
            else:
                print("Initializing hybrid chatbot...")
                rule_bot = RuleBasedChatbot(faqs, threshold=self.threshold)
                nlp_bot = NLPChatbot(faqs, threshold=self.threshold)
                self.chatbot = HybridChatbot(rule_bot, nlp_bot)
                print("✓ Hybrid chatbot initialized")
        else:
            print(f"ERROR: Unknown mode '{self.mode}'")
            sys.exit(1)
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "="*60)
        print("WELCOME TO THE FAQ CHATBOT!")
        print("="*60)
        print(f"Mode: {self.mode.upper()}")
        print(f"Confidence Threshold: {self.threshold:.0%}")
        print("\nCommands:")
        print("  - Type your question to get an answer")
        print("  - 'help' - Show available commands")
        print("  - 'stats' - Show chatbot statistics")
        print("  - 'history' - Show conversation history")
        print("  - 'clear' - Clear conversation history")
        print("  - 'exit' or 'quit' - Exit the chatbot")
        print("="*60 + "\n")
    
    def print_help(self) -> None:
        """Print help information."""
        print("\n" + "="*60)
        print("AVAILABLE COMMANDS")
        print("="*60)
        print("help       - Show this help message")
        print("stats      - Display chatbot statistics")
        print("history    - Show conversation history")
        print("clear      - Clear conversation history")
        print("analytics  - Show detailed analytics")
        print("categories - List available FAQ categories")
        print("exit/quit  - Exit the chatbot")
        print("="*60 + "\n")
    
    def print_stats(self) -> None:
        """Print chatbot statistics."""
        stats = self.loader.get_stats()
        print("\n" + "="*60)
        print("CHATBOT STATISTICS")
        print("="*60)
        print(f"Total FAQs: {stats['total_faqs']}")
        print(f"Categories: {len(stats['categories'])}")
        print("\nFAQs per Category:")
        for cat, count in sorted(stats['category_counts'].items()):
            print(f"  - {cat}: {count}")
        print("="*60 + "\n")
    
    def print_history(self) -> None:
        """Print conversation history."""
        history = self.chatbot.get_conversation_history()
        
        if not history:
            print("\nNo conversation history yet.\n")
            return
        
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        for i, entry in enumerate(history, 1):
            print(f"\n[{i}] Query: {entry['query']}")
            print(f"    Score: {entry.get('score', 0):.2%}")
            print(f"    Answer: {entry['response'][:100]}...")
        print("="*60 + "\n")
    
    def print_categories(self) -> None:
        """Print available categories."""
        categories = self.loader.get_categories()
        print("\n" + "="*60)
        print("AVAILABLE CATEGORIES")
        print("="*60)
        for cat in categories:
            count = len(self.loader.get_faqs_by_category(cat))
            print(f"  - {cat}: {count} FAQs")
        print("="*60 + "\n")
    
    def run(self) -> None:
        """Run the interactive chatbot."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                query = input("You: ").strip()
                
                # Handle empty input
                if not query:
                    continue
                
                # Handle commands
                if query.lower() in ['exit', 'quit', 'bye']:
                    print("\nThank you for using the FAQ Chatbot! Goodbye! 👋\n")
                    break
                
                elif query.lower() == 'help':
                    self.print_help()
                    continue
                
                elif query.lower() == 'stats':
                    self.print_stats()
                    continue
                
                elif query.lower() == 'history':
                    self.print_history()
                    continue
                
                elif query.lower() == 'clear':
                    self.chatbot.clear_history()
                    print("\n✓ Conversation history cleared.\n")
                    continue
                
                elif query.lower() == 'analytics':
                    self.logger.print_analytics()
                    continue
                
                elif query.lower() == 'categories':
                    self.print_categories()
                    continue
                
                # Get chatbot response
                response = self.chatbot.get_response(query)
                
                # Log the interaction
                history = self.chatbot.get_conversation_history()
                if history:
                    last_entry = history[-1]
                    self.logger.log_interaction(
                        query=query,
                        response=response,
                        score=last_entry.get('score', 0),
                        method=self.mode
                    )
                
                # Print response
                print(f"\nBot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'exit' to quit.\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")
                continue


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='FAQ Chatbot - Command Line Interface')
    parser.add_argument('--mode', type=str, default='rule',
                       choices=['rule', 'nlp', 'hybrid'],
                       help='Chatbot mode: rule (keyword matching), nlp (semantic), or hybrid')
    parser.add_argument('--threshold', type=float, default=0.4,
                       help='Confidence threshold (0-1)')
    
    args = parser.parse_args()
    
    # Create and run CLI
    cli = ChatbotCLI(mode=args.mode, threshold=args.threshold)
    cli.run()


if __name__ == "__main__":
    main()
