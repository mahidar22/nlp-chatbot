import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class NLPChatbot:
    def __init__(self, data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.questions = [faq["question"] for faq in self.faqs]
        self.answers = [faq["answer"] for faq in self.faqs]

        self.embeddings = self.model.encode(self.questions)

    def get_response(self, user_input):
        user_embedding = self.model.encode([user_input])
        similarities = cosine_similarity(user_embedding, self.embeddings)

        best_index = np.argmax(similarities)
        best_score = similarities[0][best_index]

        if best_score > 0.5:
            return self.answers[best_index]
        else:
            return "Sorry, I couldn't find a relevant answer."


if __name__ == "__main__":
    bot = NLPChatbot("faqs.json")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        print("Bot:", bot.get_response(user_input))
