
# Week 1 simulate arrivals. Replace with real API later.
import random
from datetime import timedelta
from util_db import get_conn

def main():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
                SELECT trip_id, stop_id, sched_ts
                FROM schedule
                WHERE sched_ts::date = (CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago')::date
                LIMIT 2000
                """)

    rows = cur.fetchall()
    batch = []
    for trip_id, stop_id, sched_ts in rows:
        delay_min = max(-3, int(random.gauss(3, 4)))  # skew to slight delay
        actual_ts = sched_ts + timedelta(minutes=delay_min)
        vehicle_id = f"sim-{random.randint(1,50)}"
        batch.append((trip_id, stop_id, actual_ts, vehicle_id))
    cur.executemany(
        "INSERT INTO actual(trip_id, stop_id, actual_ts, vehicle_id) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING",
        batch
    )
    conn.commit(); cur.close(); conn.close()
    print(f"Inserted {len(batch)} simulated actuals.")

if __name__ == "__main__":
    main()
