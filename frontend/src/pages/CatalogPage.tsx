import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../services/api";
import type { Course, Paginated } from "../types/api";

export function CatalogPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Paginated<Course>>("/courses/?ordering=title")
      .then((response) => setCourses(response.data.results))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="content">
      <div className="section-heading">
        <p className="eyebrow">Catalogo</p>
        <h1>Cursos de robotica</h1>
      </div>
      {loading ? (
        <div className="center-state">Carregando cursos...</div>
      ) : (
        <div className="course-grid">
          {courses.map((course) => (
            <Link className="course-card" to={`/cursos/${course.slug}`} key={course.id}>
              <span>{course.level}</span>
              <h2>{course.title}</h2>
              <p>{course.description}</p>
              <strong>{course.workload_hours}h</strong>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
