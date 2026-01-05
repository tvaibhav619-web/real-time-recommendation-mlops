from feast import FeatureView, Field, Entity
from feast.types import Int64
from feast.infra.offline_stores.file_source import FileSource
from datetime import timedelta

# -----------------
# Entities
# -----------------
user = Entity(
    name="user_id",
    join_keys=["user_id"],
)

item = Entity(
    name="item_id",
    join_keys=["item_id"],
)

# -----------------
# Offline Sources (required by Feast)
# -----------------
user_source = FileSource(
    path="data/user_features.parquet",
    timestamp_field="event_timestamp",
)

item_source = FileSource(
    path="data/item_features.parquet",
    timestamp_field="event_timestamp",
)

# -----------------
# Feature Views
# -----------------
user_features = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_views", dtype=Int64),
        Field(name="total_clicks", dtype=Int64),
        Field(name="total_purchases", dtype=Int64),
    ],
    source=user_source,
)

item_features = FeatureView(
    name="item_features",
    entities=[item],
    ttl=timedelta(days=1),
    schema=[
        Field(name="popularity", dtype=Int64),
    ],
    source=item_source,
)
