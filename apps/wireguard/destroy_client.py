
from urllib import request
from os.path import exists
import sys


if(len(sys.argv) != 2): # expects api key
    print("missing arguments")
    exit(1)

# delete registered device
if(exists("/home/vagrant/wireguard/deviceID")):
    f = open("/home/vagrant/wireguard/deviceID")
    device = f.readline().rstrip()
    req = request.Request("http://meshmash.vikaa.fi:49341/devices/"+device, headers={'Content-Type': 'application/json','x-api-key': sys.argv[1]}, method="DELETE")
    response = request.urlopen(req)
    print(response.read())