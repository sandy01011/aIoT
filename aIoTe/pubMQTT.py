import os
import json
import paho.mqtt.client as mqttClient
import time
import ssl
from env.env_pi_client_MQTT import read_env

Connected = False

class pipub(object):

    def __init__(self,topic, topic_value):
        self.env_json = read_env()
        self.realm = ''
        self.username = ''
        self.secret = ''
        self.host = ''
        self.port = 0
        self.clientID = ''
        self.assetID = ''
        self.topic = topic
        self.topic_value = topic_value
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        Connected = False

    def load_env(self):
        #self.env = json.loads(self.env_json)
        self.env = self.env_json
        self.realm = self.env['realm']
        self.username = self.env['username']
        self.secret = self.env['secret']
        self.host = self.env['host']
        self.port = self.env['port']
        self.clientID = self.env['clientID']
        self.assetID = self.env['assetID']
        print('env loaded:', self.host, self.port, self.realm,self.username, self.clientID, self.assetID)

    
    def on_publish(client, userdata, result):
        print("Data published \n")
        pass
    
    
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected to broker")
            global Connected
            Connected = True
        else:
            print("Connection failed")

    
    def pubMQTT(self):
        clientMQTT = mqttClient.Client(self.clientID)
        clientMQTT.username_pw_set(self.username, password=self.secret)
        clientMQTT.tls_set_context(self.context)
        clientMQTT.on_connect = pipub.on_connect
        clientMQTT.on_publish = pipub.on_publish
        clientMQTT.connect(self.host, port=self.port)
        clientMQTT.loop_start()

        while Connected != True:
            time.sleep(0.1)

        clientMQTT.publish(f'{self.realm}/{self.clientID}/writeattributevalue/{self.topic}/{self.assetID}', self.topic_value)
        clientMQTT.disconnect()
        clientMQTT.loop_stop()
        