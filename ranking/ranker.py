def rank_items(candidates):
    """
    candidates: list of dicts
    """
    def score(x):
        return (
            0.6 * x["relevance_score"]
            + 0.3 * x["popularity"]
            + 0.1 * x["recency"]
        )

    return sorted(candidates, key=score, reverse=True)
