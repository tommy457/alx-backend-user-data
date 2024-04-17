#!/usr/bin/env python3
"""
Model for session auth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
import os


class SessionAuth(Auth):
    """ Defines a Session Auth class. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a `user_id` """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID. """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """ returns a cookie value from a request. """
        if request is None:
            return None
        SESSION_NAME = os.getenv("SESSION_NAME")

        return request.cookies.get(SESSION_NAME)