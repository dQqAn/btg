import socket
import threading

import ssl
from FileTransferLogger import FileTransferLogger
from UserManagement import UserManagement

DISCONNECT_MESSAGE = "!DISCONNECT"


def handle_client(connections, userCount, FORMAT, SIZE, sock, logger, conn, addr):
    print(f'Connected with client {addr}', userCount)
    logger.log_activity(f'Connected with client {addr} - {userCount}')
    server_ssl = ssl.wrap_socket(
        conn,
        server_side=True,
        certfile='ssl/certificate.pem',
        keyfile='ssl/key.pem',
        ssl_version=ssl.PROTOCOL_TLSv1
    )
    connections.append(server_ssl)

    connected = True
    while connected:
        try:
            data = server_ssl.recv(SIZE).decode(FORMAT)
            if not data:
                break
            if str(data) == str(DISCONNECT_MESSAGE):
                server_ssl.send("Message received".encode(FORMAT))
                print('Disconnected with client', userCount)
                logger.log_activity(f'Disconnected with client {addr} - {userCount}')

                connections.remove(server_ssl)
                server_ssl.close()
                connected = False
            elif str(data) == str("file"):
                server_ssl.send("File received".encode(FORMAT))

                original_md5 = server_ssl.recv(SIZE).decode(FORMAT)
                if not original_md5:
                    break
                for cons in connections:
                    cons.send(original_md5.encode(FORMAT))

                filename = server_ssl.recv(SIZE).decode(FORMAT)
                if not filename:
                    break
                print(f"[RECV] Receiving the filename:", filename)
                logger.log_activity(f'[RECV] {addr} - {userCount} Receiving the filename: {filename}')
                for cons in connections:
                    if cons != server_ssl:
                        cons.send(filename.encode(FORMAT))

                server_ssl.send("Filename received.".encode(FORMAT))

                file_data = server_ssl.recv(SIZE)
                if not file_data:
                    break
                print(f"[RECV] Receiving the file data:", file_data)
                logger.log_activity(f'[RECV] {addr} - {userCount} Receiving the file data: {file_data}')
                for cons in connections:
                    if cons != server_ssl:
                        cons.send(file_data)

                server_ssl.send("File data received".encode(FORMAT))
            elif str(data) == str("log"):
                server_ssl.send("Log".encode(FORMAT))

                user_name = server_ssl.recv(SIZE).decode(FORMAT)
                if not user_name:
                    break
                server_ssl.send(user_name.encode(FORMAT))

                user_pwd = server_ssl.recv(SIZE).decode(FORMAT)
                if not user_pwd:
                    break
                server_ssl.send(user_pwd.encode(FORMAT))

                is_admin = user_manager.is_admin(user_name, user_pwd)
                if is_admin:
                    file = open(logger_file_name, "rb")

                    temp_log = file.read()

                    data_length = len(temp_log)
                    send_data_length = str(data_length).encode(FORMAT)
                    send_data_length += b' ' * (SIZE - len(send_data_length))
                    if int(send_data_length) >= 16384:
                        send_data_length = 8192
                    else:
                        send_data_length = 4096

                    server_ssl.send(temp_log[-send_data_length:])
                    file.close()
                else:
                    server_ssl.send("You are not admin.".encode(FORMAT))
            elif str(data) == str("login"):
                server_ssl.send("Login".encode(FORMAT))

                user_name = server_ssl.recv(SIZE).decode(FORMAT)
                if not user_name:
                    break
                server_ssl.send(user_name.encode(FORMAT))

                user_pwd = server_ssl.recv(SIZE).decode(FORMAT)
                if not user_pwd:
                    break
                server_ssl.send(user_pwd.encode(FORMAT))

                is_admin = server_ssl.recv(SIZE).decode(FORMAT)
                if not is_admin:
                    break
                server_ssl.send(is_admin.encode(FORMAT))

                login_info = server_ssl.recv(SIZE).decode(FORMAT)
                if not login_info:
                    break

                if str(login_info) == "sign_in":
                    login_result = user_manager.login(user_name, user_pwd)
                    if not login_result:
                        server_ssl.send("False".encode(FORMAT))
                        print('Disconnected with client', userCount)
                        logger.log_activity(f'Disconnected with client {addr} - {userCount}')
                        # userCount -= 1
                        connections.remove(server_ssl)
                        server_ssl.close()
                        connected = False
                    else:
                        server_ssl.send("True".encode(FORMAT))
                else:
                    user_manager.register_user(user_name, user_pwd, is_admin)
                    server_ssl.send("True".encode(FORMAT))
            else:
                if str(data) != str("message"):
                    for cons in connections:
                        if cons != server_ssl:
                            cons.send(data.encode(FORMAT))
                        else:
                            cons.send("Message sent".encode(FORMAT))
                else:
                    server_ssl.send("Message received".encode(FORMAT))
        except Exception as e:
            connections.remove(server_ssl)
            print("Client status:", e)
            logger.log_error(f"Client status: {e}")
            server_ssl.close()
            break


if __name__ == '__main__':
    logger_file_name = "file_transfer_log.txt"
    logger = FileTransferLogger(logger_file_name)

    user_manager = UserManagement("Users.txt")

    host = '127.0.0.1'
    port = 4455

    connections = []
    userCount = 0

    FORMAT = "utf-8"
    SIZE = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    logger.log_activity(f'Server started')

    while True:
        conn, addr = sock.accept()
        userCount = threading.activeCount()
        thread = threading.Thread(target=handle_client,
                                  args=(connections, userCount, FORMAT, SIZE, sock, logger, conn, addr))
        thread.start()

    logger.log_activity(f'Server closed')
