class User:

    def __init__(self, nom, prenom, IDe, age, genre, classe, formation):
        self.nom = nom
        self.prenom = prenom
        self.IDe = IDe
        self.age = age
        self.genre = genre
        self.classe = classe
        self.formation = formation
        self.matieres = []


class Matiere:

    def __init__(self, nom, IDc, credit):
        self.nom = nom
        self.IDc = IDc
        self.credit = credit
        self.notes = []  

    def ajouter_note(self, note):
        if 0 <= note <= 20:
            self.notes.append(note)

    def retirer_note(self, note):
        if note in self.notes:
            self.notes.remove(note)

    def calculer_moyenne(self):
        if self.notes:
            return sum(self.notes) / len(self.notes)
        return "N/A"

    def ajouter_matiere(self, matiere):
        if matiere not in self.matieres:
            self.matiere.append(matiere)

    def retirer_matiere(self, matiere):
        if matiere in self.matieres:
            self.matieres.remove(matiere)


class GestionEtudiants:

    def __init__(self):
        self.etudiants = []

    def ajouter_etudiant(self, user):
        self.etudiants.append(user)

    def retirer_etudiant(self, nom, prenom):
        self.etudiants = [
            etudiant for etudiant in self.etudiants
            if not (etudiant.nom == nom and etudiant.prenom == prenom)
        ]


def afficher_informations(self):

    print(f"{self.nom}, {self.prenom}")
    print(f"{self.age} ans, {self.genre}")
    print(f"Classe: {self.classe}, Formation: {self.formation}")
    print("Moyenne générale:", self.calculer_moyenne_generale())

    for matiere in self.matieres:
        print(f"\nMoyenne pour {matiere.nom}: {matiere.calculer_moyenne()}")
        for note in matiere.notes:
            print(f"  Note: {note}")
