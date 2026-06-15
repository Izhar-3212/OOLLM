import json
import random
from pathlib import Path
from datasets import Dataset

def generate_qa_pairs():
    qa_data = [
        {"instruction": "What is your return policy?", "input": "", "output": "We offer a 30-day return policy for all products. Items must be in original condition with tags attached."},
        {"instruction": "How do I track my order?", "input": "", "output": "You can track your order by logging into your account and clicking on 'My Orders', or by using the tracking number in your shipping email."},
        {"instruction": "What payment methods do you accept?", "input": "", "output": "We accept all major credit cards (Visa, MasterCard, Amex), PayPal, Apple Pay, and Google Pay."},
        {"instruction": "How long does shipping take?", "input": "", "output": "Standard shipping takes 5-7 business days. Express shipping is available for 2-3 business days."},
        {"instruction": "Can I change my order after placing it?", "input": "", "output": "Orders can be modified within 1 hour of placement. After that, please contact customer support immediately."},
        {"instruction": "Do you ship internationally?", "input": "", "output": "Yes, we ship to over 50 countries worldwide. International shipping typically takes 10-15 business days."},
        {"instruction": "How do I contact customer support?", "input": "", "output": "You can reach our support team via email at support@example.com or call us at 1-800-555-0199 between 9 AM and 5 PM EST."},
        {"instruction": "Is there a warranty on your products?", "input": "", "output": "Yes, all our electronics come with a standard 1-year manufacturer warranty."},
        {"instruction": "How do I reset my password?", "input": "", "output": "Click on 'Forgot Password' on the login page, enter your email, and follow the instructions sent to your inbox."},
        {"instruction": "Do you offer gift cards?", "input": "", "output": "Yes! You can purchase digital gift cards in denominations of $25, $50, and $100 on our website."}
    ]
    
    # Duplicate to make the dataset slightly larger for training
    expanded_data = []
    for item in qa_data:
        expanded_data.append(item)
        variation = item.copy()
        variation["instruction"] = f"Question: {item['instruction']}"
        expanded_data.append(variation)
    
    return expanded_data

def main():
    print("Generating synthetic Q&A data...")
    data = generate_qa_pairs()
    
    output_path = "./data/training/synthetic_qa.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(data)} examples to {output_path}")
    
    # Convert to Hugging Face dataset format
    dataset = Dataset.from_list(data)
    dataset.save_to_disk("./data/training/synthetic_qa_dataset")
    print("Dataset saved to disk successfully!")

if __name__ == "__main__":
    main()