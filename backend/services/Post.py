from fastapi import HTTPException
from backend.db.models import Post


class PostServ:
    @staticmethod
    def getPostFromID(postID, db) -> Post | None:
        pass

    @staticmethod
    def getPosts(db) -> list[Post]:
        try:
            posts = db.posts
            if posts is None:
                raise HTTPException(status_code=400, detail="No posts found")
            
            return posts.values()
        except Exception as e:
            raise e
