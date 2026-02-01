def precision_at_k(retrieved, relevant, k):
    return sum(1 for i in retrieved[:k] if i in relevant) / k

def mean_reciprocal_rank(retrieved, relevant):
    for i, r in enumerate(retrieved):
        if r in relevant:
            return 1 / (i + 1)
    return 0.0
