import json
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.client as mqttClient
from pykafka import KafkaClient
import time
import ssl
from envSmPk import read_env

class smpk(object):

    def __init__(self, env_json, topic):
        self.env_json = env_json
        self.realm = ''
        self.username = ''
        self.secret = ''
        self.host = ''
        self.port = ''
        self.clientID = ''
        self.assetID = ''
        self.topic = topic
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.Connected = False

    def load_env(self):
        self.env = json.loads(self.env_json)
        self.realm = self.env['realm']
        self.username = self.env['username']
        self.secret = self.env['secret']
        self.host = self.env['host']
        self.port = self.env['port']
        self.clientID = self.env['clientID']
        self.assetID = self.env['assetID']

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected to broker")
            global Connected
            Connected = True
        else:
            print("Connection failed")

    def on_message(self, client, userdata, message):
        print('On message client {} type {}'.format(client, type(client)))
        msg_payload = message.payload
        print("Received MQTT message type: ", type(msg_payload))
        kafka_producer.produce(str(msg_payload).encode('ascii'))
        print("MQTT-KAFKA-BKR: Just published data type {} to topic{}:".format(type(msg_payload), topic))
        
    def smpk_proxy(self):
        print('inside for topic loop with topic:', topic)
        kafka_client = KafkaClient(hosts="localhost:9092")
        kafka_clientID = self.clientID + '.' + self.topic
        mqtt_clientID = self.clientID + '_' + self.topic
        kafka_topic = self.realm + '.' + self.assetID + '.' + kafka_clientID
        kafka_topic = kafka_client.topics[kafka_topic]
        kafka_producer = kafka_topic.get_sync_producer()
        clientMQTT = mqttClient.Client(mqtt_clientID)
        clientMQTT.username_pw_set(self.username, password=self.secret)
        clientMQTT.tls_set_context(self.context)
        clientMQTT.on_connect = smpk.on_connect
    # clientMQTT.on_publish = on_publish
        clientMQTT.on_message = smpk.on_message
        clientMQTT.connect(self.host, port=self.port)
        clientMQTT.loop_start()
        try:
            clientMQTT.subscribe(f'{self.realm}/{mqtt_clientID}/attribute/{self.topic}/{self.assetID}')
        except:
            print('failed to sbscribe')


        while Connected != True:
            time.sleep(0.1)


        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting")
            clientMQTT.disconnect()
            clientMQTT.loop_stop()


if __name__ == '__main__':
    topic = sys.argv[1]
    test = smpk(read_env(), topic)
    test.smpk_proxy