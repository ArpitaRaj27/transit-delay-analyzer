# 🚍 Transit Delay Analyzer

A data-driven app to measure, visualize, and analyze public transit delays using **GTFS feeds**.  
This project helped me explore **ETL pipelines, databases, data visualization, and Streamlit apps**.  

---

## 📖 About the Project
Transit systems generate tons of data, but it’s often hard to analyze reliability in a clear way.  
I built this project to:
- Fetch and process **real GTFS data** ([sample feed](https://gtfs.org/getting-started/example-feed/))  
- Store it in a **PostgreSQL database** (Dockerized)  
- Run an **ETL pipeline** to load and clean data  
- Visualize insights with **Streamlit**: KPIs, scorecards, trends, scatter plots, and more  

What I learned:
- Setting up PostgreSQL in Docker  
- Writing ETL pipelines in Python (with `psycopg2`, `pandas`)  
- Building interactive dashboards in **Streamlit + Altair**  
- Using config-based **Streamlit theming** + custom CSS  

---

## ⚙️ Tech Stack
- **Python**: pandas, psycopg2, altair, streamlit  
- **PostgreSQL** (with Docker)  
- **GTFS Data Feed**  
- **Docker Compose** for setup  

---

## 🚀 How to Run

1. Clone the repo
```bash
git clone https://github.com/yourusername/transit-delay-analyzer.git
cd transit-delay-analyzer

