from models.ip import Ip
import os, datetime


class Dhcp(Ip):
    
    def __init__(self, ipv4: str, gateway: str, dns1: str, dns2: str, subNetMask: str, dhcpPoolInicial: str, dhcpPoolFinal: str) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__dhcpPoolInicial: str = dhcpPoolInicial
        self.__dhcpPoolFinal: str = dhcpPoolFinal
        self.__networkIp = self.networkIpSetter(self.ipv4, self.subNetMask)

    @property
    def dhcpPoolInicial(self) -> None:
        return self.__dhcpPoolInicial
    
    @property
    def dhcpPoolFinal(self) -> None:
        return self.__dhcpPoolFinal

    def dhcpConf(self:object, dhcpv: int) -> None:
        """Método que configura o serviço de DHCP.
        O método configura uma pool DHCP de acordo com os dados que forem inseridos e passados para a classe.
        O arquivo é modificado direto no diretório /etc/dhcp e /etc/default.
        
        """
        os.chdir('/etc/dhcp')
        if os.path.exists(f'/home/{os.getlogin()}/Config_Saves_PSC/configDHCP.txt') == False:
            with open('dhcpd.conf', 'a') as dhcpd:
                dhcpd.write('authoritative;\n')
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
                lines += 1
        os.system(f'cp -p /home/{os.getlogin()}/Config_Saves_PSC/dhcpd.conf /etc/dhcp/')
        os.chdir('/etc/default')
        with open('isc-dhcp-server', 'w') as iscDhcpServer:
            iscDhcpServer.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""')
    
    def saveSettings(self:object) -> None:
        """Função para salvar as configurações em um txt."""
        try:
            os.chdir(f'/home/{os.getlogin()}')
            os.mkdir('Config_Saves_PSC')
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        
        with open('ConfigDHCP.txt', 'a+') as dhcpSave:
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.subNetMask}'\
                           f'NetworkIp: {self.networkIp}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpPoolFinal}'\
                           f'\nData da modificação:{datetime.datetime.now()}\n')

    def __repr__(self):
        print('Os métodos que é possível visualizar as Docstrings:\n\ndhcpConf\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')

if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
