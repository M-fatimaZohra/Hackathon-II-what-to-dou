from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Dict, Optional
import os
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(override=True)

# JWT configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-change-in-production")
ALGORITHM = "HS256"

# Secret integrity check - ensure JWT_SECRET is exactly the same as BETTER_AUTH_SECRET in frontend
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if BETTER_AUTH_SECRET != JWT_SECRET:
    logger.warning("BETTER_AUTH_SECRET mismatch detected!")

logger.info("JWT Secret verified")

security = HTTPBearer()

def verify_jwt_token(token: str) -> Optional[Dict]:
    """
    Verify JWT token and return payload if valid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM], options={"verify_aud": False, "verify_iss": False, "verify_at_hash": False})
        return payload
    except JWTError as e:
        logger.debug(f"JWT Decode Failed: {str(e)}")
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current user from JWT token.
    Returns the user ID extracted from the token.
    """
    # Verify the JWT token
    payload = verify_jwt_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from JWT payload - look for user.id first (nested structure from session JWTs)
    # Fall back to 'sub' (subject) or 'id' (standalone) as standard OIDC claims
    user_id = payload.get('user', {}).get('id') or payload.get('sub') or payload.get('id')

    # Verify that we successfully extracted a user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT: no user ID found in token. Expected 'id' or 'sub' field.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Log successful authentication without exposing sensitive data
    logger.info(f"User authenticated: {user_id}")

    return user_id

def get_verified_user(user_id: str, current_user_id: str = Depends(get_current_user)) -> str:
    """
    Dependency to verify user access to resources.
    - Reads user_id from API path
    - Uses get_current_user to decode JWT
    - Compares path user_id with JWT user_id
    - Raises 401/403 if JWT invalid or user_id mismatch
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    return current_user_id