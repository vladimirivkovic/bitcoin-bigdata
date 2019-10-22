#!/bin/sh
docker cp . spark-master:/examples
docker exec -it spark-master bash -c "PYSPARK_PYTHON=python3 /spark/bin/spark-submit /examples/example.py"