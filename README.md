📌 README

# Student Management System 📚

Ce projet est un **système de gestion des étudiants** utilisant **Flask** et la **Programmation Orientée Objet (POO)**.

## 🚀 Fonctionnalités

- Créer des étudiants et gérer leurs informations.
- Créer des cours et leur attribuer des crédits.
- Inscrire les étudiants aux cours.
- Gérer les notes et les moyennes des étudiants.
- Exposer une API REST pour interagir avec le système.

## 🛠️ Installation

1. Cloner le projet :
   ```sh
   git clone https://github.com/ton-repo/student-management.git
   cd student-management

    Créer un environnement virtuel (optionnel) :

python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
venv\Scripts\activate  # Sur Windows

Installer les dépendances :

pip install flask

Lancer le serveur Flask :

    python api.py

L’API tournera sur http://127.0.0.1:5000/.

## 📡 API Endpoints

Méthode	Endpoint	Description
POST	/students	Ajouter un nouvel étudiant
POST	/courses	Ajouter un nouveau cours
POST	/enrollments	Inscrire un étudiant à un cours
GET	/students	Récupérer la liste des étudiants
GET	/courses	Récupérer la liste des cours
GET	/students/{id}	Obtenir les détails d’un étudiant
GET	/courses/{id}	Obtenir les détails d’un cours

## 🧪 Tester l’API avec curl

Exemples de requêtes :

1️⃣ Créer un étudiant

curl -X POST http://127.0.0.1:5000/students -H "Content-Type: application/json" -d '{
  "nom": "Doe",
  "prenom": "John",
  "age": 20,
  "genre": "Homme",
  "classe": "Mathématiques",
  "formation": "Licence"
}'

2️⃣ Créer un cours

curl -X POST http://127.0.0.1:5000/courses -H "Content-Type: application/json" -d '{
  "courseName": "Algèbre",
  "creditHours": 4
}'

3️⃣ Inscrire un étudiant à un cours

(Remplace studentID et courseCode par les valeurs renvoyées par les requêtes précédentes)

curl -X POST http://127.0.0.1:5000/enrollments -H "Content-Type: application/json" -d '{
  "studentID": "<studentID>",
  "courseCode": "<courseCode>"
}'

4️⃣ Lister tous les étudiants

curl -X GET http://127.0.0.1:5000/students

5️⃣ Lister tous les cours

curl -X GET http://127.0.0.1:5000/courses

6️⃣ Obtenir les détails d’un étudiant

curl -X GET http://127.0.0.1:5000/students/<studentID>

7️⃣ Obtenir les détails d’un cours

curl -X GET http://127.0.0.1:5000/courses/<courseCode>