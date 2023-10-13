# dependency neccessary
pip install fastapi uvicorn[standard] zodb jinja2

# to run the project
run app/main.py

# Project Structure
Web_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py  # FastAPI application
│   ├── models.py  # Define data models
│   ├── routes.py  # Define API routes
│
├── static/
│   ├── css/
│   │   ├── main.css
│   │
│   ├── js/
│       ├── main.js
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── friends.html
│
├── zodb-data/
│   ├── myfacebook.fs  # ZODB database file
│
├── requirements.txt
├── README.md
├── main.py  # Uvicorn entry point