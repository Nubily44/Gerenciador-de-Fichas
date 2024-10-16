import pandas as pd
import socket

server_ip = "ip do server"
server_port = "port do servidor"

def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    print ("Começando o gerenciador de fichas online")
    entrada =  input("Insira o código da mesa caso queira conectar a uma mesa existente ou -1 caso queira iniciar uma mesa como Dungeon Master:")
    if entrada == -1:
        client.send(entrada.encode("utf-8")[:1024])

        response = client.recv(1024)
        response = response.decode("utf-8")
        mesa = response
        User_id = 00000
    else:
        mesa = entrada
        client.send(mesa.encode("utf-8")[:1024])
        #connecta com a mesa
        #espera receber ack com um id para a pessoa
        response = client.recv(1024)
        response = response.decode("utf-8")
        User_id = response
        

    while (True):


            print("se deseja criar um personagem ")




run_client()