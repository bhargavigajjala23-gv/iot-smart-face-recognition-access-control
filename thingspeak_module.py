import requests
import time

THINGSPEAK_API_KEY = "YOUR_API_KEY"

last_upload_time = 0
last_sent_name = ""

def send_to_thingspeak(name, confidence, status, intrusion_count):

    global last_upload_time
    global last_sent_name

    # Send only if new person detected
    if name == last_sent_name:
        return

    # ThingSpeak limit
    if time.time() - last_upload_time < 15:
        return

    url = "https://api.thingspeak.com/update"

    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": name,
        "field2": confidence,
        "field3": status,
        "field4": intrusion_count
    }

    try:
        response = requests.post(url, data=data, timeout=3)

        if response.status_code == 200:
            print("Data sent to ThingSpeak:", name)

        else:
            print("ThingSpeak upload failed")

        last_upload_time = time.time()
        last_sent_name = name

    except Exception as e:
        print("ThingSpeak Error:", e)