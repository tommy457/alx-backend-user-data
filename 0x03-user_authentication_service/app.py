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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def logout() -> None:
    """ destroy the session and redirect to the root path. """
    session_id = request.form.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect("/")
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
