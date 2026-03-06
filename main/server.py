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
OPTIONS2 = "PLEASE PRESS A NUMBER TO CONTINUE:\n1.P2P CONNECTION\n2.CREATE GROUP\n3.JOIN GROUP\n4.CHANGE PASSWORD\n5.CHANGE USERNAME\n6.RETURN TO HOME PAGE\n7.DISCONNECT\n" 
INV_INPUT = "INVALID INPUT!! PLEASE TRY AGAIN"
INV_USER = "THE USER_ID IS INVALID, please try again"
USERNAME_USED = "THIS USERNAME IS ALREADY IN USE, TRY ANOTHER ONE"
USERNAME_ACCEPT = "USER NAME ACCEPTED"
PASSWORD_ACCEPT = "PASSWORD ACCEPTED"
PASSWORD_WRONG = "WRONG PASSWORD PLEASE TRY AGAIN"
DISCONNECT_MESSAGE = "DISCONNECT!"
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
        send_message(connection, "PLEASE ENTER USER ID(or q to return to options): ")
        user_id = receive_message(connection)
        if user_id:
            if user_id == "q":
                signing_up = False
                continue
            if user_id in user_dict:
                send_message(connection, USERNAME_USED)
                continue
            send_message(connection, USERNAME_ACCEPT)
            print(f"your user id was: {user_id}")
            send_message(connection, "PLEASE ENTER YOU PASSWORD(or q to return to options): ")
            user_password = receive_message(connection)
            if user_password:
                if user_password == "q":
                    signing_up = False
                    continue
                print(f"your password was: {user_password}")
                user_dict[user_id] = user_password
                send_message(connection, "SIGNED-UP SUCCESSFULLY!!")
                signing_up = False

def login(connection):
    logging_in = True
    should_log_in = True #to decide whether to proceed with the "logged in options"
    while logging_in:
        entering_user_name = True
        while entering_user_name:
            send_message(connection, "PLEASE ENTER USER ID(or q to return to options): ")
            user_id = receive_message(connection)
            if user_id:
                if user_id == "q":
                    entering_user_name = False
                    logging_in = False
                    should_log_in = False
                    continue
                if not user_id in user_dict:
                    send_message(connection, INV_USER)
                    continue
                send_message(connection, USERNAME_ACCEPT)
                entering_user_name = False
        if logging_in == False:
            continue
        entering_password = True
        while entering_password:
            send_message(connection, "PLEASE ENTER YOU PASSWORD(or q to return to options): ")
            user_password = receive_message(connection)
            if user_password:
                if user_password == "q":
                    entering_password = False
                    should_log_in = False
                    continue
                if user_dict[user_id] == user_password:
                    send_message(connection, PASSWORD_ACCEPT)
                    send_message(connection, "LOGGED-IN SUCCESSFULLY!!")
                    entering_password = False
                    continue
                else:
                    send_message(connection, PASSWORD_WRONG)
        logging_in = False
    return should_log_in

def logged_in(connection, should_login):
    logged_in = should_login
    still_connected = True # after method execution over, am i still connected to the server
#OPTIONS2 = "PLEASE PRESS A NUMBER TO CONTINUE:\n1.P2P CONNECTION\n2.CREATE GROUP\n3.JOIN GROUP\n4.CHANGE PASSWORD\n5.CHANGE USERNAME\n6.RETURN TO HOME PAGE\n7.DISCONNECT" 
    while logged_in:
        send_message(connection, OPTIONS2)
        choice = receive_message(connection)
        if choice == "1":
            # MARUMO: P2P CONNECTION(EDIT HERE, MARUMO)
            pass
        elif choice == "2":
            # LESEGO: CREATE GROUP(EDIT HERE, LESEGO)
            pass
        elif choice == "3":
            # LESEGO: JOIN GROUP(EDIT HERE, LESEGO)
            pass
        elif choice == "4":
            # Sthembiso: chnage password
            pass
        elif choice == "5":
            # Sthembiso: change username
            pass
        elif choice == "6":
            logged_in = False
            still_connected = True
            continue
        elif choice == "7":
            logged_in = False
            still_connected = False
        else:
            send_message(connection, INV_USER)
    return still_connected


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
                should_login = login(connection)
                if should_login == False:
                    continue
                is_connected = logged_in(connection, should_login)
                if is_connected == False:
                    print(f"{address} {DISCONNECT_MESSAGE}")
                    send_message(connection, DISCONNECT_MESSAGE)
                continue
            elif msg == "3":
                print(f"{address} {DISCONNECT_MESSAGE}")
                send_message(connection, DISCONNECT_MESSAGE)
                is_connected = False
                continue
            else:
                send_message(connection, INV_INPUT)
    connection.close()

def begin():
    server_socket.listen()
    while True:
        connection, address = server_socket.accept()
        thread = threading.Thread(target=thread_manage, args=(connection, address))
        thread.start()

print("the socket server is running...")
begin()
