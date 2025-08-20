# Transit Delay Analyzer

### 📌 Overview  
Transit Delay Analyzer is a data-driven project built to analyze and visualize public transit delays using **GTFS (General Transit Feed Specification)** data.  
The app processes schedule and stop data, calculates reliability metrics, and displays insights through an interactive **Streamlit dashboard**.  

The motivation for this project was to explore **real-world transit datasets**, practice **ETL pipelines**, and apply **data analytics + visualization** skills in a practical way.  

---

### 🚉 Features  
- **ETL Pipeline**: Ingests GTFS feed, parses schedules & stops, and loads into PostgreSQL.  
- **Analytics**: Computes key KPIs such as average delay, 95th percentile delay, and route reliability.  
- **Visual Dashboard**: Streamlit UI with scorecards, downloadable reports, and visualizations (scatter plots, trends, worst performers).  
- **Data Source**: GTFS open standard feeds ([example feed](https://gtfs.org/getting-started/example-feed/)).  
- **Scalable Setup**: Uses Dockerized PostgreSQL for structured data storage.  

---

### 🎯 Why I Built This  
- To **understand public transit datasets** and their structure.  
- To gain hands-on experience with:  
  - **Database design (PostgreSQL, SQLAlchemy)**  
  - **ETL pipelines (Python, Pandas, psycopg2)**  
  - **Data visualization (Streamlit)**  
  - **Containerization (Docker)**  
- To practice building a project that mimics a **real-world data engineering + analytics use case**.  

---

### 🛠️ Tech Stack  
- **Python** (pandas, psycopg2, SQLAlchemy)  
- **PostgreSQL** (relational data model)  
- **Streamlit** (dashboard & UI)  
- **Docker** (containerized DB + reproducibility)  
- **Git/GitHub** (version control & collaboration)  

---

### 🚀 Step-by-Step Guide  

#### 1. Clone the Repository  
```bash
git clone https://github.com/yourusername/transit-delay-analyzer.git
cd transit-delay-analyzer
