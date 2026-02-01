from quantum_rag.pipeline import QuantumRAG
import os

def main():
    path = input("Enter path to document (txt/pdf/docx) or press Enter for default: ").strip()
    
    if not path:
        path = "data/docs.txt"
        
    print(f"Loading from: {path}")
    rag = QuantumRAG(path, noisy=True)
    
    while True:
        q = input("\nQuery (or 'exit'): ")
        if q.lower() == 'exit':
            break
        print(rag.run(q))
