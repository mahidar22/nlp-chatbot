# 🤖 FAQ CHATBOT - COMPLETE INSTRUCTIONS

## 📦 What You Have

A complete, professional FAQ chatbot system with:

✅ **Phase 1**: Rule-based engine (keyword matching, string similarity)
✅ **Phase 2**: NLP engine (semantic understanding with AI)
✅ **Modular code**: Separate files for data, logic, UI, logging
✅ **Two interfaces**: Command-line (CLI) and Web (Flask)
✅ **Analytics**: Conversation logging and performance tracking
✅ **Sample data**: Ready-to-use FAQ dataset
✅ **Documentation**: Complete guides and examples

## 🚀 THREE WAYS TO GET STARTED

### Option 1: INSTANT DEMO (30 seconds)

Test immediately with sample data - no setup needed!

```bash
python3 demo.py
```

Select option 1 for automated demo, or option 4 for interactive chat.

### Option 2: AUTOMATED SETUP (5 minutes)

Let the setup wizard guide you:

```bash
python3 setup.py
```

This will:
- Check your Python version
- Install dependencies
- Download the FAQ dataset
- Test the chatbot
- Show you next steps

### Option 3: MANUAL SETUP (for developers)

Full control over the installation:

```bash
# 1. Install basic dependencies
pip install flask

# 2. Download the dataset (requires 'datasets' library)
pip install datasets
python3 data_loader.py

# 3. Run the chatbot
python3 chatbot_cli.py --mode rule
```

## 📱 CHOOSING YOUR INTERFACE

### Command-Line Interface (CLI)

**Best for**: Quick testing, server deployment, automation

```bash
# Start the CLI chatbot
python3 chatbot_cli.py --mode rule

# Then just type questions:
You: How do I reset my password?
Bot: To reset your password, click on...

# Available commands:
# help     - Show help
# stats    - View statistics
# history  - See conversation
# exit     - Quit
```

### Web Interface

**Best for**: End users, production deployment, better UX

```bash
# Start the web server
python3 chatbot_web.py --mode rule --port 5000

# Open browser to:
http://localhost:5000
```

You'll see a beautiful, modern chat interface!

## 🎯 UNDERSTANDING MODES

### Rule-Based Mode (Recommended to Start)

**How it works**: Matches keywords and calculates string similarity

**Pros**:
- Fast (< 1ms response time)
- No ML libraries needed
- Works offline
- Low resource usage

**Cons**:
- Less flexible with paraphrasing
- Keyword-dependent

**Use when**: Getting started, exact matches, limited resources

```bash
python3 chatbot_cli.py --mode rule
```

### NLP Mode (Advanced)

**How it works**: Uses AI embeddings to understand semantic meaning

**Pros**:
- Understands context
- Handles paraphrasing well
- More accurate overall

**Cons**:
- Requires ML libraries
- Slower first-time setup
- Higher resource usage

**Use when**: Production, complex queries, best accuracy

**Setup**:
```bash
# Install ML libraries (one time)
pip install sentence-transformers transformers torch

# Run chatbot
python3 chatbot_cli.py --mode nlp
```

### Hybrid Mode (Best of Both)

**How it works**: Combines rule-based and NLP, picks best result

**Pros**:
- Maximum accuracy
- Automatic method selection

**Cons**:
- Requires ML libraries

**Use when**: Production deployment, maximum quality

```bash
python3 chatbot_cli.py --mode hybrid
```

## 📊 WORKING WITH DATA

### Using the Provided Dataset

The chatbot uses the MakTek Customer Support FAQs dataset from Hugging Face.

```bash
# Download it once:
python3 data_loader.py

# It will be cached as: faq_data.json
```

### Using Sample Data (Testing)

A sample dataset is included for immediate testing:

```bash
# Already included in: sample_faqs.json
# Used automatically by demo.py
```

### Adding Your Own FAQs

**Method 1: Programmatically**

```python
from data_loader import DataLoader

loader = DataLoader()
loader.load_from_cache()

# Add new FAQ
loader.add_faq(
    question="What is your refund policy?",
    answer="We offer 30-day money-back guarantee...",
    category="billing"
)
```

**Method 2: Custom JSON File**

Create `my_faqs.json`:
```json
[
  {
    "question": "Your question here?",
    "answer": "Your answer here.",
    "category": "general"
  }
]
```

Then load it:
```python
from data_loader import DataLoader
loader = DataLoader()
loader.load_from_custom_file("my_faqs.json")
```

## 🔧 CUSTOMIZATION

### Adjusting Confidence Threshold

Control how strict the chatbot is:

```bash
# Strict (fewer answers, higher quality)
python3 chatbot_cli.py --mode rule --threshold 0.6

# Lenient (more answers, may be less accurate)
python3 chatbot_cli.py --mode rule --threshold 0.3

# Default
python3 chatbot_cli.py --mode rule --threshold 0.4
```

### Changing Web Port

```bash
python3 chatbot_web.py --port 8080
```

### Using Different NLP Models

```python
from nlp_engine import NLPChatbot

# Use different model
chatbot = NLPChatbot(
    faqs, 
    model_name="paraphrase-MiniLM-L6-v2"
)
```

## 📈 ANALYTICS & MONITORING

### View Statistics

In CLI mode:
```
You: stats
[Shows FAQ counts, categories, etc.]
```

### Export Analytics

```python
from logger import ChatLogger

logger = ChatLogger()
logger.print_analytics()                    # Print to console
logger.export_analytics_report("report.json")  # Export to file
```

### Identify Problem Queries

```python
# Find low-confidence interactions
logger.export_unanswered_queries("low_confidence.json")
```

