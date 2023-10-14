from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import User


import ZODB, ZODB.FileStorage
# import persistent
# import transaction
import BTrees.OOBTree

# Database setup
storage = ZODB.FileStorage.FileStorage("mydata.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# obj in db
root.users = BTrees.OOBTree.BTree()
root.users["user1"] = User(1, "username", "fname", "lname", "pwd")

# if "users" not in root:
#     root["users"] = OOBTree()
# transaction.commit()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# FastAPI route for the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = 'root["user1"].username'
    return templates.TemplateResponse("home.html", {"request": request, "users": username})

@app.get("/all_users", response_class=HTMLResponse)
async def all_users():
    users = list(root["users"].values())
    return users



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# # Define routes for signup and login
# @app.get("/signup", response_class=HTMLResponse)
# async def signup(request: Request):
#     return templates.TemplateResponse("signup.html", {"request": request})

# @app.post("/signup")
# async def signup(username: str, password: str):
#     if username not in root["users"]:
#         user = User(username, password)
#         root["users"][username] = user
#         transaction.commit()
#     return RedirectResponse("/", status_code=303)

# @app.get("/login", response_class=HTMLResponse)
# async def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

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



