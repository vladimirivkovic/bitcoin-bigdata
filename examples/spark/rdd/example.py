from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("coin-count").setMaster("local")
sc = SparkContext(conf=conf)

def addr_and_value(line):
    words = line.split(",")
    return (words[4], long(words[5]) if words[3] == 'output' else -long(words[5]))

text_file = sc.textFile("hdfs://namenode:8020/user/root/bitcoin/csv/pending.csv")
counts = text_file.map(lambda line: addr_and_value(line)).reduceByKey(lambda a, b: long(a) + long(b))

print(counts.filter(lambda r: r[1] > 1e10).collect())
print(counts.filter(lambda r: r[1] < -1e10).collect())