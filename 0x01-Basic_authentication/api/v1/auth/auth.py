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
        return False

    def authorization_header(self, request=None) -> str:
        """
        authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
