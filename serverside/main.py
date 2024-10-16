# main.py
import sys
import os
import socket
import threading
import pandas as pd

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sheet_template     import Sheet_Template  # Import the class
from equipment_template import Weapon_Template
from equipment_template import Usable_Template
from equipment_template import Permanent_Template
from equipment_template import Permanent_Buff_Template
from table              import Table

Send = 0
Recieve = 0
Ready = 0

tempMessage = []

def receive_numbers(port):
    global Recieve, tempMessage

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Listen on all available IPs
    server_socket.listen(1)
    print(f"Waiting to receive messages on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        data = conn.recv(1024)
        if data:
            Recieve = 1
            # Decode the received bytes and split into a list
            received_numbers = data.decode().split(',')

            tempMessage = received_numbers
            print(f"Received numbers: {received_numbers}")

            # Send acknowledgment back to the sender
            ack_message = "Numbers received"
            conn.send(ack_message.encode())
            print("Acknowledgment sent to sender.")

        conn.close()

def send_numbers(ip, port, array):
    global Recieve, Send
    """Function to send an array of 10 numbers to a specified IP and port."""
    
    if Send == 1:
        numbers_list = array.split(',')

        if len(numbers_list) != 10:
            print("Invalid input. Please enter exactly 10 numbers.")
            Send = 0
            Recieve = 1
            return

        print(f"Attempting to connect to {ip}:{port}")  

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((ip, port))
            
            send_socket.send(','.join(map(str, numbers_list)).encode())
            print(f"Sent numbers: {numbers_list}")

            ack_data = send_socket.recv(1024)
            if ack_data:
                print("Acknowledgment from receiver:", ack_data.decode())

        except socket.error as e:
            print(f"Failed to connect to the receiver. Error: {e}")
        finally:
            send_socket.close()

        # Reset Send after sending and allow receiving again
        Send = 0



# Testes
character_sheet = Sheet_Template("Aragorn", 20, 15, 90)
character_sheet2 = Sheet_Template("Legolas", 15, 20, 10)
character_sheet3 = Sheet_Template("Frodo", 5, 5, 5)
character_sheet4 = Sheet_Template("Gandalf", 20, 20, 20)
character_sheet5 = Sheet_Template("Sauron", 20, 20, 20)

weapon = Weapon_Template("ARMA", 10, 2, 2, 0)
usable = Usable_Template("Potion", 10, 2, 3, 2)
usable2 = Usable_Template("Potion2", 10, 5, 4, 3)
permanent = Permanent_Template("Ring", 10, 2, 5)

table = Table(1, "Table1")
table.addSheet(character_sheet)
table.addSheet(character_sheet2)
table.displayTable()


#   [0]  Primeiro Número: Remetente  
#   0 = Cliente 
#   1 = Servidor

#   [1]  Segundo Número: Id do Usuário
#   5 digitos (aleatórios)

#   [2]  Terceiro Número: Id da Mesa
#   Adicionado dinamicamente

#   [3]  Quarto Número: Id da Ficha
#   Adicionado dinamicamente - 

#   [4]  Quinto Número: Tipo de Mensagem:
#   0 = Criar Mesa
#   1 = Criar Ficha
#   2 = Mudar Atributo
#   3 = Criar Equipamento

#   [5]  Sexto Número: Valor 1
#   Caso [4] = 3:
#   0 = Arma
#   1 = Usável
#   2 = Permanente
#   3 = Buff Permanente

#   [6]  Sétimo Número: Valor 2

#   [7]  Oitavo Número: Valor 3

#   [8]  Nono Número: Valor 4

#   [9]  Décimo Número: Valor 5





if __name__ == "__main__":
    PORT = 5000  # You can adjust this port
    FRIEND_IP = '26.232.143.16'  # Change to your friend's IP if needed

    # Start the receiver thread
    receive_thread = threading.Thread(target=receive_numbers, args=(PORT,))
    receive_thread.daemon = True  # This allows the thread to exit when the main program exits
    receive_thread.start()

    # Main traffic light loop
    while True:
        if Recieve == 1 and Ready == 0:
            # Process the received message
            print("Processing the message...")

            message = tempMessage
            tempMessage = []

            sender = message[0]
            idn = message[1]
            table_id = message[2]
            sheet_id = message[3]

            tables = pd.read_csv("tables.csv")
            tables.head()

            
            value = []
            for i in range(4):
                value[i] = message[i+5]
            
            table 
            temp_sheet = table.getSheet(sheet_id)










            
            Ready = 1  # Set Ready after processing

        if Ready == 1:
            Send = 1
            Recieve = 0  # Reset Recieve after processing
            send_numbers(FRIEND_IP, PORT, "1,100,100,100,100,100,100,100,100,100")
            Ready = 0  # Reset Ready after sending
