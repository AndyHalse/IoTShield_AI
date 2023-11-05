
class User:
    def __init__(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

    def can_view(self):
        return self.access_level in ["view", "view_print", "full"]

    def can_print(self):
        return self.access_level in ["view_print", "full"]

    def has_full_access(self):
        return self.access_level == "full"

class UserManager:
    def __init__(self):
        self.users = {
            "Admin": User("Admin", "Admin1234&&", "full"),
            "Emma": User("Emma", "ViewPrint1234&&", "view_print"),
            "Andy": User("Andy", "View1234&&", "view")
        }

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

def view_content(user):
    if user.can_view():
        return "You are viewing the content."
    return "You don't have permission to view the content."

def print_content(user):
    if user.can_print():
        return "You are printing the content."
    return "You don't have permission to print the content."

def modify_content(user):
    if user.has_full_access():
        return "You have modified the content."
    return "You don't have permission to modify the content."
