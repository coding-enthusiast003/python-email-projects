import requests
import time



def scan_attachment(payload_bytes, filename, api_key):
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": api_key}
    
    files = {"file": (filename, payload_bytes)}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        print("❌ Error sending file for scan.")
        return False

    analysis_id = response.json()["data"]["id"]
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

    while True:
        res = requests.get(analysis_url, headers=headers)
        status = res.json()["data"]["attributes"]["status"]
        if status == "completed":
            break
        time.sleep(2)

    stats = res.json()["data"]["attributes"]["stats"]
    if stats["malicious"] > 0 or stats["suspicious"] > 0:
        print("⚠️ File flagged as unsafe.")
        return False
    
    return True
