#!/usr/bin/env python3
"""
Module that runs a flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """ root route. """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register() -> str:
    """ register a new user. """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(
            email=email,
            password=password
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ create a new session for the user. """
    email = request.form.get("email")
    password = request.form.get("password")

    user = AUTH.valid_login(
        email=email,
        password=password
    )
    if user:
        session_id = AUTH.create_session(email=email)
        responce = jsonify({"email": email, "message": "logged in"})
        responce.set_cookie(key="session_id", value=session_id)
        return responce

    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """ destroy the session and redirect to the root path. """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ return a user's profile. """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ return a reset token. """
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        pass
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ updates the user password. """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
