from models import Ip, Dhcp, Dns
from logger import Log
from time import sleep
import os
import subprocess
import tqdm
import json


class Software:
    
    def __init__(self):
        if not os.path.exists('/etc/psc/fst'):        
            with open('/etc/psc/fst', 'w') as fst:
                fst.write('This program has been already initialized on this system.')
            os.system(f'cp -r * /etc/psc/')
            os.system('clear')
        self.language = self.idioma()
        self.main()

    def main(self):
        os.system('clear')
        while(True != False):
            print('---------------------------------------------------\n'+ self.language['main-page']['main-menu'])
            opc = int(input(self.language['main-page']['main-menu-input']))
            if opc == 1:
                os.system('clear')
                self.configServicos()
            elif opc == 2:
                os.system('clear')
                self.checkServicos()
            elif opc == 3:
                os.system('clear')
                self.installServices()
            elif opc == 4:
                os.system('clear')
                print(self.language['main-page']['configuration-web-page'])
                opc = input('Y/n  ->')
                if opc.lower() == 'y':
                    self.preparacaoServidor()
            elif opc == 5:
                os.system('clear')
                self.idioma(int(input(self.language['main-page']['languague-change'])))
            else:
                exit()
                
    def configServicos(self: object) -> None:
        log.debug(f'{os.getlogin()} - Entrando na Configuração de Serviços')
        configs = []
        print('---------------------------------------------------'+
            self.language['services-config']['main-menu'])
        opc = int(input(self.language['services-config']['main-menu-input']))
        if opc == 1:
            log.debug(f'{os.getlogin()} - Configurando interface IPV4')
            os.system('clear')
            system_interfaces = []
            interface = subprocess.run(["ip", "addr"], stdout=subprocess.PIPE, universal_newlines=True).stdout
            print(self.language['services-config']['interface']['main-text'])
            with open("appSettings.json", "r") as interface_names:
                interfaces = json.load(interface_names)['os-interfaces-names']
                for network_interface in interfaces:
                    if network_interface in interface:
                        system_interfaces.append(network_interface)
                        print(network_interface+'\n')
                        log.debug(f'{os.getlogin()} - Interface:{network_interface} encontrada. Qtd de Interfaces: {system_interfaces}')
            for x in range((len(system_interfaces))):
                os.system('clear')
                if input(f"{self.language['services-config']['interface']['option-text']} - {system_interfaces[x]}:\nY\\n\n->").lower() == 'y':
                    for dado in ['ipv4', 'gateway', 'subnetMask', 'dns1', 'dns2']:
                        os.system('clear')
                        valor = input(f"{system_interfaces[x]} - {self.language['services-config']['interface']['data-insert']}  - {dado}\nDigite 0 para cancelar:\n->")
                        if valor == 0:
                            print('Operação cancelada.\nAperte Enter para continuar')
                            return input()
                        configs.append(valor)
                    ip_config = Ip(ipv4=configs[0], gateway=configs[1], sub_net_mask=configs[2], dns1=configs[3], dns2=configs[4], 
                                interface=system_interfaces[x], logger=log)
                    ip_config.ipConf()
        elif opc == 2:
            os.system('clear')
            system_interfaces = []
            interface = subprocess.run(["ip", "addr"], stdout=subprocess.PIPE, universal_newlines=True).stdout
            print(self.language['services-config']['dhcp']['main-text'])
            with open("appSettings.json", "r") as interface_names:
                interfaces = json.load(interface_names)['os-interfaces-names']
                for network_interface in interfaces:
                    if network_interface in interface:
                        system_interfaces.append(network_interface)
                        print(network_interface+"\n")
                        log.debug(f'{os.getlogin()} - Interface:{network_interface} encontrada. Qtd de Interfaces: {system_interfaces}')
            for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask', 'Pool Inicial do DHCP', 'Pool Final do DHCP', 'Interface']:
                if dado != 'Interface':
                    valor = input(self.language['services-config']['dhcp']['data-input'] + f' {dado} ->')
                else :
                    for x in range(len(system_interfaces)):
                        print(f'{(x + 1)} - {system_interfaces[x]}')
                    indice = int(input("->"))
                    try:
                        valor = system_interfaces[(indice - 1)]
                    except IndexError:
                        print('Interface inexistente.\nOperação cancelada.\nAperte Enter para continuar')
                        return input()
                        
                if valor == 0:
                    print('Operação cancelada.\nAperte Enter para continuar')
                    return input()
                configs.append(valor)
            dhcp_config = Dhcp(ipv4=configs[0], gateway=configs[1],
                            dns1=configs[2], dns2=configs[3], sub_net_mask=configs[4],
                            dhcp_pool_inicial=configs[5], dhcp_pool_final=configs[6], interface=configs[7], logger=log)
            dhcp_config.dhcpConf()
        elif opc == 3:
            os.system('clear')
            print(self.language['services-config']['dns']['main-text'])
            for dado in ['ipv4', 'subnetMask', 'dominio', 'Nome do servidor']:
                valor = input(self.language['services-config']['dns']['data-input'] + f'{dado} ->')
                if valor == 0:
                    print('Operação cancelada.\nAperte Enter para continuar')
                    input()
                    return
                configs.append(valor)
            dns_config = Dns(ipv4=configs[0], sub_net_mask=configs[1], domain=configs[2], server_name=configs[3], logger=log)
            dns_config.dnsConf()
        print(self.language['services-config']['final'])

    def checkServicos(self: object):
        self.language = self.language['services-config']['service-check']
        print("---------------------------------------------------"+
            self.language['main-text'])
        opc = int(input(self.language['data-input']))
        if opc == 1:
            os.system('systemctl status networking')
        elif opc == 2:
            os.system('systemctl status apache2')
            os.system('systemctl status bind9')
        elif opc == 3:
            os.system('systemctl status isc-dhcp-server')
        sleep(5)
        print(f'echo {self.language["final"]}')

    def installServices(self: object) -> None:
        log.info(f'{os.getlogin()} - Instalação de serviços necessários iniciada.')
        
        self.language = self.language['services-config']['install-services']
        print("---------------------------------------------------"+
            self.language['main-text'])
        opc = int(input(self.language['data-input']))
        if opc == 1:
            with tqdm(total=40) as pbar:
                os.system('apt-get install --assume-yes apache2 &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('apt-get install --assume-yes bind9 &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/apache2/sites-available/ &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/apache2/sites-enabled/ &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/bind &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('mkdir -p /var/www/sites &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /var/www/sites &>')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/bind/named.conf.default-zones &> /dev/null')
                pbar.update(5)
                sleep(0.5)
        elif opc == 2:
            os.system('apt-get install --assume-yes isc-dhcp-server')
            with tqdm(total=15) as pbar:
                with open('/etc/dhcp/dhcpd.conf', 'a') as dhcpd:
                    dhcpd.write('\nauthoritative;\n')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/dhcp/dhcpd.conf &> /dev/null')
                pbar.update(5)
                sleep(0.1)
                os.system('chown -R www-data:www-data /etc/default/isc-dhcp-server &> /dev/null')
                pbar.update(5)
                sleep(0.5)
        print(self.language['final'])

    def preparacaoServidor(self: object):
        with tqdm(total=50) as pbar:
            log.info(f'{os.getlogin()} - Preparamento do Servidor começou')
            self.language = self.language['server-preparation']
            print(self.language['main-text'])
            sleep(1)
            ipv4=None
            contador = 0
            os.system('apt-get install --assume-yes apache2 &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('apt-get install --assume-yes python-setuptools &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('apt-get install --assume-yes python3-pip &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('pip3 install flask')
            pbar.update(5)
            sleep(0.1)
            os.system('apt-get install --assume-yes libapache2-mod-wsgi-py3 &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            log.debug(f'{os.getlogin()} - Serviços "instalados".')
            if not os.path.exists('/etc/psc/configs/saveConfigDHCP.txt'):
                os.mknod('/etc/psc/configs/saveConfigDHCP.txt')
            if not os.path.exists('/etc/psc/configs/saveConfigDNS.txt'):
                os.mknod('/etc/psc/configs/saveConfigDNS.txt')
            pbar.update(5)
            sleep(0.1)
            os.system('chown -R www-data:www-data /etc/network/interfaces &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigDHCP.txt &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigDNS.txt &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigIp.txt &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            with open('/etc/psc/configs/saveConfigIp.txt', 'r') as config:
                configTamanho = len(tuple(config.readlines()))
                config.seek(0)
                for dado in config.readlines():
                    if 'IPV4:' in dado:
                        ipv4= dado.split(':')
                    contador +=1
                    if contador == configTamanho and 'IPV4:' in dado:
                        print(self.language['ipv4-config-error'])
                        return
            pbar.update(5)
            sleep(0.1)
            os.system('cp -p /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/flask.conf &> /dev/null')
            pbar.update(5)
            sleep(0.1)
            with open('/etc/apache2/sites-available/flask.conf', 'w') as flaskServer:         # modify the below line. 
                flaskServer.write(f"<VirtualHost *:80>\n    ServerName {ipv4[1]}\n\n    "\
                                "WSGIScriptAlias /psc /etc/psc/prototipoFlask.wsgi\n    <Directory /etc/psc>\n        Options FollowSymLinks\n"\
                                "        AllowOverride None\n        Require all granted\n"\
                                "    </Directory>\n    ErrorLog ${APACHE_LOG_DIR}/error.log\n    LogLevel warn"\
                                "\n    CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
            pbar.update(5)
            sleep(0.1)
            log.debug(f'{os.getlogin()} - Arquivo Flask de host virtual criado')
            os.chdir('/etc/apache2/sites-available/')
            os.system('a2ensite flask')
            os.system('chown -R www-data:www-data /etc/apache2/sites-available/flask.conf &> /dev/null')
            os.system('systemctl restart apache2')
            log.debug(f'{os.getlogin()} - Fim do preparamento do Servidor')

    def idioma(self: object):
        with open('/etc/psc/appSettings.json', 'r') as data_confs:
            data_confs.seek(0)
            data = json.load(data_confs)
            if(data['actualLanguage'] == 'pt-BR'):
                return data['languages']['pt-BR']["server-side"]
            elif(data['actualLanguage'] == 'en'): 
                return data['languages']['en']["server-side"]
            print('Please select your language\n1)Portuguese\n2)English')
            language_option = int(input('R:'))
            with open('appSettings.json', 'w+', encoding='utf-8') as language_config:
                if(language_option == 1):
                    data['actualLanguage'] = "pt-BR"
                elif(language_option == 2):
                    data['actualLanguage'] = "en"
                language_config.write("{\n")
                for x, y in data.items():        
                    if(x == "actualLanguage"):
                        language_config.write(f', "{x}" : "{y}",'.replace("'", '"'))
                    else:
                        language_config.write(f'"{x}" : {y}'.replace("'", '"'))
                language_config.write("\n}")
                language_config.seek(0)
                return json.load(language_config)['languages'][('pt-BR' if language_option == 1 else 'en')]['server-side']

if __name__ == '__main__':
    if not os.path.exists('/etc/psc'):
        os.system('clear')
        os.system('mkdir -p /etc/psc')
    log = Log(diretorio='/etc/psc/logs', nome_arquivo='psc.log', modo_abertura='a')
    log.debug(f'{os.getlogin()} - Aplicativo comecou')
    # os.system('apt-get install --assume-yes python3-pip &> /dev/null')
    app = Software()
    