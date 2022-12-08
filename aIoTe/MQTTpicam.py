import picamera
import os
import json
import paho.mqtt.client as mqttClient
import time
import ssl
import numpy as np
from geopy.geocoders import Nominatim
from envMQTT import read_env

# geo location json
def geo_json(address='Sector 75, Noida'):
    loc = Nominatim(user_agent=os.uname()[1])
    getLoc = loc.geocode(address)
    return json.dumps({'lat':getLoc.latitude, 'long':getLoc.longitude})

#convert array in float
def myconverter(o):
    if isinstance(o, np.uint8):
        return float(o)


def picarray():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 24
        time.sleep(2)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        # convert camera capture to numpy array
        cap_array = json.dumps(output, default=myconverter)
    return cap_array

env = read_env()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
Connected = False
username = env['username']
secret = env['secret']
host = env['host']
port = env['port']
clientID = env['clientID']
assetID = env['assetID']
cam_attribute = env['cam_attribute']
cam_attribute_value = picarray()
geo_attribute = env['geo_attribute']
geo_attribute_value = geo_json()


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

clientMQTT.publish(f'picamtest/{clientID}/writeattributevalue/{cam_attribute}/{assetID}', cam_attribute_value)
clientMQTT.publish(f'picamtest/{clientID}/writeattributevalue/{geo_attribute}/{assetID}', geo_attribute_value)

clientMQTT.disconnect()
clientMQTT.loop_stop()