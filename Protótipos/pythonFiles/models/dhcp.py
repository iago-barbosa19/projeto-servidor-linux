from models.ip import Ip
import os, datetime
from time import sleep

class Dhcp(Ip):
    
    def __init__(self: object,  ipv4: str, gateway: str, dns1: str, dns2: str, subNetMask: str, dhcpPoolInicial: str, dhcpPoolFinal: str) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, subNetMask)
        self.__dhcpPoolInicial: str = dhcpPoolInicial
        self.__dhcpPoolFinal: str = dhcpPoolFinal
        self.__networkIp: str = self.networkIpSetter(self.ipv4, self.subNetMask)

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
        if not os.path.exists('/etc/psc/configDHCP.txt'):
            with open('dhcpd.conf', 'a') as dhcpd:
                dhcpd.write('authoritative;\n')
        with open('dhcpd.conf', 'r+') as dhcpConfig:  # Configuração do Arquivo DHCPD.conf no diretório: /etc/dhcp
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
        os.chdir('/etc/default')
        with open('isc-dhcp-server', 'w') as iscDhcpServer:
            iscDhcpServer.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""')
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
        with open('/etc/psc/configs/saveConfigDHCP.txt', 'a') as dhcpSave:
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.subNetMask}'\
                            f'NetworkIp: {self.networkIp}|Pool Inicial do DHCP:{self.dhcpPoolInicial}|Pool Final do DHCP:{self.dhcpPoolFinal}'\
                            f'\nData da modificação:{datetime.datetime.now()}\nUsuário que alterou a configuração:{os.getlogin()}\n\n')

    def __repr__(self) :
        print('Os métodos que é possível visualizar as Docstrings:\n\ndhcpConf\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')
 
 
if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
