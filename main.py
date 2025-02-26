import os
import requests

API_URL = "http://127.0.0.1:5000"

def clear_terminal():
    """Efface l'écran pour une meilleure lisibilité."""
    os.system("cls" if os.name == "nt" else "clear")

def afficher_menu():
    clear_terminal()
    print("\n--- Menu Principal ---")
    print("1. Gérer les alumnis")
    print("2. Gérer les étudiants")
    print("3. Gérer les cours")
    print("4. Inscrire un étudiant")
    print("5. Ajouter une note")
    print("6. Rechercher par ID")
    print("0. Quitter")

### 📌 GESTION DES ALUMNIS
def afficher_alumnis():
    clear_terminal()
    response = requests.get(f"{API_URL}/graduate_students")
    if response.status_code == 200:
        alumnis = response.json()
        if not alumnis:
            print("Aucun alumni trouvé.")
        else:
            print("\n--- Liste des Alumnis ---")
            for alumni in alumnis:
                print(f"ID: {alumni.get('id', 'N/A')} | Nom: {alumni['nom']} {alumni['prenom']} | Diplôme: {alumni['diplome']}")
    else:
        print(f"Erreur API : {response.status_code} - {response.text}")
    input("\nAppuyez sur Entrée pour continuer...")

def ajouter_modifier_supprimer_alumni():
    while True:
        clear_terminal()
        print("\n--- Gérer les Alumnis ---")
        print("1. Ajouter un alumni")
        print("2. Afficher tous les alumnis")
        print("0. Retour")

        choix = input("Votre choix: ")

        if choix == "1":
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            try:
                age = int(input("Âge: "))
            except ValueError:
                print("Erreur : L'âge doit être un nombre entier.")
                continue
            diplome = input("Diplôme: ")

            response = requests.post(f"{API_URL}/graduate_students", json={"nom": nom, "prenom": prenom, "age": age, "diplome": diplome})
            print("✅ Alumni ajouté !" if response.status_code == 201 else f"❌ Erreur : {response.text}")

        elif choix == "2":
            afficher_alumnis()

        elif choix == "0":
            break

        input("\nAppuyez sur Entrée pour continuer...")

### 📌 GESTION DES ÉTUDIANTS
def afficher_etudiants():
    """Affiche la liste des étudiants depuis l'API."""
    response = requests.get(f"{API_URL}/students")
    if response.status_code == 200:
        students = response.json()
        if not students:
            print("Aucun étudiant trouvé.")
            return
        print("\n--- Liste des étudiants ---")
        for student in students:
            print(f"ID: {student['id']} | Nom: {student['nom']} {student['prenom']} | Formation: {student['formation']} | Classe: {student['classe']}")
    else:
        print("Erreur lors de la récupération des étudiants.")

def ajouter_modifier_supprimer_etudiant():
    """Ajoute, modifie ou supprime un étudiant."""
    while True:  
        clear_terminal()
        print("\n--- Gérer les étudiants ---")
        print("1. Ajouter un étudiant")
        print("2. Afficher tous les étudiants")
        print("0. Retour")

        choix = input("Votre choix: ")

        if choix == "1":
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            age = int(input("Âge: "))
            genre = input("Genre (M/F): ")
            classe = input("Classe: ")
            formation = input("Formation: ")

            data = {"nom": nom, "prenom": prenom, "age": age, "genre": genre, "classe": classe, "formation": formation}
            response = requests.post(f"{API_URL}/students", json=data)

            if response.status_code == 201:
                print("Étudiant ajouté avec succès !")
            else:
                print("Erreur lors de l'ajout.")

            input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
            continue   

        elif choix == "2":
            afficher_etudiants()

            input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
            continue  

        elif choix == "0":
            break  

        else:
            print("❌ Option invalide, veuillez réessayer.")
            input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
            continue  

### 📌 GESTION DES COURS
def afficher_cours():
    clear_terminal()
    response = requests.get(f"{API_URL}/courses")
    if response.status_code == 200:
        courses = response.json()
        print("\n--- Liste des Cours ---" if courses else "Aucun cours trouvé.")
        for course in courses:
            print(f"Code: {course['courseCode']} | Nom: {course['courseName']}")
    else:
        print(f"Erreur API : {response.status_code} - {response.text}")

