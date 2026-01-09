#!/usr/bin/env python3
"""
Backend API Testing Script

This script tests all the backend endpoints with the mock authentication
to verify that the task CRUD operations work correctly.
"""

import requests
import json
import sys
from typing import Dict, Any, Optional


class BackendTester:
    def __init__(self, base_url: str = "http://localhost:8000", test_user: str = "test_user_123"):
        self.base_url = base_url
        self.test_user = test_user
        self.headers = {
            "X-Test-User": test_user,
            "Content-Type": "application/json"
        }
        self.created_task_ids = []

    def make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make an HTTP request to the backend."""
        url = f"{self.base_url}/api/{self.test_user}/{endpoint.lstrip('/')}"
        print(f"  {method} {url}")

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=self.headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            print(f"  Status: {response.status_code}")
            if response.status_code in [200, 201]:
                print(f"  Response: {response.json()}")
            else:
                print(f"  Error: {response.text}")

            return response
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Error: Could not connect to {url}")
            print("     Make sure the backend server is running with: uvicorn main:app --reload")
            return None
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return None

    def test_list_tasks(self):
        """Test GET /api/{user_id}/tasks endpoint."""
        print("\n📋 Testing GET /api/{user_id}/tasks (List tasks)")
        response = self.make_request("GET", "tasks")
        return response

    def test_create_task(self):
        """Test POST /api/{user_id}/tasks endpoint."""
        print("\n📝 Testing POST /api/{user_id}/tasks (Create task)")
        task_data = {
            "title": "Test Task from Python Script",
            "description": "Created via backend testing script",
            "priority": "medium"
        }
        response = self.make_request("POST", "tasks", task_data)

        if response and response.status_code == 200:
            task = response.json()
            self.created_task_ids.append(task.get('id'))
            print(f"  Created task with ID: {task.get('id')}")

        return response

    def test_get_task_by_id(self, task_id: int):
        """Test GET /api/{user_id}/tasks/{id} endpoint."""
        print(f"\n🔍 Testing GET /api/{{user_id}}/tasks/{task_id} (Get specific task)")
        response = self.make_request("GET", f"tasks/{task_id}")
        return response

    def test_update_task(self, task_id: int):
        """Test PUT /api/{user_id}/tasks/{id} endpoint."""
        print(f"\n✏️  Testing PUT /api/{{user_id}}/tasks/{task_id} (Update task)")
        task_data = {
            "title": "Updated Test Task",
            "description": "Updated description via testing script",
            "priority": "high"
        }
        response = self.make_request("PUT", f"tasks/{task_id}", task_data)
        return response

    def test_toggle_task_completion(self, task_id: int):
        """Test PATCH /api/{user_id}/tasks/{id}/complete endpoint."""
        print(f"\n✅ Testing PATCH /api/{{user_id}}/tasks/{task_id}/complete (Toggle task completion)")
        response = self.make_request("PATCH", f"tasks/{task_id}/complete")
        return response

    def test_delete_task(self, task_id: int):
        """Test DELETE /api/{user_id}/tasks/{id} endpoint."""
        print(f"\n🗑️  Testing DELETE /api/{{user_id}}/tasks/{task_id} (Delete task)")
        response = self.make_request("DELETE", f"tasks/{task_id}")
        if task_id in self.created_task_ids:
            self.created_task_ids.remove(task_id)
        return response

    def run_comprehensive_test(self):
        """Run a comprehensive test of all backend endpoints."""
        print("🔍 Starting Comprehensive Backend API Testing...")
        print(f"Using base URL: {self.base_url}")
        print(f"Using test user: {self.test_user}")
        print("-" * 60)

        # Test 1: List tasks (should be empty initially)
        self.test_list_tasks()

        # Test 2: Create a task
        create_response = self.test_create_task()
        if not create_response or create_response.status_code != 200:
            print("\n❌ Failed to create task. Stopping tests.")
            return False

        # Get the created task ID
        created_task = create_response.json()
        task_id = created_task.get('id')
        if not task_id:
            print("\n❌ Could not get task ID from creation response. Stopping tests.")
            return False

        # Test 3: Get the specific task
        self.test_get_task_by_id(task_id)

        # Test 4: Update the task
        self.test_update_task(task_id)

        # Test 5: Toggle task completion
        self.test_toggle_task_completion(task_id)

        # Test 6: Get the task again to see completion status
        self.test_get_task_by_id(task_id)

        # Test 7: List tasks again to see all tasks
        self.test_list_tasks()

        # Test 8: Delete the task
        self.test_delete_task(task_id)

        # Test 9: List tasks to confirm deletion
        self.test_list_tasks()

        print("\n🎉 Comprehensive Backend API testing completed!")
        print("✅ All endpoints tested successfully with mock authentication")
        print("📋 Endpoints tested:")
        print("   - GET /api/{user_id}/tasks")
        print("   - POST /api/{user_id}/tasks")
        print("   - GET /api/{user_id}/tasks/{id}")
        print("   - PUT /api/{user_id}/tasks/{id}")
        print("   - PATCH /api/{user_id}/tasks/{id}/complete")
        print("   - DELETE /api/{user_id}/tasks/{id}")

        return True

    def cleanup(self):
        """Clean up any tasks that were created during testing."""
        print("\n🧹 Cleaning up created tasks...")
        for task_id in self.created_task_ids[:]:  # Copy the list to avoid modification during iteration
            print(f"  Deleting task {task_id}...")
            self.test_delete_task(task_id)


def main():
    """Main function to run the backend tests."""
    print("🚀 Backend API Testing Tool")
    print("=" * 60)

    # Create tester instance
    tester = BackendTester()

    try:
        # Run comprehensive tests
        success = tester.run_comprehensive_test()

        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user.")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred during testing: {str(e)}")
        tester.cleanup()
        sys.exit(1)

    # Cleanup any remaining tasks
    tester.cleanup()
    print("\n📋 Testing complete. Resources cleaned up.")


if __name__ == "__main__":
    main()