import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model
from datasets import load_from_disk
import yaml
from pathlib import Path
import traceback

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def format_instruction(example):
    text = f"<|system|>\nYou are a helpful assistant.</s>\n"
    text += f"<|user|>\n{example['instruction']}</s>\n"
    if example.get('input'):
        text += f"{example['input']}</s>\n"
    text += f"<|assistant|>\n{example['output']}</s>\n"
    return {"text": text}

def main():
    try:
        print("=" * 60)
        print("TinyLlama Fine-tuning with LoRA (CPU)")
        print("=" * 60)
        
        config = load_config()
        print(f"Config loaded: {config['model']['base_model']}")
        
        print("\n[1/5] Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(config['model']['base_model'])
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        print("✓ Tokenizer loaded successfully")
        
        print("\n[2/5] Loading dataset...")
        dataset = load_from_disk("./data/training/agile_pm_dataset")
        print(f"✓ Dataset loaded: {len(dataset)} examples")
        
        print("Formatting dataset...")
        dataset = dataset.map(format_instruction, remove_columns=['instruction', 'input', 'output'])
        print("✓ Dataset formatted")
        
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                truncation=True,
                max_length=config['training']['max_seq_length'],
                padding="max_length"
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        print("✓ Dataset tokenized")
        
        split_dataset = tokenized_dataset.train_test_split(
            test_size=config['data']['test_split'],
            seed=42
        )
        print(f"✓ Dataset split: {len(split_dataset['train'])} train, {len(split_dataset['test'])} test")
        
        print("\n[3/5] Loading base model...")
        print("This will download ~2.2 GB on first run...")
        model = AutoModelForCausalLM.from_pretrained(
            config['model']['base_model'],
            torch_dtype=torch.float32,
            device_map=None
        )
        print("✓ Base model loaded")
        
        print("Configuring LoRA...")
        lora_config = LoraConfig(
            r=config['training']['lora_r'],
            lora_alpha=config['training']['lora_alpha'],
            target_modules=config['training']['target_modules'],
            lora_dropout=config['training']['lora_dropout'],
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
        print("✓ LoRA configured")
        
        print("\n[4/5] Setting up training...")
        training_args = TrainingArguments(
            output_dir=config['model']['output_dir'],
            num_train_epochs=config['training']['num_epochs'],
            per_device_train_batch_size=config['training']['batch_size'],
            per_device_eval_batch_size=config['training']['batch_size'],
            gradient_accumulation_steps=config['training']['gradient_accumulation_steps'],
            learning_rate=config['training']['learning_rate'],
            warmup_steps=config['training']['warmup_steps'],
            logging_steps=config['training']['logging_steps'],
            save_steps=config['training']['save_steps'],
            save_total_limit=2,
            eval_strategy="steps",
            eval_steps=config['training']['save_steps'],
            fp16=config['training']['fp16'],
            bf16=config['training']['bf16'],
            use_cpu=True,
            dataloader_num_workers=config['training']['num_workers'],
            report_to="none",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False
        )
        print("✓ Training arguments configured")
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=split_dataset["train"],
            eval_dataset=split_dataset["test"],
            data_collator=data_collator
        )
        print("✓ Trainer initialized")
        
        print("\n[5/5] Starting training...")
        print(f"Training on CPU with {config['training']['num_epochs']} epochs")
        print("This will take some time on CPU...")
        
        trainer.train()
        
        print("\nSaving fine-tuned model...")
        trainer.save_model(config['model']['output_dir'])
        tokenizer.save_pretrained(config['model']['output_dir'])
        
        print("\n" + "=" * 60)
        print("✓ Training complete!")
        print(f"Model saved to: {config['model']['output_dir']}")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR OCCURRED:")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        print("=" * 60)

if __name__ == "__main__":
    main()