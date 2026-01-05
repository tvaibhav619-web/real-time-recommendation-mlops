from kafka import KafkaConsumer
import json
from jsonschema import validate
from pathlib import Path
from datetime import datetime
import torch
import pandas as pd


# -----------------------------
# Project imports
# -----------------------------
from serving.model_loader import model
from serving.user_features import get_user_features
from model.online_update import online_update
from streaming.reward import get_reward
from evaluation.logged_data import log_event

from feast import FeatureStore
from monitoring.drift_stats import log_reward


# -----------------------------
# Load JSON schema
# -----------------------------
schema_path = Path(__file__).parent / "schema.json"
with open(schema_path) as f:
    schema = json.load(f)

# -----------------------------
# Feast Feature Store
# -----------------------------
store = FeatureStore(repo_path="feature_store")

# -----------------------------
# Kafka Consumer
# -----------------------------
consumer = KafkaConsumer(
    "events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
)

print("🚀 Kafka consumer started (features + online learning + logging)")

# -----------------------------
# Consume loop
# -----------------------------
for msg in consumer:
    event = msg.value
    validate(instance=event, schema=schema)

    user_id = event["user_id"]
    item_id = event["item_id"]
    action = event["action"]
    propensity = event.get("propensity", 0.1)

    # -----------------------------
    # 1️⃣ Log event for IPS / DR
    # -----------------------------
    log_event(event)

    # -----------------------------
    # 2️⃣ Update Feast online features (CORRECT API)
    # -----------------------------
    feature_df = pd.DataFrame([{
        "user_id": user_id,
        "total_views": 1 if action == "view" else 0,
        "total_clicks": 1 if action == "click" else 0,
        "total_purchases": 1 if action == "purchase" else 0,
        "event_timestamp": datetime.utcnow(),
    }])

    store.write_to_online_store(
        feature_view_name="user_features",
        df=feature_df,
    )

    # -----------------------------
    # 3️⃣ Online learning update
    # -----------------------------
    reward = get_reward(action)

    if reward > 0:
        user_features = get_user_features(user_id)

        # Placeholder item features (stable for now)
        item_features = torch.rand(1, 8)

        loss = online_update(
            model=model,
            user_features=user_features,
            item_features=item_features,
            label=reward,
        )

        print(
            f"✅ Online update | user={user_id} "
            f"item={item_id} action={action} loss={loss:.4f}"
        )
log_reward(reward)
