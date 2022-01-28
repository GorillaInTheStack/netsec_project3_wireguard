import json
from urllib import request

f = open("/home/vagrant/wireguard/deviceID")
deviceID = f.readline().rstrip()

f = open("/home/vagrant/wireguard/deviceToken")
deviceToken = f.readline().rstrip()
req = request.Request("http://meshmash.vikaa.fi:49341/devices/"+deviceID+"/token"
, headers={'Content-Type': 'application/json','Authorization': 'Bearer '+deviceToken})
response = request.urlopen(req)
newToken = json.loads(response.read())['token']
f = open("/home/vagrant/wireguard/deviceToken", "w")
f.write(newToken)
f.close()