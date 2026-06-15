import sys
print(f"Python version: {sys.version}")

print("\n1. Testing basic imports...")
try:
    from transformers import AutoTokenizer, AutoConfig
    print("✓ Imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print("\n2. Testing with trust_remote_code=False...")
try:
    tokenizer = AutoTokenizer.from_pretrained(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        trust_remote_code=False,
        use_fast=True
    )
    print("✓ Tokenizer loaded!")
except Exception as e:
    print(f"❌ Failed with use_fast=True: {e}")
    
    print("\n3. Trying with use_fast=False...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            trust_remote_code=False,
            use_fast=False
        )
        print("✓ Tokenizer loaded with use_fast=False!")
    except Exception as e2:
        print(f"❌ Failed with use_fast=False: {e2}")
        
        print("\n4. Trying a different model (distilbert)...")
        try:
            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            print("✓ DistilBERT tokenizer loaded!")
        except Exception as e3:
            print(f"❌ Even distilbert failed: {e3}")
            import traceback
            traceback.print_exc()