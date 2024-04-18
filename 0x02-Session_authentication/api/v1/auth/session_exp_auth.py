#!/usr/bin/env python3
"""
Model for Sessions expiration.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from uuid import uuid4
from typing import TypeVar
import os


class SessionExpAuth(SessionAuth):
    """ Defines a Sessions expiration class. """
    def __init__(self) -> None:
        """ Constructor """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ creates a Session ID for a `user_id` """
        session_id = super().create_session()
        if not session_id:
            return None
        session_dictionary = {}
        session_dictionary["user_id"] = user_id
        session_dictionary["created_at"] = datetime.now()


        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ returns a User ID based on a Session ID. """
        info = self.user_id_by_session_id.get(session_id)
        user_id = self.info.get("user_id")
        created_at = self.info.get("created_at")

        if session_id is None \
                or info is None \
                or user_id is None \
                or created_at is None:
            return None

        if self.session_duration <= 0:
            return user_id

        duration = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > duration:
            return None
        return user_id
