from models.ip import Ip
from models.dhcp import Dhcp
from models.dns import Dns
import os

import logging

log = logging.getLogger(__name__)


def main():
    log.debug('Aplicativo comecou')
    if not os.path.exists('/etc/psc/fst'):
        os.system('Como e sua primeira vez iniciando o aplicativo neste servidor, pedimos encarecidamente, que nos deixe fazer as configuracoes\niniciais.')
        if opc := int(input('y/n  ->')) == 'y':
            preparacaoServidor()
        os.system('cp -p ./fst /etc/psc/')
        os.system('echo Seguindo para o menu principal.')
    os.system('echo ---------------------------------------------------\n1)Configurar Servicos.\n2)Checar Servicos.\n3)Instalar Servicos\n4)Sair.\n')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        log.debug('Configurando Servicos.')
        configServicos()
    elif opc == 2:
        log.debug('Configurando Servicos.')
        checkServicos()
    elif opc == 3:
        installServices()
    else:
        exit()


def configServicos():
    configs = []
    os.system('echo ---------------------------------------------------\nServicos:\n1)Interface de rede\n2)DNS\n3)DHCP\n4)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask']:
            configs.append(input(f'Insira o {dado} ->'))
        ipConfig = Ip(ipv4=dado[0], gateway=dado[1], dns1=dado[2], dns2=dado[3], subNetMask=dado[4])
        ipConfig.ipConf()
    elif opc == 2:
        for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask', 'Pool Inicial do DHCP', 'Pool Final do DHCP']:
            configs.append(input(f'Insira o(a) {dado} ->'))
        dhcpConfig = Dhcp(ipv4=dado[0], gateway=dado[1], dns1=dado[2], dns2=dado[3], subNetMask=dado[4], dhcpPoolInicial=dado[5], dhcpPoolFinal=dado[6])
        dhcpConfig.dhcpConf()
    elif opc == 3:
        for dado in ['ipv4', 'subnetMask', 'dominio', 'Nome do servidor']:
            configs.append(input(f'Insira o {dado} ->'))
        dnsConfig = Dns(ipv4=dado[0], subnetMask=dado[1], domain=dado[2], serverName=dado[3])
        dnsConfig.dnsConf()
    os.system('echo Voltando para a página inicial')
    main()


def checkServicos():
    os.system('echo ---------------------------------------------------\nServicos:\n1)Interface de rede\n2)DNS\n3)DHCP\n4)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('systemctl status networking')
    elif opc == 2:
        os.system('systemctl status apache2')
        os.system('systemctl status bind9')
    elif opc == 3:
        os.system('systemctl status isc-dhcp-server')
    os.system('echo Voltando para a página inicial')
    main()


def installServices():
    os.system('echo ---------------------------------------------------\nServicos:\n1)DNS\n2)DHCP\n3)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('apt-get install --assume-yes apache2')
        os.system('apt-get install --assume-yes bind9')
    elif opc == 2:
        os.system('apt-get install --assume-yes isc-dhcp-server')
    os.system('echo Voltando para a página inicial')
    main()


def preparacaoServidor():
    log.debug('Preparamento do Servidor começou')
    os.system('echo Iniciaremos a instalacao de alguns servicos para o funcionamento do aplicativo.')
    os.system('apt-get install --assume-yes apache2')
    os.system('apt-get install --assume-yes python-setuptools')
    os.system('apt-get install --assume-yes libapache2-mod-wsgi')
    with open('/etc/hosts', 'a') as arq:
        arq.write('192.168.15.15 www.psc.com')
    log.debug('Arquivo hosts modificado.')
    if not os.path.exists('/etc/psc'):
        os.system('mkdir /etc/psc')
    os.system(f'cp -r {os.getcwd()} /etc/psc/')
    with open('/etc/apache2/sites-available/flask', 'w') as flaskServer:        
        flaskServer.write("<VirtualHost *:80>\n    ServerName www.psc.com\n\n    WSGIDaemonProcess flasktest threads=5\n    "\
                          f"WSGIScriptAlias /etc/psc/wsgi.py\n\n    <Directory /etc/psc/>\n        WSGIProcessGroup flaskTest"\
                          "\n        WSGIApplicationGroup %{GLOBAL}\n        WSGIScriptReloading On\n        Order deny, allow\n"\
                          "        Allow from all\n   </Directory>\n</VirtualHost>")
    log.debug("Arquivo Flask de host virtual criado")
    os.chdir('/etc/apache2/sites-available/')
    os.system('a2ensite flask')
    log.debug("Fim do preparamento do Servidor")
    

if __name__ == '__main__':
    if not os.path.exists('/etc/psc'):
       os.system('mkdir -p /etc/psc')
    # Forma de se configurar um log
    logging.basicConfig(level=logging.DEBUG, 
                                format='%(asctime)s %(name)s %(levelname)s %(message)s',
                                filename='C:\\Users\iagof\Downloads\\teste.log',
                                filemode='a')  # Filemodes = A == append. w == write
    main()