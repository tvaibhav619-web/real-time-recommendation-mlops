import random

# Replace with DB / Feast item features later
POPULAR_ITEMS = list(range(1, 101))

def popular_items(k=10):
    return random.sample(POPULAR_ITEMS, k)
