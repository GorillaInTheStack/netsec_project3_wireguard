#!/usr/bin/env bash

## Traffic going to the internet
route add default gw 172.30.30.1

## NAT
#iptables --in-interface enp0s8 --append PREROUTING --table nat --protocol tcp --source 172.16.16.16 --destination 172.30.30.30 --jump DNAT --to-destination 10.0.0.2:8080

#iptables --in-interface enp0s8 --append PREROUTING --table nat --protocol tcp --source 172.18.18.18 --destination 172.30.30.30 --jump DNAT --to-destination 10.0.0.3:8080

iptables -t nat -A PREROUTING -p udp -i enp0s8 --source 172.16.16.16 --dport 52345 -j DNAT --to-destination 10.0.0.2:52345

# No need for this, masquerade already does this.
#iptables --append POSTROUTING --table nat --protocol tcp --destination 172.16.16.16 --jump SNAT --to-source 172.30.30.30

iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE

#iptables -t nat -I POSTROUTING -m policy --dir out --pol ipsec -j ACCEPT

## Firewall rules
#iptables -A INPUT ! -s 10.0.0.0/24 -d 10.0.0.1 -j REJECT # Drop everything going to gateway-s that is coming from the private network.


## Save the iptables rules
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6

