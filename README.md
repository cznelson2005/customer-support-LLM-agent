# 🎯 Customer Support Complaint Intelligence

AI-powered complaint analysis pipeline using Gemini + Async Map-Reduce Agents.

## 🔗 Live Demo
👉 [View Dashboard](https://customer-support-llm-agent-dygkzywxdkncqsbe66nkvj.streamlit.app/)

## 🏗️ Architecture
Twitter Complaints
│
▼
[Data Cleaning + Language Filter]
│
▼
[SentenceTransformer Embeddings]
│
▼
[KMeans Clustering + Silhouette Score]
│
▼
[TF-IDF Top Keywords per Cluster]
│
▼
[Async Map-Reduce Agent Pipeline]
├── Chunk 1 → MAP Agent ──┐
├── Chunk 2 → MAP Agent ──┼──→ REDUCE Agent → Final Report
└── Chunk N → MAP Agent ──┘
│
▼
[Streamlit Dashboard]

## 📁 Structure
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Dependencies
└── notebook/
├──Support_Ticket_agent.ipynb      # Full pipeline notebook
└── data/
├── cluster_analysis.csv        # Per-cluster LLM analysis
├── final_report.json           # Executive report
└── df_sample.csv               # Sample complaints

## 🔧 Tech Stack
- **Gemini 2.5 Flash** — LLM analysis
- **Async Map-Reduce** — parallel agent calls to avoid token limits
- **SentenceTransformer** — complaint embeddings
- **KMeans + Silhouette** — optimal clustering
- **TF-IDF** — keyword extraction
- **Streamlit + Plotly** — interactive dashboard

## 📊 Output
- Top complaint clusters ranked by volume
- Severity classification (High / Medium / Low)
- Root cause analysis
- Prioritized recommendations
- Sample complaints per cluster
