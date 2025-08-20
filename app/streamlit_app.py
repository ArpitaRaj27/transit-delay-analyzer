import os
import datetime as dt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# DB engine
ENGINE = create_engine("postgresql+psycopg2://transit:transit@localhost:5432/transit")

@st.cache_data(ttl=60)
def qdf(sql, params=None):
    with ENGINE.connect() as c:
        return pd.read_sql_query(text(sql), c, params=params)

st.set_page_config(page_title="Transit Delay Analyzer", layout="wide")
st.title("Transit Delay Analyzer")

# Sidebar filters
st.sidebar.header("Filters")
default_to = dt.date.today()
default_from = default_to - dt.timedelta(days=6)

date_from = st.sidebar.date_input("From", default_from)
date_to = st.sidebar.date_input("To", default_to)

routes_all = qdf("SELECT DISTINCT route FROM agg_daily ORDER BY route;")
route_options = routes_all["route"].tolist() if not routes_all.empty else []
selected_routes = st.sidebar.multiselect("Routes", options=route_options, default=route_options[:3])

st.sidebar.markdown("---")
st.sidebar.caption("Data refreshes when ETL runs")

def build_where(date_from, date_to, selected_routes):
    where = "WHERE day BETWEEN :dfrom AND :dto"
    params = {"dfrom": date_from, "dto": date_to}
    if selected_routes:  # only add filter if non-empty
        where += " AND route = ANY(:routes)"
        params["routes"] = selected_routes
    return where, params

where, base_params = build_where(date_from, date_to, selected_routes)

# KPI section
kpi = qdf(f"""
  SELECT
    ROUND(AVG(avg_delay_min)::numeric,2) AS avg_delay,
    ROUND(AVG(p95_delay_min)::numeric,2) AS p95_delay,
    ROUND(AVG(reliability_score)::numeric,3) AS reliability
  FROM agg_daily
  {where}
""", base_params)

c1, c2, c3 = st.columns(3)
c1.metric("Avg delay (min)", kpi["avg_delay"].iloc[0] if not kpi.empty else 0)
c2.metric("P95 delay (min)", kpi["p95_delay"].iloc[0] if not kpi.empty else 0)
c3.metric("Reliability", kpi["reliability"].iloc[0] if not kpi.empty else 0)

# Scorecard table
score = qdf(f"""
  SELECT route, day, ROUND(avg_delay_min::numeric,2) AS avg_delay_min,
         ROUND(p95_delay_min::numeric,2) AS p95_delay_min,
         ROUND(reliability_score::numeric,3) AS reliability_score
  FROM agg_daily
  {where}
  ORDER BY day DESC, route
""", base_params)

st.subheader("Scorecard")
st.dataframe(score, use_container_width=True)
st.download_button("Download CSV", score.to_csv(index=False).encode("utf-8"),
                   file_name="scorecard.csv", mime="text/csv")

# Trends
st.subheader("Trends")
colA, colB = st.columns(2)

trend = qdf(f"""
  SELECT day, route,
         ROUND(AVG(avg_delay_min)::numeric,2) AS avg_delay_min,
         ROUND(AVG(p95_delay_min)::numeric,2) AS p95_delay_min,
         ROUND(AVG(reliability_score)::numeric,3) AS reliability_score
  FROM agg_daily
  {where}
  GROUP BY day, route
  ORDER BY day, route
""", base_params)

if not trend.empty:
    with colA:
        st.line_chart(trend.pivot(index="day", columns="route", values="avg_delay_min"))
    with colB:
        worst = qdf(f"""
          SELECT route, ROUND(AVG(avg_delay_min)::numeric,2) AS avg_delay
          FROM agg_daily
          {where}
          GROUP BY route ORDER BY avg_delay DESC LIMIT 10
        """, base_params)
        if not worst.empty:
            st.bar_chart(worst.set_index("route")["avg_delay"])

# Weather vs delay scatter (coarse join by day)
st.subheader("Weather effect")
scatter = qdf(f"""
  WITH w AS (
    SELECT date_trunc('hour', ts) AS hr, AVG(precip_mm) AS precip
    FROM weather
    WHERE ts::date BETWEEN :dfrom AND :dto
    GROUP BY 1
  ),
  d AS (
    SELECT day, route, AVG(avg_delay_min) AS avg_delay
    FROM agg_daily
    {where}
    GROUP BY day, route
  )
  SELECT d.day, d.route, d.avg_delay, COALESCE(w.precip,0) AS precip_mm
  FROM d
  LEFT JOIN w ON w.hr::date = d.day
  ORDER BY d.day, d.route
""", base_params)

if not scatter.empty:
    st.scatter_chart(scatter.rename(columns={"avg_delay":"y","precip_mm":"x"})[["x","y"]])
    st.caption("x = precipitation mm, y = avg delay min")

# Route details
st.subheader("Route details")
sel = st.selectbox("Pick a route", route_options or ["R1"])
detail = qdf("""
  SELECT day, avg_delay_min, p95_delay_min, reliability_score
  FROM agg_daily
  WHERE route = :r
  ORDER BY day
""", {"r": sel})
if not detail.empty:
    st.line_chart(detail.set_index("day")[["avg_delay_min"]])
    st.line_chart(detail.set_index("day")[["p95_delay_min"]])
    st.line_chart(detail.set_index("day")[["reliability_score"]])
else:
    st.info("No data yet for the selected route.")
