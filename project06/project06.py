import sqlite3
import pandas as pd

# !curl awing.kis.agh.edu.pl:8080/detectors_names_traffic_s_small.csv.bz2 | bunzip2 > data.csv

con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()
pd.read_sql("SELECT * FROM readings LIMIT 10;", con)

cur.execute("""
CREATE INDEX IF NOT EXISTS detector_id ON readings (detector_id);
""").fetchall()
cur.execute("""
CREATE INDEX IF NOT EXISTS starttime ON readings (starttime);
""").fetchall()

####### ZADANIE 1 #######
df = pd.read_sql("SELECT COUNT(DISTINCT detector_id) FROM readings;", con)
df.to_pickle("proj6_ex01_detector_no.pkl")

###### ZADANIE 2 #######
df = pd.read_sql("""
SELECT detector_id, COUNT(*) AS measurement_count, MIN(starttime) AS min_starttime, MAX(starttime) AS max_starttime
FROM readings
WHERE count IS NOT NULL
GROUP BY detector_id;
""", con)

df.to_pickle("proj6_ex02_detector_stat.pkl")

##### ZADANIE 3 ########
df = pd.read_sql("""
SELECT detector_id, count, LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) AS previous_count
FROM readings
WHERE detector_id = 146
LIMIT 500;
""", con)

df.to_pickle("proj6_ex03_detector_146_lag.pkl")

####### ZADANIE 4 ######
df = pd.read_sql("""
SELECT detector_id, count, SUM(count) OVER (PARTITION BY detector_id ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) AS window_sum
FROM readings
WHERE detector_id = 146
LIMIT 500;
""", con)

df.to_pickle("proj6_ex04_detector_146_sum.pkl")