import subprocess

class Licence():
    
    def __init__(self:object, ipv4:str):
        pass
    

if __name__ == '__main__':
    interfaces = 'INTERFACESv4="enp0s3, enp0s8"\nINTERFACESv6=""'
    interfaces = interfaces.split("\n")[0]
    cmd = subprocess.Popen("ifconfig" ,stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
    if interfaces.split('"')[1]:
        print(interfaces.split('"')[1])
    