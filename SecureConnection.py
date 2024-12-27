import os
import socket

import ssl
from FileEncryption import FileEncryption

FORMAT = "utf-8"
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"


class SecureConnection:
    def __init__(self, sock, wrap_socket):
        self.host = '127.0.0.1'
        self.port = 4455
        self.socket = sock
        self.wrap_socket = wrap_socket

    def connect(self):
        self.wrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wrap_socket = ssl.wrap_socket(self.wrap_socket, ca_certs='ssl/certificate.pem')
        self.wrap_socket.connect((self.host, self.port))

    def send_message(self, message):
        data_control = "message".encode(FORMAT)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        message = message.encode(FORMAT)
        self.wrap_socket.send(message)
        print(self.wrap_socket.recv(2048).decode(FORMAT))

    def send_file(self, file_name):
        data_control = "file".encode(FORMAT)
        self.wrap_socket.send(data_control)
        self.wrap_socket.recv(2048).decode(FORMAT)

        file = open(file_name, "rb")

        original_md5 = FileEncryption().calculate_md5(file_name)
        self.wrap_socket.send(original_md5.encode(FORMAT))
        self.wrap_socket.recv(2048).decode(FORMAT)

        data = file.read()
        self.wrap_socket.send(file_name.encode(FORMAT))
        msg = self.wrap_socket.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
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

        print(self.wrap_socket.recv(8192).decode(FORMAT))

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

    def listen_message(self):
        while True:
            message = self.wrap_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print("Message arrived ->", message)
            break

    def listen_file(self):
        while True:
            original_md5 = self.wrap_socket.recv(1024).decode('utf-8')
            if not original_md5:
                break

            filename = self.wrap_socket.recv(1024).decode('utf-8')
            if not filename:
                break

            file_data: bytes = self.wrap_socket.recv(1024)
            if not file_data:
                break

            file = open(f"data/{filename}", "wb")
            file.write(file_data)
            file.close()
            temp_md5 = FileEncryption().calculate_md5(f"data/{filename}")
            if temp_md5 == original_md5:
                print("File received:", filename)
            else:
                os.remove(f"data/{filename}")
                print("Wrong MD5!")

            break
