#!/usr/bin/env python3
"""Uso: ./router IP_DESTINO PORTA"""
import socket
import sys

PORTA_ESCUTA = 5678   # porta onde os nRF enviam (UDP_SERVER_PORT do firmware)

if len(sys.argv) != 3:
    sys.exit("uso: ./router IP_DESTINO PORTA")

IP_DESTINO = sys.argv[1]
PORTA = int(sys.argv[2])

# Destino: aceita IPv4 ou IPv6
familia, _, _, _, destino = socket.getaddrinfo(
    IP_DESTINO, PORTA, type=socket.SOCK_DGRAM)[0]
saida = socket.socket(familia, socket.SOCK_DGRAM)

# Escuta em IPv6 e também em IPv4 (dual-stack)
entrada = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
entrada.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
entrada.bind(("::", PORTA_ESCUTA))

print(f"escutando UDP/{PORTA_ESCUTA} -> {IP_DESTINO}:{PORTA}", flush=True)

while True:
    dados, origem = entrada.recvfrom(2048)
    saida.sendto(dados, destino)
    print(f"{origem[0]} -> {IP_DESTINO}:{PORTA} ({len(dados)} bytes)", flush=True)
