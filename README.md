# dependency neccessary
pip install -r requirements.txt

# to run the project
python main.py

# Project Structure
SE_CONNECT/
│
├── backend/
│   ├── core
│   │   ├── config.py
│   │ 
│   ├── db
│   │   ├── models.py
│   │ 
│   ├── models
│   │   ├── base.py
│   │ 
│   ├── services
│   │   ├── Post.py
│   │   ├── User.py
│
│
│
├── requirements.txt
├── README.md
├── main.py  # Uvicorn entry point






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