from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, PrimaryKeyConstraint, String, Table
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

Base = declarative_base()


likes_table = Table(
    "association_table",
    Base.metadata,
    Column("liked_video", ForeignKey("video.id")),
    Column("like_owner", ForeignKey("robot.id")),
    PrimaryKeyConstraint("liked_video", "like_owner"),
)


class Robot(Base):
    __tablename__ = "robot"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    videos: Mapped[List["Video"]] = relationship("Video", backref="robot")
    liked_videos: Mapped[List["Video"]] = relationship(
        secondary=likes_table, back_populates="likes"
    )


class Video(Base):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(512))
    author: Mapped[int] = mapped_column(ForeignKey("robot.id"))
    likes: Mapped[List["Robot"]] = relationship(
        "Robot", secondary=likes_table, back_populates="liked_videos"
    )
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
