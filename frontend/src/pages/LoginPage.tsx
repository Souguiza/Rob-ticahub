import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Navigate, useNavigate } from "react-router-dom";
import { z } from "zod";

import { useAuth } from "../contexts/AuthContext";

const schema = z.object({
  email: z.string().email("Informe um e-mail valido"),
  password: z.string().min(8, "Senha deve ter ao menos 8 caracteres"),
});

type FormData = z.infer<typeof schema>;

export function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm<FormData>({ resolver: zodResolver(schema) });

  if (user) {
    return <Navigate to="/app" replace />;
  }

  async function onSubmit(data: FormData) {
    setError("");
    try {
      await login(data);
      navigate("/app");
    } catch {
      setError("Nao foi possivel entrar. Confira e-mail e senha.");
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit(onSubmit)}>
        <h1>Entrar</h1>
        <label>
          E-mail
          <input type="email" {...register("email")} />
          <span>{formState.errors.email?.message}</span>
        </label>
        <label>
          Senha
          <input type="password" {...register("password")} />
          <span>{formState.errors.password?.message}</span>
        </label>
        {error && <p className="form-error">{error}</p>}
        <button className="button" type="submit" disabled={formState.isSubmitting}>
          Entrar
        </button>
      </form>
    </main>
  );
}
