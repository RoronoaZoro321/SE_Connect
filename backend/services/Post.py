from fastapi import HTTPException
from backend.db.models import Post


class PostServ:
    @staticmethod
    def getPostFromID(postID, db) -> Post | None:
        try:
            posts = db.posts
            if posts is None:
                raise HTTPException(status_code=400, detail="No posts found")
            
            for post in posts.values():
                if post.id == postID:
                    return post
            
            return None
        except Exception as e:
            print(e)

    @staticmethod
    def getPosts(db) -> list[Post]:
        try:
            posts = db.posts
            if posts is None:
                raise HTTPException(status_code=400, detail="No posts found")

            return posts.values()
        except Exception as e:
            print(e)
