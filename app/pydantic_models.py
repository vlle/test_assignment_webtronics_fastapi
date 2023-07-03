from pydantic import BaseModel, EmailStr


class RobotUser(BaseModel):
    login: str
    password: str
    email: EmailStr


class RobotLoginForm(BaseModel):
    login: str
    password: str
