import ZODB
import ZODB.FileStorage
import transaction
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.core.config import settings
from backend.apis.base import api_router
from backend.db.models import User, Post

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)

templates = Jinja2Templates(directory="backend/templates")

# Create a ZODB storage and database connection
storage = ZODB.FileStorage.FileStorage("backend/db/mydb.fs")
db = ZODB.DB(storage)



# # Create a sample user and add it to the database
# user = User(2, "username", "firstname", "surname", "password")
# root.users[2] = user


@app.post("/register")
def register(id: int, username: str, firstName: str, lastname: str, password: str):
    connection = db.open()
    root = connection.root()

    try:
        # Check for duplicate emails

        # Create a UserData object and store it in the ZODB
        user_data = User(id, username, firstName, lastname, password)
        root[id] = user_data

        # Commit the transaction
        transaction.commit()

        return {"message": "Registration successful"}
    finally:
        connection.close()

# get single user
@app.get("/getUser/{user_id}")
def getUserSingle(request: Request, user_id: int):
    connection = db.open()
    root = connection.root()
    try:
        user = root[user_id]
        return user
    except:
        return {"message": "User not found"}
    finally:
        connection.close()

# get all users
@app.get("/getUsers")
def getUsers(request: Request):
    connection = db.open()
    root = connection.root()
    try:
        users = root
        return users
    except:
        return {"message": "no user"}
    finally:
        connection.close()

# # close the database connection when the application stops
# @app.on_event("shutdown")
# async def shutdown():
#     transaction.commit()  # Commit any open transactions
#     connection.close()