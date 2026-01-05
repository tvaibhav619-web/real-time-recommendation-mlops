from cold_start.popularity import popular_items

def cold_start_recommend(user_id: int):
    return {
        "strategy": "popular_fallback",
        "items": popular_items(10)
    }
