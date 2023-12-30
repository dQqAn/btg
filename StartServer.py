import socket

import ssl
from temp.FileTransferLogger import FileTransferLogger

DISCONNECT_MESSAGE = "!DISCONNECT"

if __name__ == '__main__':

    logger_file_name = "file_transfer_log.txt"
    logger = FileTransferLogger(logger_file_name)

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
        connections.append(conn)
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
                    print('Disconnected with client', userCount)
                    logger.log_activity(f'Disconnected with client {addr} - {userCount}')
                    userCount -= 1
                    server_ssl.send("Message received".encode(FORMAT))
                    server_ssl.close()
                    connected = False
                elif str(data) == str("file"):
                    server_ssl.send("File received".encode(FORMAT))

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
                    file = open(logger_file_name, "rb")
                    server_ssl.send(file.read())
                else:
                    server_ssl.send("Message received".encode(FORMAT))
                print("Data:", data)
            except Exception as e:
                print("Server error:", e)
                logger.log_error(f"Server error: {e}")
                sock.close()
                break

    logger.log_activity(f'Server closed')

# Closing all Connections
# for conn in connections:
#     conn[0].close()
