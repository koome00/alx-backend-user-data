#!/usr/bin/env python3
"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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