def ajouter_modifier_supprimer_cours():
    clear_terminal()
    print("\n--- Gérer les Cours ---")
    print("1. Ajouter un cours")
    print("2. Afficher tous les cours")
    print("0. Retour")

    choix = input("Votre choix: ")

    if choix == "1":
        nom = input("Nom du cours: ")
        credits = input("Crédits: ")
        try:
            credits = int(credits)
            response = requests.post(f"{API_URL}/courses", json={"courseName": nom, "creditHours": credits})
            print("Cours ajouté !" if response.status_code == 201 else f"Erreur : {response.text}")
        except ValueError:
            print("Erreur : Les crédits doivent être un nombre entier.")

    elif choix == "2":
        afficher_cours()

### 📌 INSCRIPTION D'UN ÉTUDIANT
def inscrire_etudiant():
    clear_terminal()
    student_id = input("ID de l'étudiant: ")
    course_code = input("Code du cours: ")

    response = requests.post(f"{API_URL}/courses/{course_code}/enroll", json={"student_id": student_id})
    print("Inscription réussie !" if response.status_code == 200 else f"Erreur : {response.text}")
    input("\nAppuyez sur Entrée pour revenir au menu des inscriptions...")

### 📌 AJOUTER UNE NOTE
def ajouter_note():
    clear_terminal()
    student_id = input("ID de l'étudiant: ")
    course_id = input("ID du cours: ")
    try:
        note = float(input("Note (sur 20) : "))
    except ValueError:
        print("Erreur : La note doit être un nombre.")
        return

    data = {"student_id": student_id, "course_id": course_id, "note": note}
    response = requests.post(f"{API_URL}/grades", json=data)

    print("✅ Note ajoutée !" if response.status_code == 201 else f"❌ Erreur : {response.text}")
    input("\nAppuyez sur Entrée pour revenir au menu des notes...")

### 📌 RECHERCHE PAR ID
def rechercher_par_id():
    while True:
        clear_terminal()  
        print("\n--- Rechercher par ID ---")
        print("1. Rechercher un étudiant")
        print("2. Rechercher un alumni")
        print("3. Rechercher un cours")
        print("0. Retour")

        choix = input("Votre choix: ")

        if choix == "1":
            student_id = input("ID de l'étudiant: ")
            response = requests.get(f"{API_URL}/students/{student_id}")
            clear_terminal()  
            if response.status_code == 200:
                etudiant = response.json()
                print(f"✅ Étudiant trouvé :")
                print(f"Nom : {etudiant['nom']}")
                print(f"Prénom : {etudiant['prenom']}")
                print(f"Âge : {etudiant['age']}")
                print(f"Genre : {etudiant['genre']}")
                print(f"Classe : {etudiant['classe']}")
                print(f"Formation : {etudiant['formation']}")
                print(f"Notes : {etudiant['grades']}")
            else:
                print("❌ Étudiant introuvable.")

        elif choix == "2": 
            alumni_id = input("ID de l'alumni: ")
            response = requests.get(f"{API_URL}/graduate_students/{alumni_id}")
            clear_terminal()  
            if response.status_code == 200:
                alumni = response.json()
                print(f"✅ Alumni trouvé :")
                print(f"Nom : {alumni['nom']}")
                print(f"Prénom : {alumni['prenom']}")
                print(f"Âge : {alumni['age']}")
                print(f"Diplôme : {alumni['diplome']}")
            else:
                print("❌ Alumni introuvable.")

        elif choix == "3":  
            course_id = input("ID du cours: ")
            response = requests.get(f"{API_URL}/courses/{course_id}")
            clear_terminal()  
            if response.status_code == 200:
                cours = response.json()
                print(f"✅ Cours trouvé :")
                print(f"Nom du cours : {cours['courseName']}")
                print(f"Crédits : {cours['creditHours']}")
            else:
                print("❌ Cours introuvable.")

        elif choix == "0":
            break

        input("\nAppuyez sur Entrée pour continuer...")

while True:
    afficher_menu()
    choix = input("Votre choix: ")

    if choix == "1":
        ajouter_modifier_supprimer_alumni()
    elif choix == "2":
        ajouter_modifier_supprimer_etudiant()
    elif choix == "3":
        ajouter_modifier_supprimer_cours()
    elif choix == "4":
        inscrire_etudiant()
    elif choix == "5":
        ajouter_note() 
    elif choix == "6":
        rechercher_par_id()
    elif choix == "0":
        print("Fermeture du programme...")
        break
    else:
        print("❌ Option invalide, veuillez réessayer.")

    input("\nAppuyez sur Entrée pour continuer...")
