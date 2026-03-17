import subprocess
import sys


def test_greet():
    res = subprocess.run([sys.executable, "-m", "myapp", "greet", "--name", "Tester"], capture_output=True, text=True)
    assert "Hello, Tester!" in res.stdout
