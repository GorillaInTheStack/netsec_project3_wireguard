from ast import arg
from urllib import request
import re
import os
import subprocess
from os.path import exists


if(not exists("/home/vagrant/args")):
    exit(1)
args_file = open('/home/vagrant/args', 'r')
args = args_file.readlines()
if(len(args) < 3):
    exit(1)
tunnelIP = args[0].strip()
listenPort = args[1].strip()
clientSite = args[2].strip()


f = open("/home/vagrant/deviceID")
deviceID = f.readline().rstrip()
proc = subprocess.Popen("sudo cat /etc/wireguard/privatekey", shell=True,stdout=subprocess.PIPE)
privatekey = proc.stdout.read().decode("ascii").strip()

interface = "[Interface]\nPrivateKey = "+privatekey  + "\nAddress = "+tunnelIP + "\nListenPort = "+str(listenPort)+"\n\n"


# request conf file    
f = open("/home/vagrant/deviceToken")
deviceToken = f.readline().rstrip()
req = request.Request("http://meshmash.vikaa.fi:49341/overlays/"+clientSite+"/devices/"+deviceID +"/wgconfig"
, headers={'Content-Type': 'application/json','Authorization': 'Bearer '+deviceToken})
response = request.urlopen(req)
res = response.read().decode("utf-8")
# fix data to match conf structure
wgconf = res.replace(": ", ":")
wgconf = re.sub('\\[Peer \d+\\]', '[Peer]', wgconf)
f = open("wg0.conf", "w")
f.write(interface + wgconf)
f.close()
os.system("sudo mv wg0.conf /etc/wireguard/wg0.conf") # no address in interface, manually configure address ifconfig
# os.system("sudo wg syncconf wg0 /etc/wireguard/wg0.conf")
# os.system("sudo wg syncconf wg0 <(wg-quick strip wg0)")
# os.system("sudo systemctl restart wg-quick@wg0")

#restart wireguard
os.system("sudo wg-quick down wg0")
os.system("sudo wg-quick up wg0")