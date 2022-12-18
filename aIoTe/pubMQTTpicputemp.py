#from gpiozero import CPUTemperature
import os
import json
import paho.mqtt.client as mqttClient
import time
import ssl
from envMQTT import read_env

def picputemp():
    cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
    cpu_temp = cpu_temp.rstrip(cpu_temp[-1])
    cpu_temp = cpu_temp.rstrip(cpu_temp[-1])
    cpu_temp = cpu_temp.rstrip(cpu_temp[-1])
    return cpu_temp



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
topic = env['topic']

cputemp = picputemp()

topic_value = picputemp()
print(topic_value)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_publish(client, userdata, result):
    print("Data published \n")
    pass


clientMQTT = mqttClient.Client(clientID)
clientMQTT.username_pw_set(username, password=secret)
clientMQTT.tls_set_context(context)
clientMQTT.on_connect = on_connect
clientMQTT.on_publish = on_publish
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

clientMQTT.publish(f'{realm}/{clientID}/writeattributevalue/{topic}/{assetID}', topic_value)
#print(pub_cam_v)
clientMQTT.disconnect()
clientMQTT.loop_stop()
