import React, { useEffect, useState } from "react";

const App = () => {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await fetch("http://localhost:5000/students");
        const data = await response.json();
        if (response.ok) {
          setStudents(data);
        } else {
          console.error("Erreur lors de la récupération des étudiants:", data.error);
        }
      } catch (error) {
        console.error("Erreur de réseau:", error);
      }
    };

    fetchStudents();
  }, []); 

  return (
    <div>
      <h1>Bienvenue !</h1>
      <h2>Liste des étudiants</h2>

      {}
      {students.length > 0 ? (
        <ul>
          {students.map((student) => (
            <li key={student.id}>
              {student.nom} {student.prenom} - {student.classe} ({student.formation})
            </li>
          ))}
        </ul>
      ) : (
        <p>Aucun étudiant trouvé.</p>
      )}
    </div>
  );
};

export default App;
