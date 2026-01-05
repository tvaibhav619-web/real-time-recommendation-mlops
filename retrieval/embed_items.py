import torch
import numpy as np
from retrieval.two_tower import TwoTower

model = TwoTower()
model.load_state_dict(torch.load("retrieval/two_tower.pt", map_location="cpu"))
model.eval()

# Example item features
item_features = torch.rand(500, 8)

with torch.no_grad():
    embeddings = model.item(item_features)

np.save("retrieval/item_embeddings.npy", embeddings.numpy())

print("✅ item_embeddings.npy saved")
