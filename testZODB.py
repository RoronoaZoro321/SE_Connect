import ZODB, ZODB.FileStorage
import persistent
import transaction

import BTrees.OOBTree
from app.models import User


# Database setup
storage = ZODB.FileStorage.FileStorage("mydata.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# obj in db
root.users = BTrees.OOBTree.BTree()
root.users["user1"] = User(1, "username", "fname", "lname", "pwd")

# get user
user = root.users["user1"]
print(user)
print(user.get_username())