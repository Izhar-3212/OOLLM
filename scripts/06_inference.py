import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    model_path = "./models/merged"
    
    print("Loading merged model and tokenizer...")
    print("(This might take 10-20 seconds to load 2GB+ into RAM...)")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32, # CPU requires float32
        device_map="cpu"
    )
    
    print("\n" + "="*60)
    print("🤖 TinyLlama Chatbot is ready!")
    print("Type 'exit' or 'quit' to stop.")
    print("="*60)
    
    system_prompt = "You are a helpful assistant."
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Format prompt using TinyLlama's specific chat template
            prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_input}</s>\n<|assistant|>\n"
            
            inputs = tokenizer(prompt, return_tensors="pt")
            
            print("Assistant: ", end="", flush=True)
            
            # Generate response
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
                
            # Decode and print only the newly generated text
            response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()