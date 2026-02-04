import requests
import hashlib
from datetime import datetime

URL = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"

def fetch_data():
    session = requests.Session()
    
    # Get server time and expected username from headers
    initial_response = session.get(URL)
    expected_username = initial_response.headers.get('X-Credentials-Username', '').split(' ')[0]
    
    # Extract date components from expected username
    # Format: tesprogrammerDDMMYYCHH
    day_str = expected_username[13:15]
    month_str = expected_username[15:17] 
    year_str = expected_username[17:19]
    
    username = expected_username
    raw_password = f"bisacoding-{day_str}-{month_str}-{year_str}"
    password_md5 = hashlib.md5(raw_password.encode()).hexdigest()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    data = {
        "username": username,
        "password": password_md5
    }

    print("USERNAME :", username)
    print("RAW PASS :", raw_password)
    print("MD5 PASS :", password_md5)
    print("COOKIE FROM FIRST REQ:", session.cookies.get_dict())

    response = session.post(URL, headers=headers, data=data)

    print("STATUS :", response.status_code)
    print("RESP   :", response.text)
    print("HEADERS:", dict(response.headers))
    print("COOKIE :", session.cookies.get_dict())
    
    if response.status_code != 200:
        return response.json()
    
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_data()
    print("\n✅ SUCCESS")
    print(data)
