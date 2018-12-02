# Bitcoin Big Data
## Big Data Architectures Course
### Sample Project
#### About
This is a sample project that should demnstrate Big Data batch and stream processing on Bitcoin transaction data.
The sample project contains the following docker containers:
  - Bitcoin pending transaction listener & Kafka producer
  - Zookeeper & Kafka
  - Kafka consumer & HDFS client
  - HDFS namenode & datanodes
  - YARN master & slaves
  - Spark master & slaves
  - Hue web-based file-browser for HDFS
#### Run using docker-compose
```sh
$ docker-compose -f docker-compose-spark.yml up
```