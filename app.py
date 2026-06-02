from flask import Flask, render_template, session, jsonify, redirect, request, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = "yourKey"

# ---------------- MONGO DB ----------------
client = MongoClient("mongodb+srv://username:password@cluster.mongodb.net/")
db = client["smart_attendance"]

student_col = db["students"]
timetable_col = db["timetable"]
attendance_col = db["attendance"]
teacher_col = db["teacher"]

# ---------------- INDEX ----------------
@app.route('/')
def index():
    return render_template("index.html")




# ---------------- STUDENT LOGIN ----------------
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        reg = request.form.get('reg')
        password = request.form.get('password')

        student = student_col.find_one({"reg": reg})

        if student:
            if password == student.get("dob"):
                session["reg"] = reg
                return redirect(url_for('dashboard'))
            else:
                return "Wrong Password (Use DOB)"
        else:
            return "Invalid Register Number"

    return render_template("student_login.html")


# ---------------- STUDENT DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if "reg" not in session:
        return redirect(url_for('student_login'))
    return render_template("student_dashboard.html")




# ---------------- STUDENT API ----------------
@app.route('/api/student')
def get_student():
    reg = session.get("reg")

    data = student_col.find_one({"reg": reg}, {"_id": 0})
    return jsonify(data if data else {})


# ---------------- STUDENT TIMETABLE ----------------
@app.route('/api/timetable')
def get_timetable():
    reg = session.get("reg")

    student = student_col.find_one({"reg": reg})
    year = student.get("year")

    data = list(timetable_col.find({"year": year}, {"_id": 0}))
    return jsonify(data)


# ---------------- STUDENT ATTENDANCE ----------------
@app.route('/api/total')
def get_attendance():
    reg = session.get("reg")

    student = student_col.find_one({"reg": reg})
    student_id = str(student.get("reg"))
    year = student.get("year")

    records = list(attendance_col.find({"year": year}))

    result = {}

    for r in records:
        sub = r["sub"]

        if sub not in result:
            result[sub] = {"total": 0, "present": 0}

        result[sub]["total"] += 1

        present_list = [str(x) for x in r.get("present", [])]

        if student_id in present_list:
            result[sub]["present"] += 1

    final = []
    for sub, val in result.items():
        final.append({
            "subject": sub,
            "present": val["present"],
            "total": val["total"]
        })

    return jsonify(final)

#-----------------student dashboard staff details----------------
@app.route('/api/staff')
def get_staff():
    reg = session.get("reg")

    student = student_col.find_one({"reg": reg})
    year = student.get("year")

    timetable = list(timetable_col.find({"year": year}))

    result = []

    for t in timetable:
        teacher = teacher_col.find_one({"tid": t["staff"]})

        result.append({
            "subject": t["sub"],
            "staff": teacher["teacherName"] if teacher else "Unknown"
        })

    return jsonify(result)

# ---------------- TEACHER LOGIN ----------------
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        teacher = teacher_col.find_one({"email": email})

        if teacher:
            if password == teacher.get("password"):
                session["teacher_email"] = email
                session["tid"] = teacher["tid"]
                return redirect(url_for('teacher_dashboard'))
            else:
                return "Wrong Password"
        else:
            return "Invalid Email"

    return render_template("teacher_login.html")


#----------------- TEACHER DASHBOARD ----------------
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if "teacher_email" not in session:
        return redirect(url_for('teacher_login'))
    return render_template("teacher_dashboard.html")


# ---------------- TEACHER INFO ----------------
@app.route('/api/teacher')
def get_teacher():
    email = session.get("teacher_email")
    teacher = teacher_col.find_one({"email": email}, {"_id": 0})
    return jsonify(teacher)


# ---------------- TEACHER TIMETABLE ----------------
@app.route('/api/teacher/timetable')
def teacher_timetable():
    tid = session.get("tid")

    data = list(timetable_col.find({"staff": tid}, {"_id": 0}))
    return jsonify(data)


# ---------------- TEACHER ATTENDANCE SUMMARY ----------------
@app.route('/api/teacher/attendance')
def teacher_attendance():
    tid = session.get("tid")

    timetable = list(timetable_col.find({"staff": tid}))
    subjects = [t["sub"] for t in timetable]

    result = []

    for sub in subjects:
        records = list(attendance_col.find({"sub": sub}))

        total = len(records)

        result.append({
            "subject": sub,
            "total_classes": total
        })

    return jsonify(result)

#--------------update attendance----------------
@app.route('/api/update_attendance', methods=['POST'])
def update_attendance():

    data = request.json

    sub = data['sub']
    year = data['year']
    present = data['present']

    today = datetime.now().strftime("%d/%m/%Y")

    attendance_col.update_one(
        {"date": today, "sub": sub, "year": year},
        {"$set": {"present": present}},
        upsert=True
    )

    return jsonify({"msg": "Attendance Updated"})

#-----------------today attendance --------
@app.route('/api/get_attendance')
def get_attendance_by_date():

    sub = request.args.get("sub")
    year = request.args.get("year")
    date = request.args.get("date")

    students = list(student_col.find({"year": year}))

    record = attendance_col.find_one({
        "date": date,
        "sub": sub,
        "year": year
    })

    present = record.get("present", []) if record else []

    return jsonify({
        "students": students,
        "present": present
    })
