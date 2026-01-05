import subprocess
import mlflow
from mlflow_config import *

def trigger_retraining():
    print("🚀 Drift detected → triggering retraining")

    with mlflow.start_run(run_name="drift_retraining"):
        mlflow.log_param("trigger", "drift")

        subprocess.Popen(
            ["python", "retrieval/train.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
