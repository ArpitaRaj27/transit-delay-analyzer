
# Week 1: load a tiny fake GTFS so you can run end to end
# Later swap this file to parse the real CTA GTFS zip.
import csv, os
from datetime import datetime, timedelta, time, date
from util_db import get_conn

STOPS = [
    # stop_id, name, lat, lon, route
    ("S1","Stop Alpha",41.88,-87.63,"R1"),
    ("S2","Stop Beta",41.89,-87.64,"R1"),
    ("S3","Stop Gamma",41.90,-87.65,"R2"),
]

def main():
    conn = get_conn(); cur = conn.cursor()
    # ensure schema exists
    with open(os.path.join(os.path.dirname(__file__), "..", "sql", "01_schema.sql"), "r", encoding="utf-8") as f:
        cur.execute(f.read())

    # load stops
    cur.executemany(
        "INSERT INTO stops(stop_id,name,lat,lon,route) VALUES(%s,%s,%s,%s,%s) ON CONFLICT (stop_id) DO NOTHING",
        STOPS
    )

    # make a tiny schedule for today, every 30 minutes
    base = datetime.combine(date.today(), time(7,0,0))
    rows = []
    for i in range(20):
        sched = base + timedelta(minutes=30*i)
        rows.append(("T1","S1",sched))
        rows.append(("T1","S2",sched + timedelta(minutes=5)))
        rows.append(("T2","S3",sched + timedelta(minutes=7)))
    cur.executemany(
        "INSERT INTO schedule(trip_id,stop_id,sched_ts) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",
        rows
    )
    conn.commit(); cur.close(); conn.close()
    print("Loaded sample stops and schedule for today.")

if __name__ == "__main__":
    main()
