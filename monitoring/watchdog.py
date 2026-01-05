import time
from monitoring.drift_detector import detect_drift
from retraining.trigger import trigger_retraining

CHECK_INTERVAL = 60  # seconds

print("🛡 Drift watchdog started")

while True:
    if detect_drift():
        trigger_retraining()
        time.sleep(600)  # cooldown after retraining
    time.sleep(CHECK_INTERVAL)
