#!/usr/bin/env python3
"""
JWT Test Token Generator

This standalone script generates valid JWT tokens for testing the backend API
without bypassing JWT validation. The tokens are fully compatible with the
existing JWT middleware in the backend.

Usage:
    python test_jwt_generator.py [user_id] [email]

Examples:
    python test_jwt_generator.py
    python test_jwt_generator.py test_user_123 test@example.com
"""

from jose import jwt
import os
import sys
from datetime import datetime, timedelta
from typing import Optional


def get_jwt_secret() -> str:
    """
    Get the JWT secret from environment variable or use default.
    Must match the secret used in the backend JWT middleware.
    """
    return os.getenv("BETTER_AUTH_SECRET", "your-default-secret-change-in-production")


def create_test_token(user_id: str = "test_user_123", email: str = "test@example.com") -> str:
    """
    Create a test JWT token with the same format and validation as the backend.

    Args:
        user_id: The user ID to embed in the token (user.id field)
        email: The email to embed in the token

    Returns:
        A signed JWT token string
    """
    JWT_SECRET = get_jwt_secret()
    ALGORITHM = "HS256"

    payload = {
        "user": {  # Better Auth uses 'user' object with 'id' field
            "id": user_id,
            "email": email,
        },
        "exp": datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
        "iat": datetime.utcnow(),  # Issued at time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    return token


def main():
    """Main function to run the token generator from command line."""
    # Parse command line arguments
    user_id = sys.argv[1] if len(sys.argv) > 1 else "test_user_123"
    email = sys.argv[2] if len(sys.argv) > 2 else "test@example.com"

    try:
        token = create_test_token(user_id, email)

        print("✅ JWT Test Token Generated Successfully")
        print(f"User ID: {user_id}")
        print(f"Email: {email}")
        print(f"Token: {token}")
        print()
        print("💡 Usage Example:")
        print(f"curl -H 'Authorization: Bearer {token}' http://localhost:8000/api/{user_id}/tasks")
        print()
        print("📋 Backend Testing Commands:")
        print(f"# Get tasks for user {user_id}")
        print(f"curl -X GET 'http://localhost:8000/api/{user_id}/tasks' \\")
        print(f"  -H 'Authorization: Bearer {token}' \\")
        print("  -H 'Content-Type: application/json'")
        print()
        print(f"# Create a new task for user {user_id}")
        print(f"curl -X POST 'http://localhost:8000/api/{user_id}/tasks' \\")
        print(f"  -H 'Authorization: Bearer {token}' \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{\"title\": \"Test Task\", \"description\": \"Test Description\", \"priority\": \"medium\"}'")
        print()
        print("📋 Mock Authentication Testing (Alternative Method):")
        print("# Use test header to bypass JWT validation temporarily")
        print(f"curl -X GET 'http://localhost:8000/api/test_user_123/tasks' \\")
        print("  -H 'X-Test-User: test_user_123' \\")
        print("  -H 'Content-Type: application/json'")
        print()
        print("# Create task with mock authentication")
        print(f"curl -X POST 'http://localhost:8000/api/test_user_123/tasks' \\")
        print("  -H 'X-Test-User: test_user_123' \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{\"title\": \"Test Task\", \"description\": \"Test Description\", \"priority\": \"medium\"}'")
        print()
        print("⚠️  Security Notes:")
        print("• JWT method: This token will work with the backend JWT middleware")
        print("• Mock method: X-Test-User header bypasses JWT validation temporarily")
        print("• Path user_id must match the JWT 'user.id' field for requests to succeed")
        print("• Invalid tokens or mismatched user_ids will be rejected by the middleware")
        print("• Remove mock authentication when ready for production deployment")

    except Exception as e:
        print(f"❌ Error generating token: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if required dependency is installed
    try:
        from jose import jwt
    except ImportError:
        print("❌ Required package 'python-jose' is not installed.")
        print("Install it with: pip install python-jose[cryptography]")
        sys.exit(1)

    main()