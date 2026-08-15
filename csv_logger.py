import csv
import os
import time
from datetime import datetime

CSV_FILE = "access_log.csv"

LOG_COOLDOWN = 3   # seconds
last_log_time = 0

# NEW VARIABLES
last_logged_name = None
last_logged_status = None


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "Name",
                "Access_Status",
                "Confidence",
                "Liveness",
                "Remarks"
            ])


def log_event(name, access_status, confidence, liveness_status, remarks):
    global last_log_time, last_logged_name, last_logged_status

    current_time = time.time()

    # -----------------------------
    #  Cooldown Protection
    # -----------------------------
    if current_time - last_log_time < LOG_COOLDOWN:
        return

    # -----------------------------
    # Prevent Same Person Same Status Re-Logging
    # -----------------------------
    if name == last_logged_name and access_status == last_logged_status:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            name,
            access_status,
            round(confidence, 2),
            liveness_status,
            remarks
        ])

    print("Event Logged:", name, access_status)

    last_log_time = current_time
    last_logged_name = name
    last_logged_status = access_status