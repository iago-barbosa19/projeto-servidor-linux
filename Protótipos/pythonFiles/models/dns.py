import os, datetime


class Dns():
    
    def __init__(self:object, ipv4:str, subNetMask:str, domain:str, nomeServer: str) -> None:
        self.__ipv4: str = ipv4
        self.__subNetMask: str = subNetMask
        self.__domain:str = domain
        self.__nomeServer:str = nomeServer

    def changeDnsBind9(self:object) -> None:
        """
        Configuração do Serviço DNS por parte do Bind9
        """
        os.chdir('/etc/bind')
        arquivo = self.__domain.split('.')
        try:
            os.system(f'cp -p db.local db.{arquivo[0]}')
        except FileExistsError:
            os.system(f'rm db.{arquivo[0]}')
            os.system(f'cp -p db.local db.{arquivo[0]}')
        with open(f'db.{arquivo[0]}', 'w+') as dbAdminFile:
            dbAdminFile.write(f'\n;\n; BIND data file for local loopback interface\n;\n$TTL    604800\n'\
                            f'@       IN      SOA     {self.__domain}. root.{self.__domain}. (\n'\
                            f'                             2         ; Serial\n'\
                            f'                        604800         ; Refresh\n'\
                            f'                         86400         ; Retry\n'\
                            f'                       2419200         ; Expire\n'\
                            f'                        604800 )       ; Negative Cache TTL\n;\n'\
                            f'@       IN      NS      {self.__domain}.\n@       IN      A       127.0.0.1\n'\
                            f'www     IN      A       {self.__ipv4}\n'\
                            f'ftp     IN      A       {self.__ipv4}')
        with open('named.conf.default-zones', 'a+') as defaultZones:
            for x in list(defaultZones.readlines()):
                if x == f'//Zona {self.__doamin}':
                    pass
                else:
                    defaultZones.write(f'//Zona {self.__domain}\nzone "{self.__domain}" '\
                                    '{\n        type master;\n        '\
                                    f'file "/etc/bind/db.{arquivo[0]}";\n'\
                                    '};')
    
    def changeDnsApache2(self:object) -> None:
        """
        Configuração do Serviço DNS por parte do Apache2.
        """
        arquivo = self.__domain.split('.')
        os.chdir('/etc/apache2/sites-available')
        try:
            os.mkdir('/var/www/sites')
        except FileExistsError:
            pass
        with open(f'{os.getlogin()}.conf', 'w+') as apacheArquivo:
            apacheArquivo.write(f"<VirtualHost *:80>\n        ServerName www.{self.__nomeServer}\n\n        ServerAlias www.{self.__domain}\n        "\
                                f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/sites\n        ErrorLog"\
                                " ${APACHE_LOG_DIR}/error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
            os.system(f'a2ensite {os.getlogin()}.conf')
            
    def dnsConf(self:object) -> None:
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
        with open('saveDNS.txt', 'a+') as save:
            save.write(f'IPV4:{self.__ipv4}| Máscara de Sub-Rede:{self.__subNetMask}|\n'\
                       f'Domínio:{self.__domain}| Prefixo:{self.__prefix}|\nData da modificação:'\
                        f'{datetime.datetime.now()}')
        os.system('echo A configuração foi salva com sucesso')


if __name__ == '__main__':
    raise NotImplementedError('Esse arquivo não pode ser inicializado como principal')
