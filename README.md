# 📶 Network Health Monitor: GNN-Based Congestion & Segment Failure Detection

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![ArangoDB](https://img.shields.io/badge/Database-ArangoDB-orange)](https://www.arangodb.com/)
[![Dashboard](https://img.shields.io/badge/Visualization-Dash-green)](https://dash.plotly.com/)

> A Dockerized system that predicts congestion in interconnected network devices using Graph Neural Network (GNN)-style message passing on multi-KPI data (latency, jitter, resource utilization, etc.). The system stores predictions in ArangoDB and visualizes device status and connections through an interactive dashboard. Segment failure is also detected using statistical heuristics on aggregated device embeddings.

---

## 📚 Table of Contents

- [📌 Project Overview](#project-overview)
- [🧰 Prerequisites](#prerequisites)
- [🚀 Getting Started](#getting-started)
  - [Start ArangoDB](#start-arangodb)
  - [Setup Database Collections](#setup-database-collections)
  - [Run Congestion Prediction](#run-congestion-prediction)
  - [Launch Dashboard](#launch-dashboard)
- [🧩 Components](#components)
- [🔍 Segment Failure Prediction](#segment-failure-prediction)
- [📄 License](#license)
- [📬 Contact](#contact)

---

## 📌 Project Overview

This project simulates a network of interconnected devices, where each device logs key performance indicators (KPIs) such as:

- Latency
- Jitter
- Resource Utilization
- Packet Loss

Devices are connected via edges representing communication links, and all data is stored in **ArangoDB**.

Using a **GNN-style message-passing mechanism**, the system computes device embeddings by propagating KPI information across the graph. These embeddings are passed to a **classifier model** that predicts whether a device is congested.

A real-time dashboard displays:
- All devices and their connections
- **Red** = Congested devices
- **Green** = Normal devices

---

## 🧰 Prerequisites

- Docker & Docker Compose  
- Python 3.8+  
- ArangoDB (runs inside Docker)

Install Python packages:
```bash
pip install pandas numpy scikit-learn python-arango dash networkx matplotlib
```

# 🚀 Getting Started

## ✅ Start ArangoDB

```bash
docker run -e ARANGO_ROOT_PASSWORD=rootpass -p 8529:8529 -v arangodata:/var/lib/arangodb3 arangodb
```

Access the ArangoDB UI at: [http://localhost:8529](http://localhost:8529)

- **Username**: `root`  
- **Password**: `rootpass` (or your custom password)

---

## 🛠️ Setup Database Collections

In the Arango UI:

1. Create **Document Collection**: `device_kpi`  
2. Create **Edge Collection**: `cell_edges`

Then populate the DB:

```bash
python update_arango.py
```

---

# 🤖 Run Congestion Prediction

```bash
python congestion.py
```

This script will:

- Load device KPIs from ArangoDB  
- Compute device embeddings via GNN-style message passing  
- Apply a classifier to predict congestion  
- Write results back to the `device_kpi` collection

---

# 📊 Launch Dashboard

```bash
python dash_code.py
```

This opens a browser window displaying:

- Network of devices and edges  
- **Red**: Congested devices  
- **Green**: Normal devices

---

# 🧩 Components

| File              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `update_arango.py` | Populates `device_kpi` and `cell_edges` collections in ArangoDB            |
| `congestion.py`    | Computes embeddings, runs classifier, updates congestion predictions       |
| `dash_code.py`     | Interactive dashboard built using Dash for visualizing network graph       |

---

# 🔍 Segment Failure Prediction

A **segment** is a group of 3–4 interconnected devices.  
Failure is predicted by:

1. Aggregating device embeddings for each segment  
2. Computing basic statistics:  
   - L2 norm  
   - Mean  
   - Standard deviation  
3. Applying a threshold:

```python
threshold = mean - std_dev
```

If a segment's score `< threshold`, it is marked as **failing**.

✔️ **Predictions are already stored in ArangoDB**  
🛠️ **Integration with dashboard is in progress**

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 📬 Contact

For questions, suggestions, or collaboration:

📧 **nssanketh@gmail.com**


