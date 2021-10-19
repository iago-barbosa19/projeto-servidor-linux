import os, sys


class Ip:

    def __init__(self:object, ipv4:str, gateway:str, dns1:str, dns2: str, subnetmask:str) -> None:
        self.__ipv4 = ipv4
        self.__gateway = gateway
        self.__dns1 = dns1
        self.__dns2 = dns2
        self.__subnetmask = subnetmask
        self.__networkIp = self.networkIpSetter(ipv4, subnetmask)
    
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
        Esse método serve para settar o ip da rede de forma fácil, sem que seja necessário o técnico inserir o IP.
        """
        subnetmask = subNetMask.split('.')
        subnetmask = [int(subnetmask[0]), int(subnetmask[1]), int(subnetmask[2]), int(subnetmask[3])]
        if subnetmask[0] == 255 and subnetmask[1] == 0 and subnetmask[2] == 0 and subnetmask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.0.0.0'
            return  ipv4
        elif subnetmask[0] == 255 and subnetmask[1] >0 and subnetmask[2] == 0 and subnetmask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[2]}.0.0'
            return  ipv4
        elif subnetmask[0] == 255 and subnetmask[1] > 0 and subnetmask[2] > 0 and subnetmask[3] == 0:
            ipv4 = ipv4.split('.')
            ipv4 = f'{ipv4[0]}.{ipv4[2]}.{ipv4[3]}.0'
            return  ipv4

    def saveSettings(self:object) -> None:
        """Método para salvar as configurações que foram feitas até então."""
        os.chdir(f'/home/{os.getlogin()}')
        os.mkdir('Saves')
        os.chdir(f'{os.getcwd}/Saves')
        with open('save.txt', 'r+') as save:
            save.write(f'Informações Gerais\nIP:{self.ipv4}|Gateway:{self.gateway}|NetworkIp:{self.__networkIp}\n'\
                       f'Subnet Mask:{self.subnetmask}\nDNS1:{self.dns1}|DNS2:{self.dns2}')
        print(f'Salvo com sucesso, no diretório.\n{os.getcwd}')

    def ipConfig(self:object) -> None:
        os.chdir(f'/home/{os.getlogin()}')
        os.mknod('interfaces')
        with open('interfaces', 'r+') as arq:
            arq.write('source /etc/network/interfaces.d/*\n'\
                'auto lo\n\niface auto lo inet loopback\n'\
                f'address {self.ip}\nnetmask {self.subnetmask}\n'\
                f'network {self.network}\ngateway {self.gateway}\ndns-server {self.dns}')
        os.system('cp -p interfaces /etc/network')
        os.system('rm interfaces')
        os.system('/etc/init.d/networking restart')
        print('Executado com sucesso')
        sys.wait(5)        

if __name__ == '__main__':
    raise NotImplementedError('Esse arquivo não pode ser inicializado como principal')
