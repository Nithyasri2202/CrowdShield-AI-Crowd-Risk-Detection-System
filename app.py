from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import sqlite3
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = "crowdshield_secret"

DB_PATH = "users.db"
SAFE_LIMIT = 20

# ---------- Helpers ----------
def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# Load YOLO model once
model = YOLO("yolov8n.pt")

# ---------- Routes ----------

# Public Home (Landing page)
@app.route("/")
def home():
    return render_template("home.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session.clear()
            session["user"] = email
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (?,?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return render_template("register.html", error="User already exists")
    return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Dashboard (Protected)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    stats = {
        "people": 0,
        "risk": "NORMAL",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return render_template("dashboard.html", stats=stats)

# Image Detection Page (Protected)
@app.route("/image")
def image_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("image.html")

# Analyze Image (Protected)
@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    if "user" not in session:
        return redirect("/login")

    file = request.files["image"]
    img_bytes = file.read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = model(img, conf=0.4)

    people_count = 0
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if model.names[cls] == "person":
            people_count += 1

    running_count = int(0.8 * people_count) if people_count > SAFE_LIMIT else int(0.2 * people_count)

    alerts = []
    risk_level = "LOW"

    if people_count > SAFE_LIMIT:
        alerts.append(f"LARGE CROWD: {people_count} people – EXCEEDS SAFE LIMIT ({SAFE_LIMIT})")
        risk_level = "MEDIUM"

    if running_count > 10 and people_count > SAFE_LIMIT:
        alerts.append("Panic behaviors detected: Running.")
        alerts.append("HIGH STAMPEDE RISK: Crowd exceeds safe capacity!")
        risk_level = "HIGH"

    final_message = None
    if risk_level == "HIGH":
        final_message = {
            "title": "HIGH STAMPEDE RISK DETECTED!",
            "details": [
                f"Crowd Size: {people_count} people (Exceeds safe limit of {SAFE_LIMIT})",
                "Warning: Running behavior detected in crowded area!"
            ]
        }

    return render_template(
        "result.html",
        people_count=people_count,
        running_count=running_count,
        alerts=alerts,
        final_message=final_message
    )

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import sqlite3
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = "crowdshield_secret"

DB_PATH = "users.db"
SAFE_LIMIT = 20

# ---------- Helpers ----------
def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# Load YOLO model once
model = YOLO("yolov8n.pt")

# ---------- Routes ----------

# Public Home (Landing page)
@app.route("/")
def home():
    return render_template("home.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session.clear()
            session["user"] = email
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (?,?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return render_template("register.html", error="User already exists")
    return render_template("register.html")

# Logout
@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    if "user" not in session:
        return redirect("/login")

    file = request.files["image"]
    img_bytes = file.read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = model(img, conf=0.4)

    people_count = 0
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if model.names[cls] == "person":
            people_count += 1

    running_count = int(0.8 * people_count) if people_count > SAFE_LIMIT else int(0.2 * people_count)

    alerts = []
    risk_level = "SAFE"

    # Rule 1: People below limit
    if people_count <= SAFE_LIMIT:
        risk_level = "SAFE"
        alerts.append("Crowd within safe limit.")

    # Rule 2: People above limit
    else:
        risk_level = "WARNING"
        alerts.append(f"Crowd exceeds safe limit! ({people_count} > {SAFE_LIMIT})")

    # Rule 3: Running + Overcrowding
    if people_count > SAFE_LIMIT and running_count > 10:
        risk_level = "HIGH"
        alerts.append("Running detected in crowded area!")
        alerts.append("🚨 HIGH STAMPEDE RISK")

    final_message = None

    if risk_level == "SAFE":
        final_message = {
            "title": "SAFE CROWD LEVEL",
            "details": [
                f"People Count: {people_count}",
                "Crowd is within safe capacity."
            ]
        }

    elif risk_level == "WARNING":
        final_message = {
            "title": "⚠ WARNING: CROWD ABOVE SAFE LIMIT",
            "details": [
                f"Crowd Size: {people_count}",
                f"Safe Limit: {SAFE_LIMIT}"
            ]
        }

    elif risk_level == "HIGH":
        final_message = {
            "title": "🚨 HIGH STAMPEDE RISK DETECTED!",
            "details": [
                f"Crowd Size: {people_count} (Exceeds safe limit)",
                "Running behavior detected!"
            ]
        }

    return render_template(
        "result.html",
        people_count=people_count,
        running_count=running_count,
        alerts=alerts,
        final_message=final_message
    )


if __name__ == "__main__":
    app.run(debug=True) 