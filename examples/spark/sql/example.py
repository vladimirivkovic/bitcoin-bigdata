from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)


conf = SparkConf().setAppName("coin-sql").setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

quiet_logs(spark)

from pyspark.sql.types import *
from pyspark.sql.functions import *

schemaFields = [('tx_id', LongType()), ('tx_hash', StringType()), \
                ('timestamp', StringType()), ('type', StringType()), \
                ('address', StringType()), ('value', LongType())]
fields = [StructField(field[0], field[1], True) for field in schemaFields]
schema = StructType(fields)

df = spark.read.csv("hdfs://namenode:8020/user/root/bitcoin/csv/pending.csv",
                    header=True, mode="DROPMALFORMED", schema=schema)
df = df.withColumn("value", df["value"].cast(DoubleType()) * 1e-8)

# address and total output value
df.filter(df['type'] == 'output').groupBy('address').sum('value').show()

# address and tx number
w = df.groupBy('address').agg(count('tx_id').alias('cnt'))
w.orderBy(w["cnt"], ascending=False).show()

# address and avg value
q = df.groupBy('address').agg(avg('value').alias('avg_value'))
q.filter(q["avg_value"] > 1000).show()

# total input and output
df.groupBy('type').sum('value').show()
