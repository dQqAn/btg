import hashlib


class UserManagement:
    def __init__(self, user_file_path):
        self.user_file_path = user_file_path

    def register_user(self, username, password, is_admin=False):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(self.user_file_path, 'a') as user_file:
            user_file.write(f"{username}:{hashed_password}:{'Yes' if str(is_admin) == 'True' else 'No'}\n")

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(self.user_file_path, 'r') as user_file:
            for line in user_file:
                stored_username, stored_hashed_password, is_admin = line.strip().split(':')
                if username == stored_username and hashed_password == stored_hashed_password:
                    return True

        return False

    def is_admin(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(self.user_file_path, 'r') as user_file:
            for line in user_file:
                stored_username, stored_hashed_password, is_admin = line.strip().split(':')
                if username == stored_username and hashed_password == stored_hashed_password:
                    return is_admin.lower() == 'yes'

        return False
