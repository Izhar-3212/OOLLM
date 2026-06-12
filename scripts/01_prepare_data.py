"""
Convert your documents into Q&A format for training
"""
import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

def load_documents(raw_dir):
    """Load documents from various formats"""
    documents = []
    
    for file_path in Path(raw_dir).glob("*"):
        if file_path.suffix == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                documents.append(f.read())
        elif file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
            documents.extend(df['content'].tolist())
        elif file_path.suffix == ".json":
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    documents.extend([item.get('content', '') for item in data])
    
    return documents

def create_qa_from_documents(documents):
    """
    Convert documents to Q&A format.
    This is a simple template - customize based on your document structure.
    """
    qa_pairs = []
    
    for doc in documents:
        # Split document into chunks (simple approach)
        chunks = doc.split('\n\n')
        
        for chunk in chunks:
            if len(chunk.strip()) > 50:  # Skip very short chunks
                # Create a generic question template
                # In practice, you'd use more sophisticated extraction
                qa_pairs.append({
                    "instruction": "What information is provided in the following text?",
                    "input": chunk.strip(),
                    "output": chunk.strip()
                })
    
    return qa_pairs

if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents("./data/raw")
    print(f"Loaded {len(documents)} documents")
    
    print("\nConverting to Q&A format...")
    qa_data = create_qa_from_documents(documents)
    print(f"Created {len(qa_data)} Q&A pairs")
    
    # Save
    output_path = "./data/training/document_qa.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved to {output_path}")