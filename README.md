# Quantum-RAG

A hybrid Retrieval-Augmented Generation system using quantum circuits for document re-ranking.

## Features
- Classical embeddings + FAISS for fast retrieval
- Quantum similarity (swap test) for re-ranking
- **Local Execution**: Runs entirely on your machine (no API keys required!)
- Support for **PDF**, **Word**, and **Text** files

## Setup

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the System**
    ```bash
    streamlit run app.py
    ```

## Usage
1.  Run the CLI: `python cli.py`
2.  Enter the path to your document (e.g., `my_paper.pdf`) or press Enter to use the default sample data.
3.  Ask questions! The system will retrieve relevant chunks and rerank them using a simulated quantum circuit.

## Configuration
**Do I need an API key?**
No. This project uses:
- `sentence-transformers` for local embedding models.
- `qiskit` for local quantum simulation.
- No external LLM API is connected by default (generation is currently a mock/stub).

## Why Quantum?
Quantum re-ranking improves semantic relevance for small candidate sets in RAG pipelines.
