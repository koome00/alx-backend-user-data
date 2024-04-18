#!/usr/bin/env python3
"""
Auth Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check auths
        """
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None:
            return True
        pathh = path + "/"
        if path in excluded_paths or pathh in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization header
        """
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        auth_header = request.headers.get("Authorization")
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        res = self.authorization_header(request)
        if res is None:
            return None
