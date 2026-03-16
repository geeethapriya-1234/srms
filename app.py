
import datetime
from flask import Flask, render_template, request, redirect, session, send_file
import mysql.connector
from fpdf import FPDF
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = "srmskey"

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_PERMANENT'] = False


try:
    from database import db, cursor
except ImportError:
    # Fallback if database module is not available
    import mysql.connector
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='srms'
    )
    cursor = db.cursor()

@app.route('/check_session')
def check_session():
    return f"SESSION DATA = {session}"

# ---------------- MAIN LOGIN (Admin/Teacher) ----------------
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['user'] = username
            session['role'] = user[3]  # role column
            
            if user[3] == 'admin':
                return redirect('/admin')
            elif user[3] == 'teacher':
                return redirect('/teacher')
                
    return render_template('login.html')


# ---------------- TEACHER DASHBOARD ----------------
@app.route('/teacher', methods=['GET','POST'])
def teacher_dashboard():

    if session.get('role') != 'teacher':
        return redirect('/')

    # ---------- SAVE MARKS (POST) ----------
    if request.method == 'POST':

        regno = request.form['regno']
        semester = request.form['semester']

        marks_list = [
            ("S1", request.form['s1']),
            ("S2", request.form['s2']),
            ("S3", request.form['s3']),
            ("S4", request.form['s4']),
            ("S5", request.form['s5'])
        ]

        for subject, mark in marks_list:

            total = int(mark)

            # percentage
            percentage = total

            # grade point calculation
            if total >= 90:
                grade_point = 10
            elif total >= 80:
                grade_point = 9
            elif total >= 70:
                grade_point = 8
            elif total >= 60:
                grade_point = 7
            elif total >= 50:
                grade_point = 6
            else:
                grade_point = 5

            cursor.execute("""
                INSERT INTO marks(regno, subject, total, grade_point, percentage, semester)
                VALUES(%s,%s,%s,%s,%s,%s)
            """, (regno, subject, total, grade_point, percentage, semester))

        db.commit()

        

    # ---------- GET TEACHER INFO ----------
    cursor.execute("""
        SELECT teachers.name, departments.dept_name
        FROM teachers
        JOIN departments ON teachers.department = departments.id
        WHERE teachers.name=%s
    """, (session['user'],))

    teacher = cursor.fetchone()

    return render_template("teacher.html", teacher=teacher)






#---------STUDENT LOGIN------        
@app.route('/student_login', methods=['GET','POST'])
def student_login():

    if request.method == 'POST':

        regno = request.form['regno']
        password = request.form['password']

        cursor.execute(
            "SELECT regno, name FROM students WHERE regno=%s AND password=%s",
            (regno, password)
        )

        student = cursor.fetchone()

        if student:
            session['regno'] = student[0]          # ✔ correct key
            session['student_name'] = student[1]
            return redirect('/student_dashboard')
        else:
            return "Invalid Register Number or Password"

    return render_template('student_login.html')



# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect('/')
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("admin.html", students=students)

# ---------------- ADD DEPARTMENT (FIXED) ----------------
@app.route('/add_department', methods=['GET','POST'])
def add_department():
    if session.get('role') != 'admin':
        return redirect('/')
    if request.method == 'POST':
        dept = request.form['dept']
        cursor.execute("INSERT INTO departments(dept_name) VALUES(%s)", (dept,))
        db.commit()
        return redirect('/admin')  # ✅ FIXED
    return render_template('add_department.html')


#---------------- ADD SEMESTER (FIXED) ----------------
@app.route('/add_semester', methods=['GET','POST'])
def add_semester():
    if session.get('role') != 'admin':
        return redirect('/')
    if request.method == 'POST':
        sem = request.form['semester']
        cursor.execute("INSERT INTO semesters(sem_name) VALUES(%s)", (sem,))
        db.commit()
        return redirect('/admin')  # ✅ FIXED
    return render_template('add_semester.html')


#-----------------ADD TEACHER-----------------
@app.route('/add_teacher', methods=['GET','POST'])
def add_teacher():
    if session.get('role') != 'admin':
        return redirect('/')
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        cursor.execute("INSERT INTO teachers(name,department) VALUES(%s,%s)", (name, dept))
        db.commit()
        return redirect('/admin')  # ✅ FIXED
    return render_template('add_teacher.html', departments=departments)

 #---------------- ADD STUDENT (FIXED) ----------------
@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if session.get('role') != 'admin':
        return redirect('/')
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    cursor.execute("SELECT * FROM semesters")
    semesters = cursor.fetchall()
    if request.method == 'POST':
        regno = request.form['regno']
        name = request.form['name']
        dept = request.form['department']
        sem = request.form['semester']
        password = request.form.get('password')
        cursor.execute("INSERT INTO students(regno,name,department,semester,password) VALUES(%s,%s,%s,%s,%s)",
                      (regno, name, dept, sem, password))
        db.commit()
        return redirect('/admin')  # ✅ FIXED
    return render_template('add_student.html', departments=departments, semesters=semesters)

