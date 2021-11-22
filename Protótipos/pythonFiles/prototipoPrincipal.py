from models.ip import Ip
from models.dhcp import Dhcp
from models.dns import Dns
import os
from time import sleep

import logging

log = logging.getLogger(__name__)


def main():
    log.debug('Aplicativo comecou')
    os.system('clear')
    if not os.path.exists('/etc/psc/fst'):
        print('Como e sua primeira vez iniciando o aplicativo neste servidor, pedimos encarecidamente, que nos deixe fazer as configuracoes\niniciais.')
        opc = input('y/n  ->')
        if opc == 'y':
            preparacaoServidor()
        os.system('cp -p ./fst /etc/psc/')
        print('Seguindo para o menu principal.')
        sleep(1.5)
        os.system('clear')
    print('---------------------------------------------------\n1)Configurar Servicos.\n2)Checar Servicos.\n3)Instalar Servicos\n4)Sair.\n')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        log.debug('Configurando Servicos.')
        os.system('clear')
        configServicos()
    elif opc == 2:
        log.debug('Configurando Servicos.')
        os.system('clear')
        checkServicos()
    elif opc == 3:
        os.system('clear')
        installServices()
    else:
        exit()


def configServicos():
    configs = []
    print('---------------------------------------------------\nServicos:\n1)Interface de rede\n2)DNS\n3)DHCP\n4)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('clear')
        print('Insira as informações necessárias para configurar a Interface de rede:\n')
        for dado in ['ipv4', 'gateway', 'subnetMask', 'dns1', 'dns2']:
            configs.append(input(f'Insira o {dado} ->'))
        ipConfig = Ip(ipv4=configs[0], gateway=configs[1], subNetMask=configs[2], dns1=configs[3], dns2=configs[4])
        ipConfig.ipConf()
    elif opc == 2:
        os.system('clear')
        print('Insira as informações necessárias para configurar o DNS:\n')
        for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask', 'Pool Inicial do DHCP', 'Pool Final do DHCP']:
            configs.append(input(f'Insira o(a) {dado} ->'))
        dhcpConfig = Dhcp(ipv4=configs[0], gateway=configs[1], dns1=configs[2], dns2=configs[3], subNetMask=configs[4], dhcpPoolInicial=configs[5], dhcpPoolFinal=configs[6])
        dhcpConfig.dhcpConf()
    elif opc == 3:
        os.system('clear')
        print('Insira as informações necessárias para configurar o DHCP:\n')
        for dado in ['ipv4', 'subnetMask', 'dominio', 'Nome do servidor']:
            configs.append(input(f'Insira o {dado} ->'))
        dnsConfig = Dns(ipv4=configs[0], subnetMask=configs[1], domain=configs[2], serverName=configs[3])
        dnsConfig.dnsConf()
    print('Voltando para a página inicial')
    main()


def checkServicos():
    print('---------------------------------------------------\nServicos:\n1)Interface de rede\n2)DNS\n3)DHCP\n4)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('systemctl status networking')
    elif opc == 2:
        os.system('systemctl status apache2')
        os.system('systemctl status bind9')
    elif opc == 3:
        os.system('systemctl status isc-dhcp-server')
    print('echo Voltando para a página inicial')
    main()


def installServices():
    print('---------------------------------------------------\nServicos:\n1)DNS\n2)DHCP\n3)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('apt-get install --assume-yes apache2')
        os.system('apt-get install --assume-yes bind9')
    elif opc == 2:
        os.system('apt-get install --assume-yes isc-dhcp-server')
    print('Voltando para a página inicial')
    main()


def preparacaoServidor():
    log.debug('Preparamento do Servidor começou')
    print('Iniciaremos a instalacao de alguns servicos para o funcionamento do aplicativo.')
    os.system('apt-get install --assume-yes apache2')
    os.system('apt-get install --assume-yes python-setuptools')
    os.system('apt-get install --assume-yes libapache2-mod-wsgi')
    with open('/etc/hosts', 'a') as arq:
        arq.write('192.168.15.15 www.psc.com')
    log.debug('Arquivo hosts modificado.')
    if not os.path.exists('/etc/psc'):
        os.system('mkdir /etc/psc')
    os.system(f'cp -r * /etc/psc/')
    with open('/etc/apache2/sites-available/flask', 'w') as flaskServer:        
        flaskServer.write("<VirtualHost *:80>\n    ServerName www.psc.com\n\n    WSGIDaemonProcess flasktest threads=5\n    "\
                          f"WSGIScriptAlias /etc/psc/wsgi.py\n\n    <Directory /etc/psc/>\n        WSGIProcessGroup flaskTest"\
                          "\n        WSGIApplicationGroup %{GLOBAL}\n        WSGIScriptReloading On\n        Order deny, allow\n"\
                          "        Allow from all\n   </Directory>\n</VirtualHost>")
    log.debug("Arquivo Flask de host virtual criado")
    os.chdir('/etc/apache2/sites-available/')
    os.system('a2ensite flask')
    os.system('systemctl restart apache2')
    log.debug("Fim do preparamento do Servidor")
    

if __name__ == '__main__':
    if not os.path.exists('/etc/psc'):
        os.system('clear')
        os.system('mkdir -p /etc/psc')
    # Forma de se configurar um log
    logging.basicConfig(level=logging.DEBUG, 
                                format='%(asctime)s %(name)s %(levelname)s %(message)s',
                                filename='C:\\Users\iagof\Downloads\\teste.log',
                                filemode='a')  # Filemodes = A == append. w == write
    main()