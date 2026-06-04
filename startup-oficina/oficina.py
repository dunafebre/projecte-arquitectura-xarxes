from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def configurar_oficina():
    # Iniciem la xarxa sense controlador extern (mode standalone)
    net = Mininet(switch=OVSSwitch, controller=None)
    
    info('*** [PAS 1] Afegint Host 1 (Servidor) i Host 2 (PC Recepcio)\n')
    # Creem els nodes amb les IPs del teu disseny
    h1 = net.addHost('h1', ip='192.168.100.10/24')
    h2 = net.addHost('h2', ip='192.168.100.20/24')
    
    info('*** Afegint Switch s1 de la oficina\n')
    # El switch apren sol sense necessitat de controlador [cite: 122]
    s1 = net.addSwitch('s1', failMode='standalone')
    
    info('*** Connectant cables virtuals\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    info('*** Engegant la xarxa de la Startup...\n')
    net.start()
    
    info('*** Comprovant connexio interna (pingAll):\n')
    net.pingAll()
    
    # Obrim la consola de Mininet per poder interactuar-hi
    info('*** Entrant a la consola de Mininet. Escriu "exit" per sortir.\n')
    CLI(net)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    configurar_oficina()
