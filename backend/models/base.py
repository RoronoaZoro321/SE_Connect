from pydantic import BaseModel


class LoginData(BaseModel):
    student_id: int
    password: str


class SignupData(BaseModel):
    student_id: int
    username: str
    firstName: str
    lastName: str
    password: str


class UserProfileData(BaseModel):
    age: int
    description: str


class PostData(BaseModel):
    content: str


class AddFriendData(BaseModel):
    friend_id: int


class PostInteractData(BaseModel):
    student_id: int
    username: str
    post_id: int

class CommentData(BaseModel):
    comment: str