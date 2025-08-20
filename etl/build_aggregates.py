from util_db import get_conn

SQL = """
WITH delays AS (
  SELECT
    s.trip_id,
    s.stop_id,
    s.sched_ts::date AS day,
    (EXTRACT(EPOCH FROM (
        (SELECT a.actual_ts
         FROM actual a
         WHERE a.trip_id = s.trip_id AND a.stop_id = s.stop_id
           AND abs(EXTRACT(EPOCH FROM (a.actual_ts - s.sched_ts))) < 1800
         ORDER BY abs(EXTRACT(EPOCH FROM (a.actual_ts - s.sched_ts))) ASC
         LIMIT 1
        ) - s.sched_ts))/60.0) AS delay_min,
    st.route
  FROM schedule s
  JOIN stops st ON st.stop_id = s.stop_id
  WHERE s.sched_ts::date >= CURRENT_DATE - INTERVAL '6 days'
),
cleaned AS (
  SELECT route, day, delay_min
  FROM delays
  WHERE delay_min IS NOT NULL
    AND delay_min BETWEEN -20 AND 60
),
p AS (
  SELECT route, day,
         AVG(delay_min) AS avg_delay_min,
         PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY delay_min) AS p95_delay_min
  FROM cleaned
  GROUP BY route, day
)
INSERT INTO agg_daily(route, day, avg_delay_min, p95_delay_min, reliability_score)
SELECT route, day, avg_delay_min, p95_delay_min,
       GREATEST(0, LEAST(1, 1 - (avg_delay_min / 20.0)))
FROM p
ON CONFLICT (route, day) DO UPDATE
SET avg_delay_min = EXCLUDED.avg_delay_min,
    p95_delay_min = EXCLUDED.p95_delay_min,
    reliability_score = EXCLUDED.reliability_score;
"""

def main():
    conn = get_conn(); cur = conn.cursor()
    cur.execute(SQL)
    conn.commit(); cur.close(); conn.close()
    print("Aggregates updated for the last 7 days.")

if __name__ == "__main__":
    main()
