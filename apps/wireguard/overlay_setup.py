from urllib import request
import json
# Post Method is invoked if data != None
def sendRequest(data):
    # Dict to Json
    data = json.dumps(data)
    # Convert to String
    data = str(data)
    # Convert string to byte
    data = data.encode('utf-8')
    req =  request.Request("http://meshmash.vikaa.fi:49341/overlays", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('x-api-key', 'c94B0EE671eC0f5BC637a9FCC3eD5A99')
    # Response
    resp = request.urlopen(req)
    print (resp.read())


# creates the overlays
sendRequest({"overlay_name": "siteA"})
sendRequest({"overlay_name": "siteB"})
# sendRequest({"overlay_name": "server1"})
# sendRequest({"overlay_name": "server2"})
