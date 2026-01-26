# Data Model: Frontend Production & Security Hardening

## Environment Configuration
- **API_URL**: String representing the production backend API endpoint (NEXT_PUBLIC_API_URL)
- **BASE_URL**: String representing the frontend application URL (NEXT_PUBLIC_BASE_URL)
- **Validation**: Both values must be present and valid URLs

## Authentication Session
- **Cookie Attributes**:
  - httpOnly: boolean (true for production security)
  - secure: boolean (true for HTTPS only)
  - sameSite: string ("lax" for CSRF protection)
- **Session Management**: Handled by Better-Auth with secure configuration

## API Request Object
- **Base URL**: Derived from environment variable
- **Headers**: Properly configured for production API calls
- **Error Handling**: Robust error handling for API failures