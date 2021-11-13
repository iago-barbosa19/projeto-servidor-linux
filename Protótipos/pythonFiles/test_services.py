import os
import unittest
from models.ip import Ip
from models.dns import Dns
from models.dhcp import Dhcp

class TestServices(unittest.TestCase):
    
    def setUp(self:object) -> None:
        self.dns = Dns(ipv4='192.168.15.15', domain='teste.com.br', nameServer='serverteste.com', subNetMask='255.255.255.0')
        self.ipv4 = Ip(ipv4='192.168.15.15', gateway='192.168.15.1', dns1='192.168.15.15', dns2='8.8.8.8', subNetMask='255.255.255.0')
        self.dhcpv4 = Dhcp(ipv4='192.168.15.15', gateway='192.168.15.1', dns1='192.168.15.15', dns2='8.8.8.8', subNetMask='255.255.255.0',\
                           dhcpPoolInicial='192.168.15.50', dhcpPoolFinal='192.168.15.60')
    
    def test_ip(self:object) -> None:
        self.ipv4.ipConf()
        self.ipv4.saveSettings()
        os.system('systemctl restart networking')
        
    def test_dns(self:object) -> None:
        self.dns.dnsConf()
        self.dns.saveSettings()
        os.system('systemctl restart bind9')
        os.system('systemctl restart apache2')
        
    def test_dhcpv4(self:object) -> None:
        self.dhcpv4.dhcpConf()
        self.dhcpv4.saveSettings()
        os.system('systemctl restart isc-dhcp-server')

    def tearDown(self:object):
        os.system('echo \nO teste foi efetuado. Verifique os resultados.')


if __name__ == '__main__':
    unittest.main()
 