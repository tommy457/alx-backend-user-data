#!/usr/bin/env python3
"""
Model for basic auth
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Defines a basic auth class. """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """ Returns the Base64 part of the Authorization header. """
        if authorization_header is None \
            or not isinstance(authorization_header, str) \
                or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """ returns the decoded value of a Base64 string. """
        if base64_authorization_header is None \
                or not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
                ).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """returns user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None\
            or not isinstance(decoded_base64_authorization_header, str)\
                or not (":" in decoded_base64_authorization_header):
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """ returns the `User` instance based on his email and password """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user: User = User.search({"email": user_email})
        try:
            user = user[0]
        except IndexError:
            return None

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request. """
        auth_header = self.authorization_header(request=request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        email, password = self.extract_user_credentials(
            decoded_base64_auth_header
        )
        user: User = self.user_object_from_credentials(email, password)

        if user:
            return user.to_json()
        return None