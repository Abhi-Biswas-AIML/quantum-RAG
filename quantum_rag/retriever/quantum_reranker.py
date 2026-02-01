import numpy as np
from quantum_rag.quantum.encoding import angle_encode
from quantum_rag.quantum.similarity import swap_test

class QuantumReranker:
    def __init__(self, backend):
        self.backend = backend

    def rerank(self, query, docs, top_m):
        scores = []
        q_circ = angle_encode(query)

        for d in docs:
            d_circ = angle_encode(d)
            score = swap_test(
                q_circ,
                d_circ,
                self.backend.backend,
                self.backend.shots
            )
            scores.append(score)

        idxs = np.argsort(scores)[::-1][:top_m]
        return idxs, scores
