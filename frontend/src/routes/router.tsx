import { createBrowserRouter } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { PublicLayout } from "../layouts/PublicLayout";
import { CatalogPage } from "../pages/CatalogPage";
import { CoursePage } from "../pages/CoursePage";
import { DashboardPage } from "../pages/DashboardPage";
import { HomePage } from "../pages/HomePage";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";
import { ProtectedRoute } from "./ProtectedRoute";

export const router = createBrowserRouter([
  {
    element: <PublicLayout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/cursos", element: <CatalogPage /> },
      { path: "/cursos/:slug", element: <CoursePage /> },
      { path: "/login", element: <LoginPage /> },
      { path: "/cadastro", element: <RegisterPage /> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/app",
        element: <AppLayout />,
        children: [
          { index: true, element: <DashboardPage /> },
          { path: "meus-cursos", element: <CatalogPage /> },
          { path: "minha-equipe", element: <DashboardPage focus="team" /> },
        ],
      },
    ],
  },
]);
