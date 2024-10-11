import socket
import threading

def receive_numbers(port):
    """Function to receive numbers and print them on the screen."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Listen on all available IPs
    server_socket.listen(1)
    print(f"Waiting to receive messages on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        data = conn.recv(1024)
        if data:
            received_number = data.decode()
            print(f"Received number: {received_number}")

        conn.close()

def send_number(ip, port):
    """Function to send a number to a specified IP and port."""
    while True:
        number_to_send = input("Enter a number to send: ")

        try:
            number_to_send = int(number_to_send)  # Ensure valid number
        except ValueError:
            print("Invalid number. Please enter an integer.")
            continue

        print(f"Attempting to connect to {ip}:{port}")  # Debugging print

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((ip, port))
            send_socket.send(str(number_to_send).encode())
            print(f"Sent number: {number_to_send}")
        except socket.error as e:
            print(f"Failed to connect to the receiver. Error: {e}")
        finally:
            send_socket.close()

if __name__ == "__main__":
    PORT = 5000  # You can adjust this port
    FRIEND_IP = '26.204.92.82'  # Change to your friend's IP if needed

    # Start the receiver thread
    receive_thread = threading.Thread(target=receive_numbers, args=(PORT,))
    receive_thread.daemon = True
    receive_thread.start()

    # Start sending numbers
    send_number(FRIEND_IP, PORT)
