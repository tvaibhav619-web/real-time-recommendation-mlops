from fastapi import FastAPI, Response
import torch
import time

# -----------------------------
# Internal imports
# -----------------------------
from serving.model_loader import model
from serving.user_features import get_user_features
from vector_db.milvus import search
from ranking.features import build_ranking_features
from ranking.ranker import rank_items
from serving.ab_canary import assign
from serving.explain import explain
from cold_start.handler import cold_start_recommend

# -----------------------------
# Prometheus imports
# -----------------------------
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="Real-Time Recommendation System")

# -----------------------------
# Metrics
# -----------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"],
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency",
    ["endpoint"],
)

RECOMMENDATION_COUNT = Counter(
    "recommendations_served_total",
    "Total recommendations served",
)

COLD_START_COUNT = Counter(
    "cold_start_requests_total",
    "Total cold start requests",
)

# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Metrics
# -----------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# -----------------------------
# Recommendation
# -----------------------------
@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    start_time = time.time()
    REQUEST_COUNT.labels("GET", "/recommend").inc()

    # 1️⃣ Get user features + cold-start flag
    user_features, is_cold = get_user_features(user_id)

    # 2️⃣ Cold-start handling
    if is_cold:
        COLD_START_COUNT.inc()
        result = cold_start_recommend(user_id)

        return {
            "user_id": user_id,
            "cold_start": True,
            "strategy": result["strategy"],
            "recommendations": result["items"],
        }

    # 3️⃣ User embedding
    with torch.no_grad():
        user_embedding = model.user(user_features).numpy()

    # 4️⃣ ANN candidate generation
    candidate_ids = search(user_embedding, top_k=50)

    # 5️⃣ Ranking
    candidates = []
    for item_id in candidate_ids:
        feats = build_ranking_features(user_id, item_id)
        feats["item_id"] = item_id
        candidates.append(feats)

    ranked = rank_items(candidates)
    top_items = [x["item_id"] for x in ranked[:10]]

    RECOMMENDATION_COUNT.inc()
    REQUEST_LATENCY.labels("/recommend").observe(
        time.time() - start_time
    )

    return {
        "user_id": user_id,
        "cold_start": False,
        "variant": assign(user_id),
        "recommendations": top_items,
        "explanation": explain(),
    }
