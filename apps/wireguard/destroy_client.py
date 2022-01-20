
from urllib import request
import os
import sys
# to be run before destroy to delete device
# req = request.Request("http://meshmash.vikaa.fi:49341/devices", headers={'Content-Type': 'application/json','x-api-key': "c94B0EE671eC0f5BC637a9FCC3eD5A99"})
# response = request.urlopen(req)
# devices = json.loads(response.read())['devices']

if(len(sys.argv) != 2): # expects api key
    print("missing arguments")
    exit(1)

f = open("deviceID")
device = f.readline().rstrip()
req = request.Request("http://meshmash.vikaa.fi:49341/devices/"+device, headers={'Content-Type': 'application/json','x-api-key': sys.argv[1]}, method="DELETE")
response = request.urlopen(req)
print(response.read())