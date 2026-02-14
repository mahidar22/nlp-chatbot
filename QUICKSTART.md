# 🚀 Quick Start Guide - FAQ Chatbot

## ⚡ Get Running in 5 Minutes

### Step 1: Check What You Have

```bash
# Check Python version (need 3.7+)
python3 --version

# You should see something like: Python 3.x.x
```

### Step 2: Choose Your Path

#### 🎯 Option A: Quick Demo (No Setup Required)

Test the chatbot immediately with sample data:

```bash
python3 demo.py
```

Then select option 1 for a basic demo, or option 4 for interactive mode.

#### 🎯 Option B: Full Setup (Recommended)

Get the complete chatbot with real FAQ data:

```bash
# 1. Run setup wizard
python3 setup.py

# 2. Start chatting
python3 chatbot_cli.py --mode rule
```

#### 🎯 Option C: Manual Setup

```bash
# 1. Install dependencies
pip install flask datasets

# 2. Download FAQ data
python3 data_loader.py

# 3. Run chatbot
python3 chatbot_cli.py --mode rule
```

## 📱 Interface Options

### Command Line Interface (CLI)

```bash
# Basic mode (fast, no ML required)
python3 chatbot_cli.py --mode rule

# After starting, just type your questions!
You: How do I reset my password?
Bot: To reset your password, click on...
```

**CLI Commands:**
- Type questions naturally
- `help` - Show commands
- `stats` - View statistics
- `history` - See conversation
- `exit` - Quit chatbot

### Web Interface

```bash
# Start web server
python3 chatbot_web.py --mode rule --port 5000

# Open browser to: http://localhost:5000
```

You'll get a beautiful web chat interface!

## 🎓 Understanding Modes

### Rule-Based Mode (Default)
- ✅ Fast and simple
- ✅ Works offline
- ✅ No ML libraries needed
- 👍 Best for: Getting started, exact matches

```bash
python3 chatbot_cli.py --mode rule
```

### NLP Mode (Advanced)
- ✅ Understands context
- ✅ Better with paraphrasing
- ⚠️ Requires ML libraries
- 👍 Best for: Production, complex queries

```bash
# First, install ML libraries
pip install sentence-transformers transformers torch

# Then run
python3 chatbot_cli.py --mode nlp
```

### Hybrid Mode (Best of Both)
- ✅ Combines both approaches
- ✅ Automatically picks best method
- ⚠️ Requires ML libraries
- 👍 Best for: Maximum accuracy

```bash
python3 chatbot_cli.py --mode hybrid
```

## 🔧 Common Adjustments

### Confidence Threshold

Control how strict the chatbot is:

```bash
# More strict (fewer answers, higher confidence)
python3 chatbot_cli.py --mode rule --threshold 0.6

# More lenient (more answers, may be less accurate)
python3 chatbot_cli.py --mode rule --threshold 0.3

# Default is 0.4
```

### Change Port (Web)

```bash
python3 chatbot_web.py --mode rule --port 8080
```

## 📝 Testing with Examples

Run example scripts to learn features:

```bash
python3 examples.py
```

Choose from:
1. Basic usage
2. NLP features
3. Analytics
4. Custom FAQs
5. And more!

## 🐛 Troubleshooting

### "Dataset not found"

```bash
# Download the dataset
python3 data_loader.py
```

### "NLP libraries not installed"

```bash
# Install them
pip install sentence-transformers transformers torch

# Or just use rule-based mode
python3 chatbot_cli.py --mode rule
```

### "Port already in use"

```bash
# Use different port
python3 chatbot_web.py --port 8080
```

### "Import error"

```bash
# Make sure you're in the right directory
cd /path/to/faq-chatbot

# Try with python instead of python3
python chatbot_cli.py --mode rule
```

## 💡 Pro Tips

1. **Start with demo**: Run `python3 demo.py` first to understand how it works

2. **Use rule-based mode first**: It's faster and requires no setup

3. **Check analytics**: Use `stats` command in CLI to see performance

4. **Add your own FAQs**: 
   ```python
   from data_loader import DataLoader
   loader = DataLoader()
   loader.load_from_cache()
   loader.add_faq("Your question?", "Your answer", "category")
   ```

5. **Monitor conversations**: Check `chat_logs.jsonl` to see what users ask

## 📊 What's Next?

After getting started:

1. **Customize FAQs**: Add your own questions and answers
2. **Try NLP mode**: Install ML libraries for better accuracy
3. **Deploy**: Use the web interface for production
4. **Monitor**: Check analytics to improve responses
5. **Extend**: Add new features using the modular code

## 🎯 Success Checklist

- [ ] Python 3.7+ installed
- [ ] Ran demo successfully
- [ ] Downloaded FAQ dataset
- [ ] Tested rule-based mode
- [ ] Understood CLI commands
- [ ] (Optional) Installed NLP libraries
- [ ] (Optional) Tried web interface

## 📚 File Reference

```
Main Files:
├── demo.py              ← Start here!
├── chatbot_cli.py       ← Command-line interface
├── chatbot_web.py       ← Web interface
├── data_loader.py       ← Dataset management
├── examples.py          ← Feature examples
└── README.md            ← Full documentation

Core Modules:
├── rule_based_engine.py ← Phase 1: Keyword matching
├── nlp_engine.py        ← Phase 2: Semantic AI
└── logger.py            ← Analytics & logging
```

## 🆘 Need Help?

1. Read `README.md` for detailed documentation
2. Run `python3 examples.py` to see usage examples
3. Check the troubleshooting section above
4. Review the code comments - they're detailed!

## 🎉 You're Ready!

Start with the demo, then move to the full chatbot. Happy chatting! 🤖💬

---

**Quick Commands Cheat Sheet:**

```bash
# Quick test
python3 demo.py

# Download data
python3 data_loader.py

# Start CLI
python3 chatbot_cli.py --mode rule

# Start web
python3 chatbot_web.py --mode rule --port 5000

# View examples
python3 examples.py
```
