import paho.mqtt.client as mqttClient
import time
import certifi


Connected = False
username = 'apex:rapi'
secret = 'KnIrbUc2Rz2wzcWYQWSRPAyEYTuCxPrs'
host = '192.168.0.100'
port = 443
clientID = 'MQTT_TESTpub'
assetID = '42dY3nRzMyL855aDOOrThM'
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

#CERTFI_PATH = certifi.where()
#print(CERTFI_PATH)
#CERTFI_PATH = '/home/maruti/anaconda3/envs/drishti_bhav_1/lib/python3.10/site-packages/certifi/cacert.pem'
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



