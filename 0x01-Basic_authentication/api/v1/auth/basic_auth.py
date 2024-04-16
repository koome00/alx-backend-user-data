#!/usr/bin/env python3
"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extracts base64 value in auth header
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if authorization_header.split()[0] != "Basic":
            return None
        b_64 = authorization_header.split("Basic ", 1)[1]
        return b_64

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        decoding base64 value in auth header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            b64_decoded = b64decode(base64_authorization_header)
            auth_str = b64_decoded.decode('utf-8')
            return auth_str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts user's credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        if decoded_base64_authorization_header.split(":"):
            email = decoded_base64_authorization_header.split(":")[0]
            password = decoded_base64_authorization_header.split(":")[1]
            return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        returns user instance based on email and
        password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_info = {"email": user_email}
        user = User.search(user_info)
        if len(user) == 0:
            return None
        else:
            if user[0].is_valid_password(user_pwd):
                return user[0]
            else:
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets current user after overloading Auth
        """
        auth_header = Auth.authorization_header(request)
        auth_b64 = self.extract_base64_authorization_header(auth_header)
        auth_str = self.decode_base64_authorization_header(auth_b64)
        email, passw = self.extract_user_credentials(auth_str)
        return self.user_object_from_credentials(email, passw)
