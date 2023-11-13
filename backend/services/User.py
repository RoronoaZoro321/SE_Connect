from fastapi import HTTPException
from backend.db.models import User
import jwt


class UserServ:
    JWT_SECRET = "secret"

    @staticmethod
    def getUserFromSession(sessionId, db) -> User | None:
        # Check for session
        if sessionId:
            print("has session id: ", sessionId)
            decoded_jwt = jwt.decode(
                sessionId, UserServ.JWT_SECRET, algorithms=["HS256"])
            print("sessionId has data: ", decoded_jwt)
            studentId = decoded_jwt["studentId"]

            # Get user data
            try:
                users = db.users
                if users is None:
                    raise HTTPException(
                        status_code=400, detail="No users found")
                for user in users.values():
                    if user.student_id == studentId:
                        return user
            except Exception as e:
                raise e

        return None

    @staticmethod
    def getUserFromStudentId(studentId, db) -> User | None:
        try:
            users = db.users
            if users is None:
                raise HTTPException(status_code=400, detail="No users found")
            for user in users.values():
                if user.student_id == studentId:
                    return user
        except Exception as e:
            raise e

        return None

    @staticmethod
    def loginUser(studentId, password, db) -> str | None:
        try:
            users = db.users
            if users is None:
                raise HTTPException(status_code=400, detail="No users found")
            for user in users.values():
                if user.student_id == studentId and user.password == password:
                    user_session = {"studentId": studentId}

                    # Encode
                    encoded_jwt = jwt.encode(
                        user_session, UserServ.JWT_SECRET, algorithm="HS256")

                    return encoded_jwt
            raise HTTPException(status_code=400, detail="Invalid credentials")
        except Exception as e:
            raise e

    def authenticateSession(self):
        pass
