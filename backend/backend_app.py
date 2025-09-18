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


# @app.route('/api/posts', methods=['GET'])
# def get_posts():
#     return jsonify(POSTS)


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

    GET: Returns all posts
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
        new_id = get_id()
        new_post["id"] = new_id

        # Add a new post
        POSTS.append(new_post)

        # Return a post
        return jsonify(new_post), 201

    # GET: Return all posts
    return jsonify(POSTS)


@app.route("/api/posts/<int:id>", methods=["DELETE", "GET"])
def delete_post(id):
    """Deletes post from database"""
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


# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify({"error:" "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
