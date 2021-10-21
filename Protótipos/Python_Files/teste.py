from models.ip import Ip

teste = Ip('192.168.1.15', '192.168.1.1', '8.8.8.8', '8.8.4.4', '255.255.0.0')
print(teste.networkIp)