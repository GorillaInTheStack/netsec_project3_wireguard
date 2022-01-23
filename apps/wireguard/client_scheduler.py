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

if(len(sys.argv) != 4): # expects privatekey tunnelip and port
    print("missing arguments client")
    print(sys.argv)
    exit(1)

tunnelIP = sys.argv[1]
listenPort = sys.argv[2]
clientSite = sys.argv[3]


f = open("deviceID")
deviceID = f.readline().rstrip()
proc = subprocess.Popen("sudo cat /etc/wireguard/privatekey", shell=True,stdout=subprocess.PIPE)
privatekey = proc.stdout.read().decode("ascii").strip()

interface = "[Interface]\nPrivateKey = "+privatekey +"\nAddress = "+tunnelIP+ "\nListenPort = "+str(listenPort)+"\n\n"

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
    print(interface + wgconf)
    f.write(interface + wgconf)
    f.close()
    os.system("sudo mv wg0.conf /etc/wireguard/wg0.conf") # no address in interface, manually configure address ifconfig
    # os.system("sudo wg syncconf wg0 /etc/wireguard/wg0.conf")
    # os.system("sudo systemctl restart wg-quick@wg0")
    os.system("sudo wg-quick down wg0")
    # proc,err = subprocess.Popen("sudo wg-quick down wg0", shell=True,stdout=subprocess.PIPE)
    # out = proc.stdout.read().decode("ascii").strip()
    # f = open("down", "a")
    # f.write(out +"errrooor" + err.read().decode("ascii").strip() )
    # f.close()
    os.system("sudo wg-quick up wg0")
    # proc,err = subprocess.Popen("sudo wg-quick up wg0", shell=True,stdout=subprocess.PIPE)
    # out = proc.stdout.read().decode("ascii").strip()
    # f = open("up", "a")
    # f.write(out +"errrooor" + err.read().decode("ascii").strip() )
    # f.close()




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