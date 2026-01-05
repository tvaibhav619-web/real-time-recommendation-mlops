import torch
from torch.optim import Adam
import mlflow

_optimizer = None
_loss_fn = torch.nn.BCEWithLogitsLoss()

def init_online_learning(model):
    global _optimizer
    _optimizer = Adam(model.user.parameters(), lr=1e-3)
    print("✅ Online learning optimizer initialized")


def online_update(model, user_features, item_features, label: float):
    if _optimizer is None:
        raise RuntimeError("Online learning optimizer not initialized")

    model.train()

    score = model(user_features, item_features)
    target = torch.tensor([label], dtype=torch.float32)

    loss = _loss_fn(score, target)

    _optimizer.zero_grad()
    loss.backward()
    _optimizer.step()

    # Log online loss to MLflow
    mlflow.log_metric("online_loss", loss.item())

    return loss.item()
