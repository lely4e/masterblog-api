from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_id():
    """Gets the maximum id in posts and generate a new one by adding 1"""
    return (
        max(
            (post.get("id") for post in POSTS if isinstance(post.get("id"), int)),
            default=0,
        )
        + 1
    )


def validate_posts_data(data):
    """Input Validation from the user"""
    if "title" not in data or "content" not in data:
        return False
    if not data["title"].strip() or not data["content"].strip():
        return False
    return True


@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    """
    Add a new post to database.

    GET: Returns all posts, with optional sorting and pagination.
    POST: Adds a new post if input is valid.
    """
    if request.method == "POST":
        # Get new post data from client
        new_post = request.get_json()

        # Input Validation
        if not new_post:
            return jsonify({"error": "Empty post data"}), 400
        if not validate_posts_data(new_post):
            return jsonify({"error": "Empty title or content"}), 400

        # Add new id
        new_post["id"] = get_id()

        # Add a new post
        POSTS.append(new_post)

        # Return a post
        return jsonify(new_post), 201

    # GET Reguest
    # Create a sort, direction query parametrs and pagination
    sort_by = request.args.get("sort", default="title")
    direction = request.args.get("direction", default="asc")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    posts = POSTS

    if sort_by:
        if sort_by not in ["title", "content", "id"]:
            return jsonify({"error": f"Sorting by {sort_by} is impossible"}), 400
        reverse = direction.lower() == "desc"
        posts = sorted(posts, key=lambda post: post.get(sort_by, ""), reverse=reverse)

    if page is not None and limit is not None:
        start_index = (page - 1) * limit
        end_index = start_index + limit
        posts = posts[start_index:end_index]

    # GET: Return all posts
    return jsonify(posts)


@app.route("/api/posts/<int:id>", methods=["DELETE", "GET"])
def delete_post(id):
    """Delete post from database"""
    if request.method == "DELETE":
        for post in POSTS:
            if post["id"] == id:
                POSTS.remove(post)
                return (
                    jsonify(
                        {
                            f"message": f"Post with id {id} has been deleted successfully."
                        }
                    ),
                    200,
                )
        return jsonify({"error": f"Post with id {id} doesn't exist"}), 404
    return jsonify(POSTS)


def find_post_by_id(id):
    """Find the post with given id or return None"""
    for post in POSTS:
        if post["id"] == id:
            return post
    return None


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update(id):
    # Find the post in posts
    post = find_post_by_id(id)

    # if post doesn't found return a 404 error
    if not post:
        return jsonify({"error": f"Post with id {id} doesn't found"}), 404

    # Update the post with new data
    new_data = request.get_json()
    post.update(new_data)

    # Return a post
    return jsonify(post)


@app.route("/api/posts/search", methods=["GET"])
def search():
    """Search for specific title or content in database"""
    # Get the title and content data
    title = request.args.get("title", "").strip()
    content = request.args.get("content", "").strip()

    if title:
        filtered_posts = [
            post for post in POSTS if title.lower() in post.get("title", "").lower()
        ]
        return jsonify(filtered_posts)

    if content:
        filtered_posts = [post for post in POSTS if content in post.get("content", "")]
        return jsonify(filtered_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
