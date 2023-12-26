from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import ecdsa
import hashlib
import os


# pip install cryptography

class FileEncryption:
    def __init__(self, sender_private_key, recipient_public_key):
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key

    """
    def dosya_sifrele(self, dosya_adi):
        with open(dosya_adi, "rb") as f:
            veri = f.read()

        # Elliptic Curve Diffie-Hellman şifrelemeyi kullan
        anahtar = ecdsa.generate_private_key(curve=ecdsa.SECP256K1)

        # Dosyayı şifrele
        encrypted_data = anahtar.encrypt(veri, hashlib.sha256(veri).digest())

        return encrypted_data

    def dosya_desifrele(self, encrypted_data):
        # Elliptic Curve Diffie-Hellman şifrelemeyi kullan
        anahtar = ecdsa.SigningKey.from_private_bytes(self.private_key)

        # Dosyayı deşifrele
        decrypted_data = anahtar.decrypt
"""
    def encrypt_file(self, file_path, output_path):
        with open(file_path, 'rb') as file:
            plaintext = file.read()

        # Dosyayı şifrele
        ciphertext = self._encrypt(plaintext)

        # Şifrelenmiş dosyayı kaydet
        with open(output_path, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)

    def decrypt_file(self, encrypted_path, output_path):
        with open(encrypted_path, 'rb') as file:
            ciphertext = file.read()

        # Şifrelenmiş dosyayı deşifrele
        plaintext = self._decrypt(ciphertext)

        # Deşifrelenmiş dosyayı kaydet
        with open(output_path, 'wb') as decrypted_file:
            decrypted_file.write(plaintext)

    def _encrypt(self, data):
        # Eliptik Eğri Şifreleme (ECIES) kullanarak veriyi şifrele
        private_key = serialization.load_pem_private_key(self.sender_private_key, password=None,
                                                         backend=default_backend())
        public_key = serialization.load_pem_public_key(self.recipient_public_key, backend=default_backend())
        shared_key = private_key.exchange(ec.ECDH(), public_key)
        derived_key = self._derive_key(shared_key)
        ciphertext = self._aes_encrypt(data, derived_key)
        return ciphertext

    def _decrypt(self, data):
        # Eliptik Eğri Şifreleme (ECIES) kullanarak veriyi deşifrele
        private_key = serialization.load_pem_private_key(self.sender_private_key, password=None,
                                                         backend=default_backend())
        public_key = serialization.load_pem_public_key(self.recipient_public_key, backend=default_backend())
        shared_key = private_key.exchange(ec.ECDH(), public_key)
        derived_key = self._derive_key(shared_key)
        plaintext = self._aes_decrypt(data, derived_key)
        return plaintext

    def _derive_key(self, shared_key):
        # Paylaşılan anahtardan türetilmiş bir anahtar elde et
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=os.urandom(16), iterations=100000,
                         backend=default_backend())
        derived_key = kdf.derive(shared_key)
        return derived_key

    def _aes_encrypt(self, data, key):
        # AES kullanarak veriyi şifrele
        # Bu kısmı uygun bir kütüphane kullanarak implement etmek daha güvenli olacaktır
        # Ancak burada basitleştirilmiş bir örnek bulunmaktadır
        # Gerekirse daha güçlü bir kütüphane kullanılabilir
        # Örneğin: https://cryptography.io/en/latest/
        # Not: Şifreleme kısmında hazır kütüphanelerden faydalanılmayacağı belirtilmişti
        encrypted_data = data  # Bu kısmı güvenli bir şekilde implement etmek gerekir
        return encrypted_data

    def _aes_decrypt(self, data, key):
        # AES kullanarak veriyi deşifrele
        # Bu kısmı uygun bir kütüphane kullanarak implement etmek daha güvenli olacaktır
        # Ancak burada basitleştirilmiş bir örnek bulunmaktadır
        # Gerekirse daha güçlü bir kütüphane kullanılabilir
        # Örneğin: https://cryptography.io/en/latest/
        # Not: Şifreleme kısmında hazır kütüphanelerden faydalanılmayacağı belirtilmişti
        decrypted_data = data  # Bu kısmı güvenli bir şekilde implement etmek gerekir
        return decrypted_data


# Örnek kullanım
sender_private_key = b"Sender Private Key"  # Örnek olarak belirtilmiş bir private key
recipient_public_key = b"Recipient Public Key"  # Örnek olarak belirtilmiş bir public key

file_encryption = FileEncryption(sender_private_key, recipient_public_key)
file_encryption.encrypt_file("plain.txt", "encrypted.txt")
file_encryption.decrypt_file("encrypted.txt", "decrypted.txt")
