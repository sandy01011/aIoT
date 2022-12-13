# create bridge between MQTT and Kafka broker
import paho.mqtt.client as mqtt
import paho.mqtt.client as mqttClient
from pykafka import KafkaClient
import time
import ssl
import json
from envMQTT import read_env



env = read_env()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
Connected = False
realm = env['realm']
username = env['username']
secret = env['secret']
host = env['host']
port = env['port']
clientID = env['clientID']
assetID = env['assetID']
pub_cam = 'pub_cam'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    msg_payload = json.loads(message.payload.decode('utf-8'))
    # id = msg['attributeState']['ref']['id']
    # att_name = msg['attributeState']['ref']['name']
    # att_value = msg['attributeState']['value']
    #msg_payload = str(message.payload)
    print("Received MQTT message type: ", type(msg_payload))
    kafka_producer.produce(msg_payload.encode('ascii'))
    print("KAFKA: Just published " + msg_payload + " to topic pub_cam")

kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics[pub_cam]
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

clientMQTT.subscribe(f'{realm}/{clientID}/attribute/{pub_cam}/{assetID}')

# mqtt_broker = "mqtt.eclipseprojects.io"
# mqtt_client = mqtt.Client("BridgeMQTT2Kafka")
# mqtt_client.connect(mqtt_broker)

# def on_message(client, userdata, message):
#     msg_payload = str(message.payload)
#     print("Received MQTT message: ", msg_payload)
#     kafka_producer.produce(msg_payload.encode('ascii'))
#     print("KAFKA: Just published " + msg_payload + " to topic temperature2")

# mqtt_client.loop_start()
# mqtt_client.subscribe("temperature2")
# mqtt_client.on_message = on_message
# time.sleep(300)
# mqtt_client.loop_end()