from kafka import KafkaProducer
import json, time, random, datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode()
)

while True:
    event = {
        "user_id": random.randint(1, 100),
        "item_id": random.randint(1, 500),
        "action": random.choice(["view", "click", "purchase"]),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    producer.send("events", event)
    time.sleep(1)
    
event = {
    "user_id": user_id,
    "item_id": item_id,
    "action": action,
    "propensity": 0.1  # probability of showing item (baseline policy)
}
