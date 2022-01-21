# handling refresh token and wg0.conf
import sys
import os
from timeloop import Timeloop
from datetime import timedelta
from urllib import request
import json
import re
import subprocess
tl = Timeloop()

#device id, token, tunnel ip, 

if(len(sys.argv) != 5): # expects privatekey tunnelip and port
    print("missing arguments client")
    print(sys.argv)
    exit(1)

privatekey = sys.argv[1]
tunnelIP = sys.argv[2]
listenPort = sys.argv[3]
clientSite = sys.argv[4]


f = open("deviceID")
deviceID = f.readline().rstrip()

interface = "[Interface]\nPrivateKey = "+privatekey + "\nListenPort = "+str(listenPort)+"\n\n"

# os.system("sudo systemctl start wg-quick@wg0")
# os.system("ifconfig wg0 "+tunnelIP)
# proc = subprocess.Popen("sudo systemctl start wg-quick@wg0", shell=True,stdout=subprocess.PIPE)
# out = proc.stdout.read().decode("ascii").strip()
# f = open("test", "w")
# f.write(out)
# f.close()

@tl.job(interval=timedelta(seconds=20))
def generate_conf():
    f = open("deviceToken")
    deviceToken = f.readline().rstrip()
    req = request.Request("http://meshmash.vikaa.fi:49341/overlays/"+clientSite+"/devices/"+deviceID +"/wgconfig"
    , headers={'Content-Type': 'application/json','Authorization': 'Bearer '+deviceToken})
    response = request.urlopen(req)
    res = response.read().decode("utf-8")
    wgconf = res.replace(": ", ":")
    wgconf = re.sub('\\[Peer \d+\\]', '[Peer]', wgconf)
    f = open("wg0.conf", "w")
    f.write(interface + wgconf)
    f.close()
    os.system("sudo mv wg0.conf /etc/wireguard/wg0.conf") # no address in interface, manually configure address ifconfig
    os.system("sudo wg syncconf wg0 /etc/wireguard/wg0.conf")
    # os.system("sudo systemctl restart wg-quick@wg0")
    # os.system("wg-quick down wg0")
    # os.system("wg-quick up wg0")




@tl.job(interval=timedelta(seconds=900)) #900s
def refresh_token():
    f = open("deviceToken")
    deviceToken = f.readline().rstrip()
    req = request.Request("http://meshmash.vikaa.fi:49341/devices/"+deviceID+"/token"
    , headers={'Content-Type': 'application/json','Authorization': 'Bearer '+deviceToken})
    response = request.urlopen(req)
    newToken = json.loads(response.read())['token']
    f = open("deviceToken", "w")
    f.write(newToken)
    f.close()


tl.start(block=True)