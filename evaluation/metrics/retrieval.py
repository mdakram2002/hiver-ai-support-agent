def retrieval_metrics(retrieved, relevant, k=5):
    """Lists are per query; relevant must contain human-labelled relevant IDs."""
    hits = rr = 0
    for got, rel in zip(retrieved, relevant):
        top = got[:k]
        hit = next((i for i, x in enumerate(top, 1) if x in set(rel)), None)
        hits += hit is not None
        rr += 0 if hit is None else 1 / hit
    n = len(retrieved)
    return {f"hit_at_{k}": hits / n if n else None, f"mrr_at_{k}": rr / n if n else None}
