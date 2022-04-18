from models.ip import Ip
from models.dhcp import Dhcp
from models.dns import Dns
from time import sleep
import os
import json
import logging



log = logging.getLogger(__name__)

language = None

def main():
    with open('appSettings.json', 'r') as dataConfs:
        data = json.load(dataConfs)['actualLanguage'];
        dataConfs.write.seek(0)
        if(data == 'pt-BR'):
            language = json.load(dataConfs)['languages']['pt-BR']["server-side"]
        elif(data == 'en'): 
            language = json.load(dataConfs)['languages']['en']["server-side"]
        else: 
            print('Please select your language\n1)Portuguese\n2)English')
            languageOption = int(input('R:'))
            with open('appSettings.json', 'w+') as languageConfig:
                if(languageOption == 1):
                    json.dump({"actualLanguage": "pt-BR"}, languageConfig)
                elif(languageOption == 2):
                    json.dump({"actualLanguage": "en"}, languageConfig)
    log.debug('Aplicativo comecou')
    os.system('clear')
    # Local temporário, para conseguir identificar se o aplicativo já está instalado, ou não.
    if not os.path.exists('/etc/psc/fst'):        
        with open('/etc/psc/fst', 'w') as fst:
            fst.write('This program has been already initialized on this system.')
        os.system(f'cp -r * /etc/psc/')
        print(language["instalation"])
        sleep(3)
        os.system('clear')
    print('---------------------------------------------------\n '+ language['main-page']['main-menu'])
    opc = int(input(language['main-page']['main-menu-input']))
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
    elif opc == 4:
        os.system('clear')
        print(language['main-page']['configuration-web-page'])
        opc = input('Y/n  ->')
        if opc.lower() == 'y':
            preparacaoServidor()
        main()
    else:
        exit()


def configServicos():
    configs = []
    print('---------------------------------------------------'+
          language['services-config']['main-menu'])
    opc = int(input(language['services-config']['main-menu-input']))
    if opc == 1:
        os.system('clear')
        print(language['services-config']['interface']['main-text'])
        for dado in ['ipv4', 'gateway', 'subnetMask', 'dns1', 'dns2']:
            configs.append(input(language['services']['interface']['data-insert'] + f' {dado} ->'))
        ipConfig = Ip(ipv4=configs[0], gateway=configs[1], subNetMask=configs[2], dns1=configs[3], dns2=configs[4])
        ipConfig.ipConf()
        os.system('systemctl restart networking')
    elif opc == 2:
        os.system('clear')
        print(language['services-config']['dhcp']['main-text'])
        for dado in ['ipv4', 'gateway', 'dns1', 'dns2', 'subnetMask', 'Pool Inicial do DHCP', 'Pool Final do DHCP']:
            configs.append(input(language['services-config']['dhcp']['data-input'] + f' {dado} ->'))
        dhcpConfig = Dhcp(ipv4=configs[0], gateway=configs[1], dns1=configs[2], dns2=configs[3], subNetMask=configs[4], dhcpPoolInicial=configs[5], dhcpPoolFinal=configs[6])
        dhcpConfig.dhcpConf()
        os.system('systemctl restart isc-dhcp-server')
    elif opc == 3:
        os.system('clear')
        print(language['services-config']['dns']['main-text'])
        for dado in ['ipv4', 'subnetMask', 'dominio', 'Nome do servidor']:
            configs.append(input(language['services-config']['dns']['data-input'] + f'{dado} ->'))
        dnsConfig = Dns(ipv4=configs[0], subNetMask=configs[1], domain=configs[2], serverName=configs[3])
        dnsConfig.dnsConf()
        os.system('systemctl restart bind9')
        os.system('systemctl restart apache2')
    print(language['services-config']['final'])
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
    sleep(5)
    print('echo Voltando para a página inicial')
    main()


