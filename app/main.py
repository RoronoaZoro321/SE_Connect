from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# import ZODB, ZODB.FileStorage
# import persistent
# import transaction
# from BTrees.OOBTree import OOBTree

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # users = root["users"].values()
    users = "roshan"
    print(request.headers)
    return templates.TemplateResponse("home.html", {"request": request, "users": users})

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
