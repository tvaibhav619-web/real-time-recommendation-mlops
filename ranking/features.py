import numpy as np

def item_is_cold(item_features: dict) -> bool:
    return item_features.get("popularity", 0) == 0

def build_ranking_features(user_id: int, item_id: int):
    """
    Ranking features for candidate items.
    """
    np.random.seed(user_id + item_id)

    feats = {
        "relevance_score": np.random.rand(),
        "popularity": np.random.randint(0, 10),
        "recency": np.random.rand(),
    }

    # Boost new items (cold items exploration)
    if item_is_cold(feats):
        feats["recency"] += 0.3

    return feats

