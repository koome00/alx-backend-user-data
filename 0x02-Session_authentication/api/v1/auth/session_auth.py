#!/usr/bin/env python3
"""
Module: Session Auth
session authentiation
"""
from api.v1.auth.auth import Auth
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
