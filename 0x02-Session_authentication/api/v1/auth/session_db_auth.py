#!/usr/bin/env python3
"""
Model for Sessions expiration.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Defines a SessionDBAuth class """
    def create_session(self, user_id=None) -> str:
        """creates a Session ID for a `user_id` """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        payload = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**payload)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ returns a User ID based on a Session ID. """
        if session_id is None:
            return None

        info = UserSession.search({"session_id": session_id})
        user_id = info.get("user_id")
        created_at = info.get("created_at")

        if user_id is None or created_at is None:
            return None

        if self.session_duration <= 0:
            return user_id

        duration = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > duration:
            return None
        return user_id

    def destroy_session(self, request=None) -> bool:
        """ deletes the user session / logout. """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user = UserSession.search({"session_id": session_id})
        if user:
            user[0].remove()
            return True
        return False
