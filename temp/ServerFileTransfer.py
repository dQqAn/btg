from FileEncryption import FileEncryption
from SecureConnection import SecureConnection


class ServerFileTransfer:
    def __init__(self, sunucu_ip, sunucu_port):
        self.sunucu_ip = sunucu_ip
        self.sunucu_port = sunucu_port

    def dosya_al(self):
        ssl_baglanti = SecureConnection(self.sunucu_ip, self.sunucu_port).connect()

        # Dosyanın adını al
        mesaj = ssl_baglanti.recv(1024).decode()
        dosya_adi = mesaj.split(",")[1]

        # Dosya verilerini al
        dosya_verileri = ssl_baglanti.recv(1024)

        # Dosyayı şifresini çözerek hedef konuma kaydet
        FileEncryption().encrypt_file(dosya_verileri, "outpath/" + dosya_adi).save(dosya_adi)

        # Cevabı gönder
        ssl_baglanti.sendall("basarili".encode())

        ssl_baglanti.close()
