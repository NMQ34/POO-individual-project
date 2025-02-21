from flask import Flask, request, jsonify

app = Flask(__name__)

students = []
courses = []

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    student = {
        'id': len(students) + 1,
        'nom': data['nom'],
        'prenom': data['prenom'],
        'age': data['age'],
        'genre': data['genre'],
        'classe': data['classe'],
        'formation': data['formation']
    }
    students.append(student)
    return jsonify(student), 201

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = next((s for s in students if s['id'] == id), None)
    if student:
        return jsonify(student)
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

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses), 200

@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = next((c for c in courses if c['id'] == id), None)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
