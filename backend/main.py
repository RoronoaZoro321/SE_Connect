import ZODB
import ZODB.FileStorage
import transaction
import BTrees.OOBTree
import logging
from fastapi import FastAPI, Request, HTTPException, Depends, Form, Response, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated

from backend.core.config import settings
from backend.apis.base import api_router
from backend.db.models import User, Post
from backend.services.User import UserServ
from backend.services.Post import PostServ
from backend.models.base import CommentData, LoginData, SignupData, UserProfileData, AddFriendData, PostInteractData

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)
app.mount("/static", app=StaticFiles(directory="backend/static"), name="static")

templates = Jinja2Templates(directory="backend/templates")

# Create a ZODB storage and database connection
storage = ZODB.FileStorage.FileStorage("backend/db/db.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Use BTrees.OOBTree to store users and posts
print("Has users", hasattr(root, "users"))
print("Has posts", hasattr(root, "posts"))
if not hasattr(root, "users"):
    root.users = BTrees.OOBTree.BTree()
if not hasattr(root, "posts"):
    root.posts = BTrees.OOBTree.BTree()

# Create or update post id count
print("Current post ID", root.post_id_count if hasattr(
    root, "post_id_count") else None)
if not hasattr(root, "post_id_count"):
    root.post_id_count = 0


# Home route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        username = user.get_username()
        return templates.TemplateResponse("home.html", {"request": request, "username": username})
    else:
        return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/se_community", response_class=HTMLResponse)
async def read_root(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        posts = PostServ.getPosts(root)
        return templates.TemplateResponse("se_community.html", {"request": request, "posts": posts})
    else:
        return RedirectResponse(url="/login")


@app.get("/userProfile", response_class=HTMLResponse)
def userProfile(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        data = {
            "id": user.get_student_id(),
            "username": user.get_username(),
            "firstName": user.get_firstname(),
            "lastName": user.get_lastname(),
            "email": user.get_email(),
            # "age": user.get_age(),
            # "description": user.get_description()
        }
        # return data
        return templates.TemplateResponse("userProfile.html", {"request": request, "data": data})
    else:
        return RedirectResponse(url="/login")


@app.post("/newPost")
def createPost(response: Response, content: str, sessionId: Annotated[str | None, Cookie()] = None):
    try:

        user = UserServ.getUserFromSession(sessionId, root)
        if user:
            user_id = user.get_student_id()
            username = user.get_username()
            post_id = root.post_id_count
            root.post_id_count += 1

            # Check for duplicate id
            if post_id in root.posts:
                raise HTTPException(
                    status_code=400, detail="This ID already exists")

            new_post = Post(post_id, user_id, username, content)
            user.add_post(new_post)
            root.posts[post_id] = new_post
            transaction.commit()

            response.status_code = 200
            return {"message": "Post created successfully"}
        else:
            response.status_code = 404
            return {"message": "User not found"}
    except Exception as e:
        raise e


@app.post("/api/like")
def like(postInteractData: PostInteractData):
    post_id = postInteractData.post_id
    post = PostServ.getPostFromID(post_id, root)

    if post:
        minimal_user = {"studentId": postInteractData.student_id,
                        "username": postInteractData.username}
        post.add_like(minimal_user)
        return {"Success": "Liked post successfully"}
    else:
        return {"Error": "Post not found"}


@app.post("/api/comment")
def comment(postInteractData: PostInteractData, comment: CommentData):
    post_id = postInteractData.post_id
    post = PostServ.getPostFromID(post_id, root)

    if post:
        minimal_user = {"studentId": postInteractData.student_id,
                        "username": postInteractData.username}
        post.add_comment(minimal_user, comment)
        return {"Success": "Commented on post successfully"}
    else:
        return {"Error": "Post not found"}

# Debug


@app.get("/clearPosts")
def clearPosts():
    root.posts = BTrees.OOBTree.BTree()
    root.post_id_count = 0
    return {"Success": "Cleared posts successfully"}


@app.get("/clearUsers")
def clearUsers():
    root.users = BTrees.OOBTree.BTree()
    return {"Success": "Cleared users successfully"}


@app.post("/userProfile")
def updateProfile(response: Response, data: UserProfileData, sessionId: Annotated[str | None, Cookie()] = None):
    print(data)
    # return data
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        user.set_age(data.age)
        user.set_description(data.description)
        transaction.commit()
        response.status_code = 200
        return {"message": "User profile updated successfully"}
    else:
        response.status_code = 404
        return {"message": "User not found"}


@app.post("/login")
def login(response: Response, data: LoginData):
    sessionId = UserServ.loginUser(data.student_id, data.password, root)
    if sessionId:
        response.set_cookie(key="sessionId", value=sessionId)
        response.status_code = 200
        return {"message": "Login successful"}

    response.status_code = 401
    return {"message": "Invalid credentials"}


@app.post("/signup")
def signup(response: Response, data: SignupData):
    try:
        # Check for duplicate id
        print(data.student_id)
        if data.student_id in root.users:
            raise HTTPException(
                status_code=400, detail="This ID already exists")
        # Create a UserData object and store it in the BTrees.OOBTree
        user = User(data.student_id, data.username,
                    data.firstName, data.lastName, data.password)
        root.users[data.student_id] = user
        # Commit the transaction
        transaction.commit()

        sessionId = UserServ.loginUser(data.student_id, data.password, root)
        response.set_cookie(key="sessionId", value=sessionId)
        response.status_code = 200
        return {"message": "User created successfully"}
    except Exception as e:
        raise e


@app.get("/getAllPosts")
def getAllPosts():
    try:
        posts = root.posts
        if posts is None:
            raise HTTPException(status_code=400, detail="No posts found")
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get single user
@app.get("/getUser")
def getUserSingle(user_id: int):
    try:
        users = root.users
        print(users)
        user = users.get(user_id)
        print(user)
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        elif user is None:
            raise HTTPException(
                status_code=400, detail="No user found for this id")
        else:
            return user
    except Exception as e:
        raise e


# get all users
@app.get("/getAllUsers")
def getAllUsers():
    try:
        users = root.users
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete single user
@app.delete("/deleteUser")
def deleteUser(user_id: int):
    try:
        users = root.users
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        user = users.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=400, detail="No user found for this id")
        del users[user_id]
        transaction.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise e


# Update user
@app.put("/updateUser")
def updateUser(user_id: int, username: str, firstName: str, lastName: str, password: str):
    try:
        users = root.users
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        user = users.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=400, detail="No user found for this id")
        user.username = username
        user.firstname = firstName
        user.lastname = lastName
        user.password = password
        transaction.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise e


@app.get("/friends", response_class=HTMLResponse)
def friends(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        friends_id = user.get_friends()
        friends = []
        for i in friends_id:
            friends.append(root.users[i].get_username())
        return templates.TemplateResponse("friends.html", {"request": request, "friends": friends})


@app.post("/add_friend")
def addFriend(response: Response, data: AddFriendData, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        if data.friend_id not in root.users:
            response.status_code = 400
            return {"message": "No user found for this id"}
        else:
            if (user.add_friend(data.friend_id)):
                transaction.commit()
                response.status_code = 200
                return {"message": "Friend added successfully"}
            return {"message": "Friend already added"}
    else:
        response.status_code = 401
        return {"message": "Invalid credentials"}


@app.get("/logout")
def logout(sessionId: Annotated[str | None, Cookie()] = None):
    if sessionId:
        new_response = RedirectResponse(url="/login")
        new_response.delete_cookie(key="sessionId")
        return new_response
    else:
        return RedirectResponse(url="/login")


# Close the database connection when the application stops


@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()
