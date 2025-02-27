# POO-individual-project
POO

📚 Gestion des Étudiants et des Notes

Ce projet est une application de gestion des étudiants et des notes en Python avec Flask.
Elle permet d'ajouter des étudiants, de les inscrire à des cours, d'ajouter des notes et de calculer leur moyenne générale ainsi que leur réussite à l'année.
🚀 Installation et Exécution
1️⃣ Cloner le projet

git clone https://github.com/ton-repo.git
cd ton-repo

2️⃣ Installer les dépendances

Assure-toi d'avoir Python 3 installé, puis installe les dépendances avec :

pip install -r requirements.txt

3️⃣ Démarrer l'API Flask

Dans un terminal, exécute :

python api.py

Cela démarre le serveur Flask qui gère les étudiants, les cours et les inscriptions.
4️⃣ Lancer l'interface utilisateur

Dans un autre terminal, lance :

python main.py

Cela démarre l'interface en ligne de commande qui permet d'interagir avec l'application.
🎮 Utilisation

Lorsque python main.py est exécuté, un menu interactif s'affiche.
Utilise les chiffres pour naviguer et réponds aux demandes affichées.
📌 Fonctionnalités principales

1️⃣ Ajouter un étudiant
2️⃣ Afficher la liste des étudiants
3️⃣ Rechercher un étudiant par ID (avec moyenne et réussite)
4️⃣ Ajouter un cours
5️⃣ Afficher la liste des cours
6️⃣ Inscrire un étudiant à un cours
7️⃣ Ajouter une note à un étudiant pour un cours
8️⃣ Quitter l'application
🛠 Structure du Projet

📂 /data/ → Stocke les données JSON (étudiants, cours, inscriptions)
📜 api.py → Gère les requêtes API avec Flask sur l'URL : http://127.0.0.1:5000/<students/courses>/<id>
📜 main.py → Interface utilisateur CLI
📜 student.py → Modèle des étudiants
📜 course.py → Modèle des cours
📜 enrollment.py → Gestion des inscriptions
💡 Exemple d'utilisation

    Ajouter un étudiant
        Saisie du nom, prénom, âge, genre, classe, formation
        Un ID unique est généré

    Inscrire l'étudiant à un cours
        Sélection d'un cours dans la liste
        L'inscription est enregistrée

    Ajouter une note à un étudiant
        Saisie de l'ID de l'étudiant et du code du cours
        Ajout d'une note sur 20

    Voir la moyenne et la réussite
        Recherche d'un étudiant par ID
        Affichage de la moyenne générale, moyennes par cours et crédits obtenus
        Indique si l'étudiant passe ou non son année 🎓

✨ Critères de réussite

🔹 Moyenne par cours = moyenne des notes obtenues
🔹 Moyenne générale = moyenne de toutes les notes
🔹 Réussite de l'année = moyenne * crédits ≥ 200

Bonne utilisation ! 🚀