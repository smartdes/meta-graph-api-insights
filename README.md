# 📊 Meta Graph API Insights Exporter & Dashboard

An end-to-end Python data pipeline and interactive Web UI that authenticates with the **Meta Graph API**, extracts Facebook Page engagement metrics, processes the payload using **Pandas**, and visualizes key performance indicators via **Streamlit**.

Built with a strong focus on **DevSecOps best practices** (environment variable isolation, non-versioned secrets, and structured dependency management).

---

## 🌟 Key Features

* **Real-Time API Extraction:** Connects to Meta's Graph API (`v19.0`) to fetch Page impressions and post engagement metrics.
* **Interactive Streamlit Dashboard:** Visualizes trends over time with dynamic line charts and summary KPI cards.
* **Automated Data Export:** Generates custom `.csv` reports directly through the UI or CLI pipeline.
* **Secure Credentials Handling:** Uses `python-dotenv` to ensure API tokens and Page IDs are never hardcoded or exposed in version control.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.x
* **Data Processing:** Pandas
* **API Integration:** Requests, Meta Graph API (`v19.0`)
* **Frontend UI:** Streamlit
* **Environment Security:** `python-dotenv`
* **Version Control:** Git, GitHub (`.gitignore` secured)

---

## ⚙️ Quickstart Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/smartdes/meta-graph-api-insights.git](https://github.com/smartdes/meta-graph-api-insights.git)
cd meta-graph-api-insights