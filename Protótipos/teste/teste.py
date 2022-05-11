interfaces_configuradas = None
with open(r'C:\Users\Fadami\Projeto_ServerLinux\projeto-servidor-linux\Protótipos\teste\interfaces', 'r') as interfaces:
    interfaces_configuradas = interfaces.read().split('#PSC-CONFIG')[1]
with open('interfaces', 'w') as interfaces:
    interfaces.write('source /etc/network/interfaces.d/*\n'\
                    f'\nauto lo\niface lo inet loopback\n\n')
    configs = []
    if "#interface configurada" in interfaces_configuradas:
        configs.extend(list(interfaces_configuradas.split("#interface configurada")))
    print(configs)
    