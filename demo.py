#!/usr/bin/env python3
"""
Quick Demo - FAQ Chatbot
Demonstrates the chatbot with sample data
"""

import json
from rule_based_engine import RuleBasedChatbot
from logger import ChatLogger


def load_sample_data():
    """Load sample FAQ data."""
    with open('sample_faqs.json', 'r') as f:
        return json.load(f)


def demo_basic_usage():
    """Demo basic chatbot usage."""
    print("\n" + "="*70)
    print(" FAQ CHATBOT - QUICK DEMO")
    print("="*70)
    
    # Load sample data
    print("\n📚 Loading sample FAQ data...")
    faqs = load_sample_data()
    print(f"✓ Loaded {len(faqs)} FAQs")
    
    # Create chatbot
    print("\n🤖 Initializing rule-based chatbot...")
    chatbot = RuleBasedChatbot(faqs, threshold=0.35)
    print("✓ Chatbot ready!")
    
    # Demo queries
    print("\n" + "="*70)
    print(" TESTING DIFFERENT QUERY TYPES")
    print("="*70)
    
    test_cases = [
        {
            "title": "Exact Match",
            "query": "How do I reset my password?",
            "description": "Query exactly matches FAQ"
        },
        {
            "title": "Keyword Match",
            "query": "password reset help",
            "description": "Keywords match the FAQ"
        },
        {
            "title": "Partial Match",
            "query": "business hours",
            "description": "Partial keyword match"
        },
        {
            "title": "Synonym/Paraphrase",
            "query": "How can I get in touch with support?",
            "description": "Similar meaning, different words"
        },
        {
            "title": "Category Question",
            "query": "shipping time",
            "description": "Question about shipping"
        },
        {
            "title": "Low Confidence",
            "query": "tell me about your company",
            "description": "Query not in FAQs"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {test['title']}")
        print(f"Description: {test['description']}")
        print(f"\n💬 User: {test['query']}")
        
        # Get response
        response = chatbot.get_response(test['query'])
        history = chatbot.get_conversation_history()
        score = history[-1].get('score', 0) if history else 0
        
        print(f"🤖 Bot: {response}")
        print(f"📊 Confidence: {score:.1%}")
        print("-" * 70)


def demo_analytics():
    """Demo analytics features."""
    print("\n" + "="*70)
    print(" ANALYTICS DEMO")
    print("="*70)
    
    faqs = load_sample_data()
    chatbot = RuleBasedChatbot(faqs, threshold=0.35)
    logger = ChatLogger("demo_logs.jsonl")
    
    # Simulate conversation
    queries = [
        "reset password",
        "business hours",
        "shipping time",
        "return policy",
        "contact support",
        "random gibberish query that won't match"
    ]
    
    print("\n📝 Simulating conversation...")
    for query in queries:
        response = chatbot.get_response(query)
        history = chatbot.get_conversation_history()
        if history:
            last = history[-1]
            logger.log_interaction(
                query=query,
                response=response,
                score=last.get('score', 0),
                method='rule-based'
            )
    
    print(f"✓ Processed {len(queries)} queries")
    
    # Show analytics
    logger.print_analytics()
    
    # Cleanup
    import os
    if os.path.exists("demo_logs.jsonl"):
        os.remove("demo_logs.jsonl")


def demo_categories():
    """Demo category-based features."""
    print("\n" + "="*70)
    print(" CATEGORY-BASED FEATURES")
    print("="*70)
    
    faqs = load_sample_data()
    
    # Count by category
    categories = {}
    for faq in faqs:
        cat = faq.get('category', 'general')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📂 FAQs by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  • {cat.title()}: {count} FAQs")
    
    # Show sample from each category
    print("\n📋 Sample FAQs from each category:")
    shown_categories = set()
    for faq in faqs:
        cat = faq.get('category', 'general')
        if cat not in shown_categories:
            print(f"\n  [{cat.upper()}]")
            print(f"  Q: {faq['question']}")
            print(f"  A: {faq['answer'][:80]}...")
            shown_categories.add(cat)
            if len(shown_categories) >= 5:  # Show 5 categories
                break


def demo_interactive():
    """Simple interactive demo."""
    print("\n" + "="*70)
    print(" INTERACTIVE DEMO")
    print("="*70)
    
    faqs = load_sample_data()
    chatbot = RuleBasedChatbot(faqs, threshold=0.35)
    
    print("\n💬 Ask me anything! (Type 'quit' to exit)")
    print("-" * 70)
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break
            
            if not query:
                continue
            
            response = chatbot.get_response(query)
            history = chatbot.get_conversation_history()
            score = history[-1].get('score', 0) if history else 0
            
            print(f"\nBot: {response}")
            print(f"(Confidence: {score:.1%})")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.\n")
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    """Main demo menu."""
    print("\n" + "="*70)
    print("   ______ ___    ____        ________  _____  __________  ____ ____ ")
    print("  / ____//   |  / __ \\      / ____/ / / /   |/_  __/ __ )/ __ \\/_  __/")
    print(" / /_   / /| | / / / /_____/ /   / /_/ / /| | / / / __  / / / / / /   ")
    print("/ __/  / ___ |/ /_/ /_____/ /___/ __  / ___ |/ / / /_/ / /_/ / / /    ")
    print("/_/   /_/  |_|\\___\\_\\     \\____/_/ /_/_/  |_/_/ /_____/\\____/ /_/     ")
    print("="*70)
    print("\nWelcome to the FAQ Chatbot Demo!")
    print("\nThis demo uses sample customer support FAQs to showcase the chatbot.")
    
    print("\n📋 Demo Options:")
    print("  1. Basic Usage Demo - See how the chatbot handles different queries")
    print("  2. Analytics Demo - View logging and analytics features")
    print("  3. Category Demo - Explore category-based organization")
    print("  4. Interactive Mode - Chat with the bot yourself")
    print("  5. Run All Demos")
    print("  q. Quit")
    
    choice = input("\nSelect option (1-5 or q): ").strip()
    
    if choice == '1':
        demo_basic_usage()
    elif choice == '2':
        demo_analytics()
    elif choice == '3':
        demo_categories()
    elif choice == '4':
        demo_interactive()
    elif choice == '5':
        demo_basic_usage()
        demo_analytics()
        demo_categories()
        print("\n💡 TIP: Run option 4 for interactive mode")
    elif choice.lower() == 'q':
        print("\nGoodbye! 👋\n")
    else:
        print("\nInvalid option!")
    
    print("\n" + "="*70)
    print("For the full chatbot with real FAQ data, run:")
    print("  python chatbot_cli.py --mode rule")
    print("\nOr for the web interface:")
    print("  python chatbot_web.py --mode rule --port 5000")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
