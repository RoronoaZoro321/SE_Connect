import persistent

class User(persistent.Persistent):
    def __init__(self, id: int, username: str, firstname: str, lastname: str, password: str):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.frineds = set() # set(id, id, id) find from user_id
        self.posts = [] # [id id id ] find from post_id
    
    def __str__(self):
        return f"User: {self.username} {self.firstname} {self.lastname} {self.password}"
    
    def print_user(self):
        print(self.__str__())
    
    def set_username(self, username: str):
        self.username = username
    def set_firstname(self, firstname: str):
        self.firstname = firstname
    def set_lastname(self, lastname: str):
        self.lastname = lastname
    def set_password(self, password: str):
        self.password = password
    
    def get_id(self):
        return self.id
    def get_username(self):
        return self.username
    def get_firstname(self):
        return self.firstname
    def get_lastname(self):
        return self.lastname
    def get_password(self):
        return self.password
    
class Post(persistent.Persistent):
    def __init__(self, id: int, user_id: int, content: str):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.comments = []
    
    def __str__(self):
        return f"Post: {self.id} {self.user_id} {self.content}"
    
    def print_post(self):
        print(self.__str__())
    
    def set_content(self, content: str):
        self.content = content
    
    def get_id(self):
        return self.id
    def get_user_id(self):
        return self.user_id
    def get_content(self):
        return self.content