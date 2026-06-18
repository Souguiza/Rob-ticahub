import { ArrowRight, Trophy, Wrench } from "lucide-react";
import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <main className="home">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">LMS brasileiro para robotica educacional e competitiva</p>
          <h1>RoboticaHub Brasil</h1>
          <p>
            Cursos, equipes, projetos e caderno de engenharia em uma plataforma preparada para escolas,
            mentores e organizacoes.
          </p>
          <div className="actions">
            <Link className="button" to="/cursos">
              Ver cursos
              <ArrowRight size={18} />
            </Link>
            <Link className="button ghost" to="/cadastro">
              Criar conta
            </Link>
          </div>
        </div>
        <div className="robot-panel" aria-hidden="true">
          <div className="robot-grid">
            {Array.from({ length: 36 }).map((_, index) => (
              <span key={index} />
            ))}
          </div>
          <div className="signal-card">
            <Trophy size={22} />
            <span>FLL · FTC · FRC · OBR</span>
          </div>
          <div className="tool-card">
            <Wrench size={22} />
            <span>Caderno de engenharia</span>
          </div>
        </div>
      </section>
      <section className="metric-band">
        <article>
          <strong>5</strong>
          <span>cursos iniciais</span>
        </article>
        <article>
          <strong>8</strong>
          <span>perfis de usuario</span>
        </article>
        <article>
          <strong>API</strong>
          <span>real desde a Fase 1</span>
        </article>
      </section>
    </main>
  );
}
