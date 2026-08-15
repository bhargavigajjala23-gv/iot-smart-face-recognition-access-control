# IoT-Enabled Smart Face Recognition Access Control System

A smart and secure access control system that combines **face recognition, blink-based liveness detection, Arduino-controlled door locking, and cloud-based event logging**.

The system verifies a person's identity using **FaceNet facial embeddings and an SVM classifier**, checks whether the detected face belongs to a live person using **blink detection**, and grants or denies access accordingly. When access is granted, an Arduino activates a relay-controlled solenoid lock. Authentication events are also logged locally and sent to **ThingSpeak** for cloud monitoring.

---

## 📌 Project Overview

Traditional access control systems such as passwords, PINs, RFID cards, and physical keys have several limitations. Passwords can be shared or stolen, cards can be lost or duplicated, and keys can be misplaced.

This project implements a computer-vision-based access control system where a camera continuously observes the user and performs multiple verification stages:

1. Detect the face.
2. Extract the face region.
3. Generate a facial embedding using FaceNet.
4. Normalize the embedding.
5. Classify the identity using an SVM model.
6. Apply a confidence threshold.
7. Smooth predictions across multiple frames.
8. Perform blink-based liveness verification.
9. Make the final access decision.
10. Control the physical door lock through Arduino.
11. Log the authentication event.
12. Send selected events to ThingSpeak.
13. Capture unknown faces for security monitoring.

The system is designed to provide an additional layer of protection against unauthorized access and simple photo/video spoofing attempts.

---

## 🎯 Objectives

The main objectives of this project are:

* To develop a face-based access control system.
* To detect faces in real time using MediaPipe.
* To generate robust facial feature embeddings using FaceNet.
* To classify registered users using a Support Vector Machine (SVM).
* To reduce false recognition using confidence thresholding.
* To improve prediction stability using frame-based smoothing.
* To distinguish live users from simple spoof attempts using blink detection.
* To control a physical electronic lock using Arduino.
* To record authentication events locally.
* To monitor authentication activity through ThingSpeak.
* To capture images of unknown users for security analysis.

---

## ✨ Key Features

### 1. Real-Time Face Detection

The system uses **MediaPipe Face Detection** to locate faces from the camera stream.

MediaPipe provides efficient real-time face detection and is suitable for applications where processing speed is important.

---

### 2. Face Extraction

Once a face is detected, the corresponding region is extracted from the camera frame and prepared for feature extraction.

The extracted face is passed to the FaceNet model.

---

### 3. Face Recognition Using FaceNet

The project uses **FaceNet** to convert a detected face into a numerical feature representation called a **face embedding**.

Each face is represented as a vector containing facial characteristics.

The generated embedding is then normalized before being passed to the classifier.

General pipeline:

```text
Camera Image
      ↓
Face Detection
      ↓
Face Extraction
      ↓
FaceNet
      ↓
512-Dimensional Face Embedding
      ↓
Normalization
      ↓
SVM Classifier
      ↓
Identity Prediction
```

---

### 4. SVM-Based Classification

A **Support Vector Machine (SVM)** is used to classify the generated face embeddings.

The SVM is trained using embeddings corresponding to the registered identities.

The trained classifier is saved as:

```text
face_classifier.pkl
```

The project uses a linear SVM with probability estimation for classification.

---

### 5. Confidence Threshold

The classifier's prediction is not accepted blindly.

A confidence threshold is used to determine whether the prediction is reliable enough to continue with authentication.

Conceptually:

```text
Confidence ≥ Threshold
        ↓
   Accept Prediction

Confidence < Threshold
        ↓
   Treat as Unknown
```

This helps reduce incorrect recognition when the detected face does not sufficiently match a registered identity.

---

### 6. Prediction Smoothing

Face recognition predictions can fluctuate between consecutive camera frames.

For example:

```text
Frame 1 → Person A
Frame 2 → Person A
Frame 3 → Unknown
Frame 4 → Person A
Frame 5 → Person A
```

Instead of making a decision from a single frame, the system uses multiple consecutive predictions to improve stability.

This reduces temporary recognition fluctuations caused by:

* Lighting changes
* Face movement
* Camera noise
* Partial face visibility
* Temporary detection errors

---

### 7. Blink-Based Liveness Detection

