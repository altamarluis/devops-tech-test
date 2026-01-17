import subprocess
import time
import requests
import signal
import sys

BASE_URL = "http://127.0.0.1:8000"

def start_server():
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def test_e2e_health_and_add():
    process = start_server()
    time.sleep(2)  # tiempo para que el server levante

    try:
        health = requests.get(f"{BASE_URL}/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        add = requests.get(f"{BASE_URL}/add?a=5&b=7")
        assert add.status_code == 200
        assert add.json()["result"] == 12

    finally:
        process.send_signal(signal.SIGTERM)
        process.wait()
