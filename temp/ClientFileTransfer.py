from FileEncryption import FileEncryption
from SecureConnection import SecureConnection


class DosyaTransferi():
    def __init__(self, sunucu_ip, sunucu_port):
        self.sunucu_ip = sunucu_ip
        self.sunucu_port = sunucu_port

    def dosya_gonder(self, dosya_adi):
        ssl_baglanti = SecureConnection(self.sunucu_ip, self.sunucu_port).connect()

        # Dosyanın adını suncuya gönder
        mesaj = "dosya_gonder" + "," + dosya_adi
        ssl_baglanti.sendall(mesaj.encode())

        # Dosyayı şifreleyerek gönder
        dosya_verileri = FileEncryption().decrypt_file(dosya_adi, "outpath/" + dosya_adi)
        ssl_baglanti.sendall(dosya_verileri)

        # Cevabı al
        cevap = ssl_baglanti.recv(1024).decode()

        ssl_baglanti.close()

        return cevap == "basarili"
