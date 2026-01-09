# Backend Testing Guide

This guide explains how to test the backend API endpoints for the Todo application.

## Prerequisites

1. Make sure the backend server is running:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. The server should be accessible at `http://localhost:8000`

## Testing Methods

### Method 1: Using the Python Test Script

Run the comprehensive test script:
```bash
python test_backend.py
```

This will test all endpoints in sequence and provide detailed output.

### Method 2: Using the Shell Script

Run the shell script to test endpoints with curl:
```bash
bash test_backend.sh
```

### Method 3: Manual Testing with curl

Use the test header `X-Test-User: test_user_123` to authenticate:

```bash
# List all tasks
curl -X GET 'http://localhost:8000/api/test_user_123/tasks' -H 'X-Test-User: test_user_123'

# Create a new task
curl -X POST 'http://localhost:8000/api/test_user_123/tasks' \
  -H 'X-Test-User: test_user_123' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Test Task", "description": "Test Description", "priority": "medium"}'

# Get a specific task
curl -X GET 'http://localhost:8000/api/test_user_123/tasks/1' -H 'X-Test-User: test_user_123'

# Update a task
curl -X PUT 'http://localhost:8000/api/test_user_123/tasks/1' \
  -H 'X-Test-User: test_user_123' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated Task", "description": "Updated Description", "priority": "high"}'

# Toggle task completion
curl -X PATCH 'http://localhost:8000/api/test_user_123/tasks/1/complete' -H 'X-Test-User: test_user_123'

# Delete a task
curl -X DELETE 'http://localhost:8000/api/test_user_123/tasks/1' -H 'X-Test-User: test_user_123'
```

## Endpoints Tested

- `GET /api/{user_id}/tasks` - List all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task

## Security Notes

- The `X-Test-User: test_user_123` header temporarily bypasses JWT validation
- In production, real JWT tokens are required in the `Authorization: Bearer <token>` header
- The user_id in the URL path must match the authenticated user (enforced by middleware)

## Troubleshooting

If you get connection errors:
- Make sure the backend server is running
- Check that the port is correct (default: 8000)
- Verify the test headers are being sent correctly

If you get 401 or 403 errors:
- Ensure the `X-Test-User: test_user_123` header is included
- Verify the user_id in the URL matches the test user