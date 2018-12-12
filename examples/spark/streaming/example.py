from __future__ import print_function

import sys
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreamingKafkaBitcoin")

    # Suppress the output logs
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 2)

    directKafkaStream = KafkaUtils.createDirectStream(
        ssc, ["bitcoin"], {"metadata.broker.list": "kafka:9092"})

    ssc.checkpoint("checkpoint")

    def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

    running_counts = directKafkaStream.map(lambda msg: json.loads(msg[1]))\
        .map(lambda tx: (tx["relayed_by"], 1))\
        .updateStateByKey(updateFunc)

    running_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
