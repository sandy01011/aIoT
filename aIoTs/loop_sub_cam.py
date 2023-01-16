#import paho.mqtt.client as mqtt
import subprocess
import paho.mqtt.client as mqttClient
import time
import ssl
from envMQTT import read_env
import PIL.Image as Image
import io
import base64
import json
from time import gmtime, strftime

#from byte_array import byte_data

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

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe(topic)
#     # The callback for when a PUBLISH message is received from the server.

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    imgx = json.loads(msg.payload)['attributeState']['value']['imgx']
    img = base64.b64decode(imgx)
    img_name = 'pi_image_{0}_{1}.jpg'.format('test',strftime("%Y%m%d%H%M%S",gmtime()))
    # Create a file with write byte permission
    f = open(img_name, "wb")
    f.write(img)
    f.close()
    print('Image captured')
    #print("Image Received", json.loads(msg.payload)['attributeState']['value']['imgx'])
    #
    #openimg = subprocess.call(["open", "output.jpg"])
    #image = Image.open(io.BytesIO(msg.payload))
    #image.save('output.jpg')

clientMQTT = mqttClient.Client(clientID)
clientMQTT.username_pw_set(username, password=secret)
clientMQTT.tls_set_context(context)
clientMQTT.on_connect = on_connect
clientMQTT.on_message = on_message
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

clientMQTT.subscribe(f'{realm}/{clientID}/attribute/{topic}/{assetID}')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('quiting')
    clientMQTT.disconnect()
    clientMQTT.loop_stop()
#clientMQTT.disconnect()
#clientMQTT.loop_stop()

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(ip_address, 1883, 60)

# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# client.loop_forever()
