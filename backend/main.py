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
from backend.db.models import User
from backend.services.User import UserServ
from backend.models.LoginData import LoginData, SignupData

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

# Use BTrees.OOBTree to store users
print(hasattr(root, "users"))
if not hasattr(root, "users"):
    root.users = BTrees.OOBTree.BTree()


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

@app.get("/userProfile" , response_class=HTMLResponse)
def userProfile(request: Request, sessionId: Annotated[str | None, Cookie()] = None):
    user = UserServ.getUserFromSession(sessionId, root)
    if user:
        data = {
            "id": user.get_student_id(),
            "username": user.get_username(),
            "firstName": user.get_firstname(),
            "lastName": user.get_lastname(),
            "email": user.get_email(),
        }
        # return data
        return templates.TemplateResponse("userProfile.html", {"request": request, "data": data})
    else:
        return RedirectResponse(url="/login")

def get_sessionId(student_id, password):
    sessionId = UserServ.loginUser(student_id, password, root)
    return sessionId

@app.post("/login")
def login(response: Response, data: LoginData):
    sessionId = get_sessionId(data.student_id, data.password)
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
        user = User(data.student_id, data.username, data.firstName, data.lastName, data.password)
        root.users[data.student_id] = user
        # Commit the transaction
        transaction.commit()

        sessionId = get_sessionId(data.student_id, data.password)
        response.set_cookie(key="sessionId", value=sessionId)
        response.status_code = 200
        return {"message": "User created successfully"}
    except Exception as e:
        raise e


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



# Close the database connection when the application stops
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()
