from models.ip import Ip
import os, datetime


class Dhcp(Ip):
    
    def __init__(self, ipv4, gateway, dns1, dns2, subNetMask, dhcpPoolInicial, dhcpPoolFinal) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__networkIp = self.networkIpSetter(self.ipv4, self.subNetMask)
        self.__dhcpPoolInicial = dhcpPoolInicial
        self.__dhcpPoolFinal = dhcpPoolFinal

    @property
    def dhcpPoolInicial(self) -> None:
        return self.__dhcpPoolInicial
    
    @property
    def dhcpPoolFinal(self) -> None:
        return self.__dhcpPoolFinal

    def dhcpConf(self:object) -> None:
        try:
            os.chdir(f'/home/{os.getlogin()}/')
            os.mkdir('Config_Saves_PSC')
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        try:
            os.system(f'cp -p /etc/dhcp/dhcpd.conf /home/{os.getlogin()}/Config_Saves_PSC/')
        except FileExistsError:
            os.system('rm dhcpd.conf')
            os.system(f'cp -p /etc/dhcp/dhcpd.conf /home/{os.getlogin()}/Config_Saves_PSC/')
        with open('dhcpd.conf', 'a+') as dhcpConfig:
            dhcpConfig.seek(0)
            teste = dhcpConfig.read()
            if f'#DHCP REDE:{self.__networkIP}' in teste:
                os.system('echo Essa rede já esta cadastrada.')
                dhcpConfig.seek(0)
            else:
                dhcpConfig.write(f'\n\n#DHCP Rede:{self.__networkIp}\nsubnet {self.__networkIp} netmask {self.subNetMask}'\
                                ' {\n  range'\
                                f' {self.dhcpPoolInicial} {self.dhcpPoolFinal};\n  option routers {self.gateway};\n  '\
                                f'option domain-name-servers {self.dns1}, {self.dns2};\n'\
                                '}')
                dhcpConfig.seek(0)
        os.system(f'cp -p /home/{os.getlogin()}/Config_Saves_PSC/dhcpd.conf /etc/dhcpd')
        os.system('/etc/init.d/isc-dhcp-server restart')
        os.system('cd /etc/default')
        with open('isc-dhcp-server', 'w') as iscDhcpServer:
            iscDhcpServer.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""')


    def saveSettings(self:object) -> None:
        try:
            os.chdir(f'/home/{os.getlogin()}')
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        with open('ConfigDHCP.txt', 'a+') as dhcpSave:
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.subNetMask}'\
                           f'NetworkIp: {self.__networkIp}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpFinal}'\
                           f'\nData da modificação:{datetime.datetime.now()}')


if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
