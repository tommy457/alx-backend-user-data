#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returns a salted, hashed password. """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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

        raise ValueError("User {} already exists.".format(user.email))
