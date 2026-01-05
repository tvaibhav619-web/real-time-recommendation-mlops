from collections import deque
import numpy as np

# Rolling windows
WINDOW_SIZE = 500

feature_window = deque(maxlen=WINDOW_SIZE)
reward_window = deque(maxlen=WINDOW_SIZE)

def log_feature(vec):
    feature_window.append(vec)

def log_reward(r):
    reward_window.append(r)

def feature_mean():
    if len(feature_window) == 0:
        return None
    return np.mean(feature_window, axis=0)

def reward_mean():
    if len(reward_window) == 0:
        return None
    return np.mean(reward_window)
