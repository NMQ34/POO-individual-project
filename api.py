from flask import Flask, jsonify, request
from student import Student, Course, students, courses

app = Flask(__name__)

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    student = Student(data['nom'], data['prenom'], data['age'], data['genre'], data['classe'], data['formation'])
    students[student._studentID] = student
    return jsonify({"id": student._studentID}), 201

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    course = Course(data['courseName'], data['creditHours'])
    courses[course.courseCode] = course
    return jsonify({"courseCode": course.courseCode}), 201

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.json
    student = students.get(data['studentID'])
    course = courses.get(data['courseCode'])
    if student and course:
        course.enrollStudent(student)
        return jsonify({"message": "Student enrolled successfully"}), 200
    return jsonify({"error": "Student or Course not found"}), 404

@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify([{ 
        "id": s._studentID, 
        "nom": s.nom, 
        "prenom": s.prenom, 
        "age": s.age, 
        "genre": s.genre, 
        "classe": s.classe, 
        "formation": s.formation 
    } for s in students.values()])

@app.route('/courses', methods=['GET'])
def get_all_courses():
    return jsonify([{ 
        "courseCode": c.courseCode, 
        "courseName": c.courseName, 
        "creditHours": c.creditHours, 
        "students": [s._studentID for s in c.students] 
    } for c in courses.values()])

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    student = students.get(student_id)
    if student:
        return jsonify({
            "nom": student.nom,
            "prenom": student.prenom,
            "age": student.age,
            "genre": student.genre,
            "classe": student.classe,
            "formation": student.formation,
            "average_grade": student.getAverageGrade()
        })
    return jsonify({"error": "Student not found"}), 404

@app.route('/courses/<course_code>', methods=['GET'])
def get_course(course_code):
    course = courses.get(course_code)
    if course:
        return jsonify({
            "courseName": course.courseName,
            "creditHours": course.creditHours,
            "students": [s._studentID for s in course.students]
        })
    return jsonify({"error": "Course not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)