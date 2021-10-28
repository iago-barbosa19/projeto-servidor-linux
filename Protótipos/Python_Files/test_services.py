import os
import unittest
from models.ip import Ip
from models.dns import Dns
from models.dhcp import Dhcp

class TestServices(unittest.TestCase):
    
    def setUp(self:object):
        dns = Dns(ipv4='192.168.15.15', domain='teste.com.br', nomeServer='serverteste.com', subNetMask='255.255.255.0')
        ipv4 = Ip(ipv4='192.168.15.15', gateway='192.168.15.1', dns1='192.168.15.15', dns2='8.8.8.8', subNetMask='255.255.255.0')
        dhcpv4 = Dhcp(ipv4='192.168.15.15', gateway='192.168.15.1', dns1='192.168.15.15', dns2='8.8.8.8', subNetMask='255.255.255.0',\
                      dhcpPoolInicial='192.168.15.50', dhcpPoolFinal='192.168.15.60')
    
    def test_ip(self:object):
        pass

    def test_dns(self:object):
        pass

    def test_dhcpv4(self:object):
        pass

    def tearDown(self:object):
        os.system('echo o teste foi efetuado. Verifique os resultados.')


if __name__ == '__main__':
    unittest.main()