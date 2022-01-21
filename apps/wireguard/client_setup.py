import sys
import subprocess
import os
from urllib import request
import json

if(len(sys.argv) != 4): # expects client name (client-ax / client-bx), api-key, public ip?
    print("missing arguments")
    exit(1)

clientName = sys.argv[1]
apikey = sys.argv[2]
publicIP = sys.argv[3]

#todo get token, tunnel ip 

# setting up wireguard key
os.system("sudo rm -rf  /etc/wireguard/privatekey")
os.system("sudo rm -rf  /etc/wireguard/publickey")
os.system("wg genkey | sudo tee -a /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey")
proc = subprocess.Popen("sudo cat /etc/wireguard/publickey", shell=True,stdout=subprocess.PIPE)
publickey = proc.stdout.read().decode("ascii").strip()
proc = subprocess.Popen("sudo cat /etc/wireguard/privatekey", shell=True,stdout=subprocess.PIPE)
privatekey = proc.stdout.read().decode("ascii").strip()
listenPort = 52345

# Post Method is invoked if data != None
def sendRequest(url, data):
    # Dict to Json
    data = json.dumps(data)
    # Convert to String
    data = str(data)
    # Convert string to byte
    data = data.encode('utf-8')
    req =  request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('x-api-key', apikey)
    # Response
    resp = request.urlopen(req)
    return (json.loads(resp.read()))


data = {"hostname": clientName+".example.com",
        "public_ip": publicIP,
        "public_key":publickey,
        "listen_port":listenPort,
        "device_name": clientName}

# extract device id and token
response = sendRequest("http://meshmash.vikaa.fi:49341/devices", data)
deviceID = response["device_id"] 
deviceToken = response['token']

# saving id and token to be used in other scripts easily
f = open("deviceID", "w")
f.write(deviceID)
f.close()
f = open("deviceToken", "w")
f.write(deviceToken)
f.close()

# find id of overlay
req = request.Request("http://meshmash.vikaa.fi:49341/overlays", headers={'Content-Type': 'application/json','x-api-key': apikey})
response = request.urlopen(req)
overlays = json.loads(response.read())['overlays']
clientSite = ""
# serverOverlay = ""
for overlayID in overlays:
    req = request.Request("http://meshmash.vikaa.fi:49341/overlays/"+overlayID
    , headers={'Content-Type': 'application/json','x-api-key': apikey})
    response = request.urlopen(req)
    current_overlay = json.loads(response.read())['overlay_name']
    if(('client-a' in clientName or "server-s1" in clientName) and current_overlay == 'siteA'):
        clientSite = overlayID
    elif(('client-b' in clientName or "server-s2" in clientName) and current_overlay == 'siteB'):
        clientSite = overlayID
    # if('client-a' in clientName and current_overlay == 'server1'):
    #     serverOverlay = overlayID
    # elif('client-b' in clientName and current_overlay == 'server2'):
    #     serverOverlay = overlayID

if(clientSite == ""):
    print("no overlay detected for this device")
    exit(1)

# subscribe device to overlay
response = sendRequest("http://meshmash.vikaa.fi:49341/overlays/"+clientSite+"/devices", {"device_id": deviceID})
tunnelIP = response["tunnel_ip"]

os.system("sudo apt-get -y install python3-pip &&  pip3 install timeloop")
interface = "[Interface]\nPrivateKey = "+privatekey + "\nListenPort = "+str(listenPort)+"\n\n"
f = open("wg0.conf", "w")
f.write(interface)
f.close()
os.system("sudo mv wg0.conf /etc/wireguard/wg0.conf")
os.system("sudo systemctl start wg-quick@wg0")
os.system("sudo ifconfig wg0 "+tunnelIP)
args = privatekey.strip()+" "+ tunnelIP +" "+str(listenPort) +" "+clientSite
os.system("nohup python3 /home/vagrant/wireguard/client_scheduler.py "+ args +" &")
print("wohooo")




