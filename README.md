# FAQ Chatbot System

A complete, production-ready chatbot application for handling frequently asked questions with both rule-based and AI-powered NLP modes.

## 🌟 Features

### Phase 1: Rule-Based Chatbot
- ✅ Keyword matching and string similarity
- ✅ Fuzzy matching for typos
- ✅ Fast response with keyword indexing
- ✅ No ML dependencies required

### Phase 2: NLP Integration
- ✅ Semantic similarity using transformer models
- ✅ Context-aware responses
- ✅ Better handling of paraphrased questions
- ✅ Sentence embeddings for accurate matching

### Additional Features
- ✅ Modular, extensible architecture
- ✅ Both CLI and Web interfaces
- ✅ Conversation logging and analytics
- ✅ Easy to add new FAQs
- ✅ Multiple chatbot modes (rule-based, NLP, hybrid)
- ✅ Real-time confidence scoring
- ✅ Category-based FAQ organization

## 📁 Project Structure

```
faq-chatbot/
├── data_loader.py          # Dataset loading and management
├── rule_based_engine.py    # Phase 1: Rule-based chatbot
├── nlp_engine.py           # Phase 2: NLP-powered chatbot
├── logger.py               # Conversation logging and analytics
├── chatbot_cli.py          # Command-line interface
├── chatbot_web.py          # Flask web interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── faq_data.json          # Cached FAQ dataset (auto-generated)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd faq-chatbot

# Install basic dependencies (for rule-based mode)
pip install flask

# Install NLP dependencies (optional, for semantic mode)
pip install sentence-transformers transformers torch datasets
```

### 2. Download the Dataset

First, download and cache the FAQ dataset:

```bash
python data_loader.py
```

This will:
- Download the dataset from Hugging Face
- Cache it locally as `faq_data.json`
- Display statistics about the FAQs

### 3. Run the Chatbot

#### Option A: Command-Line Interface (CLI)

```bash
# Rule-based mode (fast, no ML required)
python chatbot_cli.py --mode rule

# NLP mode (smarter, requires ML libraries)
python chatbot_cli.py --mode nlp

# Hybrid mode (combines both approaches)
python chatbot_cli.py --mode hybrid

# Custom threshold
python chatbot_cli.py --mode rule --threshold 0.5
```

#### Option B: Web Interface

```bash
# Start web server (rule-based mode)
python chatbot_web.py --mode rule --port 5000

# NLP mode
python chatbot_web.py --mode nlp --port 5000

# Then open http://localhost:5000 in your browser
```

## 📖 Usage Guide

### CLI Commands

When running the CLI chatbot, you can use these commands:

```
help       - Show available commands
stats      - Display chatbot statistics
history    - Show conversation history
clear      - Clear conversation history
analytics  - Show detailed analytics
categories - List FAQ categories
exit/quit  - Exit the chatbot
```

### Example Conversation

```
You: How do I reset my password?
Bot: To reset your password, click on 'Forgot Password' on the login page...

You: business hours
Bot: We are open Monday to Friday, 9 AM to 6 PM EST.

You: stats
[Shows statistics about FAQs and categories]
```

### Web Interface

The web interface provides:
- Clean, modern chat UI
- Real-time responses
- Confidence scoring
- Mobile-friendly design
- Easy integration with existing systems

## 🔧 Customization

### Adding New FAQs

You can add FAQs programmatically:

```python
from data_loader import DataLoader

loader = DataLoader()
loader.load_from_cache()

# Add a new FAQ
loader.add_faq(
    question="What is your refund policy?",
    answer="We offer a 30-day money-back guarantee...",
    category="billing"
)
```

### Using Custom Dataset

Load FAQs from your own JSON or CSV file:

```python
from data_loader import DataLoader

loader = DataLoader()
loader.load_from_custom_file("my_faqs.json")
```

Expected JSON format:
```json
[
    {
        "question": "Your question here?",
        "answer": "Your answer here.",
        "category": "general"
    }
]
```

### Adjusting Confidence Threshold

The threshold determines how confident the bot must be before giving an answer:

