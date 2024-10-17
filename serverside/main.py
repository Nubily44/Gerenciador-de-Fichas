# main.py
import sys
import os
import socket
import threading
import pandas as pd
import random
import json

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# from sheet_template  import Sheet_Template  # Import the class
# from equipment_template import (
#     Weapon_Template,
#     Usable_Template,
#     Permanent_Template,
#     Permanent_Buff_Template,
# )
# from table import Table

Send = 0
Receive = 0
Ready = 0

tempMessage = []
tempIp = []
tempIp2 = []

lock = threading.Lock()

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.client_Ip = addr[0]

    def run(self):
        data = self.conn.recv(1024)
        if data:
            received_data = data.decode().split(',')
            print(f"Received data: \n{received_data}")
            global tempMessage, Receive, tempIp, tempIp2
            with lock:
                tempMessage = received_data
                Receive = 1
                tempIp2 = self.client_Ip  # Store client IP address
                tempIp = list(map(int, self.client_Ip.split('.')))  # Store as integers
            ack_message = "data received"
            self.conn.send(ack_message.encode('utf-8'))
        self.conn.close()

def receive_data(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(20)

    while True:
        conn, addr = server_socket.accept()
        client_handler = ClientHandler(conn, addr)
        client_handler.start()

def send_numbers(ip, port, array):
    global receive, Send
    
    if Send == 1:
        array = str(array).strip("[]")
        numbers_list = array.split(',')
        if len(numbers_list) != 10:
            Send = 0
            receive = 1
            return

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((ip, port))
            send_socket.send(array.encode('utf-8'))
            print(f"\nSent numbers: \n{array}")
            ack_data = send_socket.recv(1024)
        finally:
            send_socket.close()
        Send = 0

def send_phrase(ip, port, array):
    global receive, Send
    
    if Send == 1:
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((ip, port))
            send_socket.send(array.encode('utf-8'))
            print(f"\nSent phrase: \n{array}")
            ack_data = send_socket.recv(1024)
        finally:
            send_socket.close()
        Send = 0



#FODASEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
# Caro professor, perdemos 5 horas da nossa vida tentando fazer esse código funcionar, conseguimos. Espero q essa função queime no inferno

def identify(ip):
    path = os.path.join("serverside", "idns.csv")
    
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["Ip", "Id"])
    else:
        df = pd.DataFrame(columns=["Ip", "Id"])

    ip = str(ip).strip()

    if ip in df["Ip"].astype(str).values:  
        print(f"IP existente: {ip}")
        match = df[df["Ip"] == ip]
        return match["Id"].values[0]
    else:
        
        idn = random.randint(10000, 99999)
        while idn in df["Id"].values:
            idn = random.randint(10000, 99999)
        
        df.loc[len(df)] = [ip, idn]
        df.to_csv(path, index=False)
        
        print(f"Novo IP adicionado: {ip}, ID: {idn}")

        return idn

def searchTable(i):
    for x in range(i):
        if i<10:
            folder_name = f"table0{i}"
        else:
            folder_name = f"table{i}"
        full_path = os.path.join("serverside", "tables", folder_name)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            return True
        else:
            return False
    return -1
        
def checkTable(i):
    if searchTable(i):
        print("Mesa Encontrada")
        return True
    else:
        print("Mesa não encontrada")
        if i<10:
            folder_name = f"table0{i}"
        else:
            folder_name = f"table{i}"
        full_path = os.path.join("serverside", "tables", folder_name)
        os.mkdir(full_path)
    
def searchSheet(i, table):
    for x in range(i):
        if i<10:
            file_name = f"sheet0{i}"
        else:
            file_name = f"sheet{i}"
        full_path = os.path.join("serverside","tables",f"table0{str(table)}", file_name)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            return True
        else:
            return False

def checkSheet(i, table):
    if searchSheet(i, table):
        print("Ficha Encontrada")
        return True
    else:
        print("Criando ficha")
        if i<10:
            file_name = f"sheet0{i}.txt"
        else:
            file_name = f"sheet{i}.txt"
        if table<10:
            full_path = os.path.join("serverside","tables",f"table0{str(table)}", file_name)
        else:
            full_path = os.path.join("serverside","tables",f"table{str(table)}", file_name)
        with open(full_path, "w"):
            pass


# Testes
# character_sheet = Sheet_Template("Aragorn", 20, 15, 90)
# character_sheet2 = Sheet_Template("Legolas", 15, 20, 10)
# character_sheet3 = Sheet_Template("Frodo", 5, 5, 5)
# character_sheet4 = Sheet_Template("Gandalf", 20, 20, 20)
# character_sheet5 = Sheet_Template("Sauron", 20, 20, 20)

# weapon = Weapon_Template("ARMA", 10, 2, 2, 0)
# usable = Usable_Template("Potion", 10, 2, 3, 2)
# usable2 = Usable_Template("Potion2", 10, 5, 4, 3)
# permanent = Permanent_Template("Ring", 10, 2, 5)

