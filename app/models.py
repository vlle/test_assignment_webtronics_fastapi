from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

Base = declarative_base()


class Robot(Base):
    __tablename__ = "robot"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(50))
    videos: Mapped[List["Video"]] = relationship("Video", backref="robot")


class Video(Base):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(512))
    author: Mapped[int] = mapped_column(ForeignKey("robot.id"))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
