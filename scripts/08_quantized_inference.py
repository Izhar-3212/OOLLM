import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from feedback_manager import FeedbackManager

def main():
    model_path = "./models/merged"
    
    print("Loading Mini Me...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    
    model.eval()
    torch.set_num_threads(8)
    
    # Initialize feedback manager
    feedback_mgr = FeedbackManager()
    
    print("\n" + "="*60)
    print("🤖 Mini Me with Continuous Learning is ready!")
    print("="*60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
            
            # Get good examples from feedback for in-context learning
            good_examples = feedback_mgr.get_good_examples(limit=3)
            
            # Build prompt with examples
            prompt = "<|system|>\nYou are Mini Me, a helpful assistant. Learn from the examples below.</s>\n"
            
            # Add good examples as context
            if good_examples:
                prompt += "\nHere are some examples of good responses:\n"
                for ex in good_examples:
                    answer = ex.get("corrected_answer") or ex["answer"]
                    prompt += f"Q: {ex['question']}\nA: {answer}\n"
            
            # Add current question
            prompt += f"\n<|user|>\n{user_input}</s>\n<|assistant|>\n"
            
            inputs = tokenizer(prompt, return_tensors="pt")
            
            print("Mini Me: ", end="", flush=True)
            
            start_time = time.time()
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=100,
                    max_length=None,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2
                )
            
            response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            print(response)
            
            elapsed = time.time() - start_time
            print(f"\n[{elapsed:.2f}s]")
            
            # Ask for feedback
            print("\n--- Feedback ---")
            print("1. Good answer 👍")
            print("2. Bad answer 👎")
            print("3. Let me correct it ✏️")
            print("4. Skip (no feedback)")
            
            feedback_choice = input("Your choice (1-4): ").strip()
            
            if feedback_choice == "1":
                feedback_mgr.add_feedback(user_input, response, "good")
            elif feedback_choice == "2":
                feedback_mgr.add_feedback(user_input, response, "bad")
            elif feedback_choice == "3":
                corrected = input("Enter the correct answer: ").strip()
                if corrected:
                    feedback_mgr.add_feedback(user_input, response, "corrected", corrected)
                    print("✓ Thanks! Mini Me will learn from this.")
            elif feedback_choice == "4":
                print("Skipped.")
            else:
                print("Invalid choice, skipping.")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()