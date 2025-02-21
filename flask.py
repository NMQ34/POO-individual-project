from flask import Flask, request, jsonify

app = Flask(__name__)

students = []
courses = []
enrollments = []

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(**data)
    students.append(student)
    return jsonify({"message": "Student created", "id": student._studentID}), 201

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    course = Course(**data)
    courses.append(course)
    return jsonify({"message": "Course created", "code": course.courseCode}), 201

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data.get('studentID')
    course_code = data.get('courseCode')

    student = next((s for s in students if s._studentID == student_id), None)
    course = next((c for c in courses if c.courseCode == course_code), None)

    if student and course:
        enrollment = Enrollment(student, course)
        enrollment.register()
        enrollments.append(enrollment)
        return jsonify({"message": "Enrollment successful"}), 201
    return jsonify({"message": "Student or Course not found"}), 404

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s._studentID == student_id), None)
    if student:
        return jsonify({
            "name": student.nom,
            "age": student.age,
            "grades": student.grades,
            "average": student.getAverageGrade()
        }), 200
    return jsonify({"message": "Student not found"}), 404

@app.route('/courses/<course_code>', methods=['GET'])
def get_course(course_code):
    course = next((c for c in courses if c.courseCode == course_code), None)
    if course:
        enrolled_students = course.getEnrolledStudents()
        return jsonify({"courseName": course.courseName, "students": enrolled_students}), 200
    return jsonify({"message": "Course not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)