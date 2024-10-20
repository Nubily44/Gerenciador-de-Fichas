import pandas as pd
import socket
import threading
import os
import time

Id = 1
tempMessage = []
proceed = 0

lock = threading.Lock()

def sep():
    print("\n")

def keepAlive(conn):
    while True: 
        time.sleep(30) 
        with lock:
            message = str([1, getId()]) 
            try:
                conn.send(message.encode())
                pass
            except socket.error as e:
                print(f"Failed to connect to the receiver. Error: {e}")
                break

def getId():
    global Id
    file_path = os.path.join("clientside", "src", "client_id.txt")

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("1")  
        Id = 1
        return Id
    
    with open(file_path, "r") as f:
        content = f.read().strip()
        
        if content == "":
            Id = 1 
        else:
            Id = int(content) 
    
    return Id

def start_connection(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        return client_socket
    except:
        print("não foi possível conectar com o servidor")  
    

def receive_data(socket):
    global tempMessage
    global proceed

    while True:

        data = socket.recv(1024)
        if data:
            received_data = data.decode('utf-8')

            print(received_data)

            if len(received_data.split(",")) == 10:
                receive_data = received_data.split(",")
                tempMessage = receive_data
                proceed += 1
            
            ack_message = "ACK"
            socket.send(ack_message.encode())



def send_numbers(client_socket, numbers):
    with lock:
        try:  
            message_to_send = ','.join(map(str, numbers))
            client_socket.send(message_to_send.encode())
            print("enviado: ", message_to_send)

        except (ConnectionResetError, BrokenPipeError):
            print("Desconectou do servidor, verifique o status do servidor")
        except socket.error as e:
            print(f"Não foi possível conectar com o servidor. Erro: {e}")
        


def run_client(server_ip, server_port):
    global tempMessage, proceed
    Id = getId()
    socket = start_connection(server_ip, server_port)

    receive_data_thread = threading.Thread(target=receive_data, args=(socket,))
    receive_data_thread.daemon = True
    receive_data_thread.start()

    print("Iniciando autenticação com o servidor...")
    #Autenticação
    
    send_numbers(socket, [0, str(Id), -1, -1, 5, -1, -1, -1, -1, -1])
    
    keepAliveThread = threading.Thread(target=keepAlive, args=(socket,))
    keepAliveThread.daemon = True  
    keepAliveThread.start() 
    while proceed < 1:
        pass
    
    print("Autenticação realizada com sucesso!")
    sep()
    print("Agora você está conectado ao servidor!")
    sep()
    
    path = os.path.join("clientside", "src", "client_id.txt")
    with open(path, "w") as f:
        tempId = tempMessage[1]
        f.write(tempId)
    mesas = int(tempMessage[2])
    time.sleep(1)
    print ("Começando o gerenciador de fichas online")
    print (f"O servidor atualmente possui {mesas} mesas.")
    mesa =  input("Insira:\n-1 - criar uma nova mesa, como Dungeon Master\nn - entrar em uma mesa existente (com n sendo o número da mesa)\nInput: ")
    sep()
    mesa = int(mesa)
    if mesa == -1:
        send_numbers(socket, [0, str(Id), (mesas+1), -1, 0, -1, -1, -1, -1, -1]) # <- mesaS, não mesa (é pra criar uma mesa nova)
        time.sleep(1)
        print(f"Entrando na mesa {mesas+1}...")
        print(f"Na mesa {mesas+1}, qual ficha você deseja acessar?")
        ficha = input("Insira:\n-1 - criar uma nova ficha\n-2 - deletar mesa\nInput: ")
        sep()
        ficha = int(ficha)

        if ficha == -1:
            send_numbers(socket, [0, str(Id), mesas+1, mesas, 1, -1, -1, -1, -1, -1])
        elif ficha == -2:
            send_numbers(socket, [0, str(Id), mesa, -1, 2, -1, -1, -1, -1, -1])
            return
        interface(mesa, ficha, socket)
    else:
        send_numbers(socket, [0, str(Id), mesa, -1, 14, -1, -1, -1, -1, -1])
        time.sleep(1)
        print(f"Entrando na mesa {mesa}...")
        print(f"Na mesa {mesa}, qual ficha você deseja acessar?")
        ficha = input("Insira:\nn - para acessar a ficha n\n-1 - criar uma nova ficha\n-2 - deletar mesa\nInput: ")
        sep()
        ficha = int(ficha)
        if ficha == -1:
            numero = input("Insira o número da ficha\n(lembre-se de não inserir números que ja existem na mesa): ")
            ficha = numero
            nome = input("Insira o nome da ficha: ")
            AttC = input("Insira o valor de AttC: ")
            AttB = input("Insira o valor de AttB: ")
            AttV = input("Insira o valor de AttV: ")
            send_numbers(socket, [0, str(Id), mesa, numero, 1, nome, AttC, AttB, AttV, -1])
        elif ficha == -2:
            send_numbers(socket, [0, str(Id), mesa, -1, 2, -1, -1, -1, -1, -1])
        else:
            time.sleep(1)
            print("Agora você está conectado a uma ficha!")
        interface(mesa, ficha, socket)
        
def interface(mesa, ficha, socket):
    while True: 
        time.sleep(1)
        print("O que deseja fazer?")
        escolha1 = input("Insira:\n0 - sair\n1 - visualizar ficha\n2 - deletar ficha\n3 - mudar ficha de mesa\n4 - modificar ou receber atributo\n5 - adicionar item\n6 - fazer uma ação\n7 - usar um equipamento\n8 - deletar um equipamento\n9 - modificar um equipamento\nInput: ")
        escolha1 = int(escolha1)
        if escolha1 == 0:
            send_numbers(socket, [0, str(Id), mesa, ficha, -1, 0, 0, 0, 0, 0])
            socket.close()
            break

        elif escolha1 == 1:
            send_numbers(socket, [0, str(Id), mesa, ficha, 13, -1, -1, -1, -1, -1])

        elif escolha1 == 2:
            send_numbers(socket, [0, str(Id), mesa, ficha, 3, -1, -1, -1, -1, -1])

        elif escolha1 == 3:
            escolha2 = input("Insira o número da mesa para a qual deseja mover a ficha: ")
            send_numbers(socket, [0, str(Id), mesa, ficha, 4, escolha2, -1, -1, -1, -1])

        elif escolha1 == 4:
            atributo = input("Insira o atributo que deseja modificar:\n1 - AttB\n2 - AttC\n3 - AttV\n4 - nome\nInput: ")
            type = input("Insira:\n0 - visualizar\n1 - modificar\nInput: ")
            valor = ""
            if type == 1:
                valor = input("Insira o novo valor: ")
            send_numbers(socket, [0, str(Id), mesa, ficha, 6, atributo, type, valor, -1, -1])

        elif escolha1 == 5:
            print("Essa feature ainda não foi implementada :(") 

            #nome = input("Insira o nome do item: ")
            #tipo = input("Insira o tipo do item: ")
            #raridade = input("Insira a raridade do item: ")
            #estado = input("Insira o estado do item: ")
            #classe = input("Insira a classe do item:\n0 - arma\n1 - usável\n2 - permanente\n3 - permanente com buff\nInput: ")
            #send_numbers(socket, [0, str(Id), mesa, ficha, 7, nome, tipo, raridade, estado, classe])
        elif escolha1 == 6:
            acao = input("Insira a ação que deseja fazer:\n0 - dançar\n1 - punch\n2 - piscar\n3 - dar um item\nInput: ")
            dest = input("Insira o destino da ação: ")
            if acao == 3:
                item = input("Insira o nome do item: ")
                quantidade = input("Insira a quantidade de itens: ")
                send_numbers(socket, [0, str(Id), mesa, ficha, 9, acao, dest, item, quantidade, -1])

            else:
                send_numbers(socket, [0, str(Id), mesa, ficha, 9, acao, dest, -1, -1, -1])

        elif escolha1 == 7:
            print("Essa feature ainda não foi implementada :(")    

        elif escolha1 == 8:
            nome = input("Insira o nome do item que deseja deletar: ")
            send_numbers(socket, [0, str(Id), mesa, ficha, 11, nome, -1, -1, -1, -1])

        elif escolha1 == 9:
            print("Essa feature ainda não foi implementada :(")

        else:
            print("Opção inválida")
        sep()




if __name__ == "__main__":
    option1 = 0 
    print("Bem-vindo ao gerenciador de fichas online!")
    option1 = input("É sua primeira vez aqui?\nSim - digite 0\nNão - digite 1\n Input: ")
    sep()
    if option1 == 0:
        print("\nEsse programa se conecta a um servidor, para gerenciar fichas de rpg. Para isso, basta selecionar os números correspondentes as ações desejadas.\nBom Jogo!")
        sep()
    else:
        pass
    print("Para se conectar ao servidor:")
    server_ip = input("ip do servidor: ")
    server_port = int(input("porta do servidor: "))

    sep()

    run_client(server_ip, server_port)