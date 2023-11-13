import datetime
from fastapi import HTTPException
try:
    from backend.db.models import Post
except ImportError:
    import sys
    Post = sys.modules[__package__ + '.Post']


class PostServ:
    @staticmethod
    def getPostFromID(postID, db):
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
    def getPosts(db):
        try:
            posts = db.posts
            if posts is None:
                raise HTTPException(status_code=400, detail="No posts found")

            return posts.values()
        except Exception as e:
            print(e)

    @staticmethod
    def getTimeNow():
        date = datetime.datetime.now()
        return date
    
    @staticmethod
    def getTimeDifference(time):
        time_diff_seconds = (datetime.datetime.now() - time).total_seconds()
        # datetime.timedelta(0, 8, 562000)
        years = int(divmod(time_diff_seconds, 31536000)[0])
        days  = int(divmod(time_diff_seconds, 86400)[0])
        hours = int(divmod(time_diff_seconds, 3600)[0])
        minutes = int(divmod(time_diff_seconds, 60)[0])
        
        if years:
            return (str(years) + " year ago") if years == 1 else (str(years) + " years ago")
        elif days:
            return (str(days) + " day ago") if days == 1 else (str(days) + " days ago")
        elif hours:
            return (str(hours) + " hour ago") if hours == 1 else (str(hours) + " hours ago")
        elif minutes:
            return (str(minutes) + " minute ago") if minutes == 1 else (str(minutes) + " minutes ago")
        else:
            return "Just now"

    @staticmethod
    def hasUserLikedPost(post, minimal_user):
        return minimal_user in post.get_likes()