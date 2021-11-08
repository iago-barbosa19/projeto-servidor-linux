from models.ip import Ip
import os, datetime


class Dhcp(Ip):
    
    def __init__(self, ipv4, gateway, dns1, dns2, subNetMask, dhcpPoolInicial, dhcpPoolFinal) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__dhcpPoolInicial = dhcpPoolInicial
        self.__dhcpPoolFinal = dhcpPoolFinal
        self.__networkIp = self.networkIpSetter(self.ipv4, self.subNetMask)

    @property
    def dhcpPoolInicial(self) -> None:
        return self.__dhcpPoolInicial
    
    @property
    def dhcpPoolFinal(self) -> None:
        return self.__dhcpPoolFinal

    def dhcpConf(self:object) -> None:
        """Método que configura o serviço de DHCP.
        O método configura uma pool DHCP de acordo com os dados que forem inseridos e passados para a classe.
        O arquivo é modificado direto no diretório /etc/dhcp e /etc/default.
        
        """
        os.chdir('/etc/dhcp')
        with open('dhcpd.conf', 'r+') as dhcpConfig:
            lines = 0
            temporaryData = []
            dhcpConfig.seek(0)
            for data in dhcpConfig.readlines():
                temporaryData.append(data)
            for data in temporaryData:
                if f'#DHCP Rede:{self.__networkIp}\n' == data:
                    os.system('echo Essa rede já esta cadastrada.')
                    break
                elif lines == (len(temporaryData) - 1):
                    with open('dhcpd.conf', 'a') as dhcpd:
                        dhcpd.write(f'\n\n#DHCP Rede:{self.networkIp}\nsubnet {self.networkIpSetter(self.ipv4, self.subNetMask)} netmask {self.subNetMask}'\
                                    ' {\n  range'\
                                    f' {self.dhcpPoolInicial} {self.dhcpPoolFinal};\n  option routers {self.gateway};\n  '\
                                    f'option domain-name-servers {self.dns1}, {self.dns2};\n'\
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
        """Função para salvar as configurações em um txt."""
        try:
            os.chdir(f'/home/{os.getlogin()}')
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        with open('ConfigDHCP.txt', 'a+') as dhcpSave:
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.subNetMask}'\
                           f'NetworkIp: {self.networkIp}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpFinal}'\
                           f'\nData da modificação:{datetime.datetime.now()}')

    def __repr__(self):
        print('Os métodos que é possível visualizar as Docstrings:\n\ndhcpConf\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')

if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
