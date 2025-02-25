from flask import Flask, request, jsonify
from student import Student, Course, Enrollment, GraduateStudent, Person
from flask_cors import CORS
import json
import os
app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data({"students": [], "graduate_students": [], "courses": []})

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"students": [], "graduate_students": [], "courses": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

db_data = load_data()
students = db_data.get("students", [])
courses = db_data.get("courses", [])
students = load_data().get("students", []) 

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    student = Student(
        nom=data['nom'],
        prenom=data['prenom'],
        age=data['age'],
        genre=data['genre'],
        classe=data['classe'],
        formation=data['formation']
    )

    db_data = load_data()

    new_student = {
        'id': student._studentID,
        'nom': student.nom,
        'prenom': student.prenom,
        'age': student.age,
        'genre': student.genre,
        'classe': student.classe,
        'formation': student.formation,
        'grades': student.grades
    }

    db_data["students"].append(new_student)

    save_data(db_data)

    return jsonify(new_student), 201
    
@app.route('/students', methods=['GET'])
def get_all_students():
    db_data = load_data()  
    students = db_data.get("students", []) 

    if not students:
        return jsonify({'error': 'No students found'}), 404

    return jsonify(students), 200

@app.route('/students/<string:id>', methods=['GET'])
def get_student(id):
    student = next((s for s in students if s._studentID == id), None)
    if student:
        return jsonify({
            'id': student._studentID,
            'nom': student.nom,
            'prenom': student.prenom,
            'age': student.age,
            'genre': student.genre,
            'classe': student.classe,
            'formation': student.formation,
            'grades': student.grades
        })
    return jsonify({'error': 'Student not found'}), 404

@app.route('/graduate_students', methods=['POST'])
def add_graduate_student():
    data = request.get_json()

    graduate_student = GraduateStudent(
        nom=data['nom'],
        prenom=data['prenom'],
        age=data['age'],
        diplome=data['diplome']
    )

    students.append(graduate_student)

    return jsonify({
        'id': graduate_student._graduateID,
        'nom': graduate_student.nom,
        'prenom': graduate_student.prenom,
        'age': graduate_student.age,
        'diplome': graduate_student.diplome
    }), 201

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()

    course = Course(
        courseName=data['courseName'],
        creditHours=data['creditHours']
    )

    db_data = load_data()
    new_course = {
        'courseCode': course.courseCode,
        'courseName': course.courseName,
        'creditHours': course.creditHours
    }
    
    db_data["courses"].append(new_course)
    save_data(db_data)

    return jsonify(new_course), 201

@app.route('/courses', methods=['GET'])
def get_all_courses():
    db_data = load_data()
    courses = db_data.get("courses", [])

    if not courses:
        return jsonify({'error': 'No courses found'}), 404

    return jsonify(courses), 200

@app.route('/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    db_data = load_data()
    course = next((c for c in db_data["courses"] if c['courseCode'] == course_code), None)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']

    student = next((s for s in students if s._studentID == student_id), None)
    course = next((c for c in courses if isinstance(c, Course) and c.courseCode == course_id), None)

    if student and course:
        course.enrollStudent(student)
        return jsonify({"message": "Student enrolled successfully!"}), 201
    return jsonify({"error": "Student or Course not found"}), 404

@app.route('/students/<string:id>/grades', methods=['POST'])
def add_grade(id):
    data = request.get_json()
    course_code = data['courseCode']
    grade = data['grade']

    student = next((s for s in students if s._studentID == id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student.addGrade(course_code, grade)

    return jsonify({"message": "Grade added successfully!"}), 200

@app.route('/students/<string:id>/average', methods=['GET'])
def get_student_average(id):
    student = next((s for s in students if s._studentID == id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify({
        'id': student._studentID,
        'nom': student.nom,
        'prenom': student.prenom,
        'average': student.getAverageGrade()
    }), 200

@app.route('/students/<string:id>/pass', methods=['GET'])
def check_student_pass(id):
    student = next((s for s in students if s._studentID == id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    result = student.hasPassed(courses)
    return jsonify({
        'id': student._studentID,
        'nom': student.nom,
        'prenom': student.prenom,
        'status': "Passed" if result else "Failed"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)