import socket
import threading

PORT = 4040
HOSTNAME = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOSTNAME, PORT)

HEADER = 2048
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

OPTIONS = "PLEASE PRESS A NUMBER TO CONTINUE:\n1.SIGN-UP\n2.LOGIN\nnote:OTHER OPTIONS COMMING?\n"
INV_INPUT = "INVALID INPUT!! PLEASE TRY AGAIN"
USERNAME_USED = "THIS USERNAME IS ALREADY IN USE, TRY ANOTHER ONE"

def send_message(connection, msg):
    msg = msg.encode(FORMAT)
    msg_len = str(len(msg)).encode(FORMAT)
    space_padding = HEADER - len(msg_len)
    msg_len = msg_len + b" " * space_padding
    connection.send(msg_len)
    connection.send(msg)


def receive_message(connection):
    msg_len = connection.recv(HEADER).decode(FORMAT).strip()
    if not msg_len:
        return None
    msg_len = int(msg_len)
    return connection.recv(msg_len).decode(FORMAT)


def signup(connection):
    send_message(connection, "PLEASE ENTER USER ID: ")
    user_id = receive_message(connection)
    if user_id:
        print(f"your user id was: {user_id}")
    #have check if user name is taken, for now just forget about this

def thread_manage(connection, address):
    print(f"{address} CONNECTED SUCCESSFULLY!!")
    send_message(connection, OPTIONS)
    is_connected = True
    while is_connected:
        msg = receive_message(connection)
        if msg:
            print(f"message: {msg}\nfrom: {address}")
            if msg == "1":
                signup(connection)
            elif msg == "2":
                pass
            else:
                pass
            if msg == DISCONNECT_MESSAGE:
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
