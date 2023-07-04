from pydantic import BaseModel, EmailStr, Field


class RobotUser(BaseModel):
    login: str
    password: str
    email: EmailStr


class RobotLoginForm(BaseModel):
    login: str
    password: str


class Video(BaseModel):
    video: str = Field(..., description="Video file")
    description: str = Field(..., description="Video description")


class EditVideo(BaseModel):
    description: str = Field(..., description="Video description")
