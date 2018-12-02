from kafka import KafkaProducer
import kafka.errors
import json
import websocket
import os
import time
try:
    import thread
except ImportError:
    import _thread as thread
import time

WS_SERVER = 'wss://ws.blockchain.info/inv' # 'wss://mainnet.infura.io/_ws'
SUB_MSG = '{"op":"unconfirmed_sub"}' # '{"id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions", {}]}'
TOPIC = 'bitcoin'

while True:
    try:
        producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_HOST'])
        print("Connected to Kafka!")
        break
    except kafka.errors.NoBrokersAvailable as e:
        print(e)
        time.sleep(3)

def on_message(ws, message):
    tx = json.loads(message)
    producer.send(TOPIC, value=json.dumps(tx[u'x']), key=str(tx[u'x'][u'hash']))
    # print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        ws.send(SUB_MSG)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WS_SERVER,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
