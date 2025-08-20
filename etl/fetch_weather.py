import random
from datetime import datetime, timedelta
from util_db import get_conn

def main():
    conn = get_conn(); cur = conn.cursor()
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    rows = []
    for h in range(0, 24*7):  # last 7 days hourly
        ts = now - timedelta(hours=h)
        # make rain more likely in afternoons
        hour = ts.hour
        base = ["clear"]*6 + ["cloudy"]*3 + ["light rain"]*2 + ["rain"]
        if 14 <= hour <= 20:
            base += ["light rain","rain"]
        condition = random.choice(base)
        temp_c = 12.0 + (10.0 * abs((hour-15)/15)) + random.random()*4
        precip_mm = 0.0 if "rain" not in condition else round(random.random()*4,2)
        rows.append((ts, 41.8781, -87.6298, temp_c, precip_mm, condition))
    cur.executemany("""
      INSERT INTO weather(ts, lat, lon, temp_c, precip_mm, condition)
      VALUES(%s,%s,%s,%s,%s,%s)
      ON CONFLICT (ts) DO NOTHING
    """, rows)
    conn.commit(); cur.close(); conn.close()
    print(f"Upserted ~{len(rows)} weather rows for last 7 days.")

if __name__ == "__main__":
    main()
