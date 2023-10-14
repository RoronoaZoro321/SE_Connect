from fastapi import FastAPI, HTTPException
import ZODB
import transaction
import BTrees.OOBTree

app = FastAPI()

# Open a connection to the ZODB database
db = ZODB.DB("mydb.fs")


@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/get_user/{user_id}")
def get_user(user_id: int):
    # Open a ZODB connection
    connection = db.open()
    root = connection.root()

    try:
        # Retrieve data by ID from the ZODB database
        if user_id in root:
            user = root[user_id]
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        connection.close()

@app.post("/create_user")
def create_user(user: dict):
    # Create a ZODB connection and transaction
    connection = db.open()
    root = connection.root()

    try:
        # Get the next available data ID
        user_id = 1
        user['id'] = user_id

        # Store data in the ZODB database with the assigned ID
        root[user_id] = user
        transaction.commit()

        return {"message": "User created successfully", "id": user_id}
    finally:
        connection.close()


# @app.post("/create_data")
# def create_data(data: dict):
#     # Create a ZODB connection and transaction
#     connection = db.open()
#     root = connection.root()

#     try:
#         # Get the next available data ID
#         data_id = get_next_data_id()
#         data['id'] = data_id

#         # Store data in the ZODB database with the assigned ID
#         root[data_id] = data
#         transaction.commit()

#         return {"message": "Data created successfully", "id": data_id}
#     finally:
#         connection.close()

# @app.get("/get_data/{data_id}")
# def get_data(data_id: int):
#     # Open a ZODB connection
#     connection = db.open()
#     root = connection.root()

#     try:
#         # Retrieve data by ID from the ZODB database
#         if data_id in root:
#             data = root[data_id]
#             return data
#         else:
#             raise HTTPException(status_code=404, detail="Data not found")
#     finally:
#         connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("try_zodb:app", host="0.0.0.0", port=8000, reload=True)


# def get_next_data_id():
#     # Open a connection to the ZODB database
#     connection = db.open()
#     root = connection.root()

#     try:
#         if 'data_id_counter' not in root:
#             # Initialize the data ID counter if it doesn't exist
#             root['data_id_counter'] = 1
#         else:
#             # Increment the data ID counter
#             root['data_id_counter'] += 1
#         transaction.commit()

#         # Return the next available data ID
#         return root['data_id_counter']
#     finally:
#         connection.close()