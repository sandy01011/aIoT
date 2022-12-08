# return required MQTT values
import os

username = 'picamtest:rpi'
secret = '6fb5tWZJ1okebeS9rFNVWlfN9dNvUxze'
host = '62.171.143.248'
port = 8883
clientID = os.uname()[1]
assetID = '32Yvwv1NbFQgTocQVjkGDv'
attribute = 'rpicampublish'

def read_env():
    return {'username':username, 'secret':secret, 'host':host, 'port':port, 'clientID':clientID,
             'assetID':assetID, 'attribute':attribute}
             
