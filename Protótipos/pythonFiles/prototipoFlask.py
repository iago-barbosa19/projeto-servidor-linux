import secrets
from flask import Flask, redirect, render_template, session, url_for, make_response, request
from secrets import token_hex
from models.ip import Ip
from models.dns import Dns
from models.dhcp import Dhcp

software = Flask(__name__)
software.secret_key = secrets.token_hex(16)

@software.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if request.form['email'] == 'iagofbarbosa23@gmail.com':
            if request.form['senha'] == 'Senai*123':
                session['username'] = 'Iago'
                return redirect(url_for('home'))

@software.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if request.form['tipoConfig'] == 'configIp':
            if request.form['dnsChoice'] == 'dnsProprio':
                configIp = Ip(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subnetMask'],
                            dns1=request.form['dns1'], dns2=request.form['dns2'])
            else:
                configIp = Ip(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subnetMask'],
                            dns1='8.8.8.8', dns2='8.8.4.4')
            configIp.ipConf()
        elif request.form['tipoConfig'] == 'configDhcp':
            if request.form['dnsChoice'] == 'dnsProprio':
                configDhcp = Dhcp(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subnetMask'],
                            dns1=request.form['dns1'], dns2=request.form['dns2'],
                            dhcpPoolInicial=request.form['dhcpPoolInicial'], dhcpPoolFinal=request.form['dhcpPoolFinal'])
            else:
                configDhcp = Dhcp(ipv4=request.form['ipv4'], gateway=request.form['gateway'], subNetMask=request.form['subnetMask'],
                            dns1='8.8.8.8', dns2='8.8.4.4',
                            dhcpPoolInicial=request.form['dhcpPoolInicial'], dhcpPoolFinal=request.form['dhcpPoolFinal'])
            configDhcp.dhcpConf()
        elif request.form['tipoConfig'] == 'configDns':
            configDns = Dns(ipv4=request.form['ipv4'], domain=request.form['domain'], serverName=request.form['serverName'])
            configDns.dnsConf()
    