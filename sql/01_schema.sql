
CREATE TABLE IF NOT EXISTS stops (
  stop_id TEXT PRIMARY KEY,
  name TEXT,
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  route TEXT
);

CREATE TABLE IF NOT EXISTS schedule (
  trip_id TEXT,
  stop_id TEXT,
  sched_ts TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (trip_id, stop_id, sched_ts)
);

CREATE TABLE IF NOT EXISTS actual (
  trip_id TEXT,
  stop_id TEXT,
  actual_ts TIMESTAMP WITHOUT TIME ZONE,
  vehicle_id TEXT,
  PRIMARY KEY (trip_id, stop_id, actual_ts)
);

CREATE TABLE IF NOT EXISTS weather (
  ts TIMESTAMP WITHOUT TIME ZONE PRIMARY KEY,
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  temp_c DOUBLE PRECISION,
  precip_mm DOUBLE PRECISION,
  condition TEXT
);

CREATE TABLE IF NOT EXISTS agg_daily (
  route TEXT,
  day DATE,
  avg_delay_min DOUBLE PRECISION,
  p95_delay_min DOUBLE PRECISION,
  reliability_score DOUBLE PRECISION,
  PRIMARY KEY (route, day)
);

CREATE INDEX IF NOT EXISTS idx_actual_stop_ts ON actual(stop_id, actual_ts);
CREATE INDEX IF NOT EXISTS idx_schedule_stop_ts ON schedule(stop_id, sched_ts);
ALTER DATABASE transit SET timezone TO 'America/Chicago';
