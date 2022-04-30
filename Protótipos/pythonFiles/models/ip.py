from time import sleep
import os
import datetime
import tqdm
import logging

log = logging.getLogger(__name__)


class Ip:

    def __init__(self:object, ipv4:str, gateway:str, dns1:str, dns2: str, sub_net_mask:str, interface: str) -> None:
        self.__ipv4 = ipv4
        self.__gateway = gateway
        self.__dns1 = dns1
        self.__dns2 = dns2
        self.__interface = interface
        self.__sub_net_mask = sub_net_mask
        self.__network_ip = self.network_ip_setter(ipv4, sub_net_mask)
    
    @property
    def ipv4(self:object) -> str:
        return self.__ipv4

    @property
    def gateway(self:object) -> str:
        return self.__gateway

    @property
    def dns1(self:object) -> str:
        return self.__dns1

    @property
    def dns2(self:object) -> str:
        return self.__dns2
    
    @property
    def network_ip(self:object) -> str:
        return self.__network_ip

    @property
    def sub_net_mask(self:object) -> str:
        return self.__sub_net_mask

    @property
    def interface(self:object) -> str:
        return self.__interface
    
    @ipv4.setter
    def ipv4(self:object, ipv4:str) -> None:
        self.__ipv4 = ipv4
    
    @gateway.setter
    def gateway(self:object, gateway: str) -> None:
        self.__gateway = gateway

    @dns1.setter
    def dns1(self:object, dns1: str) -> None:
        self.__dns1 = dns1

    @dns2.setter
    def dns2(self:object, dns2: str) -> None:
        self.__dns2 = dns2
        
    @interface.setter
    def interface(self:object, interface: str) -> None:
        self.__interface = interface
        
    @staticmethod
    def network_ip_setter(ipv4:str, sub_net_mask:str) -> str:
        """
        Esse método serve para settar o ip da rede de forma fácil, sem que seja necessário o técnico inserir o IP da rede.
        Ele vai funcionar mesmo se a máscara de sub rede usar VLSM.
        
        Ele separa a máscara de sub-rede para que vire uma lista com 4 indíces, para que assim cada indíce contenha uma string.
        É feito um cast nas Strings para virarem Int, e assim poder ser checado os valores maiores ou iguais a 0.
        """
        sub_net_mask = sub_net_mask.split('.')
        sub_net_mask = [int(sub_net_mask[0]), int(sub_net_mask[1]), int(sub_net_mask[2]), int(sub_net_mask[3])]
        if sub_net_mask[0] == 255 and sub_net_mask[1] == 0 and sub_net_mask[2] == 0 and sub_net_mask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.0.0.0'
            return  ipv4
        elif sub_net_mask[0] == 255 and sub_net_mask[1] >0 and sub_net_mask[2] == 0 and sub_net_mask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.0.0'
            return  ipv4
        elif sub_net_mask[0] == 255 and sub_net_mask[1] == 255 and sub_net_mask[2] > 0 and sub_net_mask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.{ipv4[2]}.0'
            return  ipv4
        elif sub_net_mask[0] == 255 and sub_net_mask[1] == 255 and sub_net_mask[2] == 255 and sub_net_mask[3] > 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.{ipv4[2]}.0'
            return  ipv4

    def ipConf(self:object) -> None:
        """Método de configuraçãodo serviço networking.
        Ele usa as informações usadas na hora da criação do objeto, para poder efetuar à escrita
        no arquivo interfaces.
        Esse método devia ser usado '@final' nele, para que não possa ser extendido por mais nenhum outro, porém
        como é normal ver máquinas com Python 3.7 para baixo, ainda não coloquei os itens da nova versão.
        """
        log.info(f"{os.getlogin()} - Iniciando configuração de interface")
        with tqdm(total=10) as pbar:
            os.chdir('/etc/network')
            with open('interfaces', 'w') as interfaces:
                interfaces.write('source /etc/network/interfaces.d/*\n'\
                    f'\nauto lo\niface lo inet loopback\n\nauto {self.interface}\niface {self.interface} inet static\n'\
                    f'address {self.ipv4}\nnetmask {self.sub_net_mask}\n'\
                    f'network {self.network_ip}\ngateway {self.gateway}\ndns-server {self.dns1} {self.dns2}')
            log.debug(f"{os.getlogin()} - Arquivo interfaces configurado")
            pbar.update(5)
            sleep(0.2)
            os.system('systemctl restart networking')
            if os.getlogin() != 'www-data':
                self.save_settings()
            pbar.update(5)
            sleep(0.2)
            os.system('clear')
            
        def ipConfAlt(self:object) -> None:
            with tqdm(total=15) as pbar:
                with open('/etc/apache2/sites-available/flask.conf', 'w') as flask_server:
                    flask_server.write(f"<VirtualHost *:80>\n    ServerName {self.ipv4}\n\n    "\
                                    "WSGIScriptAlias /psc /etc/psc/prototipoFlask.wsgi\n    <Directory /etc/psc>\n        Options FollowSymLinks\n"\
                                    "        AllowOverride None\n        Require all granted\n"\
                                    "    </Directory>\n    ErrorLog ${APACHE_LOG_DIR}/error.log\n    LogLevel warn"\
                                    "\n    CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
                pbar.update(5)
                sleep(0.2)
                os.chdir('/etc/network')
                with open('interfaces', 'w') as interfaces:
                    interfaces.write('source /etc/network/interfaces.d/*\n'\
                        f'\nauto lo\niface lo inet loopback\n\nauto {self.interface}\niface {self.interface} inet static\n'\
                        f'address {self.ipv4}\nnetmask {self.sub_net_mask}\n'\
                        f'network {self.network_ip}\ngateway {self.gateway}\ndns-server {self.dns1} {self.dns2}')
                pbar.update(5)
                sleep(0.2)
                if os.getlogin() != 'www-data':
                    self.save_settings()
                pbar.update(5)
                sleep(0.2)
                os.system('clear')
    
    def save_settings(self:object) -> None:
        """Método para salvar as configurações que foram feitas até então.
        Aqui salva todas as informaçãos das interfaces de rede, para seber quando foram modificadas, e para o que foram modificadas, para que assim seja
        possível ter uma espécie de backup de configurações passadas e qual usuário mudou elas."""
        if os.path.exists('/etc/psc'):
            pass
        else:
            os.system(f"mkdir /etc/psc")
        if os.path.exists('/etc/psc/configs'):
            pass
        else:
            os.system(f"mkdir /etc/psc/configs")
        with open('/etc/psc/configs/saveConfigIp.txt', 'a') as save:
            save.write(f'Informações Gerais\n|Interface:{self.interface}\n|IPV4:{self.ipv4}\n|Gateway:{self.gateway}\n|network_ip:{self.__network_ip}\n'\
                        f'Subnet Mask:{self.sub_net_mask}\nDNS1:{self.dns1}\n|DNS2:{self.dns2}\nData da modificação:'\
                        f'{datetime.datetime.now()}\nUsuário que alterou a configuração: {os.getlogin()}\n\n')
                
    def __repr__(self):
        print('Os métodos que são possíveis visualizar com as Docstrings:\nipConf\nnetwork_ip_setter\nsave_settings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')    
        
        
if not __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, 
                                format='%(asctime)s %(name)s %(levelname)s %(message)s',
                                filename='psc.log',
                                filemode='a',
                                encoding='utf8')
else:
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
    