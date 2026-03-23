import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import round, avg, max, min, sum, count
from delta import configure_spark_with_delta_pip

JARS = os.path.expanduser("~/de-journey/stock-platform/jars/postgresql-42.7.3.jar")

builder = SparkSession.builder \
    .appName("StockBatchJob") \
    .config("spark.jars", JARS) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

BASE = os.path.expanduser("~/de-journey/stock-platform/lakehouse")
BRONZE = f"{BASE}/bronze"
SILVER = f"{BASE}/silver"
GOLD   = f"{BASE}/gold"

# Read from PostgreSQL
DB_URL = "jdbc:postgresql://localhost:5433/stocks"
DB_PROPS = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

print("=== Reading from PostgreSQL ===")
df = spark.read.jdbc(DB_URL, "stock_prices", properties=DB_PROPS)
df.show(5)

print("=== Writing Bronze Layer ===")
df.write.format("delta").mode("overwrite").save(BRONZE)

print("=== Writing Silver Layer ===")
silver = df.withColumn("price", round(df["price"], 2))
silver.write.format("delta").mode("overwrite").save(SILVER)

print("=== Writing Gold Layer ===")
gold = df.groupBy("symbol").agg(
    round(avg("price"), 2).alias("avg_price"),
    max("price").alias("max_price"),
    min("price").alias("min_price"),
    sum("volume").alias("total_volume"),
    count("*").alias("total_records")
).orderBy("symbol")

gold.write.format("delta").mode("overwrite").save(GOLD)
gold.show()

print("=== Batch job complete ===")
spark.stop()