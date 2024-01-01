import socket
import threading

import ssl
from UserManagement import UserManagement
from temp.FileTransferLogger import FileTransferLogger

DISCONNECT_MESSAGE = "!DISCONNECT"


def handle_client(connections, userCount, FORMAT, SIZE, sock, logger, conn, addr):
    userCount += 1
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
        # data = server_ssl.recv(1024)
        # data = server_ssl.read()

        # data_length = server_ssl.recv(SIZE).decode(FORMAT)
        # if not data_length:
        #     break
        # data_length = int(data_length)
        # data = server_ssl.recv(data_length).decode(FORMAT)

        try:
            data = server_ssl.recv(SIZE).decode(FORMAT)
            if not data:
                break
            if str(data) == str(DISCONNECT_MESSAGE):
                server_ssl.send("Message received".encode(FORMAT))
                print('Disconnected with client', userCount)
                logger.log_activity(f'Disconnected with client {addr} - {userCount}')
                userCount -= 1
                connections.remove(server_ssl)
                server_ssl.close()
                connected = False
            elif str(data) == str("file"):
                server_ssl.send("File received".encode(FORMAT))

                original_md5 = server_ssl.recv(SIZE).decode(FORMAT)
                if not original_md5:
                    break
                server_ssl.send(original_md5.encode(FORMAT))

                filename = server_ssl.recv(SIZE).decode(FORMAT)
                if not filename:
                    break
                print(f"[RECV] Receiving the filename:", filename)
                logger.log_activity(f'[RECV] {addr} - {userCount} Receiving the filename: {filename}')
                # file = open(f"data/{filename}", "w")
                file = open(f"data/{filename}", "wb")
                server_ssl.send("Filename received.".encode(FORMAT))

                # file_data = server_ssl.recv(SIZE).decode(FORMAT)
                file_data = server_ssl.recv(SIZE)
                if not file_data:
                    break
                print(f"[RECV] Receiving the file data:", file_data)
                logger.log_activity(f'[RECV] {addr} - {userCount} Receiving the file data: {file_data}')
                # print(f"[RECV] Receiving the file data:", file_data.decode('ISO-8859-1'))
                file.write(file_data)
                server_ssl.send("File data received".encode(FORMAT))
                file.close()
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
                    server_ssl.send(file.read())
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
                        userCount -= 1
                        connections.remove(server_ssl)
                        server_ssl.close()
                        connected = False
                    else:
                        server_ssl.send("True".encode(FORMAT))
                else:
                    user_manager.register_user(user_name, user_pwd, is_admin)
                    server_ssl.send("True".encode(FORMAT))
            else:
                server_ssl.send("Message received".encode(FORMAT))
            # print("Data:", data)
        except Exception as e:
            print("Server error:", e)
            logger.log_error(f"Server error: {e}")
            # Closing all Connections
            for cons in connections:
                cons.close()
            sock.close()
            connected = False
            break


if __name__ == '__main__':
    logger_file_name = "file_transfer_log.txt"
    logger = FileTransferLogger(logger_file_name)

    user_manager = UserManagement("Users.txt")

    host = '127.0.0.1'
    # host = socket.gethostbyname(socket.gethostname())
    # port = 8080
    # port = 8443
    # port = 8060
    port = 4455

    # totalclient = int(input('Enter number of clients: '))

    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain(certfile='ssl/certificate.pem', keyfile='ssl/key.pem')
    # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # server_sock.bind((host, port))
    # server_sock.listen()

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
        # handle_client(connections, userCount, FORMAT, SIZE, sock, logger, conn, addr)
        thread = threading.Thread(target=handle_client,
                                  args=(connections, userCount, FORMAT, SIZE, sock, logger, conn, addr))
        thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    logger.log_activity(f'Server closed')
