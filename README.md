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
$ export HADOOP_VERSION=2.0.0-hadoop3.1.2-java8
$ docker-compose -f docker-compose-hadoop.yml up
```
or
```sh
$ export HADOOP_VERSION=2.0.0-hadoop3.1.2-java8
$ export SPARK_VERSION=2.4.0-hadoop3.1
$ docker-compose -f docker-compose-spark.yml up
```