from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def get_id():
    """ Gets the maximum id in posts and generate a new one by adding 1 """
    return max((post.get("id") for post in POSTS if isinstance(post.get("id"), int)), default=0) + 1


# @app.route('/api/posts', methods=['GET'])
# def get_posts():
#     return jsonify(POSTS)

def validate_posts_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET','POST'])
def get_posts():
    if request.method == 'POST':
        # Get new post data from client
        new_post = request.get_json()

        # Input Validation
        if not new_post or not validate_posts_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        # Add new id 
        new_id = get_id()
        new_post["id"] = new_id
        
        # Add a new post
        POSTS.append(new_post)

        # Return a post
        return jsonify(new_post), 201

        # Return a post
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
