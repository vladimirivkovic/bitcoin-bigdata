from kafka import KafkaConsumer
import kafka.errors
from hdfs import InsecureClient
import requests
import os
import sys
import time
import json

TOPIC = 'bitcoin'
MAX_TRANSACTIONS = 100
BITCOIN_DIR = '/user/root/bitcoin'
PENDING_PATH = '/csv/pending.csv'


def connect_to_hdfs():
    return InsecureClient(os.environ['HDFS_HOST'], user='root')


def upload_to_hdfs(hdfs, content, format):
    filename = BITCOIN_DIR + format[1:] + '/pending_' + \
        str(time.time()).split('.')[0]
    print("writing " + filename + " ...")
    hdfs.write(filename + format, data=content, encoding="utf-8")


def transform(tx):
    rows = []

    tx_hash = tx["hash"]
    time = str(tx["time"])
    tx_index = str(tx["tx_index"])

    for i in tx["inputs"]:
        addr = i["prev_out"]["addr"]
        addr = addr if addr != None else "None"
        value = str(i["prev_out"]["value"])
        rows.append(','.join([tx_index, tx_hash, time, "input", addr, value]))

    for o in tx["out"]:
        addr = o["addr"]
        addr = addr if addr != None else "None"
        value = str(o["value"])
        rows.append(','.join([tx_index, tx_hash, time, "output", addr, value]))

    return '\n'.join(rows)


def handle_msg(transactions, msg):
    transactions.append(json.loads(msg.value))
    if (len(transactions) > MAX_TRANSACTIONS):
        content = "\n".join([transform(tx) for tx in transactions]) + "\n"
        pending_new_path = '/csv/pending_new.csv'
        hdfs.write(BITCOIN_DIR + pending_new_path,
                   data=content, encoding='utf-8')

        concat_path = "{}/webhdfs/v1{}{}?op=CONCAT&sources={}{}".format(
            os.environ['HDFS_HOST'], BITCOIN_DIR, PENDING_PATH, BITCOIN_DIR, pending_new_path)
        r = requests.post(concat_path)
        print(r.status_code, r.reason)

        # upload_to_hdfs(hdfs, json.dumps(transactions), ".json")

        transactions = []


def consume(hdfs, consumer):
    transactions = []

    try:
        hdfs.write(BITCOIN_DIR + PENDING_PATH,
                   data="", encoding="utf-8")
    except:
        pass

    for msg in consumer:
        handle_msg(transactions, msg)


def connect_to_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC, bootstrap_servers=os.environ['KAFKA_HOST'], group_id="hdfs-consumer")
            print("Connected to Kafka!")
            return consumer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(3)


if __name__ == '__main__':
    time.sleep(60)

    hdfs = connect_to_hdfs()
    # hdfs.delete(BITCOIN_DIR, recursive=True)
    try:
        hdfs.makedirs(BITCOIN_DIR)
    except:
        pass

    consumer = connect_to_kafka()
    consume(hdfs, consumer)
