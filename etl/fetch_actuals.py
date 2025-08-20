import random
from datetime import timedelta, date
from util_db import get_conn

def main():
    conn = get_conn(); cur = conn.cursor()
    # find schedules in last 7 days that do not have a matching actual within +/-30 min
    cur.execute("""
      WITH s AS (
        SELECT trip_id, stop_id, sched_ts
        FROM schedule
        WHERE sched_ts::date >= CURRENT_DATE - INTERVAL '6 days'
      ),
      unmatched AS (
        SELECT s.trip_id, s.stop_id, s.sched_ts
        FROM s
        LEFT JOIN actual a
          ON a.trip_id = s.trip_id AND a.stop_id = s.stop_id
         AND abs(EXTRACT(EPOCH FROM (a.actual_ts - s.sched_ts))) < 1800
        WHERE a.trip_id IS NULL
      )
      SELECT trip_id, stop_id, sched_ts FROM unmatched
      LIMIT 5000
    """)
    rows = cur.fetchall()
    batch = []
    for trip_id, stop_id, sched_ts in rows:
        # route-sensitive delay pattern to make charts interesting
        # extract route from stop_id via join for realism
        cur.execute("SELECT route FROM stops WHERE stop_id = %s", (stop_id,))
        route = cur.fetchone()[0]
        if route == "R1":
            delay_min = max(-2, int(random.gauss(1.5, 3)))
        elif route == "R2":
            delay_min = max(-3, int(random.gauss(3.5, 5)))
        elif route == "R3":
            delay_min = max(-1, int(random.gauss(0.5, 2)))
        else:  # R4
            delay_min = max(-4, int(random.gauss(2.5, 4)))
        actual_ts = sched_ts + timedelta(minutes=delay_min)
        vehicle_id = f"sim-{abs(hash((trip_id, stop_id))) % 100}"
        batch.append((trip_id, stop_id, actual_ts, vehicle_id))
    if batch:
        cur.executemany(
            "INSERT INTO actual(trip_id, stop_id, actual_ts, vehicle_id) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            batch
        )
    conn.commit(); cur.close(); conn.close()
    print(f"Inserted {len(batch)} simulated actuals.")

if __name__ == "__main__":
    main()
