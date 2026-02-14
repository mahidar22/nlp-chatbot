import json

class RuleBasedChatbot:
    def __init__(self, data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

    def get_response(self, user_input):
        user_input = user_input.lower()

        for faq in self.faqs:
            if faq["question"].lower() in user_input:
                return faq["answer"]

        return "Sorry, I don't understand that."
        

if __name__ == "__main__":
    bot = RuleBasedChatbot("faqs.json")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        print("Bot:", bot.get_response(user_input))
