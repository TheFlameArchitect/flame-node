import requests, json

def fetch_pulse(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        with open("rituals/pulse_cache.json", "w") as f:
            json.dump(data, f, indent=2)
        print("📡 Pulse updated.")
    except Exception:
        print("⚠️ Pulse unreachable. Proceeding offline.") 