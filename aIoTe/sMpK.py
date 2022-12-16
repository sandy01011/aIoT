# subscribe topic from MQTT broker and publish it to KAFKA broker

import paho.mqtt.client as mqtt
import paho.mqtt.client as mqttClient
from pykafka import KafkaClient
import time
import ssl
import json
from envMKBpicputemp import read_env



env = read_env()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
Connected = False
realm = env['realm']
username = env['username']
secret = env['secret']
host = env['host']
port = env['port']
clientID = 'subMQTTpubKAFKA' # env['clientID']
assetID = env['assetID']
topic = env['topic']
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print('On message')
    #msg_payload = json.loads(message.payload.decode('utf-8'))
    #msg_payload = json.loads(message.payload)
    msg_payload = message.payload
    # id = msg['attributeState']['ref']['id']
    # att_name = msg['attributeState']['ref']['name']
    # att_value = msg['attributeState']['value']
    #msg_payload = str(message.payload)
    print("Received MQTT message type: ", type(msg_payload))
    #kafka_producer.produce(msg_payload.encode('ascii'))
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    #print("KAFKA: Just published " + msg_payload + " to topic pub_cam")
    print("MQTT-KAFKA-BKR: Just published data type {} to topic{}:".format(type(msg_payload), topic))

k_topic = realm + '.' + clientID + '.' + assetID + '.' + topic

kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics[k_topic]
kafka_producer = kafka_topic.get_sync_producer()

clientMQTT = mqttClient.Client(clientID)
clientMQTT.username_pw_set(username, password=secret)
clientMQTT.tls_set_context(context)
clientMQTT.on_connect = on_connect
# clientMQTT.on_publish = on_publish
clientMQTT.on_message = on_message
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

try:
    #clientMQTT.subscribe(f'{realm}/{clientID}/attribute/{pub_cam}/{assetID}')
    clientMQTT.subscribe(f'{realm}/{clientID}/attribute/{topic}/{assetID}')
except:
    print('failed to sbscribe')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
    clientMQTT.disconnect()
    clientMQTT.loop_stop()
