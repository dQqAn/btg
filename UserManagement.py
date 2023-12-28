from flask import Flask, render_template, request, redirect, url_for
import hashlib


class UserManagement:
    def __init__(self, user_file_path):
        self.user_file_path = user_file_path

    def register_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(self.user_file_path, 'a') as user_file:
            user_file.write(f"{username}:{hashed_password}\n")

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(self.user_file_path, 'r') as user_file:
            for line in user_file:
                stored_username, stored_hashed_password = line.strip().split(':')
                if username == stored_username and hashed_password == stored_hashed_password:
                    return True

        return False


"""
 # Sunucu tarafında kullanıcı bilgilerini saklayan dosya yolu
user_file_path = "users.txt"

# Kullanıcı yönetimi sınıfını başlat
user_manager = UserManagement(user_file_path)

# Kullanıcı kaydı
user_manager.register_user("kullanici1", "parola123")

# Kullanıcı girişi
login_result = user_manager.login("kullanici1", "parola123")

if login_result:
    print("Başarıyla giriş yapıldı.")
else:
    print("Kullanıcı adı veya şifre hatalı.")
"""
