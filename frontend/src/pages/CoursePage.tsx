import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";

import { api } from "../services/api";
import type { Course, Paginated } from "../types/api";

export function CoursePage() {
  const { slug } = useParams();
  const [course, setCourse] = useState<Course | null>(null);
  const lessonCount = useMemo(
    () => course?.modules?.reduce((total, module) => total + module.lessons.length, 0) ?? 0,
    [course],
  );

  useEffect(() => {
    api.get<Paginated<Course>>(`/courses/?search=${slug}`).then((response) => {
      setCourse(response.data.results.find((item) => item.slug === slug) ?? response.data.results[0] ?? null);
    });
  }, [slug]);

  if (!course) {
    return <main className="center-state">Curso nao encontrado ou ainda carregando.</main>;
  }

  return (
    <main className="content">
      <section className="course-detail">
        <div>
          <p className="eyebrow">{course.level}</p>
          <h1>{course.title}</h1>
          <p>{course.description}</p>
        </div>
        <aside>
          <strong>{course.workload_hours}h</strong>
          <span>{lessonCount} aulas</span>
          <button className="button" type="button">
            Matricular
          </button>
        </aside>
      </section>
      <section className="module-list">
        {course.modules?.map((module) => (
          <article key={module.id}>
            <h2>{module.title}</h2>
            {module.lessons.map((lesson) => (
              <p key={lesson.id}>{lesson.title}</p>
            ))}
          </article>
        ))}
      </section>
    </main>
  );
}
