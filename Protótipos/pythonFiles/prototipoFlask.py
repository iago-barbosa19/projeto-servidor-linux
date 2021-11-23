import os
from flask import Flask, redirect, render_template, session, url_for, request
from secrets import token_hex
from models.ip import Ip
from models.dns import Dns
from models.dhcp import Dhcp

software = Flask(__name__)
software.secret_key = token_hex(16)


@software.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if request.form['email'] == 'iagofbarbosa23@gmail.com':
            if request.form['senha'] == 'Senai*123':
                session['username'] = 'Iago'
                return redirect(url_for('home'))
        return render_template('loginIncorreto.html')
        

@software.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
        
    
@software.route('/alterar', methods=['POST'])
def alterar():
    if request.method == 'POST':
        if request.form['tipoConfig'] == 'configIp':
                if request.form['dnsChoice'] == 'dnsProprio':
                    configIp = Ip(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subNetMask'],
                                dns1=request.form['dns1'], dns2=request.form['dns2'])
                else:
                    configIp = Ip(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subNetMask'],
                                dns1='8.8.8.8', dns2='8.8.4.4')
                configIp.ipConfAlt()
                os.system('systemctl restart networking')
                os.system('systemctl restart apache2')
        elif request.form['tipoConfig'] == 'configDhcp': 
            if request.form['dnsChoice'] == 'dnsProprio': 
                configDhcp = Dhcp(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subNetMask'],
                                    dns1=request.form['dns1'], dns2=request.form['dns2'],
                                dhcpPoolInicial=request.form['rangeInicial'], dhcpPoolFinal=request.form['rangeFinal'])
            else:
                configDhcp = Dhcp(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subNetMask'],
                            dns1='8.8.8.8', dns2='8.8.4.4',
                            dhcpPoolInicial=request.form['rangeInicial'], dhcpPoolFinal=request.form['rangeFinal'])
            configDhcp.dhcpConf()
            os.system('systemctl restart isc-dhcp-server')
        else: # Configuracao do DNS
            configDns = Dns(ipv4=request.form['ipv4'], subNetMask=request.form['subNetMask'], domain=request.form['domain'], serverName=request.form['serverName'])
            configDns.dnsConf()
            os.system('systemctl restart bind9')
            os.system('systemctl restart apache2')
        return redirect(url_for('home'))
        

@software.route('/visuDados')
def VisuDados():
    """"
    Codigo inicial para montar um possivel gerador de tabelas. 
    Seria necessario um arquivo CSV para a melhor qualidade de arquivos e dados, porem, isso serve somente para o prototipo
    code: 
    teste = None
    arquivo = None
    arq = None
    
    with open("./static/saves/saveConfigIp.txt", 'r') as arq:
        teste = arq.read()
    with open("./templates/teste.html", 'r') as arq:
        arquivo = arq.read()
        with open('./templates/uso.html', 'w+') as temp:
            temp.write(arquivo)
            temp.write(f'\n<p>{teste}</p>\n</div>\n</body>\n</html>')
    with open('./templates/uso.html', 'r') as teste:
        arq = teste.read()"""
    return render_template('dados.html')


@software.route('/forgotPass', methods=[ 'GET', 'POST'])
def forgotPass():
    if request.method == 'GET':
        return render_template('forgotPass.html')
    else:
        return render_template('forgotPassEnv.html')


if __name__ == '__main__':
    software.run()