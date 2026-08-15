import cv2

# -----------------------------
# User Database
# -----------------------------
user_data = {
    "Bhargavi_G": {"age": 20, "role": "Student", "dept": "ECE"},
    "Ariel_Sharon": {"age": 75, "role": "Politician", "dept": "Government"},
    "Colin_Powell": {"age": 80, "role": "Leader", "dept": "Defense"},
    "George_W_Bush": {"age": 78, "role": "President", "dept": "Government"},
    "Tony_Blair": {"age": 71, "role": "PM", "dept": "Government"},
    "Gerhard_Schroeder": {"age": 80, "role": "Former Chancellor", "dept": "Government"}
}

# -----------------------------
# Profile Panel UI
# -----------------------------
def draw_profile_panel(frame, name, status, confidence, w):

    overlay = frame.copy()

    x1, y1 = w - 300, 50
    x2, y2 = w - 20, 250

    # Glass background
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (40, 40, 40), -1)
    frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    # Title
    cv2.putText(frame, "USER PROFILE",
                (x1 + 10, y1 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (200, 200, 200), 2)

    y_text = y1 + 70

    # -----------------------------
    # Known Person
    # -----------------------------
    if name in user_data:

        data = user_data[name]

        cv2.putText(frame, f"Name: {name}", (x1 + 10, y_text),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(frame, f"Age: {data['age']}", (x1 + 10, y_text+25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(frame, f"Role: {data['role']}", (x1 + 10, y_text+50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(frame, f"Dept: {data['dept']}", (x1 + 10, y_text+75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    # -----------------------------
    # Unknown Person
    # -----------------------------
    else:

        cv2.putText(frame, "Name: Unknown", (x1 + 10, y_text),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(frame, "Info: Not Registered", (x1 + 10, y_text+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        cv2.putText(frame, "Info: No Data Found", (x1 + 10, y_text+60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    # -----------------------------
    # Status (common)
    # -----------------------------
    color = (0,255,0) if "Granted" in status else (0,0,255)

    cv2.putText(frame, f"Status: {status}",
                (x1 + 10, y2 - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                color, 2)

    return frame