# main.py
import sys
import os
import socket
import threading
import pandas as pd
import random
import json
import shutil
import glob
import time

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sheet_template  import Sheet_Template  # Import the class
from equipment_template import (
    Weapon_Template,
    Usable_Template,
    Permanent_Template,
    Permanent_Buff_Template,
)
from table import Table

Send = 0 # 0 = Not sending, 1 = Sending
Receive = 0 # 0 = Not receiving, 1 = Receiving
Ready = 0 # 0 = Not ready, 1 = Ready

tempMessage = []
tempIp = []
conn = None

lock = threading.Lock()



class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, timeout):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.client_Ip = addr[0]
        self.alive = 1
        self.lastTime = time.time()
        self.conn.settimeout(timeout)


    def run(self):
        while True:
            try:
                data = self.conn.recv(1024).decode('utf-8')
                received_data = data.split(',')
                print(f"\nDados recebidos: \n{received_data}")
                if received_data and len(received_data) == 10:

                    global tempMessage, tempIp, Receive, Send, conn
                    with lock:
                        Receive = 1
                        tempMessage = received_data
                        tempIp = self.client_Ip
                        conn = self.conn

                if len(received_data) == 2 and int(received_data[0].strip("[]")) == 1:
                    self.lastTime = time.time()


            except socket.timeout:
                if time.time() - self.lastTime > 60:  
                    try:    
                        self.alive = 0
                        self.conn.close()
                        print(f"Conexão perdida com o cliente {self.client_Ip}")
                        break
                    except:
                        print("Não foi possivel fechar conexão\n")
                        break

            except OSError as e:
                if e.errno == 10054:  # WinError 10054
                    print(f"Conexão foi fechada forçadamente pelo cliente: {self.client_Ip}")
                    break
                else:
                    print(f"O cliente {self.client_Ip} causou o erro: {e} ")  
                    break   

def receive_connection(port):
    print("threads ativas:", threading.active_count())
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket.bind(('0.0.0.0', port))
    connection_socket.listen(20)

    while True:
        try:
            conn, addr = connection_socket.accept()
            client_handler = ClientHandler(conn, addr, 60)
            client_handler.start()

        except:
            print("ERRO: Não aceitou a conexão")
            break

def send_data(conn, arr):
    
    arr = str(arr).strip("[]")
    global Receive, Send
    try:
        
        if Send == 0:
            with lock:
                Send = 1
                if len(arr) == 10:
                    arr = arr.split(',')
            
                conn.send(arr.encode('utf-8'))
                print(f"\nDados Enviados: \n{arr}")
                Send = 0
    except(ConnectionResetError, BrokenPipeError):
         print("ERRO: Conexão perdida. Impossível enviar...")
         
    

#def send_numbers(conn, array):
#    global Receive, Send
#    if Send == 1:
#        array = str(array).strip("[]")
#        numbers_list = array.split(',')
#        if len(numbers_list) != 10:
#            Send = 0
#            Receive = 1
#            return
#        try:
#            conn.send(array.encode('utf-8'))
#            print(f"\nSent phrase: \n{array}")
#            
#        except(ConnectionResetError, BrokenPipeError):
#            print("ERRO: Conexão perdida. Impossível enviar...")
#           conn.close()
#        
#        finally:
#            Send = 0

#def send_phrase(conn, array):
#    global Receive, Send
#   
#    if Send == 1:
#        try:
#            conn.send(array.encode('utf-8'))
#            print(f"\nSent phrase: \n{array}")
#            ack_data = conn.recv(1024) #pode ser usado para mostrar que recebeu
#        except(ConnectionResetError, BrokenPipeError):
#            print("ERRO: Conexão perdida. Impossível enviar...")
#            conn.close()
#        Send = 0

#FODASEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#Caro professor, perdemos 5 horas da nossa vida tentando fazer essa função do código funcionar, conseguimos. Espero q essa função queime no inferno

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
        return int(match["Id"].values[0])
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

def checkExistingTables():
    max = 0
    for i in range(100):
        if searchTable(i):
            max = i
        else:
            break
    return max

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

def checkExistingSheets(i):
    max = 0
    for x in range(i):
        if i<10:
            folder_name = f"table0{i}"
        else:
            folder_name = f"table{i}"
        full_path = os.path.join("serverside", "tables", folder_name)
        for y in range(100):
            if searchSheet(y, i):
                max = y
            else:
                break
    return max

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


