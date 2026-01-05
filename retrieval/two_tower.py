import torch.nn as nn

class TwoTower(nn.Module):
    def __init__(self):
        super().__init__()
        self.user = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Linear(64, 32))
        self.item = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Linear(64, 32))

    def forward(self, u, i):
        return (self.user(u) * self.item(i)).sum(dim=1)
