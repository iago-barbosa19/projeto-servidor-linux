import os, sys
from ip import Ip

class Dns(Ip):
    
    def __init__(self:object, ipv4:str, subNetMask:str, networkIp:str, domain:str, prefix:str, serverAlias:str) -> None:
        super().__init__(ipv4, subNetMask, networkIp)
        self.__domain:str = domain
        self.__prefix:str = prefix
        self.__serverAlias:str = serverAlias

    def changeDnsBind9(self:object) -> None:
        """
        Configuração do Serviço DNS por parte do Bind9
        """
        arquivo = self.__domain.split('.')
        try:
            os.mknod(f'db.{arquivo[0]}')
        except FileExistsError:
            os.system(f'rm db.{arquivo[0]}')
            os.mknod(f'db.{arquivo[0]}')
        with open(f'db.{arquivo[0]}', 'r') as dbAdminFile:
            dbAdminFile.write(f'\n;\n\n; BIND data file for local loopback interface\n;\n$TTL     604800\n'\
                            f'@      IN     SOA      {self.__domain}. root.{self.__domain}. (\n'\
                            f'                              2         ; Serial\n'\
                            f'                         604800         ; Refresh\n'\
                            f'                          86400         ; Retry\n'\
                            f'                        2419200         ; Expire\n'\
                            f'                         604800 )       ; Negative Cache TTL\n;\n'\
                            f'@       IN      NS      {self.__domain}.\n@       IN      A       127.0.0.1\n'\
                            f'www     IN       A      {self.ipv4}\n'\
                            f'ftp     IN       A      {self.ipv4}')
        os.system(f'cp -p db.{arquivo[0]} /etc/bind')
        try:                              
            os.mknod('named.conf.default-zones')
        except FileExistsError:
            os.system('rm named.conf.default-zones')
            os.mknod('named.conf.default-zones')
        with open('named.conf.default-zones', 'r+') as defaultZones:
            defaultZones.write('zone "." {\n        type master;\n        file "usr/share/dns/root.hints";\n};\n'\
                            'zone "localhost\n        typemaster;\n        file "etc/bind/db.local;\n};\n'\
                            'zone "127.inaddr.arpa" {\n        type master;\n        file "/etc/bind/db/127";\n};\n'\
                            'zone  "0.in-addr.arpa" {\n        type master;\n        file "/etc/bind/db.0";\n};\n'\
                            'zone "255.in-addr.arpa {\n        type master;\n        file "/etc/bind/db.255";\n};\n'\
                            f'zone "{self.__domain}'\
                            ' {        type master;\n        '\
                            f'file "/etc/bind/db.{arquivo[0]}";\n'\
                            '};')
        os.system('cp -p named.conf.default-zones /etc/bind')
    
    def changeDnsApache2(self:object) -> None:
        """
        Configuração do Serviço DNS por parte do Apache2.
        """
        arquivo = self.__domain.split('.')
        try:
            os.mknod(f'{os.getlogin()}.conf')
        except FileExistsError:
            os.system(f'rm {os.getlogin()}.conf')
            os.mknod(f'{os.getlogin()}.conf')
        with open(f'{os.getlogin()}.conf', 'r+') as apacheArquivo:
            apacheArquivo.write(f"<VirtualHost *:80>\n        ServerName www.{arquivo[0]}\n\n        ServerAlias www.{self.__domain}\n        "\
                                f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/html\n        ErrorLog"\
                                " ${APACHE_LOG_DIR}\error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost")
            os.system(f'cp -p {os.getlogin()}.conf /etc/apache2/sites-available')
            os.system(f'rm {os.getlogin()}.conf')
            os.chdir('/etc/apache2/sites-available')
            os.system(f'a2ensite {os.getlogin()}.conf')
            
    def configDns(self:object) -> None:
        """Função que vai efetuar a configuração do DNS"""
        self.changeDnsBind9()
        self.changeDnsApache2()
        os.system("/etc/init.d/apache2 restart")
        os.system("/etc/init.d/bind9 restart")
        os.system('echo Serviço concluído.')
        
    def saveSettings(self:object) -> None:
        """Função para salvar as configurações em um txt."""
        os.chdir(f'/home/{os.getlogin()}')
        try:
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            os.chdir(f'{os.getcwd()}/Config_Saves_PSC')
        with open('saveDNS.txt', 'x+') as save:
            save.write(f'IPV4:{self.ipv4}| Máscara de Sub-Rede:{self.subNetMask}| NetworkIp:{self.networkIp}|\n'\
                       f'Domínio:{self.__domain}| Prefixo:{self.__prefix}| ServerAlias:{self.__serverAlias}|')
        os.system('echo A configuração foi salva com sucesso')

if __name__ == '__main__':
    raise NotImplementedError('Esse arquivo não pode ser inicializado como principal')
