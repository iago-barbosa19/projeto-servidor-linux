interface_atual = "enp0s3"
interface_teste = {"ipv4": "192.168.1.101", "sub_net_mask": "255.255.255.0", "network": "192.168.1.0",
             "gateway": "192.168.1.1", "dns1": "192.168.1.100", "dns2": "8.8.8.8"}
interfaces_configuradas = None
with open(r'C:\Users\Fadami\Projeto_ServerLinux\projeto-servidor-linux\Protótipos\teste\interfaces', 'r') as interfaces:
    interfaces_configuradas = interfaces.read().split('#PSC-CONFIG')[1]
configs = []
if "#interface configurada" in interfaces_configuradas:
    configs = tuple(interface for interface in tuple(interfaces_configuradas.split("#interface configurada")) if not interface_atual in interface)
with open('interfaces', 'w') as interfaces:
    interfaces.write('source /etc/network/interfaces.d/*\n'\
                    '\nauto lo\niface lo inet loopback\n#PSC-CONFIG\n\n')
    interfaces.write(f"#interface configurada\nauto {interface_atual}\niface {interface_atual} inet static\n"\
                     f"address {interface_teste['ipv4']}\nnetmask {interface_teste['sub_net_mask']}\n"\
                     f"network {interface_teste['network']}\ngateway {interface_teste['gateway']}\n"\
                     f"dns-server {interface_teste['dns1']} {interface_teste['dns2']}\n")
    for x in configs:
        if not x.replace("\n", "").strip() == "":
            interfaces.write("\n#interface configurada"+x)        
    interfaces.write("\n")
    print(configs)