```bash
# More strict (fewer wrong answers, more "I don't know")
python chatbot_cli.py --mode rule --threshold 0.6

# More lenient (more answers, might be less accurate)
python chatbot_cli.py --mode rule --threshold 0.3
```

## 📊 Analytics

View analytics to improve your chatbot:

```python
from logger import ChatLogger

logger = ChatLogger()
logger.print_analytics()
```

This shows:
- Total interactions
- Average confidence scores
- Low-confidence queries (need improvement)
- Most common questions
- Method performance (rule vs NLP)

Export analytics:
```python
logger.export_analytics_report("analytics.json")
logger.export_unanswered_queries("need_improvement.json")
```

## 🎯 Modes Comparison

### Rule-Based Mode
**Pros:**
- Fast response time
- No ML dependencies
- Works offline
- Low resource usage

**Cons:**
- Less flexible with paraphrasing
- Keyword dependent
- May miss semantic meaning

**Best for:** Simple FAQs, exact matches, resource-constrained environments

### NLP Mode
**Pros:**
- Understands context and semantics
- Handles paraphrasing well
- Better with varied questions
- More accurate overall

**Cons:**
- Requires ML libraries
- Slower first-time setup
- Higher resource usage

**Best for:** Complex queries, varied phrasing, high accuracy requirements

### Hybrid Mode
**Pros:**
- Best of both worlds
- Automatically picks best method
- Balanced performance

**Cons:**
- Requires NLP libraries
- Slightly more complex

**Best for:** Production deployments, maximum accuracy

## 🔌 API Integration

The web interface provides REST API endpoints:

```bash
# Send a query
POST /api/chat
{
    "query": "How do I reset my password?"
}

# Response
{
    "response": "To reset your password...",
    "score": 0.95,
    "timestamp": "2024-01-01T12:00:00",
    "mode": "nlp"
}

# Get statistics
GET /api/stats

# Get analytics
GET /api/analytics

# Get conversation history
GET /api/history

# Clear history
POST /api/clear-history
```

## 🛠️ Development

### Running Tests

Test the rule-based engine:
```bash
python rule_based_engine.py
```

Test the logger:
```bash
python logger.py
```

### Extending the Chatbot

1. **Add new features** to `rule_based_engine.py` or `nlp_engine.py`
2. **Modify UI** in `chatbot_web.py` (HTML template included)
3. **Add new API endpoints** in `chatbot_web.py`
4. **Customize logging** in `logger.py`

## 📦 Dependencies

### Core (Required)
- Python 3.7+
- Flask (for web interface)

### NLP Features (Optional)
- sentence-transformers
- transformers
- torch
- datasets

### Data Processing
- Built-in Python libraries (json, pickle, difflib)

## 🐛 Troubleshooting

### Dataset Not Loading
```bash
# Ensure you have internet connection
# Install datasets library
pip install datasets

# Manually download
python data_loader.py
```

### NLP Mode Not Working
```bash
# Install required libraries
pip install sentence-transformers transformers torch

# First run will download models (may take time)
```

### Port Already in Use
```bash
# Use a different port
python chatbot_web.py --port 8080
```

## 📈 Performance Tips

1. **Cache embeddings**: First NLP run generates embeddings (slow), subsequent runs are fast
2. **Use rule-based for simple FAQs**: Faster and sufficient for exact matches
3. **Hybrid mode for production**: Best accuracy with reasonable performance
4. **Monitor analytics**: Identify low-confidence queries to improve FAQs

## 🔒 Security Notes

- Change the Flask `SECRET_KEY` in production
- Implement rate limiting for public deployments
- Sanitize user inputs
- Use HTTPS in production
- Consider authentication for sensitive FAQs

## 📝 License

This project is open-source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new features
- Improve algorithms
- Fix bugs
- Enhance documentation

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the analytics for insights
3. Ensure dependencies are installed
4. Check the conversation logs

## 🎓 Learning Resources

- **Rule-based NLP**: keyword matching, string similarity
- **Semantic search**: sentence embeddings, cosine similarity
- **Web development**: Flask, REST APIs, async programming
- **Data management**: JSON, caching, file I/O

---

**Happy Chatting! 🤖💬**
