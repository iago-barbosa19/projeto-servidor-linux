import os, datetime
from time import sleep

class Ip:

    def __init__(self:object, ipv4:str, gateway:str, dns1:str, dns2: str, subNetMask:str) -> None:
        self.__ipv4 = ipv4
        self.__gateway = gateway
        self.__dns1 = dns1
        self.__dns2 = dns2
        self.__subNetMask = subNetMask
        self.__networkIp = self.networkIpSetter(ipv4, subNetMask)
    
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
    def networkIp(self:object) -> str:
        return self.__networkIp

    @property
    def subNetMask(self:object) -> str:
        return self.__subNetMask

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
        
    def networkIpSetter(self:object, ipv4:str, subNetMask:str) -> str:
        """
        Esse método serve para settar o ip da rede de forma fácil, sem que seja necessário o técnico inserir o IP da rede.
        Ele vai funcionar mesmo se a máscara de sub rede usar VLSM.
        
        Ele separa a máscara de sub-rede para que vire uma lista com 4 indíces, para que assim cada indíce contenha uma string.
        É feito um cast nas Strings para virarem Int, e assim poder ser checado os valores maiores ou iguais a 0.
        """
        subNetMask = subNetMask.split('.')
        subNetMask = [int(subNetMask[0]), int(subNetMask[1]), int(subNetMask[2]), int(subNetMask[3])]
        if subNetMask[0] == 255 and subNetMask[1] == 0 and subNetMask[2] == 0 and subNetMask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.0.0.0'
            return  ipv4
        elif subNetMask[0] == 255 and subNetMask[1] >0 and subNetMask[2] == 0 and subNetMask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.0.0'
            return  ipv4
        elif subNetMask[0] == 255 and subNetMask[1] == 255 and subNetMask[2] > 0 and subNetMask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.{ipv4[2]}.0'
            return  ipv4
        elif subNetMask[0] == 255 and subNetMask[1] == 255 and subNetMask[2] == 255 and subNetMask[3] > 0:
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
        os.chdir('/etc/network')
        with open('interfaces', 'w') as interfaces:
            interfaces.write('source /etc/network/interfaces.d/*\n'\
                '\nauto lo\niface lo inet loopback\n\nauto enp0s3\niface enp0s3 inet static\n'\
                f'address {self.ipv4}\nnetmask {self.subNetMask}\n'\
                f'network {self.networkIp}\ngateway {self.gateway}\ndns-server {self.dns1} {self.dns2}')
        os.system('echo Configuração efetuada com sucesso!')
        sleep(2)
        os.system('clear')
    
    def saveSettings(self:object) -> None:
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
            save.write(f'Informações Gerais\nIP:{self.ipv4}|Gateway:{self.gateway}|NetworkIp:{self.__networkIp}\n'\
                        f'Subnet Mask:{self.subNetMask}\nDNS1:{self.dns1}|DNS2:{self.dns2}\nData da modificação:'\
                        f'{datetime.datetime.now()}\nUsuário que alterou a configuração: {os.getlogin()}\n\n')
                
    def __repr__(self):
        print('Os métodos que é possível visualizar as Docstrings:\nipConf\nnetworkIpSetter\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')    
        
        
if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
