import io
import picamera
import cv2
import numpy

import paho.mqtt.publish as publish
from time import sleep
import paho.mqtt.client as mqttClient
from envMQTT import read_env
import ssl
import time
import json
import base64
import os
import datetime
import traceback
import math
import random, string
from time import gmtime, strftime


# create mqtt env
env = read_env()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
Connected = False
realm = env['realm']
username = env['username']
secret = env['secret']
host = env['host']
port = env['port']
clientID = env['clientID'] +'_' + env['topic']
assetID = env['assetID']
topic = env['topic']
topic_value = ''

def publish_image(img):
    #img = take_pic()
    #img = img_name
    data = {"type":"piCAM"}
    with open(img, mode='rb') as file:
        imgx = file.read()
    data['imgx'] = base64.b64encode(imgx).decode("utf-8")
    print('data published', type(data))
    return json.dumps(data)

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


# while Connected != True:
#     time.sleep(0.1)



#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')

while True:
    print('Inside while main loop')

    #Convert the picture into a numpy array
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    #Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print("Found "+str(len(faces))+" face(s)")

    #Draw a rectangle around every found face
    # for (x,y,w,h) in faces:
        # cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    if len(faces) > 0:
        # Create unique image name
        img_name = 'pi_image_{0}_{1}.jpg'.format('test',strftime("%Y%m%d%H%M%S",gmtime()))
        #Save the result image
        cv2.imwrite(img_name,image)
        clientMQTT.loop_start()
        clientMQTT.publish(f'{realm}/{clientID}/writeattributevalue/{topic}/{assetID}', payload=publish_image(img_name), qos=1, retain=False)
        clientMQTT.disconnect()
        clientMQTT.loop_stop()
    else:
        pass

