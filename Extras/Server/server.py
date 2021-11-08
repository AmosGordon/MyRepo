import socket
import threading
import hashlib

HEADER = 64
PORT = 5050
SERVER = "".join(socket.gethostbyname_ex(socket.gethostname())[2][3])
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
CHANGE_NAME = "!NAME"
LOGIN = "!LOGIN"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

client_list = []
msg_list = []
master_list = []


class Client:
    def __init__(self, name, address, conn):
        self.name = name
        self.address = address
        self.conn = conn


def send(name, msg, client):
    message = f"[{name}] {msg}".encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.conn.send(send_length)
    client.conn.send(message)


def check_clients(conn):
    for i in client_list:
        if i.conn == conn:
            return i


def check_login(conn, username, password):
    with open("shadow.txt", "r") as file:
        if username == file.readlines()[0][:-1]:
            temp = []
            key = 0b011011
            for char in password:
                x = ord(char) + 74
                while x > 122:
                    x = 65 + (x - 122)
                x = chr(x)
                x = bytearray(x, FORMAT)
                y = 0
                for byte in x:
                    binary = bin(byte)
                    y += int(binary, 2)
                y = y ^ key
                while y > 122:
                    y = 65 + (y - 122)
                y = chr(y)
                temp.append(y)
            full = ""
            for i in temp:
                full += i
            hashed = hashlib.md5(full.encode(FORMAT)).hexdigest()
            with open("shadow.txt", "r") as file2:
                pass_correct = False
                for lines in file2:
                    if hashed == lines:
                        pass_correct = True
                        break
                if pass_correct:
                    message = "!PASSWORD_CORRECT".encode(FORMAT)
                    msg_length = len(message)
                    send_length = str(msg_length).encode(FORMAT)
                    send_length += b" " * (HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(message)
                else:
                    message = "!PASSWORD_INCORRECT".encode(FORMAT)
                    msg_length = len(message)
                    send_length = str(msg_length).encode(FORMAT)
                    send_length += b" " * (HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(message)

        else:
            message = "!USERNAME_INCORRECT".encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(message)


def handle_client(conn, address):
    while True:
        global msg_list
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "!CONNECTED":
                returned = False
                for i in client_list:
                    if i.address[0] == address[0]:
                        returned = True
                        print(f"[Welcome Back] {i.name} has joined at address {address}")
                        i.address = address
                        i.conn = conn
                if not returned:
                    print(f"[NEW CONNECTION] {address} connected.")
                    client_list.append(Client(address[0], address, conn))
                for item in master_list:
                    send(item[0], item[1], check_clients(conn))

            elif msg == LOGIN:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                msg_length = int(msg_length)
                username = conn.recv(msg_length).decode(FORMAT)
                msg_length = int(msg_length)
                password = conn.recv(msg_length).decode(FORMAT)
                check_login(conn, username, password)
                break

            elif msg == DISCONNECT_MESSAGE:
                print(f"{address} {msg}")
                break

            elif CHANGE_NAME in msg:
                start_index = msg.index(CHANGE_NAME)
                new_name = msg[start_index + 6:]
                master_list.append((check_clients(conn).name,
                                    f"changed their name to {new_name}"))
                for i in client_list:
                    send(check_clients(conn).name, f"changed their name to {new_name}", i)
                check_clients(conn).name = new_name
                print(f"{address} changed their name to {new_name}")
            else:
                print(f"{address} {msg}")
                msg_list.append((check_clients(conn).name, msg))
                master_list.append((check_clients(conn).name, msg))
                for item in msg_list:
                    for i in client_list:
                        send(item[0], item[1], i)
                msg_list = []


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDRESS}")
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Sever is starting...")
start()
