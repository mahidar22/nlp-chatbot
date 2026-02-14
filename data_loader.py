"""
Data Loader Module
Handles loading and preprocessing the FAQ dataset from Hugging Face
"""

import json
import os
from typing import List, Dict, Any


class DataLoader:
    """
    Loads and manages the FAQ dataset from Hugging Face.
    Provides methods to access and search the FAQ data.
    """
    
    def __init__(self, cache_file: str = "faq_data.json"):
        """
        Initialize the DataLoader.
        
        Args:
            cache_file: Path to cache the dataset locally
        """
        self.cache_file = cache_file
        self.faqs: List[Dict[str, str]] = []
        
    def load_from_huggingface(self) -> bool:
        """
        Load the dataset from Hugging Face and cache it locally.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from datasets import load_dataset
            
            print("Loading dataset from Hugging Face...")
            ds = load_dataset("MakTek/Customer_support_faqs_dataset")
            
            # Extract FAQs from the dataset
            self.faqs = []
            for item in ds['train']:
                faq_entry = {
                    'question': item.get('question', ''),
                    'answer': item.get('answer', ''),
                    'category': item.get('category', 'general')
                }
                self.faqs.append(faq_entry)
            
            # Cache the data locally
            self.save_to_cache()
            print(f"✓ Loaded {len(self.faqs)} FAQs successfully!")
            return True
            
        except ImportError:
            print("ERROR: 'datasets' library not found. Please install it:")
            print("pip install datasets")
            return False
        except Exception as e:
            print(f"ERROR loading dataset: {e}")
            return False
    
    def load_from_cache(self) -> bool:
        """
        Load the dataset from local cache file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.cache_file):
            print(f"Cache file '{self.cache_file}' not found.")
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.faqs = json.load(f)
            print(f"✓ Loaded {len(self.faqs)} FAQs from cache!")
            return True
        except Exception as e:
            print(f"ERROR loading cache: {e}")
            return False
    
    def save_to_cache(self) -> bool:
        """
        Save the current dataset to cache file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.faqs, f, indent=2, ensure_ascii=False)
            print(f"✓ Dataset cached to '{self.cache_file}'")
            return True
        except Exception as e:
            print(f"ERROR saving cache: {e}")
            return False
    
    def load_from_custom_file(self, file_path: str) -> bool:
        """
        Load FAQs from a custom JSON/CSV file.
        
        Args:
            file_path: Path to the custom file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            return False
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.faqs = json.load(f)
                    
            elif file_path.endswith('.csv'):
                import csv
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.faqs = []
                    for row in reader:
                        self.faqs.append({
                            'question': row.get('question', ''),
                            'answer': row.get('answer', ''),
                            'category': row.get('category', 'general')
                        })
            else:
                print("Unsupported file format. Use .json or .csv")
                return False
            
            print(f"✓ Loaded {len(self.faqs)} FAQs from '{file_path}'")
            return True
            
        except Exception as e:
            print(f"ERROR loading file: {e}")
            return False
    
    def get_all_faqs(self) -> List[Dict[str, str]]:
        """Get all FAQ entries."""
        return self.faqs
    
    def get_categories(self) -> List[str]:
        """Get unique categories from the dataset."""
        categories = set(faq.get('category', 'general') for faq in self.faqs)
        return sorted(list(categories))
    
    def get_faqs_by_category(self, category: str) -> List[Dict[str, str]]:
        """Get all FAQs for a specific category."""
        return [faq for faq in self.faqs if faq.get('category', '').lower() == category.lower()]
    
    def add_faq(self, question: str, answer: str, category: str = 'general') -> None:
        """
        Add a new FAQ entry.
        
        Args:
            question: The question text
            answer: The answer text
            category: Category for the FAQ
        """
        self.faqs.append({
            'question': question,
            'answer': answer,
            'category': category
        })
        self.save_to_cache()
        print(f"✓ Added new FAQ to category '{category}'")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the dataset."""
        categories = self.get_categories()
        stats = {
            'total_faqs': len(self.faqs),
            'categories': categories,
            'category_counts': {cat: len(self.get_faqs_by_category(cat)) for cat in categories}
        }
        return stats


# Helper function to download dataset (run this first if you don't have cached data)
def download_dataset():
    """Download the dataset from Hugging Face and cache it."""
    loader = DataLoader()
    if loader.load_from_huggingface():
        print("\n" + "="*50)
        print("Dataset downloaded and cached successfully!")
        print("="*50)
        stats = loader.get_stats()
        print(f"\nTotal FAQs: {stats['total_faqs']}")
        print(f"Categories: {', '.join(stats['categories'])}")
        print("\nYou can now run the chatbot!")
    else:
        print("\nFailed to download dataset.")
        print("Please ensure you have internet connection and 'datasets' library installed.")


if __name__ == "__main__":
    # Run this to download the dataset
    download_dataset()
