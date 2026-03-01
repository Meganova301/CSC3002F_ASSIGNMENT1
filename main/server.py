
import socket
import threading

HEADER = 1024
PORT = 4040
HOSTNAME = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOSTNAME, PORT) 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

def thread_manage(connection, address):
    print(f"{address} CONNECTED SUCCESSFULLY!!")

    is_connected = True
    while is_connected:
        msg_size = int(connection.recv(HEADER).decode("utf-8"))
        msg = connection.recv(msg_size).decode("utf-8")

        print(f"message: {msg}\nfrom: {address}")

        if msg == "":
            is_connected = False

        print(f"{address} DISCONNECTED!!")

    connection.close()

def begin():
    server_socket.listen()
    while True:
        connection, address = server_socket.accept()
        thread = threading.Thread(target=thread_manage, args=(connection, address))
        thread.start()
print("the socket server is running...")
begin()
