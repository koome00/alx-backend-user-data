#!/usr/bin/env python3
"""
Module 4: Auth
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    takes password and returns
    it hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"),
                           bcrypt.gensalt())
    return hashed
