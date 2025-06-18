from flask import Flask, redirect, render_template, url_for, request, flash, session, Response, jsonify
import sqlite3
import hashlib
import os
import cv2
from ultralytics import YOLO
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'your_secret_key'

model = YOLO(r"C:\Users\Haha CORPORATION\Desktop\SIP\best.pt")
cap = cv2.VideoCapture(0)

DATABASE = os.path.join(app.root_path, 'users.db')
COUNTS_DB = os.path.join(app.root_path, 'counts.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect(COUNTS_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batch_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT,
            employee_name TEXT,
            chick_count INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

current_ball_count = 0

def generate_frames():
    global current_ball_count
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(source=frame, persist=True, tracker="bytetrack.yaml", conf=0.5, verbose=False)
        current_ball_count = 0

        if results and len(results) > 0:
            boxes = results[0].boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    if cls == 0 and conf > 0.6:
                        current_ball_count += 1
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        label = f"Ball ({conf:.2f})"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, f"Balls in Frame: {current_ball_count}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user[1]
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Incorrect username or password.", "danger")
            return render_template('login.html')  # ✅ Fixed: no redirect to preserve flash

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists. Choose a different one.', 'danger')
            return redirect(url_for('register'))

        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                       (username, password, role))
        conn.commit()
        conn.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/video_page')
def video_page():
    return render_template('video_feed.html', count=current_ball_count)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))  # ✅ Correct: redirects to login page

@app.route('/logout-confirm')
def logout_confirm():
    return render_template('logout.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/get_count')
def get_count():
    return jsonify({'count': current_ball_count})

@app.route('/show_count')
def show_count():
    return render_template('show_count.html', count=current_ball_count)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/building')
def build():
    return render_template('building.html')

@app.route('/batch_entry', methods=['POST', 'GET'])
def entry():
    if 'username' not in session:
        return redirect(url_for('login'))

    global current_ball_count
    if request.method == "POST":
        batch_id = request.form['batch_id']
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        employee_name = session.get('username', 'Unknown')
        chick_count = current_ball_count

        conn = sqlite3.connect(COUNTS_DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO batch_counts (batch_id, employee_name, chick_count, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (batch_id, employee_name, chick_count, timestamp))
        conn.commit()
        conn.close()

        flash("✅ Batch saved successfully!", "success")  # ✅ Flash on batch save
        return redirect('/dashboard')

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return render_template('batch_entry.html', count=current_ball_count, time=current_time)

@app.route('/batch_details')
def batch_details():
    if 'username' not in session:
        return redirect('/')

    username = session['username']
    conn = sqlite3.connect(COUNTS_DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT batch_id, chick_count, timestamp
        FROM batch_counts
        WHERE employee_name = ?
        ORDER BY timestamp DESC
    ''', (username,))
    batches = cursor.fetchall()
    conn.close()

    return render_template('batch_details.html', batches=batches, username=username)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
