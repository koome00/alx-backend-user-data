#!/usr/bin/env python3
"""
Module 2: Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Optional, Union


def _hash_password(password: str) -> bytes:
    """
    takes password and returns
    it hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"),
                           bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """
    generate uuid
    """
    return str(uuid.uuid4())


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
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        creates session ID and returns a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        takes session_id and returns user
        or none
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy's user's session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        reset token
        """
        user = self._db.find_user_by(email=email)
        if user is not None:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        else:
            raise ValueError
