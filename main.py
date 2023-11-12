import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
    # run ipconfig in cmd
    # find IPv4 Address
    # enter in the url bar of your browser: http://IPv4:8000
    # now can be access from any device in the same network
