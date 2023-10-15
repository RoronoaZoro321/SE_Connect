import ZODB
import ZODB.FileStorage
import persistent
import transaction
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from backend.core.config import settings
from backend.apis.base import api_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)

templates = Jinja2Templates(directory="backend/templates")

storage = ZODB.FileStorage.FileStorage("backend/db/mydb.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# from BTrees.OOBTree import OOBTree
import BTrees.OOBTree
from backend.db.models import User, Post

root.users = BTrees.OOBTree.BTree()
user = User(1, "username", "firstname", "surname", "password")
root.users[1] = user

# Define route for home
@app.get("/")
def home(request: Request):
    user = root.users[1]
    return templates.TemplateResponse("home.html", {"request": request, "users": user.username})


# Define route for signup
@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# Define route for login
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/getUser/{user_id}")
def get_user(user_id: int):
    pass
    # Open a ZODB connection
    connection = db.open()
    root = connection.root()

    try:
        # Retrieve data by ID from the ZODB database
        if user_id in root:
            user = root[user_id]
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        connection.close()


@app.post("/createUser")
def create_user(user: dict):
    pass
    # Create a ZODB connection and transaction
    connection = db.open()
    root = connection.root()

    try:
        # Get the next available data ID
        user_id = 1
        user['id'] = user_id

        # Store data in the ZODB database with the assigned ID
        root[user_id] = user
        transaction.commit()

        return {"message": "User created successfully", "id": user_id}
    finally:
        connection.close()

# Models for your application
# class User(Persistent):
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.friends = set()
#         self.posts = []

# Database setup
# db = DB()
# connection = db.open()
# root = connection.root

# if "users" not in root:
#     root["users"] = OOBTree()
# transaction.commit()

# FastAPI route for the home page


# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     # users = root["users"].values()
#     users = "user1"
#     return templates.TemplateResponse("home.html", {"request": request, "users": users})

# @app.post("/signup")
# async def signup(username: str, password: str):
#     if username not in root["users"]:
#         user = User(username, password)
#         root["users"][username] = user
#         transaction.commit()
#     return RedirectResponse("/", status_code=303)

# @app.post("/login")
# async def login(username: str, password: str):
#     user = root["users"].get(username)
#     if user and user.password == password:
#         # You can implement user authentication logic here
#         return RedirectResponse("/friends", status_code=303)
#     return RedirectResponse("/login", status_code=303)

# # Example route for friends page
# @app.get("/friends", response_class=HTMLResponse)
# async def friends(request: Request):
#     return templates.TemplateResponse("friends.html", {"request": request})
