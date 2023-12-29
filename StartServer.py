import socket
import ssl
import urllib
from urllib.request import urlopen

DISCONNECT_MESSAGE = "!DISCONNECT"

if __name__ == '__main__':

    host = '127.0.0.1'
    # host = socket.gethostbyname(socket.gethostname())
    # port = 8443
    # port = 8060
    port = 4455
    # port = 8080

    # totalclient = int(input('Enter number of clients: '))

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind((host, port))
    # sock.listen()

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

    while True:
        conn, addr = sock.accept()
        connections.append(conn)
        userCount += 1
        print(f'Connected with client {addr}', userCount)
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

            data_length = server_ssl.recv(SIZE).decode(FORMAT)
            if not data_length:
                break
            data_length = int(data_length)
            data = server_ssl.recv(data_length).decode(FORMAT)
            if not data:
                break
            if str(data) == str(DISCONNECT_MESSAGE):
                print('Disconnected with client', userCount)
                userCount -= 1
                server_ssl.send("Message received".encode(FORMAT))
                server_ssl.close()
                connected = False
            else:
                server_ssl.send("Message received".encode(FORMAT))
            print("Data:", data)

    # while True:
    #     try:
    #         ssock = context.wrap_socket(server_sock, server_side=True)
    #         conn, addr = ssock.accept()
    #         data = ssock.recv(1024)
    #         connections.append(conn)
    #         userCount += 1
    #     except Exception as e:
    #         print("Server error:", e)
    #         server_sock.close()
    #         break
    #     finally:
    #         server_sock.close()
    #         break

    # while True:
    #     conn, address = sock.accept()
    #     while True:
    #         connections.append(conn)
    #         userCount += 1
    #         print('Connected with client', userCount)
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         print("Data receiving...")
    #         conn.close()
"""
"""
# connections = []
# for i in range(totalclient):
#     # conn, address = sock.accept()
#     conn = sock.accept()
#     connections.append(conn)
#     print('Connected with client', i + 1)
#
# fileno = 0
# idx = 0
# for conn in connections:
#     # Receiving File Data
#     idx += 1
#     data = conn[0].recv(1024).decode()
#
#     if not data:
#         continue
#     # Creating a new file at server end and writing the data
#     filename = 'output' + str(fileno) + '.txt'
#     fileno = fileno + 1
#     fo = open(filename, "w")
#     while data:
#         if not data:
#             break
#         else:
#             fo.write(data)
#             data = conn[0].recv(1024).decode()
#
#     print()
#     print('Receiving file from client', idx)
#     print()
#     print('Received successfully! New filename is:', filename)
#     fo.close()
#     # Closing all Connections
# for conn in connections:
#     conn[0].close()
