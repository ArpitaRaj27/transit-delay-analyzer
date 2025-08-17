
# Transit Delay Analyzer - Starter Kit

This repo is a working starter for SQL + ETL + Dashboard. It runs on Windows with VS Code.

## What this does
- Loads GTFS schedule data into Postgres
- Simulates realtime arrivals and weather for week 1
- Computes delays with SQL
- Shows a Streamlit dashboard

## Quick start
1. Install Python 3.11+ and Docker Desktop.
2. Open this folder in VS Code.
3. Terminal:
   ```
   pip install -r requirements.txt
   docker compose up -d
   python etl/load_gtfs.py
   python etl/fetch_actuals.py
   python etl/fetch_weather.py
   python etl/build_aggregates.py
   streamlit run app/streamlit_app.py
   ```
4. The dashboard opens in your browser.

## Move from simulate to real data later
- Replace `fetch_actuals.py` with a real CTA API fetcher.
- Replace `fetch_weather.py` with a NOAA fetcher.
- Schedule scripts in Windows Task Scheduler.

## Windows Task Scheduler tip
- Action: Start a Program -> Program: `python.exe`
- Arguments: `C:\path\to\project\etl\build_aggregates.py`
- Set repeat every 30 minutes.
