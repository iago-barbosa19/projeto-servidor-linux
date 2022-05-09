from time import sleep
import os
import datetime
import tqdm


class Dns():
    
    def __init__(self:object, ipv4:str, sub_net_mask:str, domain:str, server_name: str, logger: object) -> None:
        self.__ipv4:str = ipv4
        self.__sub_net_mask:str = sub_net_mask
        self.log = logger
        self.__domain:str = domain
        self.__server_name:str = serverName

    def change_dns_bind9(self:object) -> None:
        """Configuração do serviço Bind9. Por meio dele que é possível ser feito o NAT.
        Esse serviço seria para a configuração da página local de rede.

        1 - Primeira parte seria a configuração do DNS Zona Direta.
        2 - Segunda parte seria a configuração do DNS Zona Indireta.

        Os arquivos db.local e db.0 respectivamente são copiados para a mesma página, com nomes devidamente alterados. 

        nome_arquivo| A variável domínio é repartida de acordo com a pontuação, separando assim o domínio.
        db.{nome_arquivo[0]}| Ele seria a cópia do nome_arquivo db.local. Usária o indíce 0 da lista. O conteúdo desse indíce seria o nome
        do domínio.


        """
        self.log.info(f'{os.getlogin()} - Configuração do serviço Bind9 iniciada')
        os.chdir('/etc/bind')
        nome_arquivo = self.__domain.split('.')
        try:
            os.system(f'cp -p db.local db.{nome_arquivo[0]}')
            self.log.debug(f'{os.getlogin()} - Arquivo db.{nome_arquivo[0]} criado com sucesso.')
        except FileExistsError:
            self.log.warning(f'{os.getlogin()} - Arquivo db.{nome_arquivo[0]} já existe no sistema. Backup enviado para /etc/bind/backup/')
            if not os.path.exists('/etc/bind/backup/'):
                os.mkdir('./backup')
            os.system(f"cp -p {nome_arquivo[0]} ./backup/{nome_arquivo[0]}")
            os.system(f'rm db.{nome_arquivo[0]}')
            os.system(f'cp -p db.local db.{nome_arquivo[0]}')
            self.log.debug(f'{os.getlogin()} - Arquivo db.{nome_arquivo[0]} criado com sucesso.')
        with open(f'db.{nome_arquivo[0]}', 'w+') as db_admin_file:
            db_admin_file.write(f'\n;\n; BIND data file for local loopback interface\n;\n$TTL    604800\n'\
                            f'@       IN      SOA     {self.__domain}. root.{self.__domain}. (\n'\
                            f'                             2         ; Serial\n'\
                            f'                        604800         ; Refresh\n'\
                            f'                         86400         ; Retry\n'\
                            f'                       2419200         ; Expire\n'\
                            f'                        604800 )       ; Negative Cache TTL\n;\n'\
                            f'@       IN      NS      {self.__domain}.\n@       IN      A       127.0.0.1\n'\
                            f'www     IN      A       {self.__ipv4}\n'\
                            f'ftp     IN      A       {self.__ipv4}\n\n')
        self.log.debug(f'{os.getlogin()} - db.{nome_arquivo[0]} configurado com sucesso')
        with open('named.conf.default-zones', 'r') as default_zones:
            lines = 0
            temporary_data = []
            for data in default_zones.readlines():
                temporary_data.append(data)
            for check_datas in temporary_data:
                    if check_datas == f'// zona {self.__domain}\n':
                        self.log.warning(f'{os.getlogin()} - A zona {self.__domain} já foi cadastrada')
                        break
                    elif lines == (len(temporary_data) - 1):
                        with open('named.conf.default-zones', 'a') as default_zones1:
                            default_zones1.write(f'// zona {self.__domain}\nzone "{self.__domain}" '\
                                            '{\n        type master;\n        '\
                                            f'file "/etc/bind/db.{nome_arquivo[0]}";\n'\
                                            '};\n')
                    lines += 1
            os.system('clear')
    
    def change_dns_apache2(self:object) -> None:
        """Configuração do serviço Apache2.
        Por meio desta configuração que é possível que o BIND9 funcione de maneira adequada e acesse sites.

        O método executa cópia o nome_arquivo 000-default.conf para a mesma página, no entanto com o nome do usuário logado.
        Como o nome_arquivo 000-default.conf já tem as permissões pré-definidas durante a instalação do serviço apache2, foi decidido
        copiar o nome_arquivo e alterá-lo, pois desta forma era possível ter certeza de que erros devido à falta de permissões não ocorreriam.

        Após executar a cópia, as alterações começam a serem feitas nela.
        
        Caso o nome_arquivo já exista, é possível sobrescreve-lo, ou deixá-lo intacto.

        Esse método também cria pasta sites, localizada no diretório /etc/www

        Nessa pasta vai ficar guardado a página html index.
        Essa vai ser a página principal do DNS.
        """
        self.log.info(f'{os.getlogin()} - Iniciada a configuração do serviço Apache2')
        nome_arquivo = self.__domain.split('.')
        os.chdir('/etc/apache2/sites-available')
        try:
            os.system(f'cp -p ./000-default.conf ./{nome_arquivo[0]}.conf')
        except FileExistsError:
            self.log.debug(f'{os.getlogin()} - O arquivo {nome_arquivo[0]} já existe. Ele será enviado para /etc/apache2/sites-available/backup')
            if not os.path.exists('/etc/apache2/sites-available/backup/'):
                os.mkdir('./backup')
            os.system(f'cp -p db.{nome_arquivo[0]} ./backup')
        try:
            os.mkdir('/var/www/sites')  # Pasta padrão. Como é para testes, vai continuar assim.
            self.log.debug(f'{os.getlogin()} - Pasta para armazenar as páginas Web criada com sucesso')
            # Talvez o usuário tenha opção de decidir a pasta mais para frente.
        except FileExistsError:
            pass
        with open('/var/www/sites/index.html', 'w') as index:
            index.write('<html>\n<meta charset="utf-8"><head>\n<title>Index</title>\n</head>\n<body>\n<h1 style="color: #333; font-size:1.5rem;'\
                        'margin: 500px; ">Página Principal funcionando</h1>\n</body>\n</html>')
        try:
            with open(f'{nome_arquivo[0]}.conf', 'w+') as apache_arquivo:
                apache_arquivo.write(f"<VirtualHost *:80>\n        ServerName www.{self.__server_name}\n\n        ServerAlias www.{self.__domain}\n        "\
                                    f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/sites\n        ErrorLog"\
                                    " ${APACHE_LOG_DIR}/error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
            self.log.debug(f'{os.getlogin()} - O arquivo {nome_arquivo[0]}.conf foi configurado com sucesso')
        except FileExistsError:
            self.log.warning(f'{os.getlogin()} - O arquivo {nome_arquivo[0]}.conf já existe no diretório /etc/apache2/sites-available')
            print(f'O arquivo já existe. Gostaria mesmo assim de sobrescreve-lo?\n')
            opc = input('y\n ->')
            if opc == 'y':
                with open(f'{nome_arquivo[0]}.conf', 'w+') as apache_arquivo:
                    apache_arquivo.write(f"<VirtualHost *:80>\n        ServerName www.{self.__server_name}\n\n        ServerAlias www.{self.__domain}\n        "\
                                        f"ServerAdmin webmaster@localhost\n        DocumentRoot /var/www/sites\n        ErrorLog"\
                                        " ${APACHE_LOG_DIR}/error.log\n        CustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
                    self.log.debug(f'{os.getlogin()} - O arquivo {nome_arquivo[0]}.conf foi sobreescrito com sucesso')
            else:
                self.log.debug(f'{os.getlogin()} - Arquivo já existente mantido')
                pass
        os.system(f'a2ensite {nome_arquivo[0]}.conf')
        self.log.debug(f'{os.getlogin()} - O arquivo {nome_arquivo[0]}.conf foi configurado com sucesso')
        # self.save_settings()
        os.system('clear')
            
    def dns_conf(self:object) -> None:
        """Função que inicializa as configurações do DNS. 
        Ela inicializa os métodos de configuração de cada um dos serviços.
        Esse método que é chamado para configurar o DNS no geral."""
        self.log.info(f"{os.getlogin()} - Configuração dos serviços DNS iniciada")
        self.change_dns_bind9()
        self.change_dns_apache2()
        os.system('systemctl restart bind9')
        os.system('systemctl restart apache2')
        
    def save_settings(self:object) -> None:
        """Método para salvar as configurações que foram feitas até então.
        Aqui salva todas as informaçãos das da configuração DNS, para seber quando foram modificadas, e para o que foram modificadas, para que assim seja
        possível ter uma espécie de backup de configurações passadas e qual usuário mudou elas."""
        if os.path.exists('/etc/psc'):
            pass
        else:
            os.system("mkdir /etc/psc")
        if os.path.exists('/etc/psc/configs'):
            pass
        else:
            os.system(f"mkdir /etc/psc/configs")
        with open('/etc/psc/configs/saveConfigDNS.txt', 'a') as save:
            save.write(f'IPV4:{self.__ipv4}| Máscara de Sub-Rede:{self.__sub_net_mask}|\n'\
                        f'Domínio:{self.__domain}|\nData da modificação:'\
                        f'{datetime.datetime.now()}\nUsuário que alterou a configuração:{os.getlogin()}\n\n')


if __name__ == '__main__':
    raise NotImplementedError('\nErro de Inicialização. \nInicialize o arquivo principal para o funcionamento correto.')
