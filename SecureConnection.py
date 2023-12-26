import socket
import ssl


# pip install flask

class SecureConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    def establish_connection(self):
        # Socket oluştur
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SSL/TLS bağlantısını kur
        secure_socket = self.context.wrap_socket(client_socket, server_hostname=self.host)

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
secure_connection = SecureConnection("example.com", 443)
secure_connection.establish_connection()
