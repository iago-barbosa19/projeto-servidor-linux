from models import Ip, Dhcp, Dns
from time import sleep
import os
import subprocess
import tqdm
import json
import logging


log = logging.getLogger(__name__)

language = None

def main():
    # Tentativa de idioma
    idioma()
    os.system('clear')
    # Local temporário, para conseguir identificar se o aplicativo já está instalado, ou não.
    # if not os.path.exists('/etc/psc/fst'):        
        # with open('/etc/psc/fst', 'w') as fst:
            # fst.write('This program has been already initialized on this system.')
        # os.system(f'cp -r * /etc/psc/')
        # print(language["instalation"])
        # sleep(3)
        # os.system('clear')
    print('---------------------------------------------------\n '+ language['main-page']['main-menu'])
    opc = int(input(language['main-page']['main-menu-input']))
    if opc == 1:
        os.system('clear')
        configServicos()
    elif opc == 2:
        os.system('clear')
        checkServicos()
    elif opc == 3:
        os.system('clear')
        installServices()
    elif opc == 4:
        os.system('clear')
        print(language['main-page']['configuration-web-page'])
        opc = input('Y/n  ->')
        if opc.lower() == 'y':
            preparacaoServidor()
        main()
    elif opc == 5:
        os.system('clear')
        idioma(int(input(language['main-page']['languague-change'])))
    else:
        exit()


def configServicos():
    log.debug('Entrando na Configuração de Serviços')
    configs = []
    print('---------------------------------------------------'+
          language['services-config']['main-menu'])
    opc = int(input(language['services-config']['main-menu-input']))
    if opc == 1:
        log.debug('Configurando interface IPV4')
        os.system('clear')
        system_interfaces = []
        interface = subprocess.run(["ip", "addr"], stdout=subprocess.PIPE, universal_newlines=True).stdout
        with open("appSettings.json", "r") as interface_names:
            interfaces = interface_names['os-interfaces-names'].readlines()
            for network_interface in interfaces:
                if network_interface in interface:
                    system_interfaces.append(network_interface)
                    log.debug(f'Interface:{network_interface} encontrada. Qtd de Interfaces: {system_interfaces}')
        print(len(system_interfaces) == 1 if language['services-config']['interface']['main-text'] 
              else language['services-config']['interface']['main-text2'])
        for x in range((len(system_interfaces))):
            for dado in ['ipv4', 'gateway', 'subnetMask', 'dns1', 'dns2']:
                configs.append(input(language['services']['interface']['data-insert'] + f' {dado} ->'))
            ip_config = Ip(ipv4=configs[0], gateway=configs[1], subNetMask=configs[2], dns1=configs[3], dns2=configs[4], interface=configs[5])
            ip_config.ipConf()
    elif opc == 2:
        os.system('clear')
        print(language['services-config']['dhcp']['main-text'])
        for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask', 'Pool Inicial do DHCP', 'Pool Final do DHCP']:
            configs.append(input(language['services-config']['dhcp']['data-input'] + f' {dado} ->'))
        dhcp_config = Dhcp(ipv4=configs[0], gateway=configs[1], dns1=configs[2], dns2=configs[3], subNetMask=configs[4], dhcpPoolInicial=configs[5], dhcpPoolFinal=configs[6])
        dhcp_config.dhcpConf()
    elif opc == 3:
        os.system('clear')
        print(language['services-config']['dns']['main-text'])
        for dado in ['ipv4', 'subnetMask', 'dominio', 'Nome do servidor']:
            configs.append(input(language['services-config']['dns']['data-input'] + f'{dado} ->'))
        dns_config = Dns(ipv4=configs[0], subNetMask=configs[1], domain=configs[2], serverName=configs[3])
        dns_config.dnsConf()
    print(language['services-config']['final'])
    main()


def checkServicos():
    language = language['services-config']['service-check']
    print("---------------------------------------------------"+
          language['main-text'])
    opc = int(input(language['data-input']))
    if opc == 1:
        os.system('systemctl status networking')
    elif opc == 2:
        os.system('systemctl status apache2')
        os.system('systemctl status bind9')
    elif opc == 3:
        os.system('systemctl status isc-dhcp-server')
    sleep(5)
    print(f'echo {language["final"]}')
    main()


def installServices():
    log.info(f'{os.getlogin()} - Instalação de serviços necessários iniciada.')
    
    language = language['services-config']['install-services']
    print("---------------------------------------------------"+
          language['main-text'])
    opc = int(input(language['data-input']))
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
    print(language['final'])
    main()


def preparacaoServidor():
    with tqdm(total=50) as pbar:
        log.info(f'{os.getlogin()} - Preparamento do Servidor começou')
        language = language['server-preparation']
        print(language['main-text'])
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
        log.debug('Serviços "instalados".')
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
                    print(language['ipv4-config-error'])
                    main()
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
        log.debug("Arquivo Flask de host virtual criado")
        os.chdir('/etc/apache2/sites-available/')
        os.system('a2ensite flask')
        os.system('chown -R www-data:www-data /etc/apache2/sites-available/flask.conf &> /dev/null')
        os.system('systemctl restart apache2')
        log.debug("Fim do preparamento do Servidor")
        main()


def idioma():
    os.chdir('./Protótipos/pythonFiles/')
    with open('appSettings.json', 'r') as data_confs:
        data = json.load(data_confs)['actualLanguage']
        data_confs.seek(0)
        data = json.load(data_confs)
        if(data == 'pt-BR'):
            language = json.load(data_confs)['languages']['pt-BR']["server-side"]
        elif(data == 'en'): 
            language = json.load(data_confs)['languages']['en']["server-side"]
        else: 
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
                        language_config.write(f', "{x}" : "{y}"'.replace("'", '"'))
                    else:
                        language_config.write(f'"{x}" : {y}'.replace("'", '"'))
                language_config.write("\n}")


if __name__ == '__main__':
    # Forma de se configurar um log
    logging.basicConfig(level=logging.DEBUG, 
                                format='%(asctime)s %(name)s %(levelname)s %(message)s',
                                filename='psc.log',
                                filemode='a')
    log.debug('Aplicativo comecou')
    if not os.path.exists('/etc/psc'):
        os.system('clear')
        os.system('mkdir -p /etc/psc')
    main()