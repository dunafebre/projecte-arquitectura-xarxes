# PROJECTE FINAL ARQUITECTURA DE XARXES

## Documentació d'execució i configuració

### Estructura del repositori

El repositori conté dues carpetes principals:

* `startup-oficina`

  * `oficina.py`
  * `index.html`
  * `Dockerfile`

* `startup-escalada`

  * `oficina-escalada.py`
  * `web-roba.html`
  * `Dockerfile`

---

# PART 1. Teletreball: l'Oficina a Casa

## 1. Execució de la topologia Mininet

Situar-se dins la carpeta del projecte:

```bash
cd startup-oficina
```

Executar la topologia:

```bash
sudo python3 oficina.py
```

Verificar la connectivitat:

```bash
pingall
```

---

## 2. Creació de la pàgina web interna

Crear l'arxiu HTML:

```bash
nano index.html
```

---

## 3. Creació de la imatge Docker

Crear el Dockerfile:

```bash
nano Dockerfile
```

Construir la imatge:

```bash
docker build -t bd-startup .
```

Comprovar les imatges disponibles:

```bash
docker images
```

---

## 4. Desplegament del contenidor al servidor h1

Des de la consola de Mininet:

```bash
h1 docker run -d --name bd-confidencial --publish 9999:80 bd-startup
```

Comprovar que el contenidor està executant-se:

```bash
h1 docker ps
```

---

## 5. Servei HTTP dins la topologia

```bash
h1 python3 -m http.server 80 &
```

Verificació des del PC de recepció:

```bash
h2 curl http://192.168.100.10
```

---

## 6. Accés remot mitjançant SSH Port Forwarding

Des de l'ordinador físic de la treballadora:

```bash
ssh -L 9090:localhost:80 usuari@IP_VM
```

Accés a través del navegador:

```text
http://localhost:9090
```

---

## 7. Configuració del Firewall

Permetre accés des de recepció:

```bash
h1 iptables -A INPUT -s 192.168.100.20 -j ACCEPT
```

Permetre accés des del túnel SSH:

```bash
h1 iptables -A INPUT -s 127.0.0.1 -j ACCEPT
```

Bloquejar la resta de connexions:

```bash
h1 iptables -P INPUT DROP
```

Consultar les regles aplicades:

```bash
h1 iptables -L -n -v
```

Prova d'accés no autoritzat:

```bash
curl --connect-timeout 5 http://192.168.100.10
```

---

# PART 2. Escalabilitat i Gestió de Congestió

## 1. Execució de la nova topologia

Situar-se dins la carpeta corresponent:

```bash
cd startup-escalada
```

Executar la xarxa:

```bash
sudo python3 oficina-escalada.py
```

Comprovació:

```bash
pingall
```

---

## 2. Construcció de la web de roba

Crear l'arxiu HTML:

```bash
nano web-roba.html
```

Crear el Dockerfile:

```bash
nano Dockerfile
```

Construir la imatge:

```bash
docker build -t web-roba .
```

Verificar:

```bash
docker images
```

---

## 3. Desplegament dels servidors web

Servidor 1:

```bash
web1 docker run -d --name srv-roba1 --publish 8001:80 web-roba
```

Servidor 2:

```bash
web2 docker run -d --name srv-roba2 --publish 8002:80 web-roba
```

Servidor 3:

```bash
web3 docker run -d --name srv-roba3 --publish 8003:80 web-roba
```

Verificació:

```bash
web1 docker ps
web2 docker ps
web3 docker ps
```

---

## 4. Configuració del Load Balancer

Activar IP Forwarding:

```bash
lb sysctl -w net.ipv4.ip_forward=1
```

Configuració de repartiment de càrrega:

```bash
lb iptables -t nat -A PREROUTING -p tcp --dport 80 -m statistic --mode random --probability 0.33 -j DNAT --to-destination 192.168.100.11:80

lb iptables -t nat -A PREROUTING -p tcp --dport 80 -m statistic --mode random --probability 0.50 -j DNAT --to-destination 192.168.100.12:80

lb iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.100.13:80
```

Gestionar el retorn dels paquets:

```bash
lb iptables -t nat -A POSTROUTING -j MASQUERADE
```

Consultar les regles:

```bash
lb iptables -t nat -L -n -v
```

---

## 5. Verificació del Load Balancer

Prova amb un client:

```bash
cli1 curl http://192.168.100.200/web-roba.html
```

---

## 6. Simulació de càrrega Black Friday

Generar múltiples peticions simultànies:

```bash
for i in {1..30}; do
    cli$i curl -s http://192.168.100.200 > /dev/null &
done
```

Comprovar el repartiment de trànsit:

```bash
lb iptables -t nat -L PREROUTING -v -n
```
