#!/usr/bin/env python3
"""
Module that runs a flask app
"""
from auth import Auth

from flask import Flask, jsonify, request


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")