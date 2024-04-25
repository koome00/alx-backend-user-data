
"""
Module 3: Flask App
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def message():
    """
    simple endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_users():
    """
    endpoint to register user
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
