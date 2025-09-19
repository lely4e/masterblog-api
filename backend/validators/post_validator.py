def validate_posts_data(data):
    """Input Validation from the user"""
    if "title" not in data or "content" not in data or "category" not in data:
        return False
    if (
        not data.get("title").strip()
        or not data.get("content").strip()
        or not data.get("category").strip()
    ):
        return False
    return True
