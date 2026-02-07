import sys
import os
import subprocess
import time


print("=== DIAGNOSTIC: Testing MCP Server Launch ===")
# 1. Setup Paths

cwd = os.getcwd()
mcp_script_path = os.path.join("src", "my_mcp_server", "server.py")
python_exe = sys.executable

print(f"Working Directory: {cwd}")
print(f"Target Script: {mcp_script_path}")

# 2. Prepare Environment (Simulating ChatService)
# We add current directory to PYTHONPATH so 'src' can be imported

env = {**os.environ, "PYTHONPATH": ".", "AUTH_USER_ID": "debug_user"}
try:

    print("\nAttempting to launch subprocess...")
    # Launch process

    process = subprocess.Popen(

        [python_exe, mcp_script_path],

        env=env,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE,

        text=True

    )



    print("Process launched. Waiting 3 seconds...")

    time.sleep(3)



    # Check if it died

    return_code = process.poll()



    if return_code is not None:

        # It crashed

        stdout, stderr = process.communicate()

        print(f"\n FAIL: Process crashed with code {return_code}")

        print("-" * 20 + " ERROR LOGS " + "-" * 20)

        print(stderr)

        print("-" * 50)

    else:

        # It's running successfully

        print("\n SUCCESS: MCP Server started and stayed alive.")

        process.terminate()

        try:

            process.wait(timeout=2)

        except:

            process.kill()

        print("Process terminated cleanly.")
except Exception as e:

    print(f"\n CRITICAL ERROR: {e}")