Face recognition alone may be vulnerable to simple presentation attacks such as showing a photograph of a registered person to the camera.

To provide an additional verification layer, the project includes **blink-based liveness detection**.

The system observes the user's eye movement and checks for a valid blink.

The authentication process therefore becomes:

```text
Face Recognition
       +
Liveness Verification
       ↓
Final Access Decision
```

Possible outcomes include:

* Live user
* Spoof attempt
* Unknown live person
* Access granted
* Access denied

---

## 🔐 Access Decision Pipeline

The overall decision process is:

```text
                Camera
                   ↓
           Face Detection
                   ↓
          Face Extraction
                   ↓
        FaceNet Embedding
                   ↓
            Normalization
                   ↓
          SVM Classification
                   ↓
        Confidence Threshold
                   ↓
         Prediction Smoothing
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   Known Person           Unknown Person
        ↓                     ↓
 Liveness Check        Capture Unknown Face
        ↓                     ↓
   ┌────┴────┐             Log Event
   ↓         ↓
  Live      Spoof
   ↓         ↓
Access     Deny
Granted    Access
   ↓
Arduino Signal
   ↓
Relay Module
   ↓
Solenoid Lock
```

---

## ⚙️ Hardware Components

The physical access-control portion uses the following components:

| Component                 | Purpose                                     |
| ------------------------- | ------------------------------------------- |
| Arduino Uno R3 SMD        | Controls the electronic lock and indicators |
| 1-Channel 5V Relay Module | Switches the solenoid lock                  |
| 12V DC Adapter            | Provides power to the solenoid lock         |
| Solenoid Door Lock        | Physical locking mechanism                  |
| RGB LED Module            | Indicates system/access status              |
| Active Buzzer             | Provides audio feedback                     |
| Camera                    | Captures the user's face                    |
| Jumper Wires              | Electrical connections                      |
| Breadboard                | Prototyping and connections                 |

---

## 🔌 Hardware Working

The Python application performs the recognition and authentication process.

After a successful authentication, Python sends a control signal to the Arduino through serial communication.

The Arduino then controls:

```text
Python Application
       ↓
Serial Communication
       ↓
Arduino Uno
       ↓
Relay Module
       ↓
Solenoid Lock
```

The relay provides electrical isolation between the Arduino control circuit and the higher-power lock circuit.

The Arduino also controls the RGB LED and buzzer to provide status feedback.

---

## 💻 Software Technologies

### Programming Language

* Python
* Arduino C/C++

### Computer Vision

* OpenCV
* MediaPipe

### Face Recognition

* FaceNet
* `keras-facenet`

### Machine Learning

* Scikit-learn
* Support Vector Machine (SVM)

### Numerical Processing

* NumPy

### Data Storage

* Pickle
* CSV

### Cloud Monitoring

* ThingSpeak

### Development Environment

* PyCharm
* Arduino IDE

---

## 🧠 Machine Learning Pipeline

The machine-learning portion of the project follows these stages:

### Training

```text
Training Images
      ↓
Face Detection
      ↓
Face Alignment / Extraction
      ↓
FaceNet
      ↓
Face Embeddings
      ↓
Normalization
      ↓
SVM Training
      ↓
Trained Classifier
```

The trained classifier and related data are saved locally for later recognition.

### Recognition

```text
Live Camera Frame
      ↓
Face Detection
      ↓
Face Extraction
      ↓
FaceNet Embedding
      ↓
Normalization
      ↓
SVM Prediction
      ↓
Confidence Check
      ↓
Identity
```

---

## ☁️ ThingSpeak Cloud Logging

The project includes cloud-based logging using **ThingSpeak**.

Authentication-related information can be sent to a ThingSpeak channel for remote monitoring.

The cloud logging component allows the project to extend beyond local authentication and provides a way to observe system activity remotely.

The ThingSpeak communication is implemented in:

```text
thingspeak_module.py
```

### Security Note

API keys and other credentials should **never be committed to a public GitHub repository**.

Before uploading this project, replace any real ThingSpeak API key in the source code with a placeholder or move the credential to an environment variable or local configuration file.

Example:

```python
WRITE_API_KEY = "YOUR_THINGSPEAK_API_KEY"
```

---

## 👤 Unknown Person Capture

When the system cannot confidently identify a person, the project can capture an image of the unknown face.

