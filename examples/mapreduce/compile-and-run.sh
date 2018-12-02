DIR=/bitcoin

printf "\nINSTALLING PYTHON\n"

# apt update && apt install python -y

cd $DIR

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/share/hadoop/tools/lib/hadoop-streaming-$HADOOP_VERSION.jar \
    -input /user/root/bitcoin/json/ \
    -output /user/root/bitcoin_mr \
    -mapper $DIR/mapper.py \
    -reducer $DIR/reducer.py

printf "\nRESULTS\n"

$HADOOP_PREFIX/bin/hdfs dfs -cat /user/root/bitcoin_mr/*