import json
from evaluation.reward_model import predict_reward

def doubly_robust(log_path):
    total = 0.0
    count = 0

    with open(log_path) as f:
        for line in f:
            e = json.loads(line)
            reward = 1.0 if e["action"] in ["click", "purchase"] else 0.0
            p = e["propensity"]

            r_hat = predict_reward(e["user_id"], e["item_id"])

            total += r_hat + (reward - r_hat) / p
            count += 1

    return total / count if count > 0 else 0.0
