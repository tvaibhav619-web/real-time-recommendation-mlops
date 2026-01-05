import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch

from retrieval.two_tower import TwoTower
from mlflow_config import *

EPOCHS = 5
LR = 0.001

def train():
    model = TwoTower()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    # Dummy training loop (replace with real data later)
    for epoch in range(EPOCHS):
        user = torch.rand(32, 8)
        item = torch.rand(32, 8)
        labels = torch.randint(0, 2, (32,)).float()

        preds = model(user, item)
        loss = loss_fn(preds, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model, loss.item()


if __name__ == "__main__":
    with mlflow.start_run(run_name="two_tower_training"):
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("lr", LR)
        mlflow.log_param("embedding_dim", 8)

        model, final_loss = train()

        mlflow.log_metric("final_loss", final_loss)

        mlflow.pytorch.log_model(
            model,
            artifact_path="model",
            registered_model_name="TwoTowerRecommender",
        )

        print("✅ Training complete & model logged to MLflow")
