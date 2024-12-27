import hashlib


class FileEncryption:

    def calculate_md5(self, file_name):
        md5_hash = hashlib.md5()
        with open(file_name, 'rb') as file:
            while chunk := file.read(8192):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
