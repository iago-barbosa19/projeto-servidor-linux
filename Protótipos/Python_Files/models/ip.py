import os, sys
from typing import final


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
        elif subNetMask[0] == 255 and subNetMask[1] > 0 and subNetMask[2] > 0 and subNetMask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[1]}.{ipv4[2]}.0'
            return  ipv4

    def saveSettings(self:object) -> None:
        """Método para salvar as configurações que foram feitas até então."""
        os.chdir(f'/home/{os.getlogin()}')
        try:
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'{os.getcwd()}/Config_Saves_PSC')
        with open('saveIp.txt', 'r+') as save:
            save.write(f'Informações Gerais\nIP:{self.ipv4}|Gateway:{self.gateway}|NetworkIp:{self.__networkIp}\n'\
                       f'Subnet Mask:{self.subNetMask}\nDNS1:{self.dns1}|DNS2:{self.dns2}')
        print(f'Salvo com sucesso, no diretório.\n{os.getcwd}')

    @final
    def ipConfig(self:object) -> None:
        os.chdir(f'/home/{os.getlogin()}')
        try:
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'{os.getcwd()}/Config_Saves_PSC')
        os.mknod('interfaces')
        with open('interfaces', 'r+') as arq:
            arq.write('source /etc/network/interfaces.d/*\n'\
                'auto lo\n\niface auto lo inet loopback\n'\
                f'address {self.ip}\nnetmask {self.subNetMask}\n'\
                f'network {self.network}\ngateway {self.gateway}\ndns-server {self.dns}')
        os.system('cp -p interfaces /etc/network')
        os.system('rm interfaces')
        os.system('/etc/init.d/networking restart')
        print('Executado com sucesso')
        sys.wait(5)        

if __name__ == '__main__':
    raise NotImplementedError('Esse arquivo não pode ser inicializado como principal')
