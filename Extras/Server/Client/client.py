import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
SERVER = "192.168.100.138"
ADDRESS = (SERVER, PORT)


class Connection:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(FORMAT)
            return msg
