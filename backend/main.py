import ZODB
import ZODB.FileStorage
import transaction
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.core.config import settings
from backend.apis.base import api_router
from backend.db.models import User
import BTrees.OOBTree
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)

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
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Login route
# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     user = root.users.get(username)
#     if user is None or user.password != password:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     return {"message": "Login successful"}


@app.post("/signup")
def signup(id: int, username: str, firstName: str, lastName: str, password: str):
    try:
        # Check for duplicate id
        if id in root.users:
            raise HTTPException(
                status_code=400, detail="This Id already exists")
        # Create a UserData object and store it in the BTrees.OOBTree
        user = User(id, username, firstName, lastName, password)
        root.users[id] = user

        # Commit the transaction
        transaction.commit()

        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get single user
@app.get("/getUser")
def getUserSingle(user_id: int):
    try:
        users = root.users
        if users is None:
            raise HTTPException(status_code=400, detail="No users found")
        user = users.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=400, detail="No user found for this id")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

# Close the database connection when the application stops
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()
