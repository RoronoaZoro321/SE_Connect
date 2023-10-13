import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # run ipconfig in cmd
    # find IPv4 Address
    # enter in the url bar of your browser: http://IPv4:8000
    # now can be access from any device in the same network
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


