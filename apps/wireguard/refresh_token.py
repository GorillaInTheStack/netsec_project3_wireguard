import json
from urllib import request

f = open("deviceID")
deviceID = f.readline().rstrip()

f = open("deviceToken")
deviceToken = f.readline().rstrip()
req = request.Request("http://meshmash.vikaa.fi:49341/devices/"+deviceID+"/token"
, headers={'Content-Type': 'application/json','Authorization': 'Bearer '+deviceToken})
response = request.urlopen(req)
newToken = json.loads(response.read())['token']
f = open("deviceToken", "w")
f.write(newToken)
f.close()