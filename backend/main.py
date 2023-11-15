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
from backend.db.models import User, Post, StartUpPost
from backend.services.User import UserServ
from backend.services.Post import PostServ
from backend.models.base import CommentData, LoginData, PostData, SignupData, UserProfileData, AddFriendData, PostInteractData, AddStartUpData

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
print("Has startUp posts", hasattr(root, "startUpPosts"))

if not hasattr(root, "users"):
    root.users = BTrees.OOBTree.BTree()
if not hasattr(root, "posts"):
    root.posts = BTrees.OOBTree.BTree()
if not hasattr(root, "startUpPosts"):
    root.startUpPosts = BTrees.OOBTree.BTree()


# Create or update post id count
print("Current post ID", root.post_id_count if hasattr(
    root, "post_id_count") else None)
if not hasattr(root, "post_id_count"):
    root.post_id_count = 0

# Create or update startUpPost id count
if not hasattr(root, "startUpPost_id_count"):
    root.startUpPost_id_count = 0
print("Current  startUpPost ID", root.startUpPost_id_count if hasattr(
    root, "post_id_count") else None)


# Home route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        username = user.get_username()
        return templates.TemplateResponse("home.html", {"request": request,"authenticated": True, "username": username})
    else:
        return templates.TemplateResponse("home.html", {"request": request,"authenticated": False})

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
        minimal_user = {"studentId": user.get_student_id(), "username": user.get_username()}
        return templates.TemplateResponse("se_community.html", {"request": request,"authenticated": True, "posts": posts, "minimal_user": minimal_user, "has_liked": PostServ.hasUserLikedPost})
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
            "age": user.get_age(),
            "description": user.get_description()
        }
        # return data
        return templates.TemplateResponse("userProfile.html", {"request": request,"authenticated": True, "data": data})
    else:
        return RedirectResponse(url="/login") 
    
