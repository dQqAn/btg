# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


"""
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""

from SecureConnection import SecureConnection
from UserManagement import UserManagement
import socket
import ssl

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrap_socket = ssl.wrap_socket(sock, ca_certs='ssl/certificate.pem')
secure_connection = SecureConnection(sock, wrap_socket)

user_manager = UserManagement("Users.txt")

control = False

while not control:

    login = int(input('Sign in: 1, Sign Up: 2 \n'))
    userName = (input('userName: '))
    userPwd = (input('userPwd: '))

    if login == 1:
        login_result = user_manager.login(userName, userPwd)
        if login_result:
            control = True
            print("Başarıyla giriş yapıldı.")
            secure_connection.connect()
            # secure_connection.send_message("ada")
            # secure_connection.send_file("temp.txt")
            secure_connection.send_file("ert.png")
            # secure_connection.send_message("!DISCONNECT")
        else:
            print("Kullanıcı adı veya şifre hatalı.")
    elif login == 2:
        user_manager.register_user(userName, userPwd)
        control = True
        print("Kayıt yapıldı.")
        secure_connection.connect()
    else:
        print("Geçersiz komut.")
