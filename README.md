# dependency neccessary
pip install -r requirements.txt

# to run the project
python main.py

# Project Structure
```
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
|   |
|   |── static/
|   |   ├── css/
|   |   │   ├── base.css
|   |   │   ├── freinds.css
|   |   │   ├── home.css
|   |   │   ├── main.css
|   |   │   ├── login.css
|   |   │   ├── se_community.css
|   |   │   ├── signup.css
|   |   │   ├── startup.css
|   |   │   ├── signupAdd.css
|   |   │   ├── signupSingle.css
|   |   │   ├── user_profile.css
|   |   │   ├── viewMyStartUpPostedLists.css
|   |   │
|   |   ├── js/
|   |   |   ├── freinds.js
|   |   |   ├── home.js
|   |   |   ├── login.js
|   |   |   ├── se_community.js
|   |   |   ├── signup.js
|   |   |   ├── startUpAdd.js
|   |   |   ├── userProfile.js
|   |   │
|   |   ├── images/
|   |   
|   |
|   |── templates/
|   |   │   ├── base.html
|   |   │   ├── freinds.html
|   |   │   ├── home.html
|   |   │   ├── login.html
|   |   │   ├── se_community.html
|   |   │   ├── signup.html
|   |   │   ├── startup.html
|   |   │   ├── signupAdd.html
|   |   │   ├── signupSingle.html
|   |   │   ├── user_profile.html
|   |   │   ├── userProfileFromOther.html
|   |   │   ├── viewMyStartUpPostedLists.html
|
├── requirements.txt
├── README.md
├── main.py  # Uvicorn entry point
```
