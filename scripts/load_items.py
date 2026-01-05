import numpy as np
from vector_db.milvus import insert_embeddings

embeddings = np.load("retrieval/item_embeddings.npy")
insert_embeddings(embeddings)

print("✅ Item embeddings loaded into Milvus")