## 🎓 LEARNING FROM EXAMPLES

Run the examples script to see various features:

```bash
python3 examples.py
```

Available examples:
1. Basic rule-based usage
2. NLP-powered chatbot
3. Hybrid approach
4. Analytics and logging
5. Adding custom FAQs
6. Category-based search
7. Custom data sources
8. Batch processing

## 🏗️ PROJECT STRUCTURE

```
Your chatbot files:
├── Core Engines
│   ├── rule_based_engine.py    # Phase 1: Keyword matching
│   ├── nlp_engine.py           # Phase 2: AI semantic matching
│   ├── data_loader.py          # Dataset management
│   └── logger.py               # Analytics and logging
│
├── Interfaces
│   ├── chatbot_cli.py          # Command-line interface
│   ├── chatbot_web.py          # Web interface (Flask)
│   └── demo.py                 # Quick demonstration
│
├── Utilities
│   ├── setup.py                # Setup wizard
│   ├── examples.py             # Usage examples
│   └── requirements.txt        # Dependencies
│
├── Data
│   ├── sample_faqs.json        # Sample data (20 FAQs)
│   └── faq_data.json           # Full dataset (auto-generated)
│
└── Documentation
    ├── README.md               # Complete documentation
    ├── QUICKSTART.md           # 5-minute guide
    ├── PROJECT_OVERVIEW.md     # Technical overview
    └── INSTRUCTIONS.md         # This file
```

## 🐛 TROUBLESHOOTING

### Problem: "Dataset not found"

**Solution**:
```bash
python3 data_loader.py
```

### Problem: "NLP libraries not installed"

**Solution**: Either install them or use rule-based mode
```bash
# Option 1: Install libraries
pip install sentence-transformers transformers torch

# Option 2: Use rule-based mode
python3 chatbot_cli.py --mode rule
```

### Problem: "Port 5000 already in use"

**Solution**: Use a different port
```bash
python3 chatbot_web.py --port 8080
```

### Problem: "ModuleNotFoundError"

**Solution**: Make sure you're in the right directory
```bash
cd /path/to/chatbot-files
python3 chatbot_cli.py --mode rule
```

### Problem: "Slow first-time NLP startup"

**Expected**: First run downloads the AI model (~100MB)
- Takes 5-10 seconds first time
- Subsequent runs are fast (~200ms per query)

## 💡 TIPS & BEST PRACTICES

1. **Start Simple**: Begin with demo.py, then try rule-based mode

2. **Check Logs**: Review `chat_logs.jsonl` to see actual usage

3. **Monitor Analytics**: Use stats command to track performance

4. **Tune Threshold**: Adjust based on your accuracy needs
   - Higher (0.6+): Fewer false positives
   - Lower (0.3-): More coverage

5. **Use Categories**: Organize FAQs by topic for better management

6. **Test Both Modes**: Compare rule-based vs NLP for your use case

7. **Add Gradually**: Start with core FAQs, expand over time

8. **Review Low-Confidence**: Identify gaps in your FAQ coverage

## 🚀 DEPLOYMENT TO PRODUCTION

### Local Development
```bash
python3 chatbot_web.py --mode rule --port 5000
```

### Production Server (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 chatbot_web:app
```

### With Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
python3 chatbot_web.py
```

## 📚 API INTEGRATION

The web interface provides REST API endpoints:

```bash
# Send a chat query
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I reset my password?"}'

# Response:
{
  "response": "To reset your password...",
  "score": 0.95,
  "timestamp": "2024-01-01T12:00:00",
  "mode": "rule"
}

# Get statistics
curl http://localhost:5000/api/stats

# Get analytics
curl http://localhost:5000/api/analytics
```

## 🎯 QUICK REFERENCE

### Installation Commands
```bash
pip install flask                          # Basic
pip install datasets                       # Dataset download
pip install sentence-transformers          # NLP mode
```

### Running Commands
```bash
python3 demo.py                           # Quick demo
python3 data_loader.py                    # Download data
python3 chatbot_cli.py --mode rule        # CLI chatbot
python3 chatbot_web.py --mode rule        # Web chatbot
python3 examples.py                       # See examples
```

### CLI Commands (during chat)
```
help       - Show commands
stats      - View statistics
history    - See conversation
clear      - Clear history
analytics  - Show analytics
exit       - Quit chatbot
```

## 📞 NEXT STEPS

1. ✅ **Run the demo**: `python3 demo.py`
2. ✅ **Download dataset**: `python3 data_loader.py`
3. ✅ **Try CLI**: `python3 chatbot_cli.py --mode rule`
4. ✅ **Try Web**: `python3 chatbot_web.py --mode rule --port 5000`
5. ✅ **Explore examples**: `python3 examples.py`
6. ✅ **Read docs**: Check README.md for details
7. ✅ **Customize**: Add your own FAQs
8. ✅ **Deploy**: Use in production

## 🎉 YOU'RE READY!

You now have a complete, professional FAQ chatbot. Start with the demo, experiment with the examples, and customize it for your needs!

**Happy Chatting! 🤖💬**

---

## 📖 ADDITIONAL RESOURCES

- `README.md` - Complete technical documentation
- `QUICKSTART.md` - 5-minute getting started guide
- `PROJECT_OVERVIEW.md` - Architecture and technical details
- `examples.py` - Runnable code examples
- Code comments - Every file has detailed explanations

## 🆘 GETTING HELP

1. Start with QUICKSTART.md
2. Check the troubleshooting section above
3. Run examples.py to see working code
4. Review the code comments
5. Check chat_logs.jsonl for debugging

---

**Version**: 1.0
**Last Updated**: 2024
**Status**: Production Ready ✅
