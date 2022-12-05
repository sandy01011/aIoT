import paho.mqtt.client as mqttClient
import time
import certifi


Connected = False
username = 'master:pyMQTT_test'
secret = '7ZDB3BodOzZvfB0A9q7mdWMTMB37cRrA'
host = '62.171.143.248'
port = 8883
clientID = 'MQTTpub'
assetID = '68V4Vpla9jqklo8bK1rBlk'
attribute = 'publish'
attribute_value = 15


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
clientMQTT.tls_set(certifi.where())
clientMQTT.on_connect = on_connect
clientMQTT.on_publish = on_publish
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

clientMQTT.publish(f"master/{clientID}/writeattributevalue/{attribute}/{assetID}", attribute_value)

clientMQTT.disconnect()
clientMQTT.loop_stop()



