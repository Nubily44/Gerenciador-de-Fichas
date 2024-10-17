import pandas as pd
import socket
import threading
import os

Id = 1
tempMessage = []
proceed = 0


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

def receive_data(server_ip, server_port):
    global tempMessage
    global proceed
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", server_port))
    server_socket.listen(1)

    print(f"Waiting to receive messages on port {server_port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        data = conn.recv(1024)
        if data:
            received_data = data.decode()
            print("recebe frase", len(received_data))
            receive_data = received_data.split(",")
            print(f"Received data: {receive_data}")
            if len(receive_data) == 10:

                tempMessage = receive_data
                proceed += 1

            ack_message = "Phrase received"
            conn.send(ack_message.encode())
            print("Acknowledgment sent to sender.")
        conn.close()


def send_numbers(server_ip, server_port, numbers):
    # Ensure numbers_list is already a list and has 10 elements
    if len(numbers) != 10:
        print("Invalid input. Please enter exactly 10 numbers.")
        return
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        
        # Send the list of numbers as a comma-separated string
        client_socket.send(','.join(map(str, numbers)).encode())
        print(f"Sent numbers: {numbers}")

        ack_data = client_socket.recv(1024)
        if ack_data:
            print("Acknowledgment from receiver:", ack_data.decode())

    except socket.error as e:
        print(f"Failed to connect to the receiver. Error: {e}")
    finally:
        client_socket.close()


def run_client(server_ip, server_port):
    global tempMessage
    global proceed
    Id = getId()

    #Autenticação
    send_numbers(server_ip, server_port, [0, str(Id), -1, -1, 5, -1, -1, -1, -1, -1])
    
    while proceed < 1:
        pass
    
    type(tempMessage)
    print(f"TempMessage: {tempMessage}")
    with open("clientside", "src", "client_id.txt", "w") as f:
        tempId = int(tempMessage[1])
        f.write(tempId)

    print ("Começando o gerenciador de fichas online")
    entrada =  input("Insira o código da mesa caso queira conectar a uma mesa existente ou -1 caso queira iniciar uma mesa como Dungeon Master:\n")
    
    if entrada == -1:
        pass  


if __name__ == "__main__":
    getId()
    print(getId())
    server_ip = input("insira o ip do server:")
    server_port = int(input("insira a porta do servidor:"))

    receive_data_thread = threading.Thread(target=receive_data, args=(server_ip, server_port))
    receive_data_thread.daemon = True
    receive_data_thread.start()

    run_client(server_ip, server_port)