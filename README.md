# IoT-Enabled Smart Face Recognition Access Control System

A smart access control prototype that combines **face recognition, blink-based liveness detection, Arduino-controlled door locking, and ThingSpeak cloud logging**.

The system identifies registered users using FaceNet facial embeddings and an SVM classifier. It performs blink-based liveness verification before granting access and controls a solenoid door lock through an Arduino Uno. Authentication events can also be recorded locally and monitored through ThingSpeak.

## Project Overview

Traditional access control methods such as passwords, PINs, RFID cards, and physical keys have limitations, including unauthorized sharing, loss, and duplication.

This project provides a contactless authentication approach using computer vision and machine learning. It combines identity recognition with liveness verification and hardware-based access control.

## Project Screenshots

Add your actual project photographs here after uploading them to the repository.

Suggested photographs:
- Application interface
- Face recognition and detection
- Arduino and relay hardware setup
- Authorized access
- Unauthorized access or liveness detection
- ThingSpeak dashboard

## Key Features

- **Real-Time Face Detection:** Uses MediaPipe to detect faces from the camera stream.
- **Face Recognition:** Uses FaceNet to generate 512-dimensional facial embeddings.
- **SVM Classification:** Identifies registered users using a trained Support Vector Machine classifier.
- **Confidence Thresholding:** Checks prediction confidence before accepting an identity.
- **Prediction Smoothing:** Uses multiple consecutive predictions to improve recognition stability.
- **Blink-Based Liveness Detection:** Checks for a valid blink as an additional verification step.
- **Arduino-Based Lock Control:** Controls a relay and solenoid lock through serial communication.
- **Local Event Logging:** Records authentication events using CSV.
- **Cloud Monitoring:** Sends selected authentication information to ThingSpeak.
- **Unknown Face Capture:** Captures images of unidentified users for security review.

## System Architecture

The overall authentication process follows this sequence:

```text
             Camera Input
                  |
                  v
           MediaPipe Face Detection
                  |
                  v
             Face Extraction
                  |
                  v
          FaceNet Feature Extraction
                  |
                  v
          512-D Face Embedding
                  |
                  v
              Normalization
                  |
                  v
             SVM Classifier
                  |
                  v
          Confidence Verification
                  |
                  v
           Prediction Smoothing
                  |
          +-------+-------+
          |               |
          v               v
     Known Person     Unknown Person
          |               |
          v               v
    Blink Detection   Capture Image
          |               |
          v               v
    Liveness Check    Log Event
          |
     +----+----+
     |         |
     v         v
    Live     Spoof
     |         |
     v         v
   Grant     Deny
   Access   Access
     |
     v
  Arduino Uno
     |
     v
  Relay Module
     |
     v
  Solenoid Lock
```

## Machine Learning Pipeline

### 1. Face Detection and Extraction

MediaPipe detects faces in the camera frames. The detected face region is extracted and prepared for feature extraction.

### 2. Face Embedding Generation

FaceNet converts the extracted face into a numerical feature vector containing facial characteristics.

The project uses a 512-dimensional embedding.

### 3. Embedding Normalization

The generated embedding is normalized before being passed to the classifier.

### 4. SVM Classification

A Support Vector Machine with a linear kernel is trained using the registered users' face embeddings.

The trained classifier is saved as:

```text
face_classifier.pkl
```

### 5. Confidence Verification and Smoothing

The classifier's prediction confidence is checked against a configured threshold. Multiple consecutive predictions are also considered to improve stability and reduce temporary recognition fluctuations.

### 6. Blink-Based Liveness Detection

After a known identity is recognized, the system checks for a valid blink before making the final access decision.

This provides an additional layer of verification against simple photo-based spoofing attempts.

## Hardware Components

