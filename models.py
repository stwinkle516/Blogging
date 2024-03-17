from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import String, Integer, DATETIME,Text,ForeignKey
from flask_login import UserMixin
from typing import List


"""
for response_type
1. Like
2.comment

"""


class Base(DeclarativeBase):
    pass

class Users(UserMixin,Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    Firstname: Mapped[str] = mapped_column(String(45))
    Lastname : Mapped[str] = mapped_column(String(45))
    email : Mapped[str] = mapped_column(String(45))
    contact : Mapped[str] = mapped_column(String(45))
    Pass : Mapped[str] = mapped_column(String(128))
    Created_at : Mapped[str] = mapped_column(DATETIME)
    Updated_at : Mapped[str] = mapped_column(DATETIME)
    Username : Mapped[str] = mapped_column(String(45))

    user_blog : Mapped[List["Blog"]] = relationship(back_populates="blog_user")
    user_response : Mapped['Response'] = relationship(back_populates='response_user')


class Blog(Base):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    content : Mapped[str] = mapped_column(Text)
    title : Mapped[str] = mapped_column(String(45))
    category_id : Mapped[int] = mapped_column(ForeignKey('category.id'))
    is_deleted : Mapped[int] = mapped_column(Integer)
    created_at : Mapped[str] = mapped_column(DATETIME)
    updated_at : Mapped[str] = mapped_column(DATETIME)
    

    blog_user:Mapped[Users]= relationship(back_populates='user_blog')
    blog_category : Mapped["Category"] = relationship(back_populates='category_blog')
    blog_response : Mapped[List['Response']] = relationship(back_populates='response_blog')

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    category: Mapped[str] = mapped_column(String(45))

    category_blog : Mapped[List["Blog"]] = relationship(back_populates='blog_category')


class Response(Base):
    __tablename__= "response"
    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    blog_id : Mapped[int] = mapped_column(ForeignKey('blog.id'))
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    response_type : Mapped[int] = mapped_column(Integer)
    response_args : Mapped[str] = mapped_column(String(128))

    response_user : Mapped['Users'] = relationship(back_populates='user_response')
    response_blog :Mapped['Blog'] = relationship(back_populates='blog_response')
    










