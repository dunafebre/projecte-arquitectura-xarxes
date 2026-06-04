
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def topologia():

    net = Mininet(switch=OVSSwitch, controller=None)

    info('*** SWITCH CENTRAL\n')
    s1 = net.addSwitch('s1', failMode='standalone')

    # =========================
    # SERVIDORES WEB (ESCALADO)
    # =========================
    web_servers = []

    for i in range(1, 4):   #3 servidores para el Load Balancer
        srv = net.addHost(
            f'web{i}',
            ip=f'192.168.100.{10+i}/24'
        )
        net.addLink(srv, s1)
        web_servers.append(srv)
        info(f'*** Web server web{i}\n')

    # =========================
    # LOAD BALANCER
    # =========================
    lb = net.addHost('lb', ip='192.168.100.200/24')
    net.addLink(lb, s1)
    info('*** Load Balancer\n')

    # =========================
    # BASE DE DATOS (PRIVADA)
    # =========================
    db = net.addHost('db', ip='192.168.100.50/24')
    net.addLink(db, s1)
    info('*** Database server (privado)\n')

    # =========================
    # CLIENTES (BLACK FRIDAY)
    # =========================
    for i in range(1, 31):
        cli = net.addHost(
            f'cli{i}',
            ip=f'192.168.100.{100+i}/24'
        )
        net.addLink(cli, s1)

    net.start()

    info('\n*** TEST CONNECTIVITY\n')
    net.pingAll()

    info('\n*** INFRAESTRUCTURA LISTA\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topologia()

