import paho.mqtt.client as mqttClient
import time
import certifi
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
Connected = False
username = 'sandeep:gateway-60ssyvgytmzt5u47z7oj1f'
secret = '390953f2-6884-455e-abff-55ed8c15c90b'
host = '62.171.143.248'
port = 8883
clientID = 'MQTT_1403'
assetID = '60SsyVGyTmzt5u47Z7Oj1F'
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
#clientMQTT.tls_set(certifi.where(),tls_version=2)
clientMQTT.tls_set_context(context)
clientMQTT.on_connect = on_connect
clientMQTT.on_publish = on_publish
clientMQTT.connect(host, port=port)
clientMQTT.loop_start()

while Connected != True:
    time.sleep(0.1)

clientMQTT.publish(f'sandeep/{clientID}/writeattributevalue/{attribute}/{assetID}', attribute_value)

clientMQTT.disconnect()
clientMQTT.loop_stop()



