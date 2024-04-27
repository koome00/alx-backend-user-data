#!/usr/bin/env python3
"""
Module 3: Flask App
"""
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    login endpoint to implement sessions
    """
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email,
                      "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def log_out():
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        print(user)
        AUTH.destroy_session(user.id)
        return redirect(url_for("message"))
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
