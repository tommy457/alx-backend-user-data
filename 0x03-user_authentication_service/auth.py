#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import uuid


def _hash_password(password: str) -> bytes:
    """ returns a salted, hashed password. """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return a string representation of a new UUID """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ save the user to the database and return the user object. """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            new_user = self._db.add_user(
                email=email,
                hashed_password=_hash_password(password)
            )
            return new_user

        raise ValueError("User {} already exists".format(user.email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if email and password matchs with auser in DB. """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ create and returns the session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ returns the corresponding User to the session_id or None. """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ updates the corresponding user’s session ID to None """
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generate a UUID and update the user’s reset_token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ hashes the password and update the user’s hashed_password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user_id=user.id,
                hashed_password=_hash_password(password),
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
