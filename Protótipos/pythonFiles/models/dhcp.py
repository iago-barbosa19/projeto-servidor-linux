from models.ip import Ip
import os, datetime


class Dhcp(Ip):
    
    def __init__(self, ipv4, gateway, dns1, dns2, subNetMask, dhcpPoolInicial, dhcpPoolFinal) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__dhcpPoolInicial = dhcpPoolInicial
        self.__dhcpPoolFinal = dhcpPoolFinal
        self._Ip__networkIpSetter(self._Ip__ipv4, self._Ip__subNetMask)

    @property
    def dhcpPoolInicial(self) -> None:
        return self.__dhcpPoolInicial
    
    @property
    def dhcpPoolFinal(self) -> None:
        return self.__dhcpPoolFinal

    def dhcpConf(self:object) -> None:
        os.chdir('/etc/dhcp')
        with open('dhcpd.conf', 'r') as dhcpConfig:
            lines = 0
            temporaryData = []
            dhcpConfig.seek(0)
            for data in dhcpConfig.readlines():
                temporaryData.append(data)
            for data in temporaryData:
                if f'#DHCP REDE:{self.networkIpSetter(self._Ip__ipv4, self._Ip__subNetMask)}\n' == data:
                    os.system('echo Essa rede já esta cadastrada.')
                    break
                elif lines == (len(temporaryData) - 1):
                    with open('dhcpd.conf', 'a') as dhcpd:
                        dhcpd.write(f'\n\n#DHCP Rede:{self.networkIpSetter(self._Ip__ipv4, self._Ip__subNetMask)}\nsubnet {self.networkIpSetter(self.ipv4, self.subNetMask)} netmask {self.subNetMask}'\
                                        ' {\n  range'\
                                        f' {self.dhcpPoolInicial} {self.dhcpPoolFinal};\n  option routers {self._Ip__gateway};\n  '\
                                        f'option domain-name-servers {self._Ip__dns1}, {self._Ip__dns2};\n'\
                                        '}')
                    dhcpConfig.seek(0)
                
        os.system(f'cp -p /home/{os.getlogin()}/Config_Saves_PSC/dhcpd.conf /etc/dhcp/')
        os.system('cd /etc/default')
        with open('isc-dhcp-server', 'w+') as iscDhcpServer:
            for x in iscDhcpServer.readlines():
                if x == 'INTERFACESv4="enp0s3"\n':
                    pass
                else:
                    iscDhcpServer.write('INTERFACESv4="enp0s3"\n')
                if x == 'INTERFACESv6="enp0s3"':
                    pass
                else:
                    iscDhcpServer.write('INTERFACESv6=""')
        os.system('/etc/init.d/isc-dhcp-server restart')
    
    
    def saveSettings(self:object) -> None:
        try:
            os.chdir(f'/home/{os.getlogin()}')
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        with open('ConfigDHCP.txt', 'a+') as dhcpSave:
            dhcpSave.write(f'IPV4:{self._Ip__ipv4}|Gateway{self._Ip__gateway}|DNS1{self._Ip__dns1}|DNS2{self._Ip__dns2}|Máscara de Sub-Rede{self._Ip__subNetMask}'\
                           f'NetworkIp: {self._Ip__networkIpSetter(self._Ip__ipv4, self._Ip__subNetMask)}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpFinal}'\
                           f'\nData da modificação:{datetime.datetime.now()}')


if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
