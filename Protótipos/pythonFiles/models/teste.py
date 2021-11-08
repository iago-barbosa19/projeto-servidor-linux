with open('isc-dhcp-server', 'r+') as iscDhcpServer:
            for x in iscDhcpServer.readlines():
                if x == 'INTERFACESv4="enp0s3"\n':
                    pass
                else:
                    with open('isc-dhcp-server', 'w') as iscDhcpServer2:
                        iscDhcpServer2.write('INTERFACESv4="enp0s3"\n')
                if x == 'INTERFACESv6="enp0s3"':
                    pass
                else:
                    with open('isc-dhcp-server', 'a') as iscDhcpServer2:
                        iscDhcpServer2.write('INTERFACESv6=""')