import socket

PORT = 4040
HOSTNAME = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOSTNAME, PORT) 

FORMAT = "utf-8"
HEADER = 2048
DISCONNECT_MESSAGE = "DISCONNECT!"

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

options_menu = receive_message()
print(options_menu)

resp1 = input("Enter choice: ")
send_message(resp1)
if resp1 == "1":
    user_id_prompt = receive_message() 
    resp2 = input(user_id_prompt)
    send_message(resp2)
