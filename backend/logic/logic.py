from data.data import POSTS


def filtered_posts(field, text):
    """Filter post by choosen parameter"""
    return [post for post in POSTS if text.lower() in post.get(field, "").lower()]


def find_post_by_id(id):
    """Find the post with given id or return None"""
    for post in POSTS:
        if post["id"] == id:
            return post
    return None
