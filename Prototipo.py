import sys, os


def installServices():
    """Classe que vai executar a instalação dos serviços desejados.
    Os serviços que são abraangidos são:
    IP, DHCP e DNS (talvez o SAMBA)"""
    print('Esse serviço ainda não está disponível.\nEntre em contato com o suporte.')
    sys.wait(5)


def confServer():
    """Classe que vai executar a Configuração dos serviços desejados.
    Os serviços que são abraangidos são:
    IP, DHCP e DNS (talvez SAMBA)"""
    while True != False:
        op = int(input('O que você deseja configurar:\n1)IP\n2)DHCP\n3)DNS\nR:'))
        if(op == 1):
            os.chdir(f'/home/{os.getlogin()}')
            os.mknod('interfaces')
            ip = input('Insira o IP do computador: ')
            sub_mask = input('Insira a máscara de sub-rede: ')
            gateway = input('Insira o Gateway: ')
            op2 = int(input('Deseja inserir o DNS, ou usar o padrão?\n1)Inserir DNS\n2)Padrão\nR:'))
            if op2 == 1: 
                dns1 = input('Insira o DNS primário: ')
                dns2 = input('Insira o DNS primário: ')
                dns = f'{dns1} {dns2}'
            else:
                dns = '8.8.8.8 8.8.4.4'
            network = f'{ip.split(".")[0]}.{ip.split(".")[1]}.{ip.split(".")[2]}.0'
            with open('interfaces', 'r+') as arq:
                arq.write('source /etc/network/interfaces.d/*\n'\
                    'auto lo\n\niface auto lo inet loopback\n'\
                    f'address {ip}\nnetmask {sub_mask}\n'\
                    f'network {network}\ngateway {gateway}\ndns-server {dns}')
            os.system('cp -p interfaces /etc/network')
            os.system('rm interfaces')
            print('Executado com sucesso')
        else:
            print('Esse serviço ainda não está disponível.\nEntre em contato com o suporte.\nVoltando para tela inicial.')
            sys.wait(5)


if __name__ == '__main__':
    while True != False:
        try:
            op = int(input("----------------------------- PSC ------------------------------"\
                        "\n---------------- Insira o que você deseja fazer ----------------\n"\
                        " 1)Instalar serviços\n 2)Configurar serviços \n 3)Sair\nR:"))  
            if op == 1:
                os.system('clear')
                installServices()
            elif op == 2:
                os.system('clear')
                confServer()
            elif op == 3:
                os.system('clear')
                sys.exit(1)
            else:
                os.system('clear')
                print('Comando inválido!')
        except ValueError:
            print('Comando inválido!')
            sys.wait(2)
            os.system('clear')
