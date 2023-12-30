import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)
    """ Opening and reading the file data. """
    file = open("data/yt.txt", "r")
    data = file.read()
    """ Sending the filename to the server. """
    client.send("yt.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    """ Sending the file data to the server. """
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    """ Closing the file. """
    file.close()
    """ Closing the connection from the server. """
    client.close()


if __name__ == "__main__":
    main()

# import socket
#
# if __name__ == '__main__':
#     # Creating Client Socket
#
#     host = '127.0.0.1'
#     port = 8080
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # Connecting with Server
#     sock.connect((host, port))
#
#     while True:
#
#         filename = input('Input filename you want to send: ')
#         try:
#             # Reading file and sending data to server
#             fi = open(filename, "r")
#             data = fi.read()
#             if not data:
#                 break
#             while data:
#                 sock.send(str(data).encode())
#                 data = fi.read()
#                 # File is closed after data is sent
#             fi.close()
#
#         except IOError:
#             print('You entered an invalid filename!\
#             Please enter a valid name')
