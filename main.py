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
    print("4. Gérer les inscriptions")
    print("5. Gérer les notes")
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
        print("2. Modifier un alumni")
        print("3. Supprimer un alumni")
        print("4. Afficher tous les alumnis")
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
            id_alumni = input("ID de l'alumni: ")
            nom = input("Nom (laisser vide si inchangé) : ")
            prenom = input("Prénom: ")
            diplome = input("Diplôme: ")
            data = {k: v for k, v in {"nom": nom, "prenom": prenom, "diplome": diplome}.items() if v}
            response = requests.put(f"{API_URL}/graduate_students/{id_alumni}", json=data)
            print("✅ Alumni modifié !" if response.status_code == 200 else f"❌ Erreur : {response.text}")

        elif choix == "3":
            id_alumni = input("ID de l'alumni: ")
            response = requests.delete(f"{API_URL}/graduate_students/{id_alumni}")
            print("✅ Alumni supprimé !" if response.status_code == 200 else f"❌ Erreur : {response.text}")

        elif choix == "4":
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
        print("2. Modifier un étudiant")
        print("3. Supprimer un étudiant")
        print("4. Afficher tous les étudiants")
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
            id_etudiant = input("ID de l'étudiant à modifier: ")
            response = requests.get(f"{API_URL}/students/{id_etudiant}")
            if response.status_code != 200:
                print("Étudiant introuvable.")
                input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
                continue  

            nom = input("Nouveau nom (laisser vide pour ne pas modifier): ")
            prenom = input("Nouveau prénom: ")
            classe = input("Nouvelle classe: ")
            formation = input("Nouvelle formation: ")

            data = {k: v for k, v in {"nom": nom, "prenom": prenom, "classe": classe, "formation": formation}.items() if v}
            response = requests.put(f"{API_URL}/students/{id_etudiant}", json=data)

            if response.status_code == 200:
                print("Étudiant modifié avec succès !")
            else:
                print("Erreur lors de la modification.")

            input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
            continue  

        elif choix == "3":
            id_etudiant = input("ID de l'étudiant à supprimer: ")
            response = requests.delete(f"{API_URL}/students/{id_etudiant}")

            if response.status_code == 200:
                print("Étudiant supprimé avec succès !")
            else:
                print("Erreur lors de la suppression.")

            input("\nAppuyez sur Entrée pour revenir au menu des étudiants...")
            continue  

        elif choix == "4":
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
    print("2. Modifier un cours")
    print("3. Supprimer un cours")
    print("4. Afficher tous les cours")
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
        code = input("Code du cours: ")
        nom = input("Nom (laisser vide si inchangé) : ")
        credits = input("Crédits (laisser vide si inchangé) : ")
        data = {k: v for k, v in {"courseName": nom, "creditHours": credits}.items() if v}
        response = requests.put(f"{API_URL}/courses/{code}", json=data)
        print("Cours modifié !" if response.status_code == 200 else f"Erreur : {response.text}")

    elif choix == "3":
        code = input("Code du cours: ")
        response = requests.delete(f"{API_URL}/courses/{code}")
        print("Cours supprimé !" if response.status_code == 200 else f"Erreur : {response.text}")

    elif choix == "4":
        afficher_cours()

### 📌 GESTION DES INSCRIPTIONS
def inscrire_supprimer_etudiant_cours():
    while True:
        clear_terminal()
        print("\n--- Gérer les inscriptions ---")
        print("1. Inscrire un étudiant")
        print("2. Désinscrire un étudiant")
        print("0. Retour")

        choix = input("Votre choix: ")

        if choix == "1":
            student_id = input("ID de l'étudiant: ")
            course_code = input("Code du cours: ")

            response = requests.post(f"{API_URL}/courses/{course_code}/enroll", json={"student_id": student_id})
            print("Inscription réussie !" if response.status_code == 200 else f"Erreur : {response.text}")
            input("\nAppuyez sur Entrée pour revenir au menu des inscriptions...")
            continue

        elif choix == "2":
            student_id = input("ID de l'étudiant: ")
            course_code = input("Code du cours: ")

            response = requests.delete(f"{API_URL}/courses/{course_code}/unenroll", json={"student_id": student_id})
            print("Désinscription réussie !" if response.status_code == 200 else f"Erreur : {response.text}")
            input("\nAppuyez sur Entrée pour revenir au menu des inscriptions...")
            continue 

        elif choix == "0":
            break

### 📌 GESTION DES NOTES
def gerer_notes():
    while True:
        clear_terminal()
        print("\n--- Gérer les notes ---")
        print("1. Ajouter une note")
        print("2. Modifier une note")
        print("3. Supprimer une note")
        print("0. Retour")

        choix = input("Votre choix: ")

        if choix == "1": 
            student_id = input("ID de l'étudiant: ")
            course_id = input("ID du cours: ")
            try:
                note = float(input("Note (sur 20) : "))
            except ValueError:
                print("Erreur : La note doit être un nombre.")
                continue

            data = {"student_id": student_id, "course_id": course_id, "note": note}
            response = requests.post(f"{API_URL}/grades", json=data)

            print("✅ Note ajoutée !" if response.status_code == 201 else f"❌ Erreur : {response.text}")

        elif choix == "2":
            grade_id = input("ID de la note à modifier: ")
            try:
                nouvelle_note = float(input("Nouvelle note (sur 20) : "))
            except ValueError:
                print("Erreur : La note doit être un nombre.")
                continue

            data = {"note": nouvelle_note}
            response = requests.put(f"{API_URL}/grades/{grade_id}", json=data)

            print("✅ Note modifiée !" if response.status_code == 200 else f"❌ Erreur : {response.text}")

        elif choix == "3":
            grade_id = input("ID de la note à supprimer: ")
            response = requests.delete(f"{API_URL}/grades/{grade_id}")
            print("✅ Note supprimée !" if response.status_code == 200 else f"❌ Erreur : {response.text}")

        elif choix == "0":
            break

        input("\nAppuyez sur Entrée pour continuer...")

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
        inscrire_supprimer_etudiant_cours()
    elif choix == "5":
        gerer_notes() 
    elif choix == "6":
        rechercher_par_id()
    elif choix == "0":
        print("Fermeture du programme...")
        break
    else:
        print("❌ Option invalide, veuillez réessayer.")

    input("\nAppuyez sur Entrée pour continuer...")
