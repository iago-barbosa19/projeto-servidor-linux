from models.ip import Ip
import os, datetime
from time import sleep

class Dhcp(Ip):
    
    def __init__(self: object,  ipv4: str, gateway: str, dns1: str, dns2: str, sub_net_mask: str, dhcp_pool_inicial: str, dhcp_pool_final: str) -> None:
        super().__init__(ipv4, gateway, dns1, dns2, sub_net_mask)
        self.__dhcp_pool_inicial: str = dhcp_pool_inicial
        self.__dhcp_pool_final: str = dhcp_pool_final
        self.__network_ip: str = self.network_ipSetter(self.ipv4, self.sub_net_mask)

    @property
    def dhcp_pool_inicial(self) -> None:
        return self.__dhcp_pool_inicial
    
    @property
    def dhcp_pool_final(self) -> None:
        return self.__dhcp_pool_final

    def dhcpConf(self:object) -> None:
        """Método que configura o serviço de DHCP.
        O método configura uma pool DHCP de acordo com os dados que forem inseridos e passados para a classe.
        O arquivo é modificado direto no diretório /etc/dhcp e /etc/default.    
        """
        os.chdir('/etc/dhcp')
        if not os.path.exists('/etc/psc/saveConfigDHCP.txt'):
            with open('dhcpd.conf', 'a') as dhcpd:
                dhcpd.write('authoritative;\n')
        with open('dhcpd.conf', 'r+') as dhcp_config:  # Configuração do Arquivo DHCPD.conf no diretório: /etc/dhcp
            lines = 0
            temporary_data = []
            dhcp_config.seek(0)
            for data in dhcp_config.readlines():
                temporary_data.append(data)
            for data in temporary_data:
                if f'#DHCP Rede:{self.__network_ip}\n' == data:
                    os.system('echo Essa rede já esta cadastrada.')
                    break
                elif lines == (len(temporary_data) - 1):
                    with open('dhcpd.conf', 'a') as dhcpd:
                        dhcpd.write(f'\n\n#DHCP Rede:{self.network_ip}\nsubnet {self.network_ipSetter(self.ipv4, self.sub_net_mask)} netmask {self.sub_net_mask}'\
                                    ' {\n  range'\
                                    f' {self.dhcp_pool_inicial} {self.dhcp_pool_final};\n  option routers {self.gateway};\n  '\
                                    f'option domain-name-servers {self.dns1}, {self.dns2};\n'\
                                    '}')
                    dhcp_config.seek(0)
                lines += 1
        os.chdir('/etc/default')
        with open('isc-dhcp-server', 'w') as iscDhcpServer:
            iscDhcpServer.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""')
        os.system('echo Configuração efetuada com sucesso!')
        sleep(2)
        os.system('systemctl restart isc-dhcp-server')
        # self.saveSettings()
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
            dhcpSave.write(f'IPV4:{self.ipv4}|Gateway{self.gateway}|DNS1{self.dns1}|DNS2{self.dns2}|Máscara de Sub-Rede{self.sub_net_mask}'\
                            f'network_ip: {self.network_ip}|Pool Inicial do DHCP:{self.dhcp_pool_inicial}|Pool Final do DHCP:{self.dhcp_pool_final}'\
                            f'\nData da modificação:{datetime.datetime.now()}\nUsuário que alterou a configuração:{os.getlogin()}\n\n')

    def __repr__(self) :
        print('Os métodos que é possível visualizar as Docstrings:\n\ndhcpConf\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')
 
 
if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
