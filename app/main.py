# robot dating application (tinder)

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# def signup
@app.get("/signup")
async def signup():
    return {"signup": "signup"}


# def login
@app.get("/login")
async def login():
    return {"login": "login"}


# def create_post
@app.post("/create_post")
async def create_post():
    return {"create_post": "create_post"}


# def edit_post
@app.put("/edit_post")
async def edit_post():
    return {"edit_post": "edit_post"}


# def delete_post
@app.delete("/delete_post")
async def delete_post():
    return {"delete_post": "delete_post"}


# def view_post
@app.get("/view_post")
async def view_post():
    return {"view_post": "view_post"}


# def like_post
@app.put("/like_post")
async def like_post():
    return {"like_post": "like_post"}


# def dislike_post
@app.put("/dislike_post")
async def dislike_post():
    return {"dislike_post": "dislike_post"}


# Description
# 	Create a simple RESTful API using FastAPI for a social networking application
# Functional requirements:
# There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
# As a user I need to be able to signup and login
# As a user I need to be able to create, edit, delete and view posts
# As a user I can like or dislike other users’ posts but not my own
# The API needs a UI Documentation (Swagger/ReDoc)
