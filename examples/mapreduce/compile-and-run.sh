#!/bin/bash
DIR=/bitcoin

printf "\nINSTALLING PYTHON\n"

# apt update && apt install python -y

hdfs dfs -rm -r -f /user/root/bitcoin_mr/

cd $DIR

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /user/root/bitcoin/csv/ \
    -output /user/root/bitcoin_mr \
    -mapper mapper.py \
    -reducer reducer.py \
    -file mapper.py \
    -file reducer.py
    

printf "\nRESULTS\n"

hdfs dfs -cat /user/root/bitcoin_mr/*