{ #Comentários
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


# -1 = null (sem valor atribuído)


#   [0]  Primeiro Número: Remetente  
#   0 = Cliente 
#   1 = Servidor

#   [1]  Segundo Número: Id do Usuário
#   Sistema de Unicidade
#   n - Id do Usuário
#   0 - Mestre
#   1 - Usuário sem Id

#   [2]  Terceiro Número: Id da Mesa
#   Adicionado dinamicamente
#   -1 = Sem Mesa
#   n = Id da Mesa

#   [3]  Quarto Número: Id da Ficha
#   Adicionado dinamicamente
#   -1 = Sem Ficha
#   n = Id da Ficha

#[feito), (testado)]   [4]  Quinto Número: Tipo de Mensagem:
#ct   0 = Criar Mesa                          [-1, -1, -1, -1, -1]
#ct   1 = Criar Ficha                         ["nome", B, C, V, -1]       nome, AttB, AttC, AttV
#ct   2 = Deletar Mesa                        [-1, -1, -1, -1, -1]
#ct   3 = Deletar Ficha                       [-1, -1, -1, -1, -1]
#c   4 = Mudar Ficha de posição              [n, -1, -1, -1, -1]         n = Id da mesa para onde a ficha será movida
#c   5 = Identificar Usuário                 [-1, -1, -1, -1, -1]
#c   6 = Modificar atributo                  [n, t, m, -1, -1]           n = Id do atributo - 1 = AttB, 2 = AttC, 3 = AttV, 4 = "nome", t = 0 - Get, 1 - Set, m = valor para set, -1 para get
#c   7 = Criar Equipamento                   ["nome", T, R, S, t]        nome, tipo, raridade, estado, tipo de equipamento: 0 - Weapon, 1 - Usable, 2 - Permanent, 3 - Permanent Buff
#   8 = Modificar ficha (mochilas)            [t, n, -1, -1, -1]          t = tipo - 0 = Weapon, 1 = Usable, 2 = Permanent, 3 = Permanent Buff
#   9 = Ações                                [t, n, -1, -1, -1]          t = tipo de ação, 0 = dance[0, n = target], 1 = punch[1, n = target, d = damage], 2 = wink[2, n = target], 3 = send[3, n = target, x= item, m = quantidade]                                                                                   
#   10 = Usar Equipamento                    [t, n, -1, -1, -1]          t = tipo de equipamento, n = Id do equipamento na mochila
#   11 = Deletar Equipamento                ["nome", -1, -1, -1, -1]     nome = nome do equipamento
#   12 = Modificar Equipamento              ["nome", -1, -1, -1, -1]     nome = nome do equipamento
#c   13 = Display Ficha                      [-1, -1, -1, -1, -1]
#c   14 =  Display fichas de uma mesa       [-1, -1, -1, -1, -1]
#   -1 = sair e desconectar

#   [5]  Sexto Número: Valor 1

#   [6]  Sétimo Número: Valor 2

#   [7]  Oitavo Número: Valor 3

#   [8]  Nono Número: Valor 4

#   [9]  Décimo Número: Valor 5

}

