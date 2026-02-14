"""
Usage Examples for FAQ Chatbot
Demonstrates various ways to use the chatbot programmatically
"""

# Example 1: Basic Rule-Based Chatbot
def example_rule_based():
    """Simple rule-based chatbot usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Rule-Based Chatbot")
    print("="*60)
    
    from data_loader import DataLoader
    from rule_based_engine import RuleBasedChatbot
    
    # Load data
    loader = DataLoader()
    loader.load_from_cache()
    faqs = loader.get_all_faqs()
    
    # Create chatbot
    chatbot = RuleBasedChatbot(faqs, threshold=0.4)
    
    # Test queries
    queries = [
        "How do I reset my password?",
        "What are your business hours?",
        "How can I contact support?",
        "shipping information",
        "return policy"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = chatbot.get_response(query, return_confidence=True)
        print(f"Response: {response}")
        print("-" * 60)


# Example 2: NLP-Powered Chatbot
def example_nlp():
    """NLP-powered semantic matching."""
    print("\n" + "="*60)
    print("EXAMPLE 2: NLP-Powered Chatbot")
    print("="*60)
    
    try:
        from data_loader import DataLoader
        from nlp_engine import NLPChatbot
        
        # Load data
        loader = DataLoader()
        loader.load_from_cache()
        faqs = loader.get_all_faqs()
        
        # Create NLP chatbot
        print("Initializing NLP chatbot...")
        chatbot = NLPChatbot(faqs, threshold=0.5)
        
        # Test with paraphrased queries
        queries = [
            "I forgot my login credentials",  # Similar to "reset password"
            "When are you open?",             # Similar to "business hours"
            "How do I reach customer service?" # Similar to "contact support"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            response = chatbot.get_response(query, return_confidence=True)
            print(f"Response: {response}")
            print("-" * 60)
            
    except ImportError:
        print("NLP libraries not installed. Install with:")
        print("pip install sentence-transformers transformers torch")


# Example 3: Hybrid Approach
def example_hybrid():
    """Combine rule-based and NLP approaches."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Hybrid Chatbot")
    print("="*60)
    
    try:
        from data_loader import DataLoader
        from rule_based_engine import RuleBasedChatbot
        from nlp_engine import NLPChatbot, HybridChatbot
        
        # Load data
        loader = DataLoader()
        loader.load_from_cache()
        faqs = loader.get_all_faqs()
        
        # Create both engines
        rule_bot = RuleBasedChatbot(faqs, threshold=0.4)
        nlp_bot = NLPChatbot(faqs, threshold=0.5)
        
        # Create hybrid chatbot
        hybrid = HybridChatbot(rule_bot, nlp_bot)
        
        # Test queries
        queries = [
            "password reset help",  # Direct match - rule-based wins
            "I can't log into my account",  # Semantic - NLP wins
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            response = hybrid.get_response(query, return_confidence=True)
            print(f"Response: {response}")
            print("-" * 60)
            
    except ImportError:
        print("NLP libraries not installed.")


# Example 4: Using Analytics
def example_analytics():
    """Demonstrate logging and analytics."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Analytics and Logging")
    print("="*60)
    
    from data_loader import DataLoader
    from rule_based_engine import RuleBasedChatbot
    from logger import ChatLogger
    
    # Setup
    loader = DataLoader()
    loader.load_from_cache()
    faqs = loader.get_all_faqs()
    
    chatbot = RuleBasedChatbot(faqs)
    logger = ChatLogger("example_logs.jsonl")
    
    # Simulate conversation
    queries = [
        "How do I reset my password?",
        "What are your hours?",
        "Can I return an item?",
        "blah blah blah"  # Low confidence query
    ]
    
    for query in queries:
        response = chatbot.get_response(query)
        
        # Log the interaction
        history = chatbot.get_conversation_history()
        if history:
            last = history[-1]
            logger.log_interaction(
                query=query,
                response=response,
                score=last.get('score', 0),
                method='rule-based'
            )
    
    # Show analytics
    logger.print_analytics()
    
    # Export low-confidence queries
    logger.export_unanswered_queries("low_confidence.json", threshold=0.5)
    
    # Cleanup
    import os
    if os.path.exists("example_logs.jsonl"):
        os.remove("example_logs.jsonl")
    if os.path.exists("low_confidence.json"):
        os.remove("low_confidence.json")


# Example 5: Adding Custom FAQs
def example_custom_faqs():
    """Add custom FAQs dynamically."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Adding Custom FAQs")
    print("="*60)
    
    from data_loader import DataLoader
    from rule_based_engine import RuleBasedChatbot
    
    loader = DataLoader()
    loader.load_from_cache()
    
    # Add new FAQs
    print("\nAdding custom FAQs...")
    loader.add_faq(
        question="What is your company's mission?",
        answer="Our mission is to provide excellent customer service and innovative solutions.",
        category="about"
    )
    
    loader.add_faq(
        question="Do you offer technical support?",
        answer="Yes, we offer 24/7 technical support via email and phone.",
        category="support"
    )
    
    # Create chatbot with updated FAQs
    faqs = loader.get_all_faqs()
    chatbot = RuleBasedChatbot(faqs)
    
    # Test new FAQs
    queries = [
        "What is your mission?",
        "Do you have tech support?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = chatbot.get_response(query)
        print(f"Response: {response}")
        print("-" * 60)


# Example 6: Category-Based Search
def example_categories():
    """Search within specific categories."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Category-Based FAQ Retrieval")
    print("="*60)
    
    from data_loader import DataLoader
    
    loader = DataLoader()
    loader.load_from_cache()
    
    # Show all categories
    categories = loader.get_categories()
    print(f"\nAvailable categories: {', '.join(categories)}")
    
    # Get FAQs by category
    for category in categories[:3]:  # Show first 3 categories
        faqs = loader.get_faqs_by_category(category)
        print(f"\n{category.upper()} ({len(faqs)} FAQs):")
        for i, faq in enumerate(faqs[:2], 1):  # Show first 2 from each
            print(f"  {i}. Q: {faq['question']}")
            print(f"     A: {faq['answer'][:60]}...")


# Example 7: Custom Data Source
def example_custom_data():
    """Load FAQs from custom file."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Custom Data Source")
    print("="*60)
    
    import json
    from data_loader import DataLoader
    from rule_based_engine import RuleBasedChatbot
    
    # Create sample custom FAQs
    custom_faqs = [
        {
            "question": "How do I install the software?",
            "answer": "Download the installer from our website and run it.",
            "category": "installation"
        },
        {
            "question": "What are the system requirements?",
            "answer": "Windows 10 or later, 4GB RAM, 500MB disk space.",
            "category": "technical"
        },
        {
            "question": "Is there a mobile app?",
            "answer": "Yes, we have apps for iOS and Android.",
            "category": "mobile"
        }
    ]
    
    # Save to file
    with open("custom_faqs.json", "w") as f:
        json.dump(custom_faqs, f, indent=2)
    
    # Load from custom file
    loader = DataLoader()
    loader.load_from_custom_file("custom_faqs.json")
    
    # Create chatbot
    faqs = loader.get_all_faqs()
    chatbot = RuleBasedChatbot(faqs)
    
    # Test
    queries = ["installation help", "system requirements", "mobile version"]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = chatbot.get_response(query)
        print(f"Response: {response}")
        print("-" * 60)
    
    # Cleanup
    import os
    if os.path.exists("custom_faqs.json"):
        os.remove("custom_faqs.json")


