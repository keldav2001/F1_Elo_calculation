import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from delta import configure_spark_with_delta_pip


from config_loader import load_config

def get_spark_session() -> SparkSession:
    """Spark session inicializálása Delta Lake támogatással."""
    print("Spark Session indítása...")
    builder = SparkSession.builder \
        .appName("F1_ELO_Silver_Layer") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.driver.memory", "4g")
    
    return configure_spark_with_delta_pip(builder).getOrCreate()