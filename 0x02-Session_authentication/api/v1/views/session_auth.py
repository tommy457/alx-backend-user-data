#!/usr/bin/env python3
""" Module of Session Auth views.
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - Retrieve the User instance based on the email.
    """
    from api.v1.app import auth

    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user: User = User.search({"email": email})
        user = user[0]
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return response


@app_views.route(
        "/auth_session/logout",
        methods=['DELETE'],
        strict_slashes=False
)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON dictionary with the status code 200.
      - abort If destroy_session returns False.
    """
    from api.v1.app import auth

    logged_out = auth.destroy_session(request)

    if not logged_out:
        abort(404)

    return jsonify({}), 200
