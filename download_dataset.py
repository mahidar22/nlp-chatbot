from datasets import load_dataset
import json

# Change dataset name if needed
dataset = load_dataset("MakTek/Customer_support_faqs_dataset")

# Convert to simple FAQ format
faqs = []

for item in dataset["train"]:
    faqs.append({
        "question": item["question"],
        "answer": item["answer"]
    })

# Save locally
with open("faqs.json", "w", encoding="utf-8") as f:
    json.dump(faqs, f, indent=4)

print("Dataset saved as faqs.json")
