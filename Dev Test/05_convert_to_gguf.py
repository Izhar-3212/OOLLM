"""
Convert model to GGUF format for CPU inference
Requires llama.cpp repository
"""
import subprocess
import os
from pathlib import Path

def convert_to_gguf():
    """Convert merged model to GGUF format"""
    
    print("Converting to GGUF format...")
    print("Note: This requires llama.cpp to be installed")
    
    # Clone llama.cpp if not exists
    if not Path("llama.cpp").exists():
        print("Cloning llama.cpp...")
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp"])
    
    # Convert to GGUF
    merged_dir = "./models/merged"
    gguf_dir = "./models/gguf"
    Path(gguf_dir).mkdir(parents=True, exist_ok=True)
    
    print("\nConverting model to GGUF...")
    cmd = [
        "python", "llama.cpp/convert-hf-to-gguf.py",
        merged_dir,
        "--outfile", f"{gguf_dir}/tinyllama-chatbot-F16.gguf",
        "--outtype", "f16"
    ]
    
    subprocess.run(cmd, check=True)
    
    # Quantize to Q4_K_M (good balance of size and quality)
    print("\nQuantizing to Q4_K_M...")
    quantize_cmd = [
        "./llama.cpp/quantize",
        f"{gguf_dir}/tinyllama-chatbot-F16.gguf",
        f"{gguf_dir}/tinyllama-chatbot-Q4_K_M.gguf",
        "Q4_K_M"
    ]
    
    # On Windows, use .exe
    if os.name == 'nt':
        quantize_cmd[0] = "./llama.cpp/quantize.exe"
    
    subprocess.run(quantize_cmd, check=True)
    
    print(f"\n✓ GGUF model saved to: {gguf_dir}")
    print("  - F16 (full precision): ~2.2 GB")
    print("  - Q4_K_M (quantized): ~0.7 GB (recommended for CPU)")

if __name__ == "__main__":
    convert_to_gguf()