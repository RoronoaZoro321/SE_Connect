import persistent
from backend.services.Post import PostServ


class User(persistent.Persistent):
    def __init__(self, student_id: int, username: str, firstname: str, lastname: str, password: str):
        self.student_id = student_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = str(self.student_id) + "@kmitl.ac.th"
        self.description = ""
        self.friends = []  # list[id, id, id] find from user_id
        self.posts = []  # [id id id ] find from post_id
        self.age = 0
        self.startUpPosts = [] # [id id id ] find from post_id

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

    def set_age(self, age: int):
        self.age = age

    def set_description(self, description: str):
        self.description = description

    def add_post(self, post):
        self.posts.append(post)
        self._p_changed = True

    def get_student_id(self):
        return self.student_id

    def get_username(self):
        return self.username

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    def get_age(self):
        return self.age

    def get_description(self):
        return self.description

    def get_friends(self):
        return self.friends

    def add_friend(self, friend_id: int):
        if friend_id not in self.friends:
            self.friends.append(friend_id)
            self._p_changed = True
            return True
        else:
            return False

    def remove_friend(self, friend_id: int):
        if friend_id in self.friends:
            self.friends.remove(friend_id)
            self._p_changed = True
            return True
        else:
            return False

    def get_posts(self):
        return self.posts
    
    def get_startUpPosts(self):
        return self.startUpPosts
    
    def add_startUpPost(self, post_id):
        self.startUpPosts.append(post_id)
        self._p_changed = True
    
    def remove_startUpPost(self, post_id):
        self.startUpPosts.remove(post_id)
        self._p_changed = True


class Post(persistent.Persistent):
    def __init__(self, id: int, user_id: int, username: str, content: str):
        self.id = id
        self.time = PostServ.getTimeNow()
        self.time_diff = None
        self.user_id = user_id
        self.username = username
        self.content = content
        self.image = ""
        self.likes = []
        self.likes_count = 0
        self.comments = []
        self.comments_count = 0
        self.share = None

    def __str__(self):
        return f"Post: {self.id} {self.user_id} {self.content}"

    def print_post(self):
        print(self.__str__())

    def set_content(self, content: str):
        self.content = content

    def get_id(self):
        return self.id
    
    def get_time(self):
        return self.time
    
    def get_time_diff(self):
        self.time_diff = PostServ.getTimeDifference(self.time)
        return self.time_diff

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username
    
    def get_content(self):
        return self.content

    def get_likes(self):
        return self.likes
    
    def get_likes_count(self):
        return self.likes_count

    def get_comments(self):
        return self.comments

    def get_comments_count(self):
        return self.comments_count
    
    def get_share(self):
        return self.share

    def add_like(self, minimal_user):
        self.likes.append(minimal_user)
        self.likes_count += 1
        self._p_changed = True

    def remove_like(self, minimal_user):
        try:
            self.likes.remove(minimal_user)
            self.likes_count -= 1
            self._p_changed = True
            return 1
        except:
            print("Unable to remove like from user" + minimal_user)
            return 0

    def add_comment(self, minimal_user, commentData):
        commentDataDict = commentData.model_dump()
        commentDataDict.update({"time": PostServ.getTimeNow(), "time_diff": None})
        minimal_user.update({"comment": commentDataDict})
        self.comments.append(minimal_user)
        self.comments_count += 1
        self._p_changed = True

    def set_share(self, link):
        self.share = link


class Skill(persistent.Persistent):
    def __init__(self, title:str, description:str):
        self.title = title
        self.description = description


class StartUpPost(persistent.Persistent):
    def __init__(self, id: int, user_id: int, username: str, title:str, description:str, skills:list):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.title = title
        self.description = description
        self.skills = skills
        self.enrolls = []
    
    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id
    
    def get_username(self):
        return self.username
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_skills(self):
        return self.skills
    
    def get_enrolls(self):
        return self.enrolls
    
    def add_skill(self, skill):
        self.skills.append(skill)
        self._p_changed = True

    def add_enroll(self, enroll_user_id):
        self.enrolls.append(enroll_user_id)
        self._p_changed = True


    