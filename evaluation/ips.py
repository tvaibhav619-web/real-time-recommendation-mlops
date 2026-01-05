import json

def ips(log_path):
    total = 0.0
    count = 0

    with open(log_path) as f:
        for line in f:
            e = json.loads(line)
            reward = 1.0 if e["action"] in ["click", "purchase"] else 0.0
            p = e["propensity"]

            total += reward / p
            count += 1

    return total / count if count > 0 else 0.0
