import paho.mqtt.client as mqttClient
import time
import json
import ssl

'''
global variables
'''

connected = False  # Stores the connection status
BROKER_ENDPOINT = "10.9.21.190"
TLS_PORT = 8883  # Secure port
MQTT_USERNAME = "mqtt001"  # Put here your Ubidots TOKEN
MQTT_PASSWORD = "7424c3f6-12d6-431c-985a-e847f97e753b"  # Leave this in blank
TOPIC = "attribute/72XvPO0vl9FWnZKWJuEgIe/textoatributo"
DEVICE_LABEL = "sandyDummy"
#TLS_CERT_PATH = "localhost.crt"  # Put here the path of your TLS cert
TLS_CERT_PATH = "localhost.pem"  # Put here the path of your TLS cert

'''
Functions to process incoming and outgoing streaming
'''

def on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    if rc == 0:

        print("[INFO] Connected to broker")
        connected = True  # Signal connection
    else:
        print("[INFO] Error, connection failed")


def on_publish(client, userdata, result):
    print("Published!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not mqtt_client.is_connected():
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
#        mqtt_client.tls_set(ca_certs=TLS_CERT_PATH)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.tls_set(ca_certs=TLS_CERT_PATH, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        mqtt_client.tls_insecure_set(False)
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:  # Wait for connection
            print(connected)
            print("Attempting to connect...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    return True


def publish(mqtt_client, topic, payload):

    try:
        mqtt_client.publish(topic, payload)

    except Exception as e:
        print("[ERROR] Could not publish data, error: {}".format(e))


def main(mqtt_client):
    payload = json.dumps({"tls_publish_test": 20})
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)

    

    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT):
        return False

    publish(mqtt_client, topic, payload)

    return True


if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    while True:
        main(mqtt_client)
        time.sleep(10)
