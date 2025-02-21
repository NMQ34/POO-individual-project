from flask import Flask, request, jsonify
from student import Student, Course, Enrollment, GraduateStudent, Person

app = Flask(__name__)

students = []  
courses = []  

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
    
    students.append(student)
    
    return jsonify({
        'id': student._studentID,
        'nom': student.nom,
        'prenom': student.prenom,
        'age': student.age,
        'genre': student.genre,
        'classe': student.classe,
        'formation': student.formation
    }), 201

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

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    
    course = {
        'id': len(courses) + 1,
        'courseName': data['courseName'],
        'creditHours': data['creditHours']
    }
    courses.append(course)
    
    return jsonify(course), 201

@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = next((c for c in courses if c['id'] == id), None)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']
    
    student = next((s for s in students if s._studentID == student_id), None)
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if student and course:
        course_obj = Course(course['courseName'], course['creditHours'])
        course_obj.enrollStudent(student)
        return jsonify({"message": "Student enrolled successfully!"}), 201
    return jsonify({"error": "Student or Course not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
