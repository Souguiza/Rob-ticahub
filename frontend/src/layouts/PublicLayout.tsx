import { Cpu, LogIn, UserPlus } from "lucide-react";
import { Link, NavLink, Outlet } from "react-router-dom";

export function PublicLayout() {
  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">
          <Cpu size={24} />
          <span>RoboticaHub Brasil</span>
        </Link>
        <nav className="nav">
          <NavLink to="/cursos">Cursos</NavLink>
          <NavLink to="/login">
            <LogIn size={18} />
            Entrar
          </NavLink>
          <NavLink className="button small" to="/cadastro">
            <UserPlus size={18} />
            Cadastro
          </NavLink>
        </nav>
      </header>
      <Outlet />
      <footer className="footer">
        Esta e uma plataforma independente de educacao em robotica e nao representa, nao e patrocinada e nao e
        oficialmente endossada pela FIRST.
      </footer>
    </div>
  );
}
