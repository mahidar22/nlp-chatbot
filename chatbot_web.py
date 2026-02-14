"""
Flask Web Interface for FAQ Chatbot
Provides a web-based chat interface with REST API
"""

from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# Import chatbot modules
from data_loader import DataLoader
from rule_based_engine import RuleBasedChatbot
from logger import ChatLogger

# Try to import NLP engine
try:
    from nlp_engine import NLPChatbot, HybridChatbot
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variables
chatbot = None
logger = None
mode = 'rule'
loader = None


def initialize_chatbot(chatbot_mode='rule', threshold=0.4):
    """Initialize the chatbot with specified mode."""
    global chatbot, logger, mode, loader
    
    mode = chatbot_mode
    logger = ChatLogger()
    loader = DataLoader()
    
    # Load data
    if not loader.load_from_cache():
        if not loader.load_from_huggingface():
            raise RuntimeError("Could not load FAQ data")
    
    faqs = loader.get_all_faqs()
    
    # Initialize chatbot based on mode
    if mode == 'rule':
        chatbot = RuleBasedChatbot(faqs, threshold=threshold)
    elif mode == 'nlp' and NLP_AVAILABLE:
        chatbot = NLPChatbot(faqs, threshold=threshold)
    elif mode == 'hybrid' and NLP_AVAILABLE:
        rule_bot = RuleBasedChatbot(faqs, threshold=threshold)
        nlp_bot = NLPChatbot(faqs, threshold=threshold)
        chatbot = HybridChatbot(rule_bot, nlp_bot)
    else:
        # Fall back to rule-based
        chatbot = RuleBasedChatbot(faqs, threshold=threshold)
        mode = 'rule'


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html', mode=mode)


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests.
    
    Expected JSON:
        {
            "query": "user question"
        }
    
    Returns:
        {
            "response": "bot answer",
            "score": 0.95,
            "timestamp": "2024-01-01T12:00:00"
        }
    """
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400
    
    query = data['query'].strip()
    
    if not query:
        return jsonify({'error': 'Empty query'}), 400
    
    # Get response from chatbot
    response = chatbot.get_response(query)
    
    # Get score from history
    history = chatbot.get_conversation_history()
    score = history[-1].get('score', 0) if history else 0
    
    # Log interaction
    logger.log_interaction(
        query=query,
        response=response,
        score=score,
        method=mode
    )
    
    return jsonify({
        'response': response,
        'score': score,
        'timestamp': datetime.now().isoformat(),
        'mode': mode
    })


@app.route('/api/stats')
def stats():
    """Get chatbot statistics."""
    stats = loader.get_stats()
    return jsonify(stats)


@app.route('/api/analytics')
def analytics():
    """Get analytics data."""
    analytics = logger.get_analytics()
    return jsonify(analytics)


@app.route('/api/history')
def history():
    """Get conversation history."""
    history = chatbot.get_conversation_history()
    return jsonify({'history': history})


@app.route('/api/categories')
def categories():
    """Get available categories."""
    cats = loader.get_categories()
    category_data = []
    
    for cat in cats:
        faqs = loader.get_faqs_by_category(cat)
        category_data.append({
            'name': cat,
            'count': len(faqs)
        })
    
    return jsonify({'categories': category_data})


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    chatbot.clear_history()
    return jsonify({'success': True, 'message': 'History cleared'})


# HTML Template (saved separately)
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAQ Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 20px 20px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .mode-badge {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .chat-area {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f7f7f7;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .input-area {
            padding: 20px;
            background: white;
            border-radius: 0 0 20px 20px;
            border-top: 1px solid #e0e0e0;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        #user-input {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #user-input:focus {
            border-color: #667eea;
        }
        
        #send-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        #send-btn:hover {
            transform: scale(1.05);
        }
        
        #send-btn:active {
            transform: scale(0.95);
        }
        
        .score {
            font-size: 11px;
            color: #999;
            margin-top: 5px;
        }
        
        .loading {
            display: none;
            padding: 12px 18px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .loading.active {
            display: block;
        }
        
        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 FAQ Chatbot</h1>
            <div class="mode-badge">{{ mode }} mode</div>
        </div>
        
        <div class="chat-area" id="chat-area">
            <div class="message bot">
                <div class="message-content">
                    👋 Hi! I'm your FAQ assistant. Ask me anything about our services!
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="input-container">
                <input 
                    type="text" 
                    id="user-input" 
                    placeholder="Type your question here..." 
                    autocomplete="off"
                >
                <button id="send-btn">Send</button>
            </div>
        </div>
    </div>
    
    <script>
        const chatArea = document.getElementById('chat-area');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        
        function addMessage(content, isUser, score = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            if (score !== null && !isUser) {
                const scoreDiv = document.createElement('div');
                scoreDiv.className = 'score';
                scoreDiv.textContent = `Confidence: ${(score * 100).toFixed(0)}%`;
                contentDiv.appendChild(scoreDiv);
            }
            
            messageDiv.appendChild(contentDiv);
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function showLoading() {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot';
            loadingDiv.id = 'loading-message';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'loading active';
            contentDiv.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
            
            loadingDiv.appendChild(contentDiv);
            chatArea.appendChild(loadingDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function removeLoading() {
            const loadingMsg = document.getElementById('loading-message');
            if (loadingMsg) {
                loadingMsg.remove();
            }
        }
        
        async function sendMessage() {
            const query = userInput.value.trim();
            
            if (!query) return;
            
            // Add user message
            addMessage(query, true);
            userInput.value = '';
            
            // Show loading
            showLoading();
            
            // Send to API
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                
                removeLoading();
                
                if (data.error) {
                    addMessage(`Error: ${data.error}`, false);
                } else {
                    addMessage(data.response, false, data.score);
                }
            } catch (error) {
                removeLoading();
                addMessage('Sorry, something went wrong. Please try again.', false);
                console.error('Error:', error);
            }
        }
        
        sendBtn.addEventListener('click', sendMessage);
        
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus input on load
        userInput.focus();
    </script>
</body>
</html>'''


def create_template_file():
    """Create the HTML template file."""
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    template_path = os.path.join(templates_dir, 'index.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)
    
    print(f"✓ Created template: {template_path}")


def main():
    """Main entry point for Flask app."""
    import argparse
    
    parser = argparse.ArgumentParser(description='FAQ Chatbot - Web Interface')
    parser.add_argument('--mode', type=str, default='rule',
                       choices=['rule', 'nlp', 'hybrid'],
                       help='Chatbot mode')
    parser.add_argument('--threshold', type=float, default=0.4,
                       help='Confidence threshold')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the server on')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                       help='Host to run the server on')
    
    args = parser.parse_args()
    
    # Create template file
    create_template_file()
    
    # Initialize chatbot
    print("\nInitializing chatbot...")
    initialize_chatbot(chatbot_mode=args.mode, threshold=args.threshold)
    print("✓ Chatbot ready!")
    
    # Run Flask app
    print(f"\nStarting web server on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
