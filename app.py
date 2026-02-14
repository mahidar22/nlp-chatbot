import os
from flask import Flask, render_template, request, jsonify
from nlp_bot import NLPChatbot  # or rule_bot import RuleBasedChatbot

app = Flask(__name__)
bot = NLPChatbot("faqs.json")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = bot.get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)