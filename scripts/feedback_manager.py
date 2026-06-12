import json
from pathlib import Path
from datetime import datetime

class FeedbackManager:
    def __init__(self, feedback_file="./data/feedback/feedback.json"):
        self.feedback_file = Path(feedback_file)
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.feedback_file.exists():
            self.feedback_file.write_text("[]")
    
    def load_feedback(self):
        """Load all feedback entries"""
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def add_feedback(self, question, answer, feedback, corrected_answer=None):
        """Add a new feedback entry"""
        feedback_data = self.load_feedback()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "feedback": feedback,  # "good", "bad", or "corrected"
            "corrected_answer": corrected_answer
        }
        
        feedback_data.append(entry)
        
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Feedback saved! Total entries: {len(feedback_data)}")
    
    def get_good_examples(self, limit=5):
        """Get recent good examples for in-context learning"""
        feedback_data = self.load_feedback()
        
        # Get examples marked as "good" or "corrected"
        good_examples = [
            entry for entry in feedback_data 
            if entry["feedback"] in ["good", "corrected"]
        ]
        
        # Sort by timestamp (most recent first) and limit
        good_examples.sort(key=lambda x: x["timestamp"], reverse=True)
        return good_examples[:limit]
    
    def get_training_data(self):
        """Convert feedback to training format for retraining"""
        feedback_data = self.load_feedback()
        training_data = []
        
        for entry in feedback_data:
            if entry["feedback"] in ["good", "corrected"]:
                # Use corrected answer if available, otherwise original answer
                answer = entry.get("corrected_answer") or entry["answer"]
                
                training_data.append({
                    "instruction": entry["question"],
                    "input": "",
                    "output": answer
                })
        
        return training_data