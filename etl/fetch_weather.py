
# Week 1 simulate weather. Replace with NOAA later.
import random
from datetime import datetime, timedelta
from util_db import get_conn

def main():
    conn = get_conn(); cur = conn.cursor()
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    rows = []
    for i in range(0, 24):
        ts = now - timedelta(hours=i)
        condition = random.choice(["clear","cloudy","light rain","rain"])
        temp_c = 18.0 + random.random()*10
        precip_mm = 0.0 if "rain" not in condition else round(random.random()*3,2)
        rows.append((ts, 41.8781, -87.6298, temp_c, precip_mm, condition))
    cur.executemany(
        "INSERT INTO weather(ts, lat, lon, temp_c, precip_mm, condition) VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT (ts) DO NOTHING",
        rows
    )
    conn.commit(); cur.close(); conn.close()
    print(f"Upserted {len(rows)} weather rows.")

if __name__ == "__main__":
    main()
