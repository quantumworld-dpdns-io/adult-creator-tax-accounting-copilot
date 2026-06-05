"""Authentication middleware (OAuth2 / OIDC)."""

from __future__ import annotations

import os
from typing import Any

import jwt

__all__ = ["verify_token", "AuthError"]


class AuthError(Exception):
    """Raised when a token is invalid or missing."""


def verify_token(token: str) -> dict[str, Any]:
    """Verify an OAuth2/OIDC JWT and return its claims.

    Falls back to a development mode (HS256, shared secret) when no JWKS is
    configured. Production deployments MUST set OIDC_JWKS_URL.
    """
    jwks_url = os.environ.get("OIDC_JWKS_URL")
    audience = os.environ.get("OIDC_AUDIENCE", "copilot-api")
    issuer = os.environ.get("OIDC_ISSUER")
    dev_secret = os.environ.get("DEV_JWT_SECRET", "dev-only-not-for-prod")

    if jwks_url and issuer:
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256", "EdDSA"],
            audience=audience,
            issuer=issuer,
        )
    return jwt.decode(token, dev_secret, algorithms=["HS256"], audience=audience)
