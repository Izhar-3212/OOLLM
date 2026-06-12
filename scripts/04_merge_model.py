from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import yaml

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    base_model_path = config['model']['base_model'] # Points to ./models/base
    lora_model_path = config['model']['output_dir'] # Points to ./models/fine-tuned
    merged_dir = "./models/merged"

    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        return_dict=True,
        torch_dtype="auto"
    )

    print("Loading LoRA weights...")
    model = PeftModel.from_pretrained(
        base_model,
        lora_model_path
    )

    print("Merging weights...")
    model = model.merge_and_unload()

    print("Saving merged model...")
    model.save_pretrained(merged_dir)

    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    tokenizer.save_pretrained(merged_dir)

    print(f"✓ Merged model saved to: {merged_dir}")

if __name__ == "__main__":
    main()