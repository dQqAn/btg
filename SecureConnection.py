import socket
import ssl
import http.server
from http.client import HTTPSConnection
from os import system
from os.path import join

# pip install flask

FORMAT = "utf-8"
SIZE = 1024


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
        # soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # soket.connect((self.host, self.port))

        # context = ssl.create_default_context()
        # with socket.create_connection((self.host, self.port)) as sock:
        #     with context.wrap_socket(sock, server_hostname=self.host) as ssock:
        #         print(ssock.version())

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

        # soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_ssl = ssl.wrap_socket(soket, ca_certs='ssl/certificate.pem')
        # client_ssl.connect((self.host, self.port))

        self.wrap_socket.connect((self.host, self.port))

    def send_message(self, message):
        # self.wrap_socket.write(message.encode())

        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (SIZE - len(send_length))
        self.wrap_socket.send(send_length)
        self.wrap_socket.send(message)
        print(self.wrap_socket.recv(2048).decode(FORMAT))

    def establish_connection(self):
        # Socket oluştur
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SSL/TLS bağlantısını kur
        # secure_socket = self.context.wrap_socket(client_socket, server_hostname=self.host)
        secure_socket = ssl.wrap_socket(client_socket, ca_certs=None, cert_reqs=ssl.CERT_REQUIRED)
        # secure_socket = ssl.wrap_socket(client_socket, ca_certs='cert.pem',
        #                                 cert_reqs=ssl.CERT_REQUIRED,
        #                                 ssl_version=ssl.PROTOCOL_TLSv1)

        try:
            # Bağlantıyı kur
            secure_socket.connect((self.host, self.port))
            print(f"Güvenli bağlantı başarıyla kuruldu: {self.host}:{self.port}")
            # return secure_socket
        except Exception as e:
            print(f"Hata: {e}")
            # return None
        finally:
            # Bağlantıyı kapat
            secure_socket.close()

        def veri_gonder(self, veri):
            ssl_baglanti = self.baglan()

            # Veriyi gönder
            ssl_baglanti.sendall(veri.encode())

            # Cevabı al
            cevap = ssl_baglanti.recv(1024).decode()

            ssl_baglanti.close()

            return cevap

# Örnek kullanım
# secure_connection = SecureConnection("example.com", 443)
# secure_connection.establish_connection()
