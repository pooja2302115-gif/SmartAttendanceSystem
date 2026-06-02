# 🎓 Smart Attendance Management System

A web-based Smart Attendance Management System that helps teachers manage student attendance efficiently. The system provides separate dashboards for students and teachers, attendance tracking, timetable management, attendance reports, and image-based attendance marking using OpenCV.

## 🚀 Features

### 👨‍🎓 Student Module
- Student Login
- View Personal Profile
- View Timetable
- View Attendance Percentage
- View Subject-wise Attendance
- View Staff Details

### 👨‍🏫 Teacher Module
- Teacher Login
- Teacher Dashboard
- Manage Attendance
- View Timetable
- Search Student Attendance
- Search Attendance by Subject
- Search Attendance by Date
- Generate Attendance Reports
- Change Password

### 📸 Smart Attendance
- Upload student image
- Face/Image matching using OpenCV
- Automatic attendance marking
- Stores attendance records in MongoDB

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- MongoDB Atlas

### Computer Vision
- OpenCV

## 📂 Project Structure

```
Project/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── student_login.html
│   ├── student_dashboard.html
│   ├── teacher_login.html
│   └── teacher_dashboard.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── student_dashboard.js
│   ├── teacher_dashboard.js
│   ├── image/
│   └── upload.jpg
│
└── README.md
```

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask pymongo opencv-python
```

### 5. Configure MongoDB

Update the MongoDB connection string inside `app.py`:

```python
client = MongoClient("YOUR_MONGODB_CONNECTION_STRING")
```

### 6. Run Application

```bash
python app.py
```

### 7. Open Browser

```text
http://127.0.0.1:5000
```

## 📊 Attendance Functionalities

- Daily attendance tracking
- Subject-wise attendance
- Student attendance percentage calculation
- Present/Absent reports
- Attendance history by date
- Full attendance records

## 🔒 Authentication

### Student Login
- Register Number
- DOB as Password

### Teacher Login
- Email
- Password

## 📸 Image-Based Attendance Workflow

1. Teacher uploads student image.
2. OpenCV compares uploaded image with stored images.
3. Matching student is identified.
4. Attendance is automatically marked.
5. Record is saved in MongoDB.

## 🎯 Future Enhancements

- Real Face Recognition using Deep Learning
- QR Code Attendance
- Attendance Analytics Dashboard
- Email Notifications
- Mobile Application
- Excel/PDF Report Export
- Role-Based Access Control

## 👩‍💻 Author

**Pooja M**

Computer Science Engineering Student

## 📄 License

This project is developed for educational and academic purposes.