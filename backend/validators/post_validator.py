def validate_posts_data(data):
    """Input Validation from the user"""
    if "title" not in data or "content" not in data:
        return False
    if not data["title"].strip() or not data["content"].strip():
        return False
    return True