# table = Table(1, "Table1")
# table.addSheet(character_sheet)
# table.addSheet(character_sheet2)
# table.displayTable()


#   [0]  Primeiro Número: Remetente  
#   0 = Cliente 
#   1 = Servidor

#   [1]  Segundo Número: Id do Usuário
#   Sistema de Unicidade
#   0 - Mestre
#   1 - Usuário sem Id

#   [2]  Terceiro Número: Id da Mesa
#   Adicionado dinamicamente
#   -1 = Sem Mesa

#   [3]  Quarto Número: Id da Ficha
#   Adicionado dinamicamente
#   -1 = Sem Ficha

#   [4]  Quinto Número: Tipo de Mensagem:
#   0 = Criar Mesa
#   1 = Criar Ficha
#   2 = Deletar Mesa
#   3 = Deletar Ficha
#   4 = Mudar Ficha de posição
#   5 = Identificar Usuário
#   6 = Modificar atributo
#   7 = Criar Equipamento
#   8 = Modificar ficha (mochilas e ações)
#   9 = Usar Equipamento
#   10 = Deletar Equipamento
#   11 = Modificar Equipamento
#   12 = Display Ficha
#   13 = Display TableList
#   14 = Display SheetList
#   15 = Display WeaponList
#   // = help

#   [5]  Sexto Número: Valor 1
#   Caso [4] = 0:
#   SEM ATRIBUTOS EXTRAS

#   Caso [4] = 1:
#   nome da ficha

#   Caso [4] = 7:
#   0 = Arma
#   1 = Usável
#   2 = Permanente
#   3 = Buff Permanente

#   Caso [4] = 9:

#   [6]  Sétimo Número: Valor 2

#   [7]  Oitavo Número: Valor 3

#   [8]  Nono Número: Valor 4

#   [9]  Décimo Número: Valor 5



if __name__ == "__main__":
    PORT = 5000  # You can adjust this port
    LOG_IP = '26.232.143.16'  # Our Ip

    # Start the receiver thread
    receive_thread = threading.Thread(target=receive_data, args=(PORT,))
    receive_thread.daemon = True  # This allows the thread to exit when the main program exits
    receive_thread.start()

    print("Server started. Listening for incoming connections...")

    # Main traffic light loop
    while True:
        with lock:
            if Receive == 1 and Ready == 0:
                # Process the received message
                print("Processing the message...")

                message = tempMessage
                tempMessage = []
                ip = tempIp2
                reg = tempIp
                print("ip", ip)

                tempIp = []
                tempIp2 = []

                message = [int(x) for x in message]

                sender = int(message[0])
                idn = int(message[1])
                table_id = int(message[2])
                sheet_id = int(message[3])
                message_type = int(message[4])
                values = [None] * 5
                for i in range(4):
                    values[i] = message[5+i]
                
                if table_id<10:
                    path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet{str(sheet_id)}.txt")
                    if sheet_id<10:
                        path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet0{str(sheet_id)}.txt")
                else:
                    path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(sheet_id)}.txt")
                
                match message[4]:
                    case 0:
                        if sender == 0:
                            checkTable(table_id)
                            Send=1
                            Send = 1
                            send_thread = threading.Thread(target=send_phrase, args=(ip, PORT, "Mesa criada com sucesso"))
                            send_thread.daemon = True
                            send_thread.start()
                        else:
                            pass
                    case 1:
                        if sender == 0:
                            checkTable(table_id)
                            checkSheet(sheet_id, table_id)
                            for i in range(3):
                                values[i+1] = int(values[i+1])
                            values[0] = str(values[0])
                            character_sheet_instance = Sheet_Template(values[0], values[1], values[2], values[3])
                            json_str = character_sheet_instance.to_dict()
                            with open(path, "w") as json_file:
                                json.dump(json_str, json_file, indent=4)
                            character_sheet_instance.logging(path)
                            
                            Send = 1
                            send_thread = threading.Thread(target=send_phrase, args=(ip, PORT, "Ficha criada com sucesso"))
                            send_thread.daemon = True
                            send_thread.start()
                        else:
                            pass

                    case 5:
                        print("Identificação")
                        idn = identify(ip)
                        Send = 1
                        send_thread = threading.Thread(target=send_phrase, args=(ip, PORT, "Identificação feita com sucesso"))
                        send_thread.daemon = True
                        send_thread.start()
                        
                        send_thread = threading.Thread(target=send_numbers, args=(ip, PORT, [1, idn, table_id, sheet_id, 5, 0, 0, 0, 0, 0]))
                        send_thread.daemon = True
                        send_thread.start()


                Ready = 1

        with lock:
            if Ready == 1:
            
                Receive = 0
                Ready = 0   
