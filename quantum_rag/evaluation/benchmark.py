import time
from quantum_rag.evaluation.metrics import *

def benchmark(query, relevant, classical, quantum):
    t0 = time.time()
    _, c_ids = classical.run(query, return_ids=True)
    c_time = time.time() - t0

    t0 = time.time()
    _, q_ids = quantum.run(query, return_ids=True)
    q_time = time.time() - t0

    return {
        "classical": {
            "p@3": precision_at_k(c_ids, relevant, 3),
            "mrr": mean_reciprocal_rank(c_ids, relevant),
            "latency": c_time
        },
        "quantum": {
            "p@3": precision_at_k(q_ids, relevant, 3),
            "mrr": mean_reciprocal_rank(q_ids, relevant),
            "latency": q_time
        }
    }
