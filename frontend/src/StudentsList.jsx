import React, { useEffect, useState } from 'react';

function StudentsList() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/students')
      .then(response => response.json())
      .then(data => setStudents(data))
      .catch(error => console.error('Erreur :', error));
  }, []);

  return (
    <div>
      <h2>Liste des étudiants</h2>
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.nom} {student.prenom} - {student.classe}</li>
        ))}
      </ul>
    </div>
  );
}

export default StudentsList;
