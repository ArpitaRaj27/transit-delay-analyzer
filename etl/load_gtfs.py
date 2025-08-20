import os, csv, zipfile
from datetime import datetime, date, time, timedelta
from util_db import get_conn

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GTFS_ZIP = os.path.join(DATA_DIR, "gtfs.zip")
GTFS_DIR = os.path.join(DATA_DIR, "gtfs_unzipped")

DAYS_BACK = 7  # load this many days

def open_reader(name):
    if os.path.exists(GTFS_ZIP):
        z = zipfile.ZipFile(GTFS_ZIP)
        f = z.open(f"{name}.txt")
        return csv.DictReader(iter(f.read().decode("utf-8-sig").splitlines()))
    fpath = os.path.join(GTFS_DIR, f"{name}.txt")
    if os.path.exists(fpath):
        return csv.DictReader(open(fpath, "r", encoding="utf-8-sig"))
    raise FileNotFoundError(f"Missing {name}.txt in data/gtfs_unzipped or data/gtfs.zip")

def parse_gtfs_time(hms: str):
    h, m, s = map(int, hms.split(":"))
    return time(hour=h % 24, minute=m, second=s), (h // 24)

def load_stops(cur):
    rows = []
    for row in open_reader("stops"):
        rows.append((row["stop_id"], row.get("stop_name",""),
                     float(row["stop_lat"]), float(row["stop_lon"]), None))
    if rows:
        cur.executemany(
            "INSERT INTO stops(stop_id,name,lat,lon,route) VALUES(%s,%s,%s,%s,%s) "
            "ON CONFLICT (stop_id) DO NOTHING", rows)

def load_schedule(cur):
    # trip_id -> (route_id)
    trips = {}
    for r in open_reader("trips"):
        trips[r["trip_id"]] = r["route_id"]

    # route_id -> label
    route_label = {}
    for r in open_reader("routes"):
        route_label[r["route_id"]] = r.get("route_short_name") or r.get("route_long_name") or r["route_id"]

    stop_to_route = {}
    batch = []
    flush = 5000

    # Force every trip/stop_time to exist on each of the last N days
    today = date.today()
    days = [today - timedelta(days=i) for i in range(DAYS_BACK)]

    for r in open_reader("stop_times"):
        trip_id = r["trip_id"]
        route_id = trips.get(trip_id)
        if not route_id:
            continue
        t_str = r.get("arrival_time") or r.get("departure_time")
        if not t_str:
            continue
        t_clock, carry = parse_gtfs_time(t_str)
        stop_id = r["stop_id"]

        # assign a label for UI
        stop_to_route.setdefault(stop_id, route_label.get(route_id, route_id))

        for d in days:
            dt_sched = datetime.combine(d, t_clock) + timedelta(days=carry)
            batch.append((trip_id, stop_id, dt_sched))
            if len(batch) >= flush:
                cur.executemany(
                    "INSERT INTO schedule(trip_id, stop_id, sched_ts) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",
                    batch
                )
                batch = []
    if batch:
        cur.executemany(
            "INSERT INTO schedule(trip_id, stop_id, sched_ts) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",
            batch
        )

    # Tag stops with a route label
    if stop_to_route:
        cur.executemany("UPDATE stops SET route = %s WHERE stop_id = %s",
                        [(lbl, sid) for sid, lbl in stop_to_route.items()])

def main():
    conn = get_conn(); cur = conn.cursor()
    with open(os.path.join(os.path.dirname(__file__), "..", "sql", "01_schema.sql"), "r", encoding="utf-8") as f:
        cur.execute(f.read())
    print("Loading stops...")
    load_stops(cur)
    print(f"Loading schedule (calendar ignored) for last {DAYS_BACK} days...")
    load_schedule(cur)
    conn.commit(); cur.close(); conn.close()
    print("GTFS load complete.")

if __name__ == "__main__":
    main()