This provides an additional security feature because unauthorized attempts can be reviewed later.

The unknown-face functionality is implemented in:

```text
unknown_capture.py
```

Generated unknown-person images should normally remain outside the Git repository and are therefore excluded through `.gitignore`.

---

## 📝 Local Event Logging

The project also includes CSV-based event logging.

The logging functionality is implemented in:

```text
csv_logger.py
```

Events can include information related to:

* Recognized users
* Unknown users
* Access granted
* Access denied
* Liveness status
* Spoof attempts
* Authentication time

The generated `access_log.csv` file is excluded from GitHub because it is a runtime-generated file.

---

## 📁 Project Structure

```text
SA Control/
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
├── .gitignore
├── README.md
│
├── Dataset/                 # Not included in GitHub
├── Dataset_split/           # Not included in GitHub
├── aligned_faces/          # Not included in GitHub
├── unauthorized_attempts/  # Not included in GitHub
├── .venv/                   # Not included in GitHub
└── access_log.csv           # Not included in GitHub
```

---

## 📌 Important Python Files

### `main.py`

Main application file responsible for integrating the complete authentication pipeline.

### `train_svm.py`

Used for training the SVM classifier using face embeddings.

### `build_database.py`

Used for preparing the face database and generating the required data for recognition.

### `align_faces.py`

Handles face alignment/extraction during the preprocessing stage.

### `blink_liveness.py`

Implements blink-based liveness detection.

### `unknown_capture.py`

Captures and stores images of unknown users.

### `arduino_comm.py`

Handles serial communication between Python and Arduino.

### `thingspeak_module.py`

Handles communication with ThingSpeak for cloud logging.

### `csv_logger.py`

Handles local authentication-event logging.

### `evaluate_model.py`

Used for evaluating the trained recognition model.

### `profile_ui.py`

Provides the profile/status user-interface elements used by the application.

---

## 🔄 Complete System Workflow

The complete system works as follows:

### Step 1 — Camera Input

The camera continuously captures frames.

### Step 2 — Face Detection

MediaPipe identifies whether a face is present.

### Step 3 — Face Extraction

The detected face region is extracted and prepared for recognition.

### Step 4 — Face Embedding

FaceNet converts the face into a numerical embedding.

### Step 5 — Normalization

The embedding is normalized before classification.

### Step 6 — Identity Classification

The SVM classifier predicts the most likely registered identity.

### Step 7 — Confidence Verification

The prediction is checked against the configured confidence threshold.

### Step 8 — Prediction Smoothing

Multiple predictions are considered to improve stability.

### Step 9 — Liveness Verification

For a recognized user, blink detection verifies that the person is physically present.

### Step 10 — Access Decision

The system determines whether access should be granted or denied.

### Step 11 — Physical Lock Control

For successful authentication:

```text
Python → Arduino → Relay → Solenoid Lock
```

### Step 12 — User Feedback

The RGB LED and buzzer provide system-status feedback.

### Step 13 — Logging

The event can be recorded locally and transmitted to ThingSpeak.

### Step 14 — Unknown Person Handling

If the person cannot be identified confidently, the system can capture an image for later review.

---

## 🛡️ Security Considerations

The system combines multiple verification mechanisms rather than relying only on face recognition.

Security-related features include:

* Face recognition
* Confidence thresholding
* Prediction smoothing
* Blink-based liveness detection
* Unknown-face capture
* Authentication logging
* Cloud monitoring
* Physical relay-controlled locking

However, blink-based liveness detection is designed as a lightweight liveness mechanism and should not be considered equivalent to advanced anti-spoofing systems used in commercial biometric products.

---

## 🚀 Installation

### 1. Clone the Repository

After the project is uploaded to GitHub:

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install opencv-python
pip install numpy
pip install mediapipe
pip install keras-facenet
pip install scikit-learn
pip install tensorflow
pip install requests
```

Depending on the installed versions and operating system, some packages may require compatible versions.

---

## 🔧 Configuration

Before running the application:

1. Connect the camera.
2. Connect the Arduino.
3. Connect the relay module and solenoid lock according to the hardware design.
4. Upload the Arduino control program using Arduino IDE.
5. Configure the correct Arduino serial/COM port.
6. Configure ThingSpeak credentials securely.
7. Ensure the required trained model files are available.
8. Verify that the required Python packages are installed.

---

## ▶️ Running the Project

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Then run:

```bash
python main.py
```

The camera-based authentication system should start.

---

## 🔧 Arduino Communication

The Python application communicates with Arduino through serial communication.

The Arduino receives control signals and performs the required hardware actions.

Example logical flow:

```text
Authentication Successful
        ↓
