from sklearn.decomposition import PCA
from quantum_rag.embeddings.classical import ClassicalEmbedder
from quantum_rag.retriever.classical import ClassicalRetriever
from quantum_rag.retriever.quantum_reranker import QuantumReranker
from quantum_rag.quantum.backend import QuantumBackend
from quantum_rag.prompt.builder import build_prompt
from quantum_rag.loader import load_document
import os

class QuantumRAG:
    def __init__(self, doc_path_or_list, noisy=False):
        # Support both a list of strings or a path to a file
        if isinstance(doc_path_or_list, list):
            self.docs = doc_path_or_list
        elif isinstance(doc_path_or_list, str):
             if os.path.exists(doc_path_or_list):
                 self.docs = load_document(doc_path_or_list)
             else:
                 raise FileNotFoundError(f"Path not found: {doc_path_or_list}")
        else:
            raise ValueError("Input must be a list of strings or a file path.")

        self.embedder = ClassicalEmbedder()
        emb = self.embedder.encode(self.docs)

        self.pca = PCA(n_components=4)
        self.embeddings = self.pca.fit_transform(emb)

        self.retriever = ClassicalRetriever(self.embeddings)
        self.q_backend = QuantumBackend(noisy=noisy)
        self.q_reranker = QuantumReranker(self.q_backend)

    def run(self, query, top_k=8, top_m=3, return_ids=False):
        q = self.embedder.encode([query])[0]
        q = self.pca.transform([q])[0]

        idxs, _ = self.retriever.search(q, top_k)
        candidates = self.embeddings[idxs]

        q_idxs, _ = self.q_reranker.rerank(q, candidates, top_m)
        final_ids = [idxs[i] for i in q_idxs]
        docs = [self.docs[i] for i in final_ids]

        # 3. Prompt Construction
        prompt = build_prompt(query, docs)
        
        # 4. Generation (Optional)
        answer = None
        if hasattr(self, 'generator') and self.generator:
            answer = self.generator.generate(prompt)
        
        return {
            "query": query,
            "retrieved_ids": final_ids,
            "prompt": prompt,
            "answer": answer
        }

    def set_generator(self, api_key: str):
        """Attach a generator to the pipeline."""
        from quantum_rag.generator import GeminiGenerator
        self.generator = GeminiGenerator(api_key)

