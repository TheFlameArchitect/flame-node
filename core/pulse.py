import requests, json

def fetch_pulse(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        with open("rituals/pulse_cache.json", "w") as f:
            json.dump(data, f, indent=2)
        print("📡 Pulse updated.")
    except requests.exceptions.ConnectionError:
        print("⚠️ Pulse unreachable. Network connection failed. Proceeding offline.")
    except requests.exceptions.Timeout:
        print("⚠️ Pulse unreachable. Connection timeout. Proceeding offline.")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Pulse unreachable. HTTP error {e.response.status_code}. Proceeding offline.")
    except Exception as e:
        print(f"⚠️ Pulse unreachable. {type(e).__name__}: {str(e)}. Proceeding offline.") 