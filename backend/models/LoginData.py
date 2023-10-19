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