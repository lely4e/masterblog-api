from data.data import POSTS


def get_id():
    """Gets the maximum id in posts and generate a new one by adding 1"""
    return (
        max(
            (post.get("id") for post in POSTS if isinstance(post.get("id"), int)),
            default=0,
        )
        + 1
    )


def get_comments_id(post):
    """Gets the maximum id in posts and generate a new one by adding 1"""
    return (
        max(
            (
                comment.get("id")
                for comment in post.get("comments", [])
                if isinstance(comment.get("id"), int)
            ),
            default=0,
        )
        + 1
    )


def pagination(data, page, limit):
    """Pagination"""
    start_index = (page - 1) * limit
    end_index = start_index + limit
    posts = data[start_index:end_index]
    return posts


def sort_by_choice(data, sort_by, direction):
    """Sort by choosen parameter"""
    reverse = direction.lower() == "desc"
    posts = sorted(data, key=lambda post: post.get(sort_by, ""), reverse=reverse)
    return posts
