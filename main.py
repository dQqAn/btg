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

import socket

import ssl
from SecureConnection import SecureConnection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrap_socket = ssl.wrap_socket(sock, ca_certs='ssl/certificate.pem')
secure_connection = SecureConnection(sock, wrap_socket)

control = False
DISCONNECT_MESSAGE = "!DISCONNECT"

while not control:

    login = int(input('Sign in: 1, Sign Up: 2 -> '))
    userName = str(input('userName: '))
    userPwd = str(input('userPwd: '))

    if login == 1:
        login_result = secure_connection.login("sign_in", userName, userPwd)

        if str(login_result) == "True":
            control = True
            print("Login success.")
            # secure_connection.send_message("yum")
            # secure_connection.send_file("temp.txt")
            # secure_connection.show_log(userName, userPwd)
            secure_connection.send_file("ert.png")
            # secure_connection.send_message(DISCONNECT_MESSAGE)
            secure_connection.close_conn()
        else:
            print("Wrong user name or password.")
            secure_connection.close_conn()
    elif login == 2:
        is_admin = input('Admin: True or False -> ')
        secure_connection.login("sign_up", userName, userPwd, is_admin)
        control = True
        print("Register success.")
    else:
        print("Unknown command.")
        secure_connection.close_conn()
