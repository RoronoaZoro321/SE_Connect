from pydantic import BaseModel

class LoginData(BaseModel):
    student_id: int
    password: str