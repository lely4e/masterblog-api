from flask import Flask, jsonify, request
from flask_cors import CORS
from data.data import POSTS
from logic.logic import filtered_posts, find_post_by_id
from utils.utils import get_id, pagination, sort_by_choice
from validators.post_validator import validate_posts_data
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

limiter = Limiter(app=app, key_func=get_remote_address)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@app.route("/api/posts", methods=["GET", "POST"])
@limiter.limit("10/minute")  # Limit to 10 requests per minute
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
    # Log a message
    app.logger.info("GET request received for /api/posts")

    # Create a sort, direction query parametrs and pagination
    sort_by = request.args.get("sort", default="title")
    direction = request.args.get("direction", default="asc")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    posts = POSTS

    if sort_by:
        if sort_by not in ["title", "content", "id"]:
            return jsonify({"error": f"Sorting by {sort_by} is impossible"}), 400
        posts = sort_by_choice(posts, sort_by, direction)

    if page is not None and limit is not None:
        posts = pagination(posts, page, limit)

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
        return jsonify(filtered_posts("title", title))

    if content:
        return jsonify(filtered_posts("content", content))

    return jsonify({"error": "There are no parameters"}), 400


@app.errorhandler(429)
def ratelimit_error(e):
    return (
        jsonify(
            {
                "error": "To many requests, try again later",
            }
        ),
        429,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