# Example 8: Batch Processing
def example_batch():
    """Process multiple queries in batch."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Batch Query Processing")
    print("="*60)
    
    from data_loader import DataLoader
    from rule_based_engine import RuleBasedChatbot
    
    loader = DataLoader()
    loader.load_from_cache()
    faqs = loader.get_all_faqs()
    
    chatbot = RuleBasedChatbot(faqs)
    
    # Batch queries
    queries = [
        "reset password",
        "business hours",
        "contact info",
        "shipping policy",
        "return process"
    ]
    
    # Process all at once
    results = []
    for query in queries:
        matches = chatbot.find_best_match(query, top_k=1)
        if matches:
            faq, score = matches[0]
            results.append({
                'query': query,
                'answer': faq['answer'],
                'score': score
            })
    
    # Display results
    print(f"\nProcessed {len(queries)} queries:\n")
    for result in results:
        print(f"Q: {result['query']}")
        print(f"A: {result['answer'][:60]}...")
        print(f"Confidence: {result['score']:.2%}\n")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("FAQ CHATBOT - USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        ("Rule-Based Chatbot", example_rule_based),
        ("NLP-Powered Chatbot", example_nlp),
        ("Hybrid Chatbot", example_hybrid),
        ("Analytics & Logging", example_analytics),
        ("Adding Custom FAQs", example_custom_faqs),
        ("Category-Based Search", example_categories),
        ("Custom Data Source", example_custom_data),
        ("Batch Processing", example_batch)
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\nOptions:")
    print("  - Enter number (1-8) to run specific example")
    print("  - Enter 'all' to run all examples")
    print("  - Enter 'q' to quit")
    
    choice = input("\nYour choice: ").strip().lower()
    
    if choice == 'q':
        print("Goodbye!")
        return
    
    if choice == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {e}")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                name, func = examples[idx]
                func()
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")


if __name__ == "__main__":
    main()
