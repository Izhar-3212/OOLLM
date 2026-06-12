import requests
import sys

print("Testing internet connection to Hugging Face...")

try:
    print("Attempting to reach huggingface.co...")
    response = requests.get("https://huggingface.co", timeout=10)
    print(f"✓ Connection successful! Status: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot reach Hugging Face: {e}")
    print("\nThis might be blocked by:")
    print("  - Windows Firewall")
    print("  - Antivirus software")
    print("  - Corporate network restrictions")
    sys.exit(1)

print("\nTrying to download a tiny tokenizer file...")
try:
    url = "https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tokenizer_config.json"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        print("✓ Successfully downloaded tokenizer config!")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Download failed with status: {response.status_code}")
except Exception as e:
    print(f"❌ Download error: {e}")