#-------------------save attendance----------------
@app.route('/api/save_attendance', methods=['POST'])
def save_attendance():

    data = request.json

    sub = data.get("sub")
    year = data.get("year")
    date = data.get("date")
    present = data.get("present")

    attendance_col.update_one(
        {"date": date, "sub": sub, "year": year},
        {"$set": {"present": present}},
        upsert=True
    )

    return jsonify({"msg": "Attendance Updated"})

#-----------------today attendance details----------------
@app.route('/api/today_attendance')
def today_attendance():

    sub = request.args.get("sub")
    year = request.args.get("year")

    today = datetime.now().strftime("%d/%m/%Y")

    students = list(student_col.find({"year": year}))
    record = attendance_col.find_one({
        "date": today,
        "sub": sub,
        "year": year
    })

    present_regs = record.get("present", []) if record else []

    present = []
    absent = []

    for s in students:
        if str(s["reg"]) in present_regs:
            present.append(s["name"])
        else:
            absent.append(s["name"])

    return jsonify({
        "subject": sub,
        "present": present,
        "absent": absent
    })



#--------------full attendance details----------------
@app.route('/api/full_attendance')
def full_attendance():

    sub = request.args.get("sub")
    year = request.args.get("year")

    students = list(student_col.find({"year": year}))
    records = list(attendance_col.find({"sub": sub, "year": year}))

    dates = sorted(list(set(r["date"] for r in records)))

    table = []

    for s in students:
        row = {"name": s["name"], "data": []}

        for d in dates:
            rec = next((r for r in records if r["date"] == d), None)

            if rec and str(s["reg"]) in rec.get("present", []):
                row["data"].append("P")
            else:
                row["data"].append("A")

        table.append(row)

    return jsonify({
        "dates": dates,
        "table": table
    })

# ---------------- SEARCH ----------------
@app.route('/api/teacher/search')
def teacher_search():

    q = request.args.get("q")

    # -------- REG SEARCH --------
    if q.isdigit():

        reg = q

        student = student_col.find_one({"reg": reg})
        if not student:
            return jsonify({"msg": "No student"})

        year = student["year"]
        records = list(attendance_col.find({"year": year}))

        result = {}

        for r in records:
            sub = r["sub"]

            if sub not in result:
                result[sub] = {"total":0,"present":0}

            result[sub]["total"] +=1

            if reg in [str(x) for x in r.get("present",[])]:
                result[sub]["present"] +=1

        final=[]
        for sub,v in result.items():
            percent = (v["present"]/v["total"])*100 if v["total"] else 0

            final.append({
                "subject":sub,
                "present":v["present"],
                "total":v["total"],
                "percent":round(percent,2)
            })

        return jsonify({"type":"reg","data":final})

    # -------- DATE SEARCH --------
    if "/" in q:

        records = list(attendance_col.find({"date": q}))

        if not records:
            return jsonify({"msg":"No data"})

        r = records[0]

        students = list(student_col.find({"year": r["year"]}))

        present = r.get("present",[])
        absent = []

        for s in students:
            if str(s["reg"]) not in present:
                absent.append(s["name"])

        return jsonify({
            "type":"date",
            "subject": r["sub"],
            "present": present,
            "absent": absent
        })

    # -------- SUBJECT SEARCH (NEW) --------
    else:

        records = list(attendance_col.find({
            "sub": {"$regex": f"^{q}$", "$options": "i"}
        }))

        if not records:
            return jsonify({"msg": "No subject found"})

        result = []

        for r in records:
            result.append({
                "date": r["date"],
                "present": r.get("present", [])
            })

        return jsonify({
            "type": "subject",
            "data": result
        })

#----------------image upload----------------
import cv2

@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():

    file = request.files['image']
    sub = request.form.get("sub")
    year = request.form.get("year")
    date = request.form.get("date")

    path = "static/upload.jpg"
    file.save(path)

    input_img = cv2.imread(path, 0)

    students = list(student_col.find({"year": year}))

    matched = []   # ✅ store all matched students

    for s in students:

        db_img = cv2.imread("static/" + s["image"], 0)

        db_img = cv2.resize(db_img, (200, 200))
        input_img_resized = cv2.resize(input_img, (200, 200))

        diff = cv2.absdiff(db_img, input_img_resized)

        if diff.mean() < 120:

            reg = str(s["reg"])
            matched.append(reg)

            attendance_col.update_one(
                {"date": date, "sub": sub, "year": year},
                {"$addToSet": {"present": reg}},
                upsert=True
            )

    # ✅ AFTER LOOP
    if matched:
        return jsonify({"msg": f"Marked: {', '.join(matched)}"})
    else:
        return jsonify({"msg": "No match"})



#-------------password change----------------

@app.route('/api/change_password', methods=['POST'])
def change_password():

    data = request.json
    new_pass = data.get("password")

    email = session.get("teacher_email")

    teacher_col.update_one(
        {"email": email},
        {"$set": {"password": new_pass}}
    )

    return jsonify({"msg": "Password Updated"})

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)