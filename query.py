from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("token")

# You can generate a Token from the "Tokens Tab" in the UI
org = "org"
bucket = "example"

client = InfluxDBClient(url="http://localhost:8086", token=token)
print("starting query")
query = f'from(bucket: "example") |> range(start: -1h) |> filter(fn: (r) => r["cpus"] == "2") |> filter(fn: (r) => r["_field"] == "gauge" or r["_field"] == "counter") |> yield(name: "mean")'
tables = client.query_api().query(query, org=org)

for table in tables:
    for record in table.records:
        print(record)
