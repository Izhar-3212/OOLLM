import sys
print("Python version:", sys.version)
print("Testing tokenizer loading...")

try:
    from transformers import AutoTokenizer
    print("✓ Transformers imported successfully")
    
    print("Attempting to load tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    print("✓ Tokenizer loaded successfully!")
    print(f"Vocab size: {tokenizer.vocab_size}")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()