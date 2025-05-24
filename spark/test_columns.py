from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Test").getOrCreate()

df = spark.read.csv("/app/data/processed/merged_data.csv", header=True, inferSchema=True)

print("🧪 Spalten im DataFrame:")
print(df.columns)

print("📊 Werte für 'country' und 'year':")
df.select("country", "year").show(10)

print("🔎 Anzahl der Zeilen ab Jahr 1970:")
print(df.filter(df["year"] >= 1970).count())

spark.stop()
