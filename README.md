Real-Time Recommendation System with End-to-End MLOps

A production-grade real-time recommendation system built from scratch using modern MLOps practices.
This project demonstrates online learning, feature stores, vector search, monitoring, drift detection, automated retraining, cold-start handling, and MLflow model governance.

⚠️ This is not a toy project or notebook demo — it is a full system designed like real production recommender platforms (Netflix / Amazon-style).

🧠 Problem Statement

Traditional recommendation systems are:

Batch-trained

Slow to adapt to user behavior

Hard to monitor and retrain

This project solves that by building a real-time recommender that:

Learns continuously from streaming events

Handles cold-start users & items

Detects data & concept drift automatically

Retrains itself without human intervention

Tracks experiments and model versions using MLflow

🏗️ High-Level Architecture
Client
  │
  ▼
FastAPI (Serving + Swagger)
  │
  ├── Feature Fetch (Feast + Redis)
  ├── Cold-Start Detection
  ├── Two-Tower User Embedding
  ├── ANN Retrieval (Milvus)
  ├── Ranking Layer
  │
  ▼
Recommendations
  │
  ▼
Kafka (User Events)
  │
  ├── Online Learning Updates
  ├── Feature Updates (Feast)
  ├── Counterfactual Logging (IPS / DR)
  │
  ▼
Monitoring + Drift Detection
  │
  ├── Prometheus / Grafana
  ├── Drift Watchdog
  │
  ▼
MLflow Retraining Pipeline

✨ Key Features
🔹 Real-Time Streaming

Kafka-based ingestion of user events (views, clicks, purchases)

Near-instant feedback loop

🔹 Feature Store (Feast)

Offline + online feature consistency

Redis-backed low-latency feature serving

🔹 Two-Tower Recommendation Model

Separate user and item towers

Efficient embedding-based retrieval

🔹 ANN Search (Milvus)

Production-grade vector database

Fast candidate generation at scale

🔹 Ranking Layer

Post-retrieval ranking with business signals

Cold-item exploration boost

🔹 Online Learning

Incremental updates from streaming events

Real-time adaptation to user behavior

🔹 Cold-Start Strategy

Feature-store-based cold user detection

Popularity-based fallback

Exploration for new items

🔹 Counterfactual Evaluation

IPS (Inverse Propensity Scoring)

Doubly Robust (DR) estimation

Offline evaluation without risky A/B tests

🔹 Drift Detection & Auto-Retraining

Feature drift + reward drift monitoring

Automatic retraining triggers

Cool-down protection

🔹 MLflow Integration

Experiment tracking

Model versioning

Model registry (Staging → Production)

Drift-triggered retraining runs logged automatically

🔹 Monitoring & Observability

Prometheus metrics

Grafana dashboards

Latency, throughput, cold-start rate

🛠️ Tech Stack
Category	Tools
API	FastAPI, Swagger
Streaming	Kafka
Feature Store	Feast + Redis
Vector Search	Milvus
ML	PyTorch
MLOps	MLflow
Monitoring	Prometheus, Grafana
Serving	Uvicorn
Language	Python
▶️ How to Run the Project
1️⃣ Clone Repository
git clone https://github.com/USERNAME/real-time-recommendation-mlops.git
cd real-time-recommendation-mlops

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Start MLflow
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns


Open:

http://127.0.0.1:5000

4️⃣ Train & Register Model
python -m retrieval.train


Promote model to Production in MLflow UI.

5️⃣ Start API
uvicorn serving.app:app --reload


Swagger UI:

http://127.0.0.1:8000/docs

6️⃣ Start Streaming Components
python -m streaming.consumer
python -m monitoring.watchdog

🧪 Example API Usage
Known User
GET /recommend/1


Response:

{
  "cold_start": false,
  "recommendations": [12, 5, 42, 8]
}

Cold User
GET /recommend/999999


Response:

{
  "cold_start": true,
  "strategy": "popular_fallback",
  "recommendations": [3, 7, 1, 19]
}

📊 MLflow Model Governance

All training runs tracked

Drift-triggered retraining logged

Model promotion controlled via registry

Serving loads Production model automatically

🎯 Why This Project Is Different

Most ML projects:

Train once

Serve static models

Ignore drift & monitoring

This project:

Learns continuously

Detects when it is wrong

Retrains itself

Tracks everything

Handles real-world edge cases (cold start, exploration, governance)

🧠 What This Demonstrates

Real-time ML systems design

Production MLOps practices

Recommender systems expertise

Strong Python packaging discipline

End-to-end ownership mindset

📌 Future Improvements

True contextual bandits / RL policies

Distributed training

Feature attribution explainability

Cloud deployment (Kubernetes)

👤 Author

Vaibhav Tiwari
Built as a capstone-level, production-oriented ML system.

⭐ If You Like This Project

Give it a ⭐ on GitHub — it helps a lot!

🎉 Final Note

If you’re reviewing this as a recruiter or interviewer:
This project reflects how real ML systems are built and operated in production, not just academic modeling.