| Component | Purpose |
|---|---|
| Arduino Uno R3 SMD | Controls the lock and indicators |
| 1-Channel 5V Relay Module | Switches the solenoid lock |
| 12V DC Adapter | Supplies power to the lock |
| Solenoid Door Lock | Physical locking mechanism |
| RGB LED Module | Indicates system status |
| Active Buzzer | Provides audio feedback |
| Camera | Captures the user's face |
| Jumper Wires | Electrical connections |
| Breadboard | Hardware prototyping |

## Hardware Integration

The Python application handles face recognition and authentication. Once the access decision is made, it communicates with the Arduino Uno through serial communication.

```text
Python Application
        |
        v
Serial Communication
        |
        v
Arduino Uno
        |
        v
Relay Module
        |
        v
Solenoid Door Lock
```

The Arduino also controls the LED and buzzer to provide status feedback.

The relay is used to switch the higher-power lock circuit using the Arduino control signal.

## Software Technologies

| Category | Technologies |
|---|---|
| Programming Languages | Python, Arduino C/C++ |
| Computer Vision | OpenCV, MediaPipe |
| Face Recognition | FaceNet, keras-facenet |
| Machine Learning | Scikit-learn, SVM |
| Deep Learning Framework | TensorFlow, Keras |
| Numerical Processing | NumPy |
| Data Storage | Pickle, CSV |
| Hardware Communication | PySerial |
| Cloud Monitoring | ThingSpeak |
| Development Tools | PyCharm, Arduino IDE |
| Version Control | Git, GitHub |

## Local and Cloud Logging

### Local Event Logging

The project uses `csv_logger.py` to record authentication-related events locally.

These may include:
- Recognized users
- Unknown users
- Access granted or denied
- Liveness status
- Authentication time

The generated CSV log is a runtime file and is not included in the repository.

### ThingSpeak Cloud Logging

The project uses ThingSpeak for cloud-based monitoring of selected authentication events.

The communication functionality is implemented in:

```text
thingspeak_module.py
```

ThingSpeak allows authentication-related information to be viewed remotely through a cloud dashboard.

### Unknown Person Capture

The `unknown_capture.py` module handles the capture of images when an identity cannot be confidently recognized.

These images are intended for security review and are not included in the public repository.

## Project Structure

```text
iot-smart-face-recognition-access-control/
│
├── main.py
├── align_faces.py
├── arduino_comm.py
├── blink_liveness.py
├── build_database.py
├── csv_logger.py
├── data.py
├── evaluate_model.py
├── photos.py
├── profile_ui.py
├── thingspeak_module.py
├── train_svm.py
├── unknown_capture.py
│
├── haarcascade_frontalface_alt2.xml
│
├── embeddings.npy
├── labels.npy
├── face_classifier.pkl
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** Dataset images, aligned face images, virtual environments, generated logs, and unknown-person captures are excluded from the public repository.

## Important Python Files

| File | Description |
|---|---|
| `main.py` | Main application and authentication workflow |
| `align_faces.py` | Face alignment and preprocessing |
| `build_database.py` | Prepares the face database |
| `train_svm.py` | Trains the SVM classifier |
| `blink_liveness.py` | Implements blink-based liveness detection |
| `arduino_comm.py` | Handles serial communication with Arduino |
| `thingspeak_module.py` | Handles ThingSpeak communication |
| `csv_logger.py` | Records local authentication events |
| `unknown_capture.py` | Captures images of unknown users |
| `evaluate_model.py` | Evaluates the trained model |
| `data.py` | Data-related functionality |
| `photos.py` | Photo-related functionality |
| `profile_ui.py` | Profile and interface functionality |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bhargavigajjala23-gv/iot-smart-face-recognition-access-control.git

cd iot-smart-face-recognition-access-control
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Python version used during development:** Python 3.10.8.

Use compatible package versions and an appropriate environment for the pinned dependencies.

## Configuration

Before running the application:

1. Connect the camera.
2. Connect the Arduino Uno to the computer.
3. Upload the corresponding Arduino control program using Arduino IDE.
4. Configure the correct serial/COM port in the Python application.
5. Configure ThingSpeak credentials.
6. Ensure the
