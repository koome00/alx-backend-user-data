#!/usr/bin/env python3
"""
Module 2: Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    takes password and returns
    it hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"),
                           bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        function to register user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError("User <user's email> already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        credentials validation
        """
        try:
            if self._db.find_user_by(email=email):
                user = self._db.find_user_by(email=email)
                hashed = user.hashed_password
                return bcrypt.checkpw(password.encode(), hashed)
        except (InvalidRequestError, InvalidRequestError):
            return False
