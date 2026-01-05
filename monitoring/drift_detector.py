import numpy as np
from monitoring.drift_stats import feature_mean, reward_mean

# Baselines (set after training)
BASELINE_FEATURE_MEAN = None
BASELINE_REWARD_MEAN = None

FEATURE_DRIFT_THRESHOLD = 0.3
REWARD_DRIFT_THRESHOLD = 0.2

def set_baseline(features, reward):
    global BASELINE_FEATURE_MEAN, BASELINE_REWARD_MEAN
    BASELINE_FEATURE_MEAN = features
    BASELINE_REWARD_MEAN = reward

def detect_drift():
    current_feat = feature_mean()
    current_reward = reward_mean()

    if current_feat is None or current_reward is None:
        return False

    feature_shift = np.linalg.norm(current_feat - BASELINE_FEATURE_MEAN)
    reward_shift = abs(current_reward - BASELINE_REWARD_MEAN)

    if feature_shift > FEATURE_DRIFT_THRESHOLD:
        print("⚠️ Data drift detected")
        return True

    if reward_shift > REWARD_DRIFT_THRESHOLD:
        print("⚠️ Concept drift detected")
        return True

    return False
