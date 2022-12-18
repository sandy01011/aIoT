import json
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.client as mqttClient
from pykafka import KafkaClient
import time
import ssl
from datetime import datetime as dt
from paho.mqtt.client import connack_string as ack
from env.env_noise_smpk import read_env

Connected = False

class smpk(object):

    def __init__(self, env_json, topic):
        self.env_json = env_json
        self.realm = ''
        self.username = ''
        self.secret = ''
        self.host = '62.171.143.248'
        self.port = 8883
        self.clientID = ''
        self.assetID = ''
        self.topic = topic
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        Connected = False

    def load_env(self):
        #self.env = json.loads(self.env_json)
        self.env = self.env_json
        print('type {} and data {}'.format(type(self.env), self.env))
        self.realm = self.env['realm']
        self.username = self.env['username']
        self.secret = self.env['secret']
        self.host = self.env['host']
        self.port = self.env['port']
        self.clientID = self.env['clientID']
        self.assetID = self.env['assetID']
        print('env loaded:', self.host, self.port, self.realm,self.username, self.clientID, self.assetID)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected to broker")
            global Connected
            Connected = True
        else:
            print("Connection failed")

    def on_message(client, userdata, message):
        #print('On message client {} type {}'.format(client, type(client)))
        #msg_payload = message.payload
        print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
                + message.topic + "' with QoS " + str(message.qos))
        msg_payload = json.loads(message.payload.decode('utf-8'))
        id = msg_payload['attributeState']['ref']['id']
        att_name = msg_payload['attributeState']['ref']['name']
        att_value = msg_payload['attributeState']['value']
        print(id,att_name,att_value)
        #msg_payload = str(message.payload)
        print("Received MQTT message type: ", type(msg_payload))
        kafka_client = KafkaClient(hosts="localhost:9092")
        kafka_topic = message.topic.replace('/','.')
        kafka_topic = kafka_client.topics[kafka_topic]
        kafka_producer = kafka_topic.get_sync_producer()
        kafka_producer.produce(str(msg_payload).encode('ascii'))
        print("MQTT-KAFKA-Proxy: Just published data type {} to topic{}:".format(type(msg_payload), kafka_topic))

    def smpk_proxy(self):
        print('smpk proxy topic:', self.topic)
        print('clientID',self.clientID)
        #kafka_client = KafkaClient(hosts="localhost:9092")
        #kafka_clientID = self.clientID + '.' + self.topic
        mqtt_clientID = self.clientID + '_' + self.topic
        #print('kafka,mqtt clientID', kafka_clientID, mqtt_clientID)
        #kafka_topic = self.realm + '.' + self.assetID + '.' + kafka_clientID
        #kafka_topic = kafka_client.topics[kafka_topic]
        #kafka_producer = kafka_topic.get_sync_producer()
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


#if __name__ == '__main__':
#    #topic = sys.argv[1]
#    test = smpk(read_env(), 'picputemp')
#    test.smpk_proxy
