import os, time, requests

API = os.getenv("API_URL", "http://localhost:8000")

def test_health():
    for _ in range(10):
        try:
            r = requests.get(f"{API}/health")
            if r.ok: break
        except Exception:
            time.sleep(1)
    assert requests.get(f"{API}/health").json()["status"] == "ok"