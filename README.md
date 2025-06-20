
![chickMate Logo](https://github.com/Yashvin186/ChickMate/blob/6ad7bbb98988e0bac8611dbb6643a561459eb1c0/images/chickmate%20image/ChickMate%20by%20Skillovate.jpeg)

# 🐥 ChickMate - AI-Based Chick Counting Software

**ChickMate** is a real-time, AI-powered chick counting software prototype designed for poultry farms. It automates the process of counting chicks in trays using a custom-trained YOLOv8 model with OpenCV and a webcam, significantly reducing manual labor, errors, and time.

> 🔬 Developed as a part of an engineering hackathon project with real-world impact in mind.

---

## 🚀 Key Features

- 🎯 Real-time chick detection and counting
- 📸 Webcam integration using OpenCV
- 🧠 YOLOv8-based custom object detection (trained on chick dataset)
- 📊 Live chick count display on dashboard
- 🧑‍🌾 Built for poultry farm workers & administrators
- 📁 Lightweight and runs on local systems
- 🧱 Built with Flask, SQLite, OpenCV, and Ultralytics YOLOv8

---

## 📈 Real-World Problem

In large poultry farms, counting chicks manually is:
- ❌ Time-consuming
- ❌ Error-prone
- ❌ Labor-intensive

**Stakeholder: Nagraj Shetty Amburi (Poultry Operator)**  
He highlighted the need for a low-cost, fast, and accurate chick counting system.

---

## ✅ Solution: ChickMate

ChickMate solves this problem by:
- Detecting and counting chicks in a tray using computer vision
- Displaying the count instantly on a user-friendly dashboard
- Storing count logs for record-keeping

> 🐤 Accuracy tested with real-world footage using a custom chick dataset

---

## 🛠️ Tech Stack

| Component       | Tech Used                 |
|----------------|---------------------------|
| Language        | Python                    |
| Framework       | Flask                     |
| Object Detection| YOLOv8 (Ultralytics)      |
| Image Processing| OpenCV                    |
| Database        | SQLite                    |
| Frontend        | HTML, CSS (Jinja2 templating) |
| Hardware        | Webcam                    |

---

## 💻 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/Yashvin186/ChickMate.git
cd ChickMate

2. Create Virtual Environment (optional)

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the App

python app.py

Then open http://127.0.0.1:5000/ in your browser.


---

📂 Project Structure

ChickMate/
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── video_feed.html
├── static/
├── users.db
├── best.pt  # (Add to .gitignore)
├── README.md
└── requirements.txt


---

🤖 AI Model

YOLOv8 trained on a custom chick dataset using Roboflow and Ultralytics

Class 0: "Chick"

Confidence threshold: 0.6



---

📌 Known Issues

Model file .pt should not be uploaded to GitHub

Webcam access may fail on some devices

Database (users.db) will reset if deleted



---

🤝 Team & Credit

Built by a 6-member engineering team for a hackathon

Stakeholder: Nagraj Shetty Amburi (Field Expert)

Thanks to Ultralytics, OpenCV, and Flask for tools



---

📜 License

This project is for educational and prototyping purposes. For commercial use, contact the developers.


---

⭐ Support Us

If you found this useful, please ⭐ the repo and share it with others.

---

### ➕ Optional Files

Create a simple `.gitignore` file like this:

```gitignore
*.pyc
__pycache__/
*.db
*.pt
.env


---

✅ Instructions to use:

1. Save the above content as a file named requirements.txt in your project root.
2. Install all dependencies at once using:

pip install -r requirements.txt

