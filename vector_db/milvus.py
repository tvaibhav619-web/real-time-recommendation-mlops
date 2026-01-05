import time
import numpy as np
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)

# -----------------------------
# Connect to Milvus (with retry)
# -----------------------------
for i in range(10):
    try:
        connections.connect(
            alias="default",
            host="127.0.0.1",
            port="19530",
            timeout=5
        )
        print("✅ Connected to Milvus")
        break
    except Exception:
        print(f"⏳ Waiting for Milvus... ({i+1}/10)")
        time.sleep(5)
else:
    raise RuntimeError("❌ Milvus did not start")

COLLECTION_NAME = "item_embeddings"
VECTOR_DIM = 32   # must match Two-Tower embedding size


# -----------------------------
# Create / Load Collection
# -----------------------------
def get_collection():
    if not utility.has_collection(COLLECTION_NAME):
        fields = [
            FieldSchema(
                name="item_id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=False
            ),
            FieldSchema(
                name="vector",
                dtype=DataType.FLOAT_VECTOR,
                dim=VECTOR_DIM
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Item embeddings for recommendations"
        )

        collection = Collection(
            name=COLLECTION_NAME,
            schema=schema
        )

        collection.create_index(
            field_name="vector",
            index_params={
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 128}
            }
        )
    else:
        collection = Collection(COLLECTION_NAME)

    collection.load()
    return collection


# -----------------------------
# INSERT ITEM EMBEDDINGS
# -----------------------------
def insert_embeddings(embeddings: np.ndarray):
    """
    embeddings: np.ndarray of shape (num_items, VECTOR_DIM)
    """
    collection = get_collection()

    item_ids = list(range(len(embeddings)))
    vectors = embeddings.tolist()

    collection.insert([item_ids, vectors])
    collection.flush()

    print(f"✅ Inserted {len(item_ids)} item embeddings into Milvus")


# -----------------------------
# SEARCH (used by API)
# -----------------------------
def search(user_embedding, top_k=10):
    collection = get_collection()

    results = collection.search(
        data=user_embedding,
        anns_field="vector",
        param={"metric_type": "IP", "params": {"nprobe": 10}},
        limit=top_k
    )

    return [hit.id for hit in results[0]]