@app.get("/userProfileFromOther/{id}", response_class=HTMLResponse)
def getUserProfileFromOther(request: Request, id: int, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        otherUser = UserServ.getUserFromStudentId(id, root)
        if otherUser:
            data = {
                "id": otherUser.get_student_id(),
                "username": otherUser.get_username(),
                "firstName": otherUser.get_firstname(),
                "lastName": otherUser.get_lastname(),
                "email": otherUser.get_email(),
                "age": otherUser.get_age(),
                "description": otherUser.get_description()
            }
            return templates.TemplateResponse("userProfileFromOther.html", {"request": request,"authenticated": True, "data": data})
        else:
            return RedirectResponse(url="/")
    else:
        return RedirectResponse(url="/login")


@app.post("/api/newPost", tags=["API"])
def createPost(response: Response, postData: PostData, sessionId: Annotated[str | None, Cookie()] = None):
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

            new_post = Post(post_id, user_id, username, postData.content)
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


@app.post("/api/like/{postId}", tags=["API"])
def like(response: Response, postId: int, sessionId: Annotated[str | None, Cookie()] = None):
    post = PostServ.getPostFromID(postId, root)

    if not sessionId:
        response.status_code = 401
        return {"message": "Unauthenticated"}

    if post:
        user = UserServ.getUserFromSession(sessionId, root)
        if not user:
            response.status_code = 404
            return {"message": "User not found"}
        
        minimal_user = {"studentId": user.student_id, "username": user.username}
        like = True
        for like_user in post.get_likes(): # Unlike instead if user already liked
            if like_user["studentId"] == user.get_student_id():
                like = False
                break

        if like:
            post.add_like(minimal_user)
            response.status_code = 200
            return {"message": "Liked post successfully", "data": "like"}
        else:
            success = post.remove_like(minimal_user)
            if success:
                response.status_code = 200
                return {"message": "Unliked post successfully", "data": "unlike"}
            else:
                response.status_code = 400
                return {"message": "Unable to unlike post"}

    else:
        response.status_code = 404
        return {"error": "Post not found"}


@app.post("/api/comment/{postId}", tags=["API"])
def comment(response: Response, postId: int, commentData: CommentData, sessionId: Annotated[str | None, Cookie()] = None):
    post = PostServ.getPostFromID(postId, root)

    if not sessionId:
        response.status_code = 401
        return {"error": "Unauthenticated"}

    if post:
        user = UserServ.getUserFromSession(sessionId, root)
        if not user:
            response.status_code = 404
            return {"error": "User not found"}
        
        minimal_user = {"studentId": user.student_id, "username": user.username}
        post.add_comment(minimal_user, commentData)

        response.status_code = 200
        return {"message": "Commented successfully"}
    else:
        response.status_code = 404
        return {"error": "Post not found"}



# Debug
@app.get("/api/clearPosts", tags=["API"])
def clearPosts():
    root.posts = BTrees.OOBTree.BTree()
    root.post_id_count = 0

    users = root.users
    for user in users.values():
        user.posts = []

    return {"Success": "Cleared posts successfully"}


@app.get("/api/clearUsers", tags=["API"])
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


@app.get("/api/getAllPosts", tags=["API"])
def getAllPosts():
    try:
        posts = root.posts
        if posts is None:
            raise HTTPException(status_code=400, detail="No posts found")
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get single user
@app.get("/api/getUser", tags=["API"])
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
@app.get("/api/getAllUsers", tags=["API"])
def getAllUsers():
    try:
        users = root.users
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete single user
@app.delete("/api/deleteUser", tags=["API"])
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
@app.put("/api/updateUser", tags=["API"])
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
        usernames = []
        for i in friends_id:
            usernames.append(root.users[i].get_username())
        data = {
            "usernames": usernames,
            "friends_id": friends_id
        }
        print(data)
        return templates.TemplateResponse("friends.html", {"request": request, "authenticated": True, "data": data})
    else:
        return RedirectResponse(url="/login")

    

@app.post("/add_friend")
def addFriend(response: Response, data: AddFriendData, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        if data.friend_id not in root.users: 
            response.status_code = 400 
            return {"message": "No user found for this id"} 
        elif data.friend_id == user.get_student_id(): 
            response.status_code = 400 
            return {"message": "Cannot add yourself as a friend"} 
        else:
            if (user.add_friend(data.friend_id)):
                transaction.commit()
                response.status_code = 200
                return {"message": "Friend added successfully"}
            else:
                response.status_code = 400
                return {"message": "Friend already added"}
    else:
        response.status_code = 401
        return {"message": "Invalid credentials"}

@app.get("/removeFriend/{id}")
def removeFriend(response: Response, id: int, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        if id not in root.users:
            response.status_code = 400
            return {"message": "No user found for this id"}
        else:
            if (user.remove_friend(id)):
                transaction.commit()
                response.status_code = 200
                # return {"message": "Friend removed successfully"}
                return RedirectResponse(url="/friends")
            else:
                response.status_code = 400
                return {"message": "Friend not found"}
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


@app.get("/startup", response_class=HTMLResponse)
def startup(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        posts = root.startUpPosts
        data = []
        for post in posts:
            data.append(posts.get(post))
        return templates.TemplateResponse("startup.html", {"request": request,"authenticated": True, "data": data})

@app.get("/startupAdd", response_class=HTMLResponse)
def startupAdd(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        return templates.TemplateResponse("startupAdd.html", {"request": request,"authenticated": True})
    else:
        return RedirectResponse(url="/login")

@app.post("/startupAdd")
def startupAdd(response: Response, data: AddStartUpData, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        post_id = root.startUpPost_id_count
        root.startUpPost_id_count += 1
        new_post = StartUpPost(post_id, user.get_student_id(), user.get_username(), data.title, data.description, data.skills)
        user.add_startUpPost(post_id)
        root.startUpPosts[post_id] = new_post
        transaction.commit()
        response.status_code = 200
        return {"message": "Post created successfully"}
    else:
        response.status_code = 404
        return {"message": "User not found"}

@app.get("/startup/{id}", response_class=HTMLResponse)
def startupPost(request: Request, id: int, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        post = root.startUpPosts.get(id)
        if post:
            return templates.TemplateResponse("startupSingle.html", {"request": request,"authenticated": True, "data": post})
        else:
            return RedirectResponse(url="/startup")
    else:
        return RedirectResponse(url="/login")

@app.get("/getAllStartupPosts")
def getAllStartupPosts():
    try:
        posts = root.startUpPosts
        if posts is None:
            raise HTTPException(status_code=400, detail="No posts found")
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/deleteStartupPost/{post_id}", response_class=HTMLResponse)
def deleteStartupPost(post_id: int, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        posts = root.startUpPosts
        if posts is None:
            raise HTTPException(status_code=400, detail="No posts found")
        post = posts.get(post_id)
        if post is None:
            raise HTTPException(
                status_code=400, detail="No post found for this id")
        del posts[post_id]
        user.remove_startUpPost(post_id)
        print(user.startUpPosts)
        transaction.commit()
        # return {"message": "Post deleted successfully"}
        return RedirectResponse(url="/viewMyStartUpPostedList")
    else:
        return {"Error": "User not found"}
    


@app.get("/startup/enrolls/{post_id}", response_class=HTMLResponse)
def enrolls(request: Request, post_id: int, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        post = root.startUpPosts.get(post_id)
        if post:
            if (user.student_id in post.get_enrolls()):
                return templates.TemplateResponse("startupSingle.html", {"request": request,"authenticated": True, "data": post, "error": "Already enrolled"})
            if (user.student_id == post.user_id):
                return templates.TemplateResponse("startupSingle.html", {"request": request,"authenticated": True, "data": post, "error": "Cannot enroll on your own post"})
            else:
                post.add_enroll(user.student_id)
                transaction.commit()
                return templates.TemplateResponse("startupSingle.html", {"request": request,"authenticated": True, "data": post, "success": "Enrolled on post successfully"})
        else:
            return {"Error": "Post not found"}
    return {"Error": "User not found"}

@app.get("/viewMyStartUpPostedList", response_class=HTMLResponse)
def viewMyStartUpPostedList(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        data = []
        print(user.get_startUpPosts())
        for post in user.get_startUpPosts():
            data.append(root.startUpPosts.get(post))
        return templates.TemplateResponse("viewMyStartUpPostedList.html", {"request": request,"authenticated": True, "data": data})
    else:
        return RedirectResponse(url="/login")

# Close the database connection when the application stops
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()