if __name__ == "__main__":
    PORT = 5000  # You can adjust this port # Our IP address

    # Start the receiver thread
    receive_thread = threading.Thread(target=receive_connection, args=(PORT,))
    receive_thread.daemon = True  # This allows the thread to exit when the main program exits
    receive_thread.start()

    print("Server started. Listening for incoming connections...")

    # Main traffic light loop
    timeinicial = time.time()
    while True:
        with lock:
            if Receive == 1 and Ready == 0:
                # Process the received message
                print("Processing the message...")

                message = tempMessage
                tempMessage = []
                ip = tempIp
                print("ip", ip)

                tempIp = []

                sender = int(message[0])
                idn = int(message[1])
                table_id = int(message[2])
                sheet_id = int(message[3])
                message_type = int(message[4])
                values = [None] * 5
                for i in range(4):
                    values[i] = message[5+i]
                if table_id<10:
                    txt_path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet{str(sheet_id)}.txt")
                    if sheet_id<10:
                        txt_path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet0{str(sheet_id)}.txt")
                else:
                    txt_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(sheet_id)}.txt")
                
                if table_id<10:
                    json_path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet{str(sheet_id)}.json")
                    if sheet_id<10:
                        json_path  = os.path.join("serverside","tables",f"table0{str(table_id)}", f"sheet0{str(sheet_id)}.json")
                else:
                    json_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(sheet_id)}.json")

                if table_id<10:
                    equipment_path = os.path.join("serverside","tables",f"table{str(table_id)}", "equipment", f"{values[0]}.json")
                else:
                    equipment_path = os.path.join("serverside","tables",f"table{str(table_id)}", "equipment", f"{values[0]}.json")

                if table_id<10:
                    table_path = os.path.join("serverside","tables",f"table0{str(table_id)}")
                else:
                    table_path = (os.path.join("serverside","tables",f"table{str(table_id)}"))

                match message_type:
                    case -1:
                        if sender == 0:
                            conn.close()
                            print(ip,"des'conn'ectou")

                    case 0: # Criar Mesa
                        if sender == 0:
                            checkTable(table_id)
                            
                            send_thread = threading.Thread(target=send_data, args=(conn, "Mesa criada com sucesso"))
                            send_thread.daemon = True
                            send_thread.start()
                        else:
                            pass
                    
                    case 1: # Criar Ficha
                        if sender == 0:
                            checkTable(table_id)
                            if searchTable(table_id):
                                checkSheet(sheet_id, table_id)

                                for i in range(3):
                                    values[i+1] = int(values[i+1])
                                    print(values[i+1])
                                values[0] = str(values[0])

                                character_sheet_instance = Sheet_Template(values[0], values[1], values[2], values[3])
                                json_str = character_sheet_instance.to_dict()
                                with open(json_path, "w") as json_file:
                                    json.dump(json_str, json_file, indent=4)
                                character_sheet_instance.logging(txt_path)

                                send_thread = threading.Thread(target=send_data, args=(conn, "Ficha criada com sucesso"))
                                send_thread.daemon = True
                                send_thread.start()

                                send_thread2 = threading.Thread(target=send_data, args=(conn, character_sheet_instance.DisplayString()))
                                send_thread2.daemon = True
                                send_thread2.start()

                    case 2: # Deletar Mesa
                        if sender == 0:
                            if searchTable(table_id):
                                shutil.rmtree(table_path)

                                send_thread = threading.Thread(target=send_data, args=(conn, "Mesa deletada com sucesso"))
                                send_thread.daemon = True
                                send_thread.start()
                    
                    case 3: # Deletar Ficha
                        if sender == 0:
                            if searchSheet(sheet_id, table_id):
                                os.remove(txt_path)
                                os.remove(json_path)

                                send_thread = threading.Thread(target=send_data, args=(conn, "Ficha deletada com sucesso"))
                                send_thread.daemon = True
                                send_thread.start()

                    case 4: # Mudar Ficha de posição
                        if sender == 0:
                            values[0] = int (values[0])
                            table_path_sent_to = os.path.join("serverside","tables",f"table{str(values[0])}")

                            if not os.path.exists(table_path_sent_to):
                                checkTable(values[0])
                            for file_type in ['*.json', '*.txt']:
                                files = glob.glob(os.path.join(table_path, file_type))
                                
                                for file in files:
                                    shutil.move(file, table_path_sent_to)

                            send_thread = threading.Thread(target=send_data, args=(conn, "Ficha movida com sucesso"))
                            send_thread.daemon = True
                            send_thread.start()

                    case 5: # Identificar Usuário
                        if sender == 0:
                            print("Identificação")
                            mesa_max = checkExistingTables()
                            sheet_max = checkExistingSheets(table_id)
                            idn = identify(ip)


                            send_thread = threading.Thread(target=send_data, args=(conn, "Identificação feita com sucesso"))
                            send_thread.daemon = True
                            send_thread.start()

                            send_thread2 = threading.Thread(target=send_data, args=(conn, [1, idn, mesa_max, sheet_max, 5, -1, -1, -1, -1, -1]))
                            send_thread2.daemon = True
                            send_thread2.start()


                    case 6: # Modificar atributo
                        if sender == 0:
                            if searchSheet(sheet_id, table_id):
                                
                                for(i) in range(3):
                                    values[i] = int(values[i])

                                with open(json_path, "r") as json_file:
                                    data = json.load(json_file)
                                sheet_object = Sheet_Template.from_dict(data)


                                if values[0] == 1:
                                    if values[1] == 0:
                                        phrase = sheet_object.getAttB()
                                    elif values[1] == 1:
                                        sheet_object.setAttB(values[2])
                                if values[0] == 2:
                                    if values[1] == 0:
                                        phrase = sheet_object.getAttC()
                                    elif values[1] == 1:
                                        sheet_object.setAttC(values[2])
                                if values[0] == 3:
                                    if values[1] == 0:
                                        phrase = sheet_object.getAttV()
                                    elif values[1] == 1:
                                        sheet_object.setAttV(values[2])


                                json_str = sheet_object.to_dict()
                                with open(json_path, "w") as json_file:
                                    json.dump(json_str, json_file, indent=4)
                                character_sheet_instance.logging(txt_path)
                                
                                send_thread = threading.Thread(target=send_data, args=(conn, "Ficha atualizada com sucesso"))
                                send_thread.daemon = True
                                send_thread.start()
                                print(character_sheet_instance.DisplayString())
                                send_thread2 = threading.Thread(target=send_data, args=(conn, character_sheet_instance.DisplayString()))
                                send_thread2.daemon = True
                                send_thread2.start()

                    case 7: # Criar Equipamento
                        if sender == 0:
                            if searchSheet(sheet_id, table_id):

                                for i in range(3):
                                    values[i] = int(values[i])
                                
                                if table_id<10:
                                    equipment_path = os.path.join("serverside","tables",f"table{str(table_id)}", "equipment", f"{values[0]}.json")
                                else:
                                    equipment_path = os.path.join("serverside","tables",f"table{str(table_id)}", "equipment", f"{values[0]}.json")
                                
                                if values[4] == 0:
                                    equipment_instance = Weapon_Template(values[0], values[1], values[2], values[3])
                                if values[4] == 1:
                                    equipment_instance = Usable_Template(values[0], values[1], values[2], values[3])
                                if values[4] == 2:
                                    equipment_instance = Permanent_Template(values[0], values[1], values[2], values[3])
                                if values[4] == 3:
                                    equipment_instance = Permanent_Buff_Template(values[0], values[1], values[2], values[3])
                                
                                with open(json_path, "r") as json_file:
                                    sheet_data = json.load(json_file)


                                send_thread = threading.Thread(target=send_data, args=(conn, "Equipamento criado com sucesso"))
                                send_thread.daemon = True
                                send_thread.start()

                    case 8: #Modificar ficha (mochilas e ações)
                        pass
                        
                    case 9: #Acões
                        if sender == 0:
                            for i in range(3):
                                values[i] = int(values[i])
                            match values[0]:
                                case 0:
                                    if searchSheet(sheet_id, table_id):
                                        other_id = values[1]
                                        with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                        character_sheet_instance = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                        if searchSheet(other_id, table_id):
                                            json_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(other_id)}.json")
                                            with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                            character_sheet_instance2 = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                            character_sheet_instance.dance(character_sheet_instance2)

                                            send_thread = threading.Thread(target=send_data, args=(conn, "Dancou com ", character_sheet_instance2.nome()))
                                            send_thread.daemon = True
                                            send_thread.start()
                                case 1:
                                    if searchSheet(sheet_id, table_id):
                                        other_id = values[1]
                                        with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                        character_sheet_instance = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                        if searchSheet(other_id, table_id):
                                            json_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(other_id)}.json")
                                            with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                            character_sheet_instance2 = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                            character_sheet_instance.punch(character_sheet_instance2,values[2])

                                            send_thread = threading.Thread(target=send_data, args=(conn, "Você socou", character_sheet_instance2.nome()))
                                            send_thread.daemon = True
                                            send_thread.start()  
                                case 2:
                                    if searchSheet(sheet_id, table_id):
                                        other_id = values[1]
                                        with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                        character_sheet_instance = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                        if searchSheet(other_id, table_id):
                                            json_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(other_id)}.json")
                                            with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                            
                                            character_sheet_instance2 = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                            character_sheet_instance.wink(character_sheet_instance2)

                                            send_thread = threading.Thread(target=send_data, args=(conn, "Piscou para", character_sheet_instance2.nome()))
                                            send_thread.daemon = True
                                            send_thread.start()      
                                case 3:
                                    if searchSheet(sheet_id, table_id):
                                        other_id = values[1]
                                        with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                        character_sheet_instance = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                        if searchSheet(other_id, table_id):
                                            json_path  = os.path.join("serverside","tables",f"table{str(table_id)}", f"sheet{str(other_id)}.json")
                                            with open(json_path, "r") as json_file:
                                                sheet_data = json.load(json_file)
                                            character_sheet_instance2 = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])
                                            character_sheet_instance.send(character_sheet_instance2,values[2], values[3])

                                            send_thread = threading.Thread(target=send_data, args=(conn, "Você deu ", values[3] , values[2], "para ", character_sheet_instance2.nome()))
                                            send_thread.daemon = True
                                            send_thread.start() 

                    case 13: # Display Ficha
                        print("Existencia da mesa")
                        checkTable(table_id)
                        if searchTable(table_id):
                            if checkSheet(sheet_id, table_id):
                                print("Existencia da ficha")
                                with open(json_path, "r") as json_file:
                                    sheet_data = json.load(json_file)
                                character_sheet_instance = Sheet_Template(sheet_data['value0'], sheet_data['value1'], sheet_data['value2'], sheet_data['value3'])

                                send_thread = threading.Thread(target=send_data, args=(conn,  character_sheet_instance.DisplayString()))
                                send_thread.daemon = True
                                send_thread.start()
                            else:

                                send_thread = threading.Thread(target=send_data, args=(conn, "Ficha não encontrada"))
                                send_thread.daemon = True
                                send_thread.start()

                    case 14: # Display fichas de uma mesa
                        sheet_max = checkExistingSheets(table_id)

                        send_thread = threading.Thread(target=send_data, args=(conn, sheet_max))
                        send_thread.daemon = True
                        send_thread.start()
                    
                Ready = 1

        with lock:
            if Ready == 1:
                Receive = 0
                Ready = 0   