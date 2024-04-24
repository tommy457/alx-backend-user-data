#!/usr/bin/env python3
"""
Module for End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Test for the register endpint. """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post('http://127.0.0.1:5000/users', payload)

    assert res.status_code == requests.codes.okay
    assert res.json().get("message") == "user created"


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test for the login endpoint """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post('http://127.0.0.1:5000/sessions', payload)

    assert res.status_code == requests.codes.unauthorized


def log_in(email: str, password: str) -> str:
    """ Test for the login endpoint """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post('http://127.0.0.1:5000/sessions', payload)

    assert res.status_code == requests.codes.okay
    assert res.json().get("message") == "logged in"
    assert res.cookies.get('session_id') is not None
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test for the profile endpoint. """

    res = requests.get('http://127.0.0.1:5000/profile')

    assert res.status_code == requests.codes.forbidden


def profile_logged(session_id: str) -> None:
    """ Test for the profile endpoint """
    cookie = {'session_id': session_id}
    res = requests.get('http://127.0.0.1:5000/profile', cookies=cookie)

    assert res.status_code == requests.codes.okay
    assert res.json().get("email") == EMAIL


def log_out(session_id: str) -> None:
    """ Test for the logout endpoint """
    cookie = {'session_id': session_id}

    res = requests.delete('http://127.0.0.1:5000/sessions', cookies=cookie)

    assert res.status_code == requests.codes.okay
    assert res.json().get("message") == "Bienvenue"
    assert res.cookies.get('session_id') is None


def reset_password_token(email: str) -> str:
    """ Test for reset_password endpoint. """
    payload = {'email': email}

    res = requests.post('http://127.0.0.1:5000/reset_password', payload)

    assert res.status_code == requests.codes.okay
    assert res.json().get("email") == EMAIL

    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for updating password """
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    res = requests.put('http://127.0.0.1:5000/reset_password', payload)

    assert res.status_code == requests.codes.okay
    assert res.json().get("message") == "Password updated"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
