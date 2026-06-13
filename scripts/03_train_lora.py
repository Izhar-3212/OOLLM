"""
Fine-tune TinyLlama with LoRA (CPU) - v2

Fixes over v1:
- pad_token = unk_token (not eos), so EOS tokens are NOT masked out of the
  loss and the model learns to stop generating.
- Completion-only loss: prompt tokens are masked to -100; the model is
  trained only on the assistant's answer.
- Prompts are built with tokenizer.apply_chat_template, identical to
  inference.
- Dynamic padding to the longest sequence in each batch (was: every example
  padded to max_seq_length).
- Train/test split comes pre-made from 15_prepare_data_v2.py (split by
  question, no leakage).
- Errors propagate instead of being swallowed.
"""
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model
from datasets import load_from_disk
import yaml


def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)


def main():
    print("=" * 60)
    print("TinyLlama Fine-tuning with LoRA (CPU) - v2")
    print("=" * 60)

    config = load_config()
    train_cfg = config['training']
    max_seq = train_cfg['max_seq_length']

    print("\n[1/5] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(config['model']['base_model'])
    # Use UNK as padding so real EOS tokens keep their training signal.
    tokenizer.pad_token = tokenizer.unk_token
    tokenizer.padding_side = "right"

    print("\n[2/5] Loading dataset...")
    dataset = load_from_disk(train_cfg['dataset_path'])
    print(f"  train: {len(dataset['train'])}, test: {len(dataset['test'])}")

    def build_example(example):
        messages = [
            {"role": "system", "content": example["system"]},
            {"role": "user", "content": example["user"]},
        ]
        prompt_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        full_text = tokenizer.apply_chat_template(
            messages + [{"role": "assistant", "content": example["assistant"]}],
            tokenize=False, add_generation_prompt=False
        )
        answer_text = full_text[len(prompt_text):]

        prompt_ids = tokenizer(prompt_text, add_special_tokens=True)["input_ids"]
        answer_ids = tokenizer(answer_text, add_special_tokens=False)["input_ids"]

        input_ids = (prompt_ids + answer_ids)[:max_seq]
        labels = ([-100] * len(prompt_ids) + answer_ids)[:max_seq]
        return {
            "input_ids": input_ids,
            "labels": labels,
            "attention_mask": [1] * len(input_ids),
        }

    columns = dataset["train"].column_names
    tokenized = dataset.map(build_example, remove_columns=columns)
    # Drop examples whose answer was fully truncated away (no trainable tokens).
    tokenized = tokenized.filter(
        lambda ex: any(l != -100 for l in ex["labels"])
    )
    print(f"  tokenized: train {len(tokenized['train'])}, test {len(tokenized['test'])}")

    def collate(batch):
        max_len = max(len(ex["input_ids"]) for ex in batch)
        input_ids, labels, attention = [], [], []
        for ex in batch:
            pad = max_len - len(ex["input_ids"])
            input_ids.append(ex["input_ids"] + [tokenizer.pad_token_id] * pad)
            labels.append(ex["labels"] + [-100] * pad)
            attention.append(ex["attention_mask"] + [0] * pad)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "attention_mask": torch.tensor(attention, dtype=torch.long),
        }

    print("\n[3/5] Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        config['model']['base_model'],
        torch_dtype=torch.float32,
        device_map=None,
    )

    lora_config = LoraConfig(
        r=train_cfg['lora_r'],
        lora_alpha=train_cfg['lora_alpha'],
        target_modules=train_cfg['target_modules'],
        lora_dropout=train_cfg['lora_dropout'],
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    print("\n[4/5] Setting up training...")
    training_args = TrainingArguments(
        output_dir=config['model']['output_dir'],
        num_train_epochs=train_cfg['num_epochs'],
        per_device_train_batch_size=train_cfg['batch_size'],
        per_device_eval_batch_size=train_cfg['batch_size'],
        gradient_accumulation_steps=train_cfg['gradient_accumulation_steps'],
        learning_rate=train_cfg['learning_rate'],
        warmup_steps=train_cfg['warmup_steps'],
        logging_steps=train_cfg['logging_steps'],
        save_steps=train_cfg['save_steps'],
        save_total_limit=2,
        eval_strategy="steps",
        eval_steps=train_cfg['save_steps'],
        fp16=train_cfg['fp16'],
        bf16=train_cfg['bf16'],
        use_cpu=True,
        dataloader_num_workers=train_cfg['num_workers'],
        report_to="none",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        data_collator=collate,
    )

    print("\n[5/5] Starting training...")
    trainer.train()

    print("\nSaving fine-tuned model...")
    trainer.save_model(config['model']['output_dir'])
    tokenizer.save_pretrained(config['model']['output_dir'])

    print("\n" + "=" * 60)
    print(f"Training complete. Model saved to: {config['model']['output_dir']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
