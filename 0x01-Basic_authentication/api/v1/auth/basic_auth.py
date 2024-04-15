#!/usr/bin/env python3
"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Basic Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if authorization_header.split()[0] != "Basic":
            return None
        b_64 = authorization_header[len("Basic "):]
        return b_64
