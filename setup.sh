#!bin/#!/usr/bin/env bash
echo "enter port: "
read port
echo "what interface do you whant to use: "
read inter
yip=$(ip addr list $inter | grep "  inet " | head -n 1 | cut -d " " -f 6 | cut -d / -f 1)
rip=$(ip route show | grep "$inter" | sed '1d' | cut -d " " -f 1)
{
    echo $port
    echo $yip
} > config.txt
pip install watchdog
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -A POSTROUTING -t nat -s $rip -o $inter -j SNAT --to-source $yip
iptables -A PREROUTING -t nat -i $inter -p tcp --dport $port -j DNAT --to-destination $yip
echo "here you need to write command that you use to open text.txt: "
read command
echo "If you whant to be Server Node you should write 's' else write 'c'"
read flag
if ["$flag" == "s"]; then
    python client2.py
else
    python client.py
fi
$command
