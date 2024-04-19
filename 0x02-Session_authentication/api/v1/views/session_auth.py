#!/usr/bin/env python3
"""
Module Session Auth
View that handles session auth routes
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"],
                 strict_slashes=False)
def login():
    """
    retrieve user information
    """
    email = request.form.get("email")
    if email is None or email.strip() == "":
        return jsonify({"error": "email missing"}), 400
    passw = request.form.get("password")
    if passw is None or passw.strip() == "":
        return jsonify({"error": "password missing"}), 400
    if User.search({"email": email}):
        user = User.search({"email": email})[0]
        if user.is_valid_password(passw):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            s = str(type(user.id))
            cookie = os.getenv("SESSION_NAME")
            response = jsonify(user.to_json())
            response.set_cookie(cookie, session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401
    else:
        return jsonify({"error": "no user found for this email"}), 401


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes="False")
def logout():
    """
    delete cookie and log out
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        return False, abort(404)
