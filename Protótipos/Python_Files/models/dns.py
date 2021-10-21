import os, sys
from ip import Ip

class Dns(Ip):
    
    def __init__(self:object, ipv4:str, subNetMask:str, networkIp:str, domain:str, prefix:str, serverAlias:str) -> None:
        super().__init__(ipv4, subNetMask, networkIp)
        self.__domain:str = domain
        self.__prefix:str = prefix
        self.__serverAlias:str = serverAlias

    def changeDns(self:object) -> None:
        """Parte que Configura o DNS"""
        try:
            os.mknod('db.admin')
        except FileExistsError:
            os.system('rm db.admin')
            os.mknod('db.admin')
            with open('db.admin', 'r') as dbAdminFile:
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
        """
        GNU nano 3.2                                                               /etc/bind/named.conf.default-zones                                                                          

// prime the server with knowledge of the root servers
zone "." {
        type hint;
        file "/usr/share/dns/root.hints";
};

// be authoritative for the localhost forward and reverse zones, and for
// broadcast zones as per RFC 1912

zone "localhost" {
        type master;
        file "/etc/bind/db.local";
};

zone "127.in-addr.arpa" {
        type master;
        file "/etc/bind/db.127";
};

zone "0.in-addr.arpa" {
        type master;
        file "/etc/bind/db.0";
};

zone "255.in-addr.arpa" {
        type master;
        file "/etc/bind/db.255";
};


        """
        with open('named.conf.default-zones') as defaultZones:
            defaultZones.write('zone "." {\n        type master;\n        file "usr/share/dns/root.hints";\n};\n'\
                               'zone "localhost\n        typemaster;\n        file "etc/bind/db.local;\n};\n'\
                               'zone "127.inaddr.arpa" {\n        type master;\n        file "/etc/bind/db/127";\n};\n'\
                               'zone  "0.in-addr.arpa" {\n        type master;\n        file "/etc/bind/db.0";\n};\n'\
                               'zone "255.in-addr.arpa {\n        type master;\n        file "/etc/bind/db.255";\n};\n'\
                               f'zone "{self.__domain}'\
                               ' {        type master;\n        file "/etc/bind//db.senai";\n};')
    def saveSettings(self):
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
