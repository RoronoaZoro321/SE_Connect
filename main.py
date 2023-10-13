import uvicorn
from app.main import app  # Assuming your FastAPI app is defined in app/main.py

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # run ipconfig in cmd
    # find IPv4 Address
    # enter in the url bar of your browser: http://IPv4:8000
    # now can be access from any device in the same network


