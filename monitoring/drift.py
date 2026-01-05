def drift_detected(metric, baseline):
    return metric < baseline * 0.9
