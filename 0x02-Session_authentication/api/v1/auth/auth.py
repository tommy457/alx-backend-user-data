#!/usr/bin/env python3
"""
Model for basic auth
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Defines a auth class. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for handling protected paths  """
        for ex_path in excluded_paths:
            if ex_path.endswith('*') and path.startswith(ex_path[:-1]):
                return False

        if path is None \
           or excluded_paths is None \
           or (path not in excluded_paths
                and path + '/' not in excluded_paths):
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """ Method for returns authorization header. """
        if request is None or request.headers.get("Authorization") is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the current log in user. """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request. """
        if request is None:
            return None
        SESSION_NAME = os.getenv("SESSION_NAME")

        return request.cookies.get(SESSION_NAME)
