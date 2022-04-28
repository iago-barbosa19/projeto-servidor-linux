import os, json
network_interfaces = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether ce:0b:69:d0:38:e5 brd ff:ff:ff:ff:ff:ff
3: enp0s8: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 42:6f:d7:d5:cb:9c brd ff:ff:ff:ff:ff:ff
4: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:7e:d9:e1 brd ff:ff:ff:ff:ff:ff
    inet 172.27.49.14/20 brd 172.27.63.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fe7e:d9e1/64 scope link
       valid_lft forever preferred_lft forever
5: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/ipip 0.0.0.0 brd 0.0.0.0
6: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
"""
with open("./Protótipos/pythonFiles/appSettings.json", "r") as interfaceNames:
    interfaces = json.load(interfaceNames)['os-interfaces-names']
    for network_interface in interfaces:
        if network_interface in network_interfaces:
            print(network_interface)