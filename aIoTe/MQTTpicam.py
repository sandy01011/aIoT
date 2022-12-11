import picamera
import os
import json
from json import JSONEncoder
import paho.mqtt.client as mqttClient
import time
import ssl
import numpy as np
from geopy.geocoders import Nominatim
from envMQTT import read_env

# geo location json
def geo_json(address='Sector 50, Noida'):
    loc = Nominatim(user_agent='GetLoc')
    getLoc = loc.geocode(address)
    json_data = {"type":"Point","coordinates": [getLoc.latitude, getLoc.longitude]}
    return json.dumps(json_data)


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

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
        #numpyData = {"array": output}
        cap_array = json.dumps(output, cls=NumpyArrayEncoder)
        print('cam array', cap_array)
    return cap_array

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
#cam_attribute = env['cam_attribute']
#cam_attribute_value = picarray()
pub_attribute = 'writeAttribute'
sub_attribute = 'subscribeAttribute'
sub_attribute_value = 'true'
pub_attribute_value = 45
pub_const = 'pub_const'
pub_const_v = 45
sub_const = 'sub_const'

#geo_attribute = env['geo_attribute']
#geo_attribute_value = geo_json()
writegps = 'writegps'
writegps_value = geo_json()
print('type of gps data', writegps_value)
writecam = 'writecam'
writecam_value = picarray()
print('type of cam data', writecam_value)


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

def on_message(client, userdata, message):
    msg = json.loads(message.payload.decode('utf-8'))
    id = msg['attributeState']['ref']['id']
    att_name = msg['attributeState']['ref']['name']
    att_value = msg['attributeState']['value']
    print(f'Message received. Asset ID: {id}. Attribute name: {writegps}. Attribute value: {writegps_value}')

clientMQTT = mqttClient.Client(clientID)
clientMQTT.username_pw_set(username, password=secret)
clientMQTT.tls_set_context(context)
clientMQTT.on_connect = on_connect
clientMQTT.on_publish = on_publish
clientMQTT.on_message = on_message
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

clientMQTT.subscribe(f'{realm}/{clientID}/attribute/{sub_attribute}/{assetID}')
clientMQTT.publish(f'{realm}/{clientID}/writeattributevalue/{pub_attribute}/{assetID}', pub_attribute_value)
clientMQTT.publish(f'{realm}/{clientID}/writeattributevalue/{writegps}/{assetID}', writegps_value)
clientMQTT.publish(f'{realm}/{clientID}/writeattributevalue/{writecam}/{assetID}', writecam_value)

clientMQTT.disconnect()
clientMQTT.loop_stop()
