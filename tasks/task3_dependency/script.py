# script.py
import requests  # ← This package is missing
import json

def fetch_data():
    try:
        response = requests.get("https://api.github.com")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_data(data):
    if "error" in data:
        return f"Failed to fetch: {data['error']}"
    return f"Success! Status: {data.get('status', 'unknown')}"

if __name__ == "__main__":
    data = fetch_data()
    result = process_data(data)
    print(result)