def installServices():
    print('---------------------------------------------------\nServicos:\n1)DNS\n2)DHCP\n3)Voltar')
    opc = int(input('O que deseja fazer? ->'))
    if opc == 1:
        os.system('apt-get install --assume-yes apache2')
        os.system('apt-get install --assume-yes bind9')
        os.system('chown -R www-data:www-data /etc/apache2/sites-available/')
        os.system('chown -R www-data:www-data /etc/apache2/sites-enabled/')
        os.system('chown -R www-data:www-data /etc/bind')
        os.system('mkdir -p /var/www/sites')
        os.system('chown -R www-data:www-data /var/www/sites')
        os.system('chown -R www-data:www-data /etc/bind/named.conf.default-zones')
    elif opc == 2:
        os.system('apt-get install --assume-yes isc-dhcp-server')
        with open('/etc/dhcp/dhcpd.conf', 'a') as dhcpd:
            dhcpd.write('\nauthoritative;\n')
        os.system('chown -R www-data:www-data /etc/dhcp/dhcpd.conf')
        os.system('chown -R www-data:www-data /etc/default/isc-dhcp-server')
    print('Voltando para a página inicial')
    main()


def preparacaoServidor():
    log.debug('Preparamento do Servidor começou')
    print('Iniciaremos a instalacao de alguns servicos para o funcionamento do aplicativo.')
    sleep(1)
    ipv4=None
    contador = 0
    os.system('apt-get install --assume-yes apache2')
    os.system('apt-get install --assume-yes python-setuptools')
    os.system('apt-get install --assume-yes python3-pip')
    os.system('pip3 install flask')
    os.system('apt-get install --assume-yes libapache2-mod-wsgi-py3')
    log.debug('Serviços "instalados".')
    if not os.path.exists('/etc/psc/configs/saveConfigDHCP.txt'):
        os.mknod('/etc/psc/configs/saveConfigDHCP.txt')
    if not os.path.exists('/etc/psc/configs/saveConfigDNS.txt'):
        os.mknod('/etc/psc/configs/saveConfigDNS.txt')
    os.system('chown -R www-data:www-data /etc/network/interfaces')
    os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigDHCP.txt')
    os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigDNS.txt')
    os.system('chown -R www-data:www-data /etc/psc/configs/saveConfigIp.txt')
    with open('/etc/psc/configs/saveConfigIp.txt', 'r') as config:
        configTamanho = len(tuple(config.readlines()))
        config.seek(0)
        for dado in config.readlines():
            if 'IPV4:' in dado:
                ipv4= dado.split(':')
            contador +=1
            if contador == configTamanho and 'IPV4:' in dado:
                print('Por favor, faca a configuracao do IP por meio do nosso programa, para que identifiquemos o IP corretamente.')
                main()
    os.system('cp -p /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/flask.conf')
    with open('/etc/apache2/sites-available/flask.conf', 'w') as flaskServer:         # modify the below line. 
        flaskServer.write(f"<VirtualHost *:80>\n    ServerName {ipv4[1]}\n\n    "\
                          "WSGIScriptAlias /psc /etc/psc/prototipoFlask.wsgi\n    <Directory /etc/psc>\n        Options FollowSymLinks\n"\
                          "        AllowOverride None\n        Require all granted\n"\
                          "    </Directory>\n    ErrorLog ${APACHE_LOG_DIR}/error.log\n    LogLevel warn"\
                          "\n    CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
    log.debug("Arquivo Flask de host virtual criado")
    os.chdir('/etc/apache2/sites-available/')
    os.system('a2ensite flask')
    os.system('chown -R www-data:www-data /etc/apache2/sites-available/flask.conf')
    os.system('systemctl restart apache2')
    log.debug("Fim do preparamento do Servidor")
    main()
    

if __name__ == '__main__':
    if not os.path.exists('/etc/psc'):
        os.system('clear')
        os.system('mkdir -p /etc/psc')
    # Forma de se configurar um log
    logging.basicConfig(level=logging.DEBUG, 
                                format='%(asctime)s %(name)s %(levelname)s %(message)s',
                                filename='psc.log',
                                filemode='a')  # Filemodes = A == append. w == write
    main()