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

OPTIONS1 = "PLEASE PRESS A NUMBER TO CONTINUE:\n1.SIGN-UP\n2.LOGIN\n3.DISCONNECT\nnote:OTHER OPTIONS COMMING?\n"
OPTIONS2 = "PLEASE PRESS A NUMBER TO CONTINUE:\n1.P2P CONNECTION\n2.CREATE GROUP\n3.JOIN GROUP\n4.CHANGE PASSWORD\n5.CHANGE USERNAME\n6DISCONNECT" 
INV_INPUT = "INVALID INPUT!! PLEASE TRY AGAIN"
INV_USER = "THE USER_ID IS INVALID, please try again"
USERNAME_USED = "THIS USERNAME IS ALREADY IN USE, TRY ANOTHER ONE"
USERNAME_ACCEPT = "USER NAME ACCEPTED"
PASSWORD_ACCEPT = "PASSWORD ACCEPTED"
PASSWORD_WRONG = "WRONG PASSWORD PLEASE TRY AGAIN"
user_dict = {"12345": "12345"}

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
    signing_up = True
    while signing_up:
        send_message(connection, "PLEASE ENTER USER ID: ")
        user_id = receive_message(connection)
        if user_id:
            if user_id in user_dict:
                send_message(connection, USERNAME_USED)
                continue
            send_message(connection, USERNAME_ACCEPT)
            print(f"your user id was: {user_id}")
            send_message(connection, "PLEASE ENTER YOU PASSWORD: ")
            user_password = receive_message(connection)
            if user_password:
                print(f"your password was: {user_password}")
                user_dict[user_id] = user_password
                send_message(connection, "SIGNED-UP SUCCESSFULLY!!")
                signing_up = False

def login(connection):
    logging_in = True
    while logging_in:
        entering_user_name = True
        while entering_user_name:
            send_message(connection, "PLEASE ENTER USER ID: ")
            user_id = receive_message(connection)
            if user_id:
                if not user_id in user_dict:
                    send_message(connection, INV_USER)
                    continue
                send_message(connection, USERNAME_ACCEPT)
                entering_user_name = False

        entering_password = True
        while entering_password:
            send_message(connection, "PLEASE ENTER YOU PASSWORD: ")
            user_password = receive_message(connection)
            if user_password:
                if user_dict[user_id] == user_password:
                    send_message(connection, PASSWORD_ACCEPT)
                    send_message(connection, "LOGGED-IN SUCCESSFULLY!!")
                    entering_password = False
                    continue
                else:
                    send_message(connection, PASSWORD_WRONG)
            logging_in = False

def thread_manage(connection, address):
    print(f"{address} CONNECTED SUCCESSFULLY!!")
    is_connected = True
    while is_connected:
        send_message(connection, OPTIONS1)
        msg = receive_message(connection)
        if msg:
            print(f"message: {msg}\nfrom: {address}")
            if msg == "1":
                signup(connection)
                continue
            elif msg == "2":
                login(connection)
            elif msg == "3":
                is_connected = False
                continue
            else:
                pass

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
