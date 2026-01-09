from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-change-in-production")
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return payload if valid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def jwt_middleware(request: Request, call_next):
    """
    Middleware to validate JWT tokens for protected routes
    Expects JWT token in Authorization header as per API specification
    """
    # Define routes that don't require authentication
    public_routes = ["/", "/health", "/docs", "/redoc", "/openapi.json"]

    # Skip authentication for public routes
    if request.url.path in public_routes:
        response = await call_next(request)
        return response

    # Skip authentication for auth-related routes
    if "/auth" in request.url.path:
        response = await call_next(request)
        return response

    # For all protected routes, require valid JWT token in Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format. Expected: 'Authorization: Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]

    # Verify the JWT token
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Add user info to request state for use in route handlers
    # Extract user_id from JWT payload - following standard JWT claims
    # Better Auth typically uses 'sub' (subject) field for user ID
    request.state.user_id = payload.get("sub") or payload.get("id") or payload.get("user_id")
    request.state.user_email = payload.get("email") or payload.get("user_email")

    # Verify that we successfully extracted a user_id
    if not request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT: no user ID found in token. Expected 'sub', 'id', or 'user_id' field.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = await call_next(request)
    return response