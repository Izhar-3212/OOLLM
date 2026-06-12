"""
Retrain Mini Me using accumulated feedback data
Run this periodically (e.g., after collecting 50+ feedback entries)
"""
import json
from pathlib import Path
from feedback_manager import FeedbackManager
from datasets import Dataset

def main():
    print("="*60)
    print("Retraining Mini Me with Feedback Data")
    print("="*60)
    
    feedback_mgr = FeedbackManager()
    
    # Get training data from feedback
    training_data = feedback_mgr.get_training_data()
    
    if len(training_data) < 10:
        print(f"\n⚠️  Not enough feedback yet! You have {len(training_data)} good examples.")
        print("Please collect at least 10 good/corrected examples before retraining.")
        return
    
    print(f"\n✓ Found {len(training_data)} training examples from feedback")
    
    # Save to training directory
    output_path = "./data/training/feedback_qa.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    # Convert to Hugging Face dataset
    dataset = Dataset.from_list(training_data)
    dataset.save_to_disk("./data/training/feedback_qa_dataset")
    
    print(f"✓ Training data saved to {output_path}")
    print(f"✓ Dataset saved to ./data/training/feedback_qa_dataset")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Run: python scripts/03_train_lora.py")
    print("   (Make sure config.yaml points to feedback_qa_dataset)")
    print("2. Run: python scripts/04_merge_model.py")
    print("3. Restart Mini Me!")
    print("="*60)

if __name__ == "__main__":
    main()