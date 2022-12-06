import paho.mqtt.client as mqtt
import time
import certifi
import ssl
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to broker')
        global Connected #Use global variable
        Connected = True #Signal connection
    else:
        print('Connection failed')

def on_publish(client, userdata, result):
    print(f'Data published. Data: {attribute_value}')
    pass

def on_message(client, userdata, message):
    msg = json.loads(message.payload.decode('utf-8'))
    id = msg['attributeState']['ref']['id']
    att_name = msg['attributeState']['ref']['name']
    att_value = msg['attributeState']['value']
    print(f'Message received. Asset ID: {id}. Attribute name: {att_name}. Attribute value: {att_value}')

Connected = False
username = 'sandy:pyMQTT_test'
secret = '7ZDB3BodOzZvfB0A9q7mdWMTMB37cRr'
host = '62.171.143.248'
port = 8883
clientID = 'MQTTpub'
assetID = '68V4Vpla9jqklo8bK1rBlk'
attributeWr = 'publish'
attribute_value = 10

attributeRd = 'subscribe'

clientMQTT = mqtt.Client(clientID)
clientMQTT.username_pw_set(username, password = secret)

# the key steps here
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# if you do not want to check the cert hostname, skip it
# context.check_hostname = False
clientMQTT.tls_set_context(context)

clientMQTT.on_connect = on_connect
clientMQTT.on_publish = on_publish
clientMQTT.on_message = on_message
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

while attribute_value <=42 :
    clientMQTT.publish(f'master/{clientID}/writeattributevalue/{attributeWr}/{assetID}', attribute_value)
    clientMQTT.subscribe(f'master/{clientID}/attribute/{attributeRd}/{assetID}')

time.sleep(5)
attribute_value += 1
clientMQTT.disconnect()
clientMQTT.loop_stop()

# the key steps here
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# if you do not want to check the cert hostname, skip it
# context.check_hostname = False

