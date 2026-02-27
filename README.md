# CrowdShield-AI-Crowd-Risk-Detection-System
CrowdShield is an AI-based safety system designed to monitor crowds and detect potential stampede risks in public places like temples, festivals, railway stations, and events.
🔹 Features

- Detects people in a crowd using AI
- Calculates total crowd size
- Detects running behavior
- Classifies crowd risk level:
  - SAFE
  - WARNING
  - HIGH RISK
- Dashboard to view results
- Image upload analysis
- Login & Registration system

---

 🔹 Technologies Used

- Python
- Flask
- YOLOv8
- OpenCV
- HTML
- CSS
- SQLite Database

---

🔹 Project Structure


crowdshield/
│
├── app.py
├── users.db
│
├── templates/
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── image.html
│ └── result.html
│
└── static/
└── style.css


---

🔹 Installation

Install required libraries:


pip install flask opencv-python ultralytics numpy


---

🔹 Run the Project

Start the application:


python app.py


Then open in browser:


http://127.0.0.1:5000


---

🔹 How It Works

1. User logs into the system
2. Uploads an image
3. AI detects number of people
4. System checks:
   - Crowd size
   - Running behavior
5. Risk level is shown as:
   - SAFE
   - WARNING
   - HIGH RISK

---

🔹 Applications

CrowdShield can be used in:

- Temples
- Festivals
- Railway stations
- Stadiums
- Public gatherings

---

🔹 Future Improvements

- Live camera monitoring
- Panic detection
- Mobile alerts

---

🔹 Purpose

This project is developed for academic and safety research purposes.
