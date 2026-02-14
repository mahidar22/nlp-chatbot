#!/usr/bin/env python3
"""
Quick Setup Script
Downloads the FAQ dataset and prepares the chatbot for use
"""

import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True


def install_basic_dependencies():
    """Install basic dependencies."""
    print("\n" + "="*60)
    print("Installing basic dependencies...")
    print("="*60)
    
    basic_packages = ['flask']
    
    for package in basic_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--break-system-packages", "-q"
            ])
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠ Could not install {package}")
            print(f"  You may need to install manually: pip install {package}")


def install_nlp_dependencies():
    """Install NLP dependencies (optional)."""
    print("\n" + "="*60)
    print("NLP Dependencies (Optional)")
    print("="*60)
    print("For semantic matching, you need: sentence-transformers, transformers, torch")
    
    choice = input("\nInstall NLP dependencies? This may take a while (y/N): ").lower()
    
    if choice != 'y':
        print("Skipping NLP dependencies. You can install them later.")
        print("Command: pip install sentence-transformers transformers torch")
        return
    
    nlp_packages = ['datasets', 'sentence-transformers', 'transformers', 'torch']
    
    for package in nlp_packages:
        try:
            print(f"Installing {package}... (this may take a few minutes)")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--break-system-packages"
            ])
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠ Could not install {package}")
            print(f"  You may need to install manually: pip install {package}")


def download_dataset():
    """Download the FAQ dataset."""
    print("\n" + "="*60)
    print("Downloading FAQ Dataset...")
    print("="*60)
    
    # Check if cache already exists
    if os.path.exists("faq_data.json"):
        print("✓ Dataset cache found (faq_data.json)")
        choice = input("Re-download dataset? (y/N): ").lower()
        if choice != 'y':
            print("Using existing cache.")
            return True
    
    try:
        from data_loader import download_dataset
        download_dataset()
        return True
    except ImportError as e:
        print(f"ERROR: Could not import data_loader: {e}")
        print("\nPlease install the datasets library:")
        print("  pip install datasets")
        return False
    except Exception as e:
        print(f"ERROR downloading dataset: {e}")
        return False


def test_chatbot():
    """Test the chatbot with a simple query."""
    print("\n" + "="*60)
    print("Testing Chatbot...")
    print("="*60)
    
    try:
        from data_loader import DataLoader
        from rule_based_engine import RuleBasedChatbot
        
        loader = DataLoader()
        if not loader.load_from_cache():
            print("ERROR: Could not load dataset from cache")
            return False
        
        faqs = loader.get_all_faqs()
        chatbot = RuleBasedChatbot(faqs)
        
        test_query = "How do I contact support?"
        print(f"\nTest Query: {test_query}")
        response = chatbot.get_response(test_query, return_confidence=True)
        print(f"Response: {response}")
        
        print("\n✓ Chatbot is working!")
        return True
        
    except Exception as e:
        print(f"ERROR testing chatbot: {e}")
        return False


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nYou can now run the chatbot in different modes:\n")
    
    print("1. Command-Line Interface:")
    print("   python chatbot_cli.py --mode rule")
    print("   python chatbot_cli.py --mode nlp     # Requires NLP libraries")
    print("   python chatbot_cli.py --mode hybrid  # Requires NLP libraries")
    
    print("\n2. Web Interface:")
    print("   python chatbot_web.py --mode rule --port 5000")
    print("   Then open http://localhost:5000 in your browser")
    
    print("\n3. Custom threshold:")
    print("   python chatbot_cli.py --mode rule --threshold 0.5")
    
    print("\n" + "="*60)
    print("For more information, see README.md")
    print("="*60 + "\n")


def main():
    """Main setup process."""
    print("\n" + "="*60)
    print("FAQ CHATBOT - SETUP WIZARD")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install basic dependencies
    install_basic_dependencies()
    
    # Ask about NLP dependencies
    install_nlp_dependencies()
    
    # Download dataset
    if not download_dataset():
        print("\n⚠ Dataset download failed.")
        print("You may need to run: python data_loader.py")
        return
    
    # Test the chatbot
    if test_chatbot():
        print_next_steps()
    else:
        print("\n⚠ Chatbot test failed. Please check the error messages above.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check the error and try again.")
