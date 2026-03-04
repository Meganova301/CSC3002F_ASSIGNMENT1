import socket

PORT = 4040
HOSTNAME = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOSTNAME, PORT) 

FORMAT = "utf-8"
HEADER = 2048
DISCONNECT_MESSAGE = "DISCONNECT!"
USERNAME_USED = "THIS USERNAME IS ALREADY IN USE, TRY ANOTHER ONE"
USERNAME_ACCEPT = "ACCEPT THIS USER NAME"
INV_USER = "THE USER_ID IS INVALID, please try again"
PASSWORD_ACCEPT = "PASSWORD ACCEPTED"
PASSWORD_WRONG = "WRONG PASSWORD PLEASE TRY AGAIN"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)

def receive_message():
    msg_len = client_socket.recv(HEADER).decode(FORMAT).strip()
    if not msg_len:
        return None
    msg_len = int(msg_len)
    return client_socket.recv(msg_len).decode(FORMAT)


def send_message(msg):
    msg = msg.encode(FORMAT)
    msg_len = str(len(msg)).encode(FORMAT)
    space_padding = HEADER - len(msg_len)
    msg_len = msg_len + b" "*space_padding

    client_socket.send(msg_len)
    client_socket.send(msg)

is_connected = True
while is_connected:
    options_menu = receive_message()
    print(options_menu)

    #resp just stands for response
    resp1 = input("Enter choice: ")
    send_message(resp1)
    if resp1 == "1":
        signing_up = True
        while signing_up:
            user_id_prompt = receive_message() 
            resp2 = input(user_id_prompt)
            send_message(resp2)
            was_user_name_accepted = receive_message()
            print(was_user_name_accepted)
            if was_user_name_accepted == USERNAME_USED:
                continue  
            password_prompt = receive_message()
            resp3 = input(password_prompt)
            print(f"your password was: {resp3}")
            send_message(resp3)
            print(receive_message())
            signing_up = False
        continue
    
    if resp1 == "2":
        logging_in = True
        while logging_in:
            is_verifying_user_name = True
            while is_verifying_user_name:
                    
                user_id_prompt = receive_message() 
                resp2 = input(user_id_prompt)
                send_message(resp2)
                was_user_name_accepted = receive_message()
                print(was_user_name_accepted)
                if was_user_name_accepted == INV_USER:
                    continue
                is_verifying_user_name = False
            is_verifying_password = True
            while is_verifying_password:
                password_prompt = receive_message()
                resp3 = input(password_prompt)
                send_message(resp3)
                is_verifying_password = True
                password_status = receive_message()
                print(password_status)
                if password_status == PASSWORD_WRONG:
                    continue
                print(receive_message())
                is_verifying_password = False
            logging_in = False
