import mlflow.pytorch
from mlflow_config import *

MODEL_NAME = "TwoTowerRecommender"
MODEL_STAGE = "Production"   # Change to "Staging" if needed

print("🔄 Loading model from MLflow registry...")

model = mlflow.pytorch.load_model(
    f"models:/{MODEL_NAME}/{MODEL_STAGE}"
)

model.eval()

print(f"✅ Model loaded from MLflow [{MODEL_NAME}:{MODEL_STAGE}]")
