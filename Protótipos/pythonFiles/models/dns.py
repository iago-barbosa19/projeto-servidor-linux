
import os, datetime


class Dns():
    
    def __init__(self:object, ipv4:str, subNetMask:str, domain:str, serverName: str) -> None:
        self.__ipv4:str = ipv4
        self.__subNetMask:str = subNetMask
        self.__domain:str = domain
        self.__nameServer:str = serverName

    def changeDnsBind9(self:object) -> None:
        """Configuração do serviço Bind9. Por meio dele que é possível ser feito o NAT.
        Esse serviço seria para a configuração da página local de rede.

        1 - Primeira parte seria a configuração do DNS Zona Direta.
        2 - Segunda parte seria a configuração do DNS Zona Indireta.

        Os arquivos db.local e db.0 respectivamente são copiados para a mesma página, com nomes devidamente alterados. 

        nomeArquivo| A variável domínio é repartida de acordo com a pontuação, separando assim o domínio.
        db.{nomeArquivo[0]}| Ele seria a cópia do nomeArquivo db.local. Usária o indíce 0 da lista. O conteúdo desse indíce seria o nome
        do domínio.


        """
        os.chdir('/etc/bind')
        nomeArquivo = self.__domain.split('.')
        try:
            os.system(f'cp -p db.local db.{nomeArquivo[0]}')
        except FileExistsError:
            os.system(f'rm db.{nomeArquivo[0]}')
            os.system(f'cp -p db.local db.{nomeArquivo[0]}')
        with open(f'db.{nomeArquivo[0]}', 'w+') as dbAdminFile:
            dbAdminFile.write(f'\n;\n; BIND data file for local loopback interface\n;\n$TTL    604800\n'\
                            f'@       IN      SOA     {self.__domain}. root.{self.__domain}. (\n'\
                            f'                             2         ; Serial\n'\
                            f'                        604800         ; Refresh\n'\
                            f'                         86400         ; Retry\n'\
                            f'                       2419200         ; Expire\n'\
                            f'                        604800 )       ; Negative Cache TTL\n;\n'\
                            f'@       IN      NS      {self.__domain}.\n@       IN      A       127.0.0.1\n'\
                            f'www     IN      A       {self.__ipv4}\n'\
                            f'ftp     IN      A       {self.__ipv4}\n\n')
        
        with open('named.conf.default-zones', 'r') as defaultZones:
            lines = 0
            temporaryData = []
            for data in defaultZones.readlines():
                temporaryData.append(data)
            for checkDatas in temporaryData:
                    if checkDatas == f'// zona {self.__domain}\n':
                        os.system('echo Zona já cadastrada')
                        break
                    elif lines == (len(temporaryData) - 1):
                        with open('named.conf.default-zones', 'a') as defaultZones1:
                            defaultZones1.write(f'// zona {self.__domain}\nzone "{self.__domain}" '\
                                            '{\n        type master;\n        '\
                                            f'file "/etc/bind/db.{nomeArquivo[0]}";\n'\
                                            '};\n')
                    lines += 1
            os.system('clear')
    
    def changeDnsApache2(self:object) -> None:
        """Configuração do serviço Apache2.
        Por meio desta configuração que é possível que o BIND9 funcione de maneira adequada e acesse sites.

        O método executa cópia o nomeArquivo 000-default.conf para a mesma página, no entanto com o nome do usuário logado.
        Como o nomeArquivo 000-default.conf já tem as permissões pré-definidas durante a instalação do serviço apache2, foi decidido
        copiar o nomeArquivo e alterá-lo, pois desta forma era possível ter certeza de que erros devido à falta de permissões não ocorreriam.

        Após executar a cópia, as alterações começam a serem feitas nela.
        
        Caso o nomeArquivo já exista, é possível sobrescreve-lo, ou deixá-lo intacto.

        Esse método também cria pasta sites, localizada no diretório /etc/www

        Nessa pasta vai ficar guardado a página html index.
        Essa vai ser a página principal do DNS.
        """
        os.chdir('/etc/apache2/sites-available')
        try:
            os.mkdir('/var/www/sites')  # Pasta padrão. Talvez eu dê a opção para o usuário eventualmente.
        except FileExistsError:
            pass
        with open('/var/www/sites/index.html', 'w') as index:
            index.write('<html>\n<meta charset="utf-8"><head>\n<title>Index</title>\n</head>\n<body>\n<h1 style="color: #333; font-size:1.5rem;'\
                        'margin: 500px; ">Página Principal funcionando</h1>\n</body>\n</html>')
        try:
            os.system(f'cp -p ./000-default.conf ./{os.getlogin()}.conf')
            with open(f'{os.getlogin()}.conf', 'w+') as apacheArquivo:
                apacheArquivo.write(f"<VirtualHost *:80>\n        ServerName www.{self.__nameServer}\n\n        ServerAlias www.{self.__domain}\n        "\
                                    f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/sites\n        ErrorLog"\
                                    " ${APACHE_LOG_DIR}/error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
                os.system(f'a2ensite {os.getlogin()}.conf')
        except FileExistsError:
            os.system(f'echo O nomeArquivo já existe. Gostaria mesmo assim de sobrescreve-lo?\ny/n')
            if opc:= input() == 'y':
                with open(f'{os.getlogin()}.conf', 'w+') as apacheArquivo:
                    apacheArquivo.write(f"<VirtualHost *:80>\n        ServerName www.{self.__nameServer}\n\n        ServerAlias www.{self.__domain}\n        "\
                                        f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/sites\n        ErrorLog"\
                                        " ${APACHE_LOG_DIR}/error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
                os.system(f'a2ensite {os.getlogin()}.conf')
            else:
                pass
        os.system('clear')
            
    def dnsConf(self:object) -> None:
        """Função que inicializa as configurações do DNS. 
        Ela inicializa os métodos de configuração de cada um dos serviços.
        Esse método que é chamado para configurar o DNS no geral."""
        self.changeDnsBind9()
        self.changeDnsApache2()
        
    def saveSettings(self:object) -> None:
        """Método para salvar as configurações que foram feitas até então.
        Aqui salva todas as informaçãos das da configuração DNS, para seber quando foram modificadas, e para o que foram modificadas, para que assim seja
        possível ter uma espécie de backup de configurações passadas e qual usuário mudou elas."""
        os.chdir(f'/home/{os.getlogin()}')
        try:
            os.mkdir('Config_Saves_PSC')
        except FileExistsError:
            pass
        finally:
            os.chdir(f'/home/{os.getlogin()}/Config_Saves_PSC')
        try:
            os.mknod('saveConfigDNS.txt')
        except FileExistsError:
            pass
        finally:
            with open('saveConfigDNS.txt', 'a+') as save:
                save.write(f'IPV4:{self.__ipv4}| Máscara de Sub-Rede:{self.__subNetMask}|\n'\
                           f'Domínio:{self.__domain}|\nData da modificação:'\
                           f'{datetime.datetime.now()}\nUsuário que alterou a configuração:{os.getlogin()}\n\n')
            os.system('echo A configuração foi salva com sucesso')
    
    def __repr__(self):
        print('Os métodos que é possível visualizar as Docstrings:\ndnsConf\nchangeDnsApache2\nchangeDnsBind9\nsaveSettings\n\n'\
              'Em casos de dúvidas no uso do programa, consulte-as.')


if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
