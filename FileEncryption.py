import hashlib


class FileEncryption:

    def calculate_md5(self, file_name):
        # Dosyanın MD5 hash'ini hesapla
        md5_hash = hashlib.md5()
        with open(file_name, 'rb') as file:
            # Dosyanın içeriğini oku ve hash'e ekle
            while chunk := file.read(8192):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
