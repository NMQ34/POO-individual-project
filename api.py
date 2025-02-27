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
        save_data({"students": [], "graduate_students": [], "courses": [], "enrollments": []}) 

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"students": [], "graduate_students": [], "courses": [], "enrollments": []} 

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

db_data = load_data()
students = db_data.get("students", [])
courses = db_data.get("courses", [])

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
    db_data = load_data()

    student_data = next((s for s in db_data["students"] if s['id'] == id), None)
    if not student_data:
        return jsonify({'error': 'Student not found'}), 404

    student_id = student_data['id']

    # Récupération des notes de tous les cours inscrits
    student_enrollments = [e for e in db_data["enrollments"] if e['student_id'] == student_id]

    course_grades = {}
    total_notes = []
    total_credits = 0

    for enrollment in student_enrollments:
        course_code = enrollment['course_code']
        grades = enrollment.get('grades', [])

        if grades:
            moyenne = sum(grades) / len(grades)
            course = next((c for c in db_data["courses"] if c['courseCode'] == course_code), None)

            if course:
                credits = course['creditHours']
                total_credits += moyenne * credits
                course_grades[course_code] = moyenne
                total_notes.extend(grades)

    moyenne_generale = sum(total_notes) / len(total_notes) if total_notes else "N/A"
    
    passes = total_credits >= 200

    return jsonify({
        'id': student_data['id'],
        'nom': student_data['nom'],
        'prenom': student_data['prenom'],
        'age': student_data['age'],
        'genre': student_data['genre'],
        'classe': student_data['classe'],
        'formation': student_data['formation'],
        'grades': moyenne_generale,
        'moyennes_par_cours': course_grades,
        'total_credits': total_credits,
        'passe_annee': passes
    }), 200

@app.route('/graduate_students', methods=['POST'])
def add_graduate_student():
    data = request.get_json()

    if not all(field in data for field in ['nom', 'prenom', 'age', 'diplome']):
        return jsonify({'error': 'Missing required fields'}), 400

    graduate_student = GraduateStudent(
        nom=data['nom'],
        prenom=data['prenom'],
        age=data['age'],
        diplome=data['diplome']
    )

    db_data = load_data()
    new_graduate = {
        'id': graduate_student._graduateID,
        'nom': graduate_student.nom,
        'prenom': graduate_student.prenom,
        'age': graduate_student.age,
        'diplome': graduate_student.diplome
    }

    db_data["graduate_students"].append(new_graduate)
    save_data(db_data)

    return jsonify(new_graduate), 201

@app.route('/graduate_students', methods=['GET'])
def get_all_graduate_students():
    db_data = load_data()
    graduate_students = db_data.get("graduate_students", [])

    if not graduate_students:
        return jsonify({'error': 'No graduate students found'}), 404

    return jsonify(graduate_students), 200

@app.route('/graduate_students/<string:id>', methods=['GET'])
def get_graduate_student(id):
    db_data = load_data()

    graduate_student_data = next((s for s in db_data["graduate_students"] if s['id'] == id), None)

    if graduate_student_data:
        graduate_student = GraduateStudent(
            nom=graduate_student_data['nom'],
            prenom=graduate_student_data['prenom'],
            age=graduate_student_data['age'],
            diplome=graduate_student_data['diplome']
        )

        return jsonify({
            'id': graduate_student._graduateID,
            'nom': graduate_student.nom,
            'prenom': graduate_student.prenom,
            'age': graduate_student.age,
            'diplome': graduate_student.diplome
        }), 200
    else:
        return jsonify({'error': 'Graduate student not found'}), 404

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
    course_code = data['course_code']

    db_data = load_data()

    student = next((s for s in db_data["students"] if s['id'] == student_id), None)
    course = next((c for c in db_data["courses"] if c['courseCode'] == course_code), None)

    if student and course:
        existing_enrollment = next(
            (e for e in db_data.get("enrollments", []) if e['student_id'] == student_id and e['course_code'] == course_code),
            None
        )
        if existing_enrollment:
            return jsonify({'error': 'Student is already enrolled in this course'}), 400

        db_data["enrollments"].append({
            'student_id': student_id,  
            'course_code': course_code,
            'grades': [] 
        })

        save_data(db_data)
        return jsonify({"message": "Student enrolled successfully!"}), 201

    return jsonify({"error": "Student or Course not found"}), 404

@app.route('/enrollments/grades', methods=['POST'])
def add_grade():
    data = request.get_json()
    student_id = data['student_id']
    course_code = data['course_code']
    grade = data['grade']

    if not (0 <= grade <= 20):
        return jsonify({"error": "La note doit être entre 0 et 20"}), 400

    db_data = load_data()

    enrollment = next((e for e in db_data["enrollments"] if e['student_id'] == student_id and e['course_code'] == course_code), None)

    if enrollment:
        enrollment['grades'].append(grade)
        save_data(db_data)
        return jsonify({"message": "Note ajoutée avec succès"}), 200

    return jsonify({"error": "Inscription non trouvée"}), 404

if __name__ == '__main__':
    app.run(debug=True)