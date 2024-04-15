#!/usr/bin/env python3
"""
Model for basic auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Defines a auth class. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for handling protected paths  """
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
