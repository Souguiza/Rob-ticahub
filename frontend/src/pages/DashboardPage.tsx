import { BookOpen, CheckCircle2, ClipboardList, Users } from "lucide-react";
import { useEffect, useState } from "react";

import { useAuth } from "../contexts/AuthContext";
import { api } from "../services/api";
import type { Course, Paginated, Team } from "../types/api";

export function DashboardPage({ focus }: { focus?: "team" }) {
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    api.get<Paginated<Course>>("/courses/").then((response) => setCourses(response.data.results));
    api.get<Paginated<Team>>("/teams/").then((response) => setTeams(response.data.results));
  }, []);

  return (
    <main className="dashboard">
      <div className="section-heading">
        <p className="eyebrow">{focus === "team" ? "Equipe" : "Dashboard"}</p>
        <h1>Ola, {user?.full_name.split(" ")[0]}</h1>
      </div>
      <div className="stats-grid">
        <article>
          <BookOpen size={22} />
          <strong>{courses.length}</strong>
          <span>cursos disponiveis</span>
        </article>
        <article>
          <Users size={22} />
          <strong>{teams.length}</strong>
          <span>equipes</span>
        </article>
        <article>
          <ClipboardList size={22} />
          <strong>0</strong>
          <span>tarefas pendentes</span>
        </article>
        <article>
          <CheckCircle2 size={22} />
          <strong>0%</strong>
          <span>progresso medio</span>
        </article>
      </div>
      <section className="panel">
        <h2>Cursos em destaque</h2>
        <div className="table">
          {courses.slice(0, 5).map((course) => (
            <div className="table-row" key={course.id}>
              <span>{course.title}</span>
              <strong>{course.workload_hours}h</strong>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