Python sends access signal
        ↓
Arduino receives signal
        ↓
Relay activated
        ↓
Solenoid lock released
        ↓
LED/Buzzer feedback
```

For denied access, the Arduino does not activate the unlocking mechanism and provides the appropriate status indication.

---

## 📊 Expected System States

The application can produce states such as:

```text
Access Granted
Access Denied
Live Granted
Spoof Attack
Unknown - Live
```

These states represent different combinations of identity recognition and liveness verification.

---

## 🧪 Testing

The system can be tested under different conditions:

### Registered User

Expected:

```text
Known Face
   ↓
High Confidence
   ↓
Live Person
   ↓
Access Granted
```

### Unknown User

Expected:

```text
Unknown Face
   ↓
Confidence Below Threshold
   ↓
Access Denied
   ↓
Unknown Image Captured
```

### Photograph / Spoof Attempt

Expected:

```text
Recognized Identity
        ↓
Liveness Verification
        ↓
No Valid Blink
        ↓
Spoof Attack
        ↓
Access Denied
```

### Difficult Lighting / Movement

The prediction-smoothing mechanism helps reduce temporary recognition fluctuations caused by changes in lighting, movement, and camera conditions.

---

## 📈 Advantages

* Contactless authentication
* Real-time face recognition
* Lightweight SVM classification
* Additional liveness verification
* Physical electronic lock integration
* Local event logging
* Cloud monitoring
* Unknown-user image capture
* Modular Python implementation
* Suitable for prototype smart-access applications

---

## ⚠️ Limitations

The current prototype has several limitations:

* Blink detection provides limited protection against sophisticated spoofing attacks.
* Recognition accuracy can be affected by lighting and camera quality.
* Extreme face angles can reduce detection/recognition performance.
* The system depends on camera availability.
* Hardware communication depends on the correct Arduino serial port.
* The prototype is intended for controlled environments rather than high-security commercial deployment.
* ThingSpeak communication requires network connectivity.
* Model performance depends on the quality and diversity of the training images.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Advanced face anti-spoofing models
* Deep-learning-based liveness detection
* Larger and more diverse face datasets
* ArcFace or other modern face-recognition models
* Better illumination and pose handling
* Secure credential management using environment variables
* Database-based authentication logs
* Mobile/web dashboard for monitoring
* Email/SMS security notifications
* Multiple-door access management
* Role-based access control
* Improved hardware enclosure
* Edge deployment using Raspberry Pi or other embedded AI hardware

---

## 👨‍💻 Skills Demonstrated

This project demonstrates practical experience in:

* Python programming
* C/C++ programming for Arduino
* Computer vision
* Face detection
* Face recognition
* Machine learning
* Feature extraction
* SVM classification
* Liveness detection
* Image processing
* Serial communication
* Embedded hardware interfacing
* Relay and solenoid control
* Cloud IoT logging
* Data logging
* Git and GitHub
* Software-hardware integration

---

## 📜 Conclusion

The **IoT-Enabled Smart Face Recognition Access Control System** combines computer vision, machine learning, embedded hardware, liveness verification, and cloud monitoring into a single access-control prototype.

The system uses **MediaPipe for face detection, FaceNet for facial feature extraction, SVM for identity classification, blink detection for liveness verification, Arduino for physical lock control, and ThingSpeak for cloud-based logging**.

By combining identity verification with liveness detection and physical access control, the project demonstrates how AI and embedded systems can be integrated to build a practical smart-security application.

---

## 🔒 Security Notice

Do not upload the following to a public GitHub repository:

* API keys
* Passwords
* Authentication tokens
* Private credentials
* Personal datasets
* Private user images
* Runtime logs containing sensitive information

Use `.gitignore` and environment variables or local configuration files to keep sensitive information private.

---

## 📄 License

This project is intended for educational and demonstration purposes.

If you plan to reuse or distribute the project, add an appropriate open-source license to this repository.
