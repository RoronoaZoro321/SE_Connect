from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# @router.post("/")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     user = create_new_user(user=user, db=db)
#     return user
