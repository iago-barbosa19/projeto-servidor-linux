from models.ip import Ip
import os, sys


class Dhcp(Ip):
    
    def __init__(self, ipv4, gateway, dns1, dns2, subNetMask, dhcpPoolInicial, dhcpPoolFinal):
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__networkIp = self.networkIpSetter(ipv4, gateway) 
        self.__dhcpPoolInicial = dhcpPoolInicial
        self.__dhcpPoolFinal = dhcpPoolFinal

    @property
    def dhcpPoolInicial(self):
        return self.__dhcpPoolInicial
    
    @property
    def dhcpPoolFinal(self):
        return self.__dhcpPoolFinal

    @property
    def networkIp(self):
        return self.__networkIp

    def dhcpConf(self:object):
        try:
            os.chdir(f'/home{os.getlogin()}/')
            os.mkdir('Config_Saves_PSC')
            os.chdir(f'/home{os.getlogin()}/Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home{os.getlogin()}/Config_Saves_PSC')
        try:
            os.system(f'cp -p /etc/dhcp/dhcpd.conf /home/{os.getlogin()}/Config_Saves_PSC/')
        except FileExistsError:
            os.system('rm dhcpd.conf')
            os.system(f'cp -p /etc/dhcp/dhcpd.conf /home/{os.getlogin()}/Config_Saves_PSC/')
        with open(f'dhcpd.conf', 'a+') as dhcpConfig:
            dhcpConfig.write(f'\n\n#DHCP Rede:{self.networkIp}\nsubnet {self.networkIp} netmask {self.subNetMask}'\
                             ' {\n  range')
        

    def saveSettings(self:object):
        try:
            os.chdir(f'/home/{os.getlogin()}')
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home{os.getlogin()}/Config_Saves_PSC')
        with open('ConfigDHCP.txt', 'w+') as dhcpSave:
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.subNetMask}'\
                           f'NetworkIp: {self.networkIp}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpFinal}')

if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
