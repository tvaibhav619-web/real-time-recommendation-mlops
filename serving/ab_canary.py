def assign(user_id):
    bucket = hash(user_id) % 100
    return "canary" if bucket < 5 else "control"
