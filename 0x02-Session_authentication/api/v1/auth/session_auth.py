#!/usr/bin/env python3
"""
Module: Session Auth
session authentiation
"""
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid


class SessionAuth(Auth):
    """
    inherits from auth to
    create sessions
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates session id for user id
        """
        if not isinstance(user_id, str):
            return None
        elif user_id is None:
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user id based on session_id
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        overloads current_user to return user based on cookie
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        destroy session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
