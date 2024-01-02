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


def menu(user_name, user_pwd):
    menu_control = True
    while menu_control:

        menu_option = int(input("1. Send File \n2. Send Message \n3. Show Log \n4. Listen Message \n5. Exit \n-> "))

        if menu_option == 1:
            file_name = str(input("File name -> "))
            secure_connection.send_file(file_name)
        elif menu_option == 2:
            message = str(input("Message -> "))
            secure_connection.send_message(message)
        elif menu_option == 3:
            secure_connection.show_log(user_name, user_pwd)
        elif menu_option == 4:
            secure_connection.receive_message()

            # message_thread = threading.Thread(target=secure_connection.receive_messages, args=())
            # message_thread.start()
            # message_thread.join(timeout=5) # snooze for 5 second
        elif menu_option == 5:
            secure_connection.close_conn()
            menu_control = False


while not control:

    login = int(input('Sign in: 1, Sign Up: 2 -> '))
    userName = str(input('userName: '))
    userPwd = str(input('userPwd: '))

    if login == 1:
        login_result = secure_connection.login("sign_in", userName, userPwd)

        if str(login_result) == "True":
            print("Login success.")
            menu(userName, userPwd)
            control = True
        else:
            print("Wrong user name or password.")
            secure_connection.close_conn()
    elif login == 2:
        is_admin = input('Admin: True or False -> ')
        secure_connection.login("sign_up", userName, userPwd, is_admin)
        print("Register success.")
        menu(userName, userPwd)
        control = True
    else:
        print("Unknown command.")
        secure_connection.close_conn()
