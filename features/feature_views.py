from feast import FeatureView, Field
from feast.types import Int64
from datetime import timedelta

user_item_features = FeatureView(
    name="user_item_features",
    entities=["user_id", "item_id"],
    ttl=timedelta(days=1),
    schema=[
        Field(name="views", dtype=Int64),
        Field(name="clicks", dtype=Int64),
        Field(name="purchases", dtype=Int64),
    ]
)
