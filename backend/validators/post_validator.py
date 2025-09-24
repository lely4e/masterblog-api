def validate_posts_data(data):
    """Input Validation from the user"""
    errors = []
    if not "title" in data or not data.get("title").strip():
        errors.append("title is empty")

    if not "content" in data or not data.get("content").strip():
        errors.append("content is empty")

    if not "category" in data or not data.get("category").strip():
        errors.append("category is empty")

    return errors
