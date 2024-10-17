import subprocess
import pytest
import time

@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Start the server
    process = subprocess.Popen(["pipenv", "run", "python", "manage.py", "runserver"])

    # Allow some time for the server to start
    time.sleep(5)  # Adjust based on how long your server needs

    yield

    # Teardown: Stop the server after tests are done
    process.terminate()
