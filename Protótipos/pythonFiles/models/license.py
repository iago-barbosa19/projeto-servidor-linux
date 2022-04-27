import subprocess

class Licence():
    
    def __init__(self:object, ipv4:str):
        pass
    

if __name__ == '__main__':
    result = subprocess.run(['ipconfig', '/all'], shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout
    for x in result.split(':'):
        if x == "Endere‡o F¡sico":
            print(x)
    pass