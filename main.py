from student import Student, GraduateStudent, Course
import random
import string
import requests

API_URL = "http://127.0.0.1:5000"

students = []
graduate_students = []
courses = []

def generer_ID():
    """Génère un ID unique pour un étudiant ou un cours."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def afficher_menu():
    print("\n--- Menu Principal ---")
    print("1. Liste des cours")
    print("2. Liste des élèves")
    print("3. Liste des alumnis")
    print("4. Rechercher un ID")
    print("5. Ajouter / Supprimer")
    print("0. Quitter")

def afficher_cours():
    """Affiche la liste des cours existants."""
    if not courses:
        print("Aucun cours trouvé.")
        return
    print("\n--- Liste des cours ---")
    for course in courses:
        print(f"Code: {course.courseCode} | Nom: {course.courseName} | Crédits: {course.creditHours}")

def afficher_etudiants():
    """Affiche la liste des étudiants."""
    if not students:
        print("Aucun étudiant trouvé.")
        return
    print("\n--- Liste des étudiants ---")
    for student in students:
        print(f"ID: {student._studentID} | Nom: {student.nom} {student.prenom} | Formation: {student.formation} | Classe: {student.classe}")

def afficher_alumnis():
    """Affiche la liste des alumnis."""
    if not graduate_students:
        print("Aucun alumni trouvé.")
        return
    print("\n--- Liste des alumnis ---")
    for graduate in graduate_students:
        print(f"ID: {graduate._graduateID} | Nom: {graduate.nom} {graduate.prenom} | Diplôme: {graduate.diplome}")

def rechercher_par_id():
    """Recherche un étudiant ou un alumni par ID et affiche ses informations complètes."""
    id_recherche = input("Entrez l'ID de l'étudiant/alumni: ")
    
    for student in students:
        if student._studentID == id_recherche:
            student.afficher_informations(courses)
            return
    
    for graduate in graduate_students:
        if graduate._graduateID == id_recherche:
            graduate.afficher_informations()
            return

    print("Aucun étudiant ou alumni trouvé avec cet ID.")

def ajouter_etudiant():
    """Ajoute un nouvel étudiant via l'API."""
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    age = int(input("Âge: "))
    genre = input("Genre (M/F): ")
    classe = input("Classe: ")
    formation = input("Formation: ")

    data = {
        "nom": nom,
        "prenom": prenom,
        "age": age,
        "genre": genre,
        "classe": classe,
        "formation": formation
    }

    response = requests.post(f"{API_URL}/students", json=data)

    if response.status_code == 201:
        student = response.json()
        print(f"Étudiant {student['nom']} {student['prenom']} ajouté avec succès ! ID: {student['id']}")
    else:
        print("Erreur lors de l'ajout de l'étudiant:", response.json().get("error", "Erreur inconnue"))

def ajouter_alumni():
    """Ajoute un alumni."""
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    age = int(input("Âge: "))
    diplome = input("Diplôme obtenu: ")

    alumni = GraduateStudent(nom, prenom, age, diplome)
    graduate_students.append(alumni)

    print(f"Alumni {nom} {prenom} ajouté avec succès ! ID: {alumni._graduateID}")

def ajouter_cours():
    """Ajoute un nouveau cours."""
    nom = input("Nom du cours: ")
    credits = int(input("Nombre de crédits: "))

    cours = Course(nom, credits)
    courses.append(cours)

    print(f"Cours {nom} ajouté avec succès ! Code: {cours.courseCode}")

def inscrire_etudiant():
    """Inscrit un étudiant à un cours."""
    student_id = input("ID de l'étudiant: ")
    course_code = input("Code du cours: ")

    etudiant = next((s for s in students if s._studentID == student_id), None)
    cours = next((c for c in courses if c.courseCode == course_code), None)

    if etudiant and cours:
        cours.enrollStudent(etudiant)
        print(f"Étudiant {etudiant.nom} inscrit au cours {cours.courseName}")
    else:
        print("Étudiant ou cours introuvable.")

def ajouter_note():
    """Ajoute une note à un étudiant pour un cours."""
    student_id = input("ID de l'étudiant: ")
    course_code = input("Code du cours: ")
    note = float(input("Note (0-20) : "))

    etudiant = next((s for s in students if s._studentID == student_id), None)
    
    if etudiant:
        etudiant.addGrade(course_code, note)
        print(f"Note ajoutée avec succès pour {etudiant.nom}.")
    else:
        print("Étudiant introuvable.")

def menu_ajouter():
    """Affiche le sous-menu d'ajout et de suppression."""
    print("\n--- Ajouter / Modifier ---")
    print("1. Ajouter un élève")
    print("2. Ajouter un alumni")
    print("3. Ajouter un cours")
    print("4. Inscrire un élève à un cours")
    print("5. Ajouter une note à un élève")
    print("0. Retour")

    choix = input("Votre choix: ")
    if choix == "1":
        ajouter_etudiant()
    elif choix == "2":
        ajouter_alumni()
    elif choix == "3":
        ajouter_cours()
    elif choix == "4":
        inscrire_etudiant()
    elif choix == "5":
        ajouter_note()

while True:
    afficher_menu()
    choix = input("Votre choix: ")

    if choix == "1":
        afficher_cours()
    elif choix == "2":
        afficher_etudiants()
    elif choix == "3":
        afficher_alumnis()
    elif choix == "4":
        rechercher_par_id()
    elif choix == "5":
        menu_ajouter()
    elif choix == "0":
        print("Fermeture du programme...")
        break
    else:
        print("Option invalide, veuillez réessayer.")