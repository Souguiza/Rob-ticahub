import { BookOpen, LayoutDashboard, LogOut, Users } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../contexts/AuthContext";

export function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">RoboticaHub</div>
        <NavLink to="/app">
          <LayoutDashboard size={18} />
          Dashboard
        </NavLink>
        <NavLink to="/app/meus-cursos">
          <BookOpen size={18} />
          Meus cursos
        </NavLink>
        <NavLink to="/app/minha-equipe">
          <Users size={18} />
          Minha equipe
        </NavLink>
        <button type="button" onClick={logout}>
          <LogOut size={18} />
          Sair
        </button>
      </aside>
      <div className="app-main">
        <header className="app-header">
          <div>
            <strong>{user?.full_name}</strong>
            <span>{user?.role}</span>
          </div>
        </header>
        <Outlet />
      </div>
    </div>
  );
}
