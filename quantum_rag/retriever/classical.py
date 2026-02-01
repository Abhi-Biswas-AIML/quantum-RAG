import faiss
import numpy as np

class ClassicalRetriever:
    def __init__(self, embeddings):
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query, k):
        scores, idxs = self.index.search(
            np.array([query]), k
        )
        return idxs[0], scores[0]
