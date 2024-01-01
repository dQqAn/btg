import socket

import ssl
from FileEncryption import FileEncryption

# pip install flask

FORMAT = "utf-8"
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"


class SecureConnection:
    def __init__(self, sock, wrap_socket):
        self.host = '127.0.0.1'
        # self.host = socket.gethostbyname(socket.gethostname())
        # self.port = 8080
        # self.port = 8443
        # self.port = 8060
        self.port = 4455
        # self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.context = ssl.create_default_context()
        # self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.socket = sock
        self.wrap_socket = wrap_socket
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.wrap_socket = ssl.wrap_socket(self.socket, ca_certs='ssl/certificate.pem')

    def connect(self):
        # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # context.verify_mode = ssl.CERT_REQUIRED
        # # context.load_verify_locations('files/server.pem')
        # context.load_verify_locations('ssl/certificate.pem')
        # # context.load_cert_chain(certfile='files/server3.crt', keyfile='files/server.key')
        # # context.verify_mode = ssl.CERT_REQUIRED
        # # context.check_hostname = True
        # # context.load_default_certs()
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # server_sock = context.wrap_socket(sock, server_hostname=self.host)
        # print("Version:", server_sock.version())
        # server_sock.connect((self.host, self.port))
        # print(f"Güvenli bağlantı başarıyla kuruldu: {self.host}:{self.port}")

        self.wrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wrap_socket = ssl.wrap_socket(self.wrap_socket, ca_certs='ssl/certificate.pem')
        self.wrap_socket.connect((self.host, self.port))

        # self.wrap_socket.connect((self.host, self.port))

    def send_message(self, message):
        # self.wrap_socket.write(message.encode())

        data_control = "message".encode(FORMAT)
        # data_length = len(data_control)
        # send_data_length = str(data_length).encode(FORMAT)
        # send_data_length += b' ' * (SIZE - len(send_data_length))
        # self.wrap_socket.send(send_data_length)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        message = message.encode(FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(FORMAT)
        # send_length += b' ' * (SIZE - len(send_length))
        # self.wrap_socket.send(send_length)
        self.wrap_socket.send(message)
        print(self.wrap_socket.recv(2048).decode(FORMAT))

    def send_file(self, file_name):
        data_control = "file".encode(FORMAT)
        # data_length = len(data_control)
        # send_data_length = str(data_length).encode(FORMAT)
        # send_data_length += b' ' * (SIZE - len(send_data_length))
        # self.wrap_socket.send(send_data_length)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        # file = open(file_name, "r")
        file = open(file_name, "rb")

        original_md5 = FileEncryption().calculate_md5(file_name)
        self.wrap_socket.send(original_md5.encode(FORMAT))
        self.wrap_socket.recv(2048).decode(FORMAT)

        data = file.read()
        self.wrap_socket.send(file_name.encode(FORMAT))
        msg = self.wrap_socket.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        # self.wrap_socket.send(data.encode(FORMAT))
        self.wrap_socket.send(data)
        msg = self.wrap_socket.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        file.close()

    def show_log(self, user_name, user_password):
        data_control = "log".encode(FORMAT)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        temp_user_name = user_name.encode(FORMAT)
        self.wrap_socket.send(temp_user_name)
        self.wrap_socket.recv(2048).decode(FORMAT)

        temp_user_password = user_password.encode(FORMAT)
        self.wrap_socket.send(temp_user_password)
        self.wrap_socket.recv(2048).decode(FORMAT)

        # data_length = self.wrap_socket.recv(2048).decode(FORMAT)
        # data_length = int(data_length)
        # log = self.wrap_socket.recv(data_length).decode(FORMAT)
        # print(log)

        print(self.wrap_socket.recv(2048).decode(FORMAT))

    def login(self, login_info, user_name, user_password, is_admin=False):
        self.connect()

        data_control = "login".encode(FORMAT)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        temp_user_name = user_name.encode(FORMAT)
        self.wrap_socket.send(temp_user_name)
        self.wrap_socket.recv(2048).decode(FORMAT)

        temp_user_password = user_password.encode(FORMAT)
        self.wrap_socket.send(temp_user_password)
        self.wrap_socket.recv(2048).decode(FORMAT)

        temp_is_admin = f"{is_admin}".encode(FORMAT)
        self.wrap_socket.send(temp_is_admin)
        self.wrap_socket.recv(2048).decode(FORMAT)

        data_control = login_info.encode(FORMAT)
        self.wrap_socket.send(data_control)
        login_result = self.wrap_socket.recv(2048).decode(FORMAT)
        return login_result

    def close_conn(self):
        self.send_message(DISCONNECT_MESSAGE)
        self.wrap_socket.close()
