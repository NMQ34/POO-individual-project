from abc import ABC, abstractmethod
import random
import string


class Person(ABC):
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

    @abstractmethod
    def afficher_informations(self):
        pass


class GraduateStudent(Person):
    def __init__(self, nom, prenom, age, diplome):
        super().__init__(nom, prenom, age)
        self._graduateID = self.generer_ID()
        self.diplome = diplome

    @staticmethod
    def generer_ID():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=23))

    def afficher_informations(self):
        print(f"{self.nom} {self.prenom}, {self.age} ans")
        print(f"ID : {self._graduateID}")
        print(f"Diplôme obtenu : {self.diplome}")


class Student(Person):
    def __init__(self, nom, prenom, age, genre, classe, formation):
        super().__init__(nom, prenom, age)
        self._studentID = self.generer_ID()
        self.genre = genre
        self.classe = classe
        self.formation = formation
        self.grades = {}

    @staticmethod
    def generer_ID():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=23))

    def addGrade(self, courseCode, grade):
        if 0 <= grade <= 20:
            if courseCode not in self.grades:
                self.grades[courseCode] = []
            self.grades[courseCode].append(grade)

    def getAverageGrade(self):
        if not self.grades:
            return "N/A"
        total_notes = [note for notes in self.grades.values() for note in notes]
        return sum(total_notes) / len(total_notes)

    def afficher_informations(self, courses=None):
        if courses is None:
            courses = []

        print(f"{self.nom} {self.prenom}, {self.age} ans, {self.genre}")
        print(f"Classe : {self.classe}, Formation : {self.formation}")
        print(f"ID : {self._studentID}\n")  

        moyenne_generale = self.getAverageGrade()
        print(f"Moyenne générale : {moyenne_generale if moyenne_generale != 'N/A' else 'Pas encore de notes'}\n")

        for course in courses:
            if self in course.students:
                if course.courseCode in self.grades:
                    notes = self.grades[course.courseCode]
                    moyenne_matiere = sum(notes) / len(notes) if notes else "Pas encore de notes"
                else:
                    moyenne_matiere = "Pas encore de notes"
                    notes = []

                print(f"Moyenne {course.courseName} / {course.courseCode} : {moyenne_matiere}")
                for note in notes:
                    print(f"    Note : {note}")
                print()


class Course:
    def __init__(self, courseName, creditHours):
        self.courseName = courseName
        self.courseCode = self.generer_Code()
        self.creditHours = creditHours
        self.students = []

    @staticmethod
    def generer_Code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def enrollStudent(self, student):
        if student not in self.students:
            self.students.append(student)

    def getEnrolledStudents(self):
        return [f"{s.nom} {s.prenom} (ID: {s._studentID})" for s in self.students]


class Enrollment:
    def __init__(self, student, course):
        self.student = student
        self.course = course

    def register(self):
        self.course.enrollStudent(self.student)


etudiant1 = Student("Collatuzo", "Loic", 20, "M", "Bachelor 1", "Cybersécurité")
etudiant2 = Student("Deschler", "Théo", 19, "M", "Bachelor 1", "Cybersécurité")
etudiant3 = Student("Dupont", "Léna", 87, "F", "Master 2", "AI")
ancien_etudiant1 = GraduateStudent("Martin", "Dubois", 26, "Master en Informatique")

maths = Course("Mathématiques", 5)
informatique = Course("Informatique", 4)
techno = Course("Technologie", 3)
philo = Course("Philosophie", 2)

inscription1 = Enrollment(etudiant1, maths)
inscription1.register()
inscription2 = Enrollment(etudiant2, maths)
inscription2.register()
inscription3 = Enrollment(etudiant1, informatique)
inscription3.register()
inscription4 = Enrollment(etudiant1, techno)
inscription4.register()
inscription5 = Enrollment(etudiant1, philo)
inscription5.register()
inscription6 = Enrollment(etudiant2, informatique)
inscription6.register()
inscription7 = Enrollment(etudiant2, philo)
inscription7.register()

etudiant1.addGrade(maths.courseCode, 18)
etudiant1.addGrade(maths.courseCode, 18)
etudiant2.addGrade(maths.courseCode, 12)
etudiant1.addGrade(informatique.courseCode, 18)
etudiant1.addGrade(techno.courseCode, 1)
etudiant1.addGrade(techno.courseCode, 8.5)
etudiant2.addGrade(informatique.courseCode, 20)
etudiant2.addGrade(philo.courseCode, 0)

etudiant1.afficher_informations([maths, informatique, techno, philo])
etudiant2.afficher_informations([maths, informatique, techno, philo])
etudiant3.afficher_informations([maths, informatique, techno, philo])
ancien_etudiant1.afficher_informations()