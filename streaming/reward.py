def get_reward(action: str) -> float:
    return {
        "view": 0.0,
        "click": 1.0,
        "purchase": 2.0
    }.get(action, 0.0)
