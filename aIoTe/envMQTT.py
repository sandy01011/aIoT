# return required MQTT values
import os

realm = 'aiote'
username = 'aiote:pi32_ser'
secret = 'hPdjI8FaxD3nc3J7lO0eXAs7ilJ7vCXY'
host = '62.171.143.248'
port = 8883
clientID = os.uname()[1]
assetID = '3fPa6ElyB4vPdoLIXut58q'
#cam_attribute = 'rpicampublish'
#geo_attribute = 'location' # geo cordinates

def read_env():
    return {'realm':realm, 'username':username, 'secret':secret, 'host':host, 'port':port, 'clientID':clientID,
             'assetID':assetID}

