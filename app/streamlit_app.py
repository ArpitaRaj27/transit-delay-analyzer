
import streamlit as st
import pandas as pd
import psycopg2
import os

def run(q, params=None):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB","transit"),
        user=os.getenv("POSTGRES_USER","transit"),
        password=os.getenv("POSTGRES_PASSWORD","transit"),
        host=os.getenv("POSTGRES_HOST","localhost"),
        port=int(os.getenv("POSTGRES_PORT","5432"))
    )
    df = pd.read_sql(q, conn, params=params)
    conn.close()
    return df

st.title("Transit Delay Analyzer")

tab1, tab2 = st.tabs(["Scorecard","Route details"])

with tab1:
    df = run("SELECT route, day, avg_delay_min, p95_delay_min, reliability_score FROM agg_daily ORDER BY day DESC, route LIMIT 200;")
    st.metric("Routes tracked", df["route"].nunique() if not df.empty else 0)
    st.dataframe(df)

with tab2:
    route = st.text_input("Route id", "R1")
    if route:
        q = """
        SELECT day, avg_delay_min, p95_delay_min, reliability_score
        FROM agg_daily
        WHERE route = %s
        ORDER BY day
        """
        d = run(q, (route,))
        if d.empty:
            st.write("No data yet. Run ETL scripts first.")
        else:
            st.line_chart(d.set_index("day")[["avg_delay_min"]])
            st.line_chart(d.set_index("day")[["p95_delay_min"]])
            st.line_chart(d.set_index("day")[["reliability_score"]])
