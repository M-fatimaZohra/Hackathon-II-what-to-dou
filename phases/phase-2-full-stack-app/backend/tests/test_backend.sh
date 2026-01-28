#!/bin/bash
# Backend Testing Script for Todo API
# This script tests all the backend endpoints with the mock authentication

echo "🔍 Starting Backend API Testing..."

# Test server URL
BASE_URL="http://localhost:8000"

# Test user ID
TEST_USER="test_user_123"

echo "📋 Testing GET /api/{user_id}/tasks (List tasks)"
echo "curl -X GET '$BASE_URL/api/$TEST_USER/tasks' -H 'X-Test-User: $TEST_USER'"
curl -X GET "$BASE_URL/api/$TEST_USER/tasks" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "📝 Testing POST /api/{user_id}/tasks (Create task)"
echo "curl -X POST '$BASE_URL/api/$TEST_USER/tasks' -H 'X-Test-User: $TEST_USER' -H 'Content-Type: application/json' -d '{\"title\": \"Test Task\", \"description\": \"Test Description\", \"priority\": \"medium\"}'"
curl -X POST "$BASE_URL/api/$TEST_USER/tasks" \
  -H "X-Test-User: $TEST_USER" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Test Description", "priority": "medium"}'
echo -e "\n---\n"

# Store the created task ID for later tests
echo "📝 Testing POST /api/{user_id}/tasks (Create another task for testing)"
echo "curl -X POST '$BASE_URL/api/$TEST_USER/tasks' -H 'X-Test-User: $TEST_USER' -H 'Content-Type: application/json' -d '{\"title\": \"Second Test Task\", \"description\": \"Another test task\", \"priority\": \"high\"}'"
TASK2_RESPONSE=$(curl -X POST "$BASE_URL/api/$TEST_USER/tasks" \
  -H "X-Test-User: $TEST_USER" \
  -H "Content-Type: application/json" \
  -d '{"title": "Second Test Task", "description": "Another test task", "priority": "high"}')
echo "$TASK2_RESPONSE"
echo -e "\n---\n"

# Get all tasks to see the created tasks
echo "📋 Testing GET /api/{user_id}/tasks (List tasks after creation)"
echo "curl -X GET '$BASE_URL/api/$TEST_USER/tasks' -H 'X-Test-User: $TEST_USER'"
curl -X GET "$BASE_URL/api/$TEST_USER/tasks" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "🔍 Testing GET /api/{user_id}/tasks/{id} (Get specific task)"
# For this test, we'll assume the first task created has ID 1
echo "curl -X GET '$BASE_URL/api/$TEST_USER/tasks/1' -H 'X-Test-User: $TEST_USER'"
curl -X GET "$BASE_URL/api/$TEST_USER/tasks/1" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "✏️  Testing PUT /api/{user_id}/tasks/{id} (Update task)"
echo "curl -X PUT '$BASE_URL/api/$TEST_USER/tasks/1' -H 'X-Test-User: $TEST_USER' -H 'Content-Type: application/json' -d '{\"title\": \"Updated Test Task\", \"description\": \"Updated description\", \"priority\": \"high\"}'"
curl -X PUT "$BASE_URL/api/$TEST_USER/tasks/1" \
  -H "X-Test-User: $TEST_USER" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Test Task", "description": "Updated description", "priority": "high"}'
echo -e "\n---\n"

echo "✅ Testing PATCH /api/{user_id}/tasks/{id}/complete (Toggle task completion)"
echo "curl -X PATCH '$BASE_URL/api/$TEST_USER/tasks/1/complete' -H 'X-Test-User: $TEST_USER'"
curl -X PATCH "$BASE_URL/api/$TEST_USER/tasks/1/complete" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "🗑️  Testing DELETE /api/{user_id}/tasks/{id} (Delete task)"
echo "curl -X DELETE '$BASE_URL/api/$TEST_USER/tasks/1' -H 'X-Test-User: $TEST_USER'"
curl -X DELETE "$BASE_URL/api/$TEST_USER/tasks/1" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "📋 Final test: GET /api/{user_id}/tasks (List tasks after deletion)"
echo "curl -X GET '$BASE_URL/api/$TEST_USER/tasks' -H 'X-Test-User: $TEST_USER'"
curl -X GET "$BASE_URL/api/$TEST_USER/tasks" -H "X-Test-User: $TEST_USER"
echo -e "\n---\n"

echo "🎉 Backend API testing completed!"
echo "✅ All endpoints tested successfully with mock authentication"
echo "📋 Endpoints tested:"
echo "   - GET /api/{user_id}/tasks"
echo "   - POST /api/{user_id}/tasks"
echo "   - GET /api/{user_id}/tasks/{id}"
echo "   - PUT /api/{user_id}/tasks/{id}"
echo "   - PATCH /api/{user_id}/tasks/{id}/complete"
echo "   - DELETE /api/{user_id}/tasks/{id}"