# ---------------- STUDENT DASHBOARD ----------------


@app.route('/student_dashboard')
def student_dashboard():
    

    if 'regno' not in session:
        return redirect('/student_login')

    regno = session['regno']
    name = session['student_name']

    # get all semesters
    cursor.execute("SELECT DISTINCT semester FROM marks WHERE regno=%s ORDER BY semester", (regno,))
    semesters = cursor.fetchall()

    all_results = {}
    overall_points = 0
    overall_subjects = 0

    for sem in semesters:
        sem_no = sem[0]

        cursor.execute("""
            SELECT subject, total, grade_point, percentage
            FROM marks
            WHERE regno=%s AND semester=%s
        """, (regno, sem_no))

        results = cursor.fetchall()

        fixed_results = []
        sem_points = 0
        sem_subjects = 0

        for r in results:
            subject = r[0]
            total = int(r[1])           # 🔥 FIX
            grade = int(r[2])           # 🔥 FIX
            percent = float(r[3])       # 🔥 FIX

            fixed_results.append((subject, total, grade, percent))

            sem_points += grade
            sem_subjects += 1

        sem_cgpa = round(sem_points / sem_subjects, 2) if sem_subjects > 0 else 0

        overall_points += sem_points
        overall_subjects += sem_subjects

        all_results[sem_no] = {
            "subjects": fixed_results,
            "cgpa": sem_cgpa
        }

    overall_cgpa = round(overall_points / overall_subjects, 2) if overall_subjects > 0 else 0

    return render_template(
        "student_dashboard.html",
        student_name=name,
        results=all_results,
        overall_cgpa=overall_cgpa
    )








#------PDF------
@app.route('/download_pdf')
def download_pdf():

    if 'regno' not in session:
        return redirect('/student_login')

    regno = session['regno']
    name = session['student_name']

    # find all semesters
    cursor.execute("SELECT DISTINCT semester FROM marks WHERE regno=%s ORDER BY semester", (regno,))
    semesters = cursor.fetchall()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ---------- COLLEGE TITLE ----------
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "KONGU VELALAR POLYTECHNIC COLLEGE", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "STUDENT RESULT REPORT", ln=True, align="C")
    pdf.ln(5)

    # ---------- STUDENT DETAILS ----------
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Register No : {regno}", ln=True)
    pdf.cell(0, 8, f"Name        : {name}", ln=True)
    pdf.ln(5)

    # overall cgpa tracking
    overall_total_cgpa = 0
    semester_count = 0

    # ---------- SEMESTER WISE ----------
    for sem in semesters:
        sem_no = sem[0]

        cursor.execute("""
            SELECT subject, total, grade_point, percentage
            FROM marks
            WHERE regno=%s AND semester=%s
        """, (regno, sem_no))

        results = cursor.fetchall()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Semester {sem_no}", ln=True)

        # table header
        pdf.set_font("Arial", "B", 10)
        pdf.cell(60, 8, "Subject", 1)
        pdf.cell(30, 8, "Marks", 1)
        pdf.cell(40, 8, "Grade Point", 1)
        pdf.cell(40, 8, "Percentage", 1)
        pdf.ln()

        # semester calculation
        total_gp = 0
        subject_count = 0

        pdf.set_font("Arial", "", 10)

        for r in results:
            pdf.cell(60, 8, r[0], 1)
            pdf.cell(30, 8, str(r[1]), 1)
            pdf.cell(40, 8, str(r[2]), 1)
            pdf.cell(40, 8, str(r[3])+"%", 1)
            pdf.ln()

            # CGPA calculation (CORRECT)
            gp = float(r[2]) if r[2] else 0
            total_gp += gp
            subject_count += 1

        # semester cgpa
        if subject_count > 0:
            sem_cgpa = round(total_gp / subject_count, 2)
        else:
            sem_cgpa = 0

        pdf.ln(2)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, f"Semester CGPA : {sem_cgpa}", ln=True)
        pdf.ln(5)

        # add to overall cgpa
        overall_total_cgpa += sem_cgpa
        semester_count += 1

    # ---------- OVERALL CGPA ----------
    if semester_count > 0:
        overall_cgpa = round(overall_total_cgpa / semester_count, 2)
    else:
        overall_cgpa = 0

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"OVERALL CGPA : {overall_cgpa}", ln=True)

    filename = f"{regno}_result.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/test')
def test():
    if 'regno' in session:
        return "LOGIN WORKS. Logged in as " + session['regno']
    else:
        return "SESSION NOT SAVED"
