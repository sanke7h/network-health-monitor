# 📶 Network Health Monitor: GNN-Based Congestion & Segment Failure Detection

A Dockerized system that predicts congestion in interconnected network devices using Graph Neural Network (GNN)-style message passing on multi-KPI data (latency, jitter, resource utilization, etc.). The system stores predictions in ArangoDB and visualizes device status and connections through an interactive dashboard. Segment failure is also detected using statistical heuristics on aggregated device embeddings.

📚 Table of Contents
Project Overview

Prerequisites

Getting Started

Start ArangoDB

Setup Database Collections

Run Congestion Prediction

Launch Dashboard

Components

Segment Failure Prediction

License

Contact

📌 Project Overview
This project simulates a network of interconnected devices where each device logs key performance indicators (KPIs) such as:

Latency

Jitter

Resource Utilization

Packet Loss

Devices are connected through edges representing communication links. All data is stored in ArangoDB.

Using a message-passing mechanism inspired by Graph Neural Networks (GNNs), device embeddings are computed by propagating KPI information through neighboring nodes. These embeddings are then passed to a classifier model that predicts whether a device is congested. Predictions are written back to the database.

A dashboard visualizes:

All devices and their connections

Congested devices (in red)

Non-congested devices (in green)

🧰 Prerequisites
Docker & Docker Compose

Python 3.8+

ArangoDB (runs in Docker)

Python packages:

bash
Copy
Edit
pip install pandas numpy scikit-learn python-arango dash networkx matplotlib
🚀 Getting Started
1. Start ArangoDB
bash
Copy
Edit
docker run -e ARANGO_ROOT_PASSWORD=rootpass -p 8529:8529 -v arangodata:/var/lib/arangodb3 arangodb
Access the web UI at:
👉 http://localhost:8529

Login:

Username: root

Password: rootpass (or your chosen password)

2. Setup Database Collections
In Arango UI, create the following:

Collection: device_kpi (Document)

Collection: cell_edges (Edge)

Then run:

bash
Copy
Edit
python update_arango.py
Populates the database with initial device and edge data.

3. Run Congestion Prediction
bash
Copy
Edit
python congestion.py
This script:

Loads device KPIs from ArangoDB

Computes device embeddings using GNN-like message passing

Applies a classifier to predict congestion

Updates predictions in device_kpi collection

4. Launch Dashboard
bash
Copy
Edit
python dash_code.py
Opens a dashboard in your browser to visualize:

All devices and their connections

Red = Congested

Green = Normal

🧩 Components
📈 update_arango.py
Populates device and edge collections in ArangoDB.

🤖 congestion.py
Performs message passing to derive device embeddings

Predicts congestion using a trained classifier

Writes results back to ArangoDB

📊 dash_code.py
Interactive dashboard built with Dash

Visualizes network graph and device states

🔍 Segment Failure Prediction
A segment is a group of 3–4 interconnected devices.

Segment failure is detected by:

Aggregating device embeddings segment-wise

Computing the L2 norm, mean, and standard deviation

Defining a threshold:

ini
Copy
Edit
threshold = mean - std_dev
If a segment score falls below the threshold, it's marked as failing

✅ Segment predictions are already stored in ArangoDB
🛠️ Yet to be integrated into the dashboard visualization

📄 License
This project is licensed under the MIT License.

📬 Contact
For questions or collaboration:
📧 nssanket@gmail.com

