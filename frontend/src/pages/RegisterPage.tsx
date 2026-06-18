import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Navigate, useNavigate } from "react-router-dom";
import { z } from "zod";

import { useAuth } from "../contexts/AuthContext";

const schema = z.object({
  full_name: z.string().min(3, "Informe seu nome completo"),
  email: z.string().email("Informe um e-mail valido"),
  password: z.string().min(8, "Senha deve ter ao menos 8 caracteres"),
  city: z.string().optional(),
  state: z.string().optional(),
  country: z.string().default("Brasil"),
  accepted_terms: z.literal(true, { errorMap: () => ({ message: "Aceite os termos" }) }),
  privacy_consent: z.literal(true, { errorMap: () => ({ message: "Aceite a politica de privacidade" }) }),
});

type FormData = z.infer<typeof schema>;

export function RegisterPage() {
  const { user, register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { country: "Brasil" },
  });

  if (user) {
    return <Navigate to="/app" replace />;
  }

  async function onSubmit(data: FormData) {
    setError("");
    try {
      await registerUser({ ...data, interests: ["programacao"], robotics_programs: ["FLL"] });
      navigate("/app");
    } catch {
      setError("Nao foi possivel criar sua conta agora.");
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card wide" onSubmit={handleSubmit(onSubmit)}>
        <h1>Cadastro</h1>
        <div className="form-grid">
          <label>
            Nome completo
            <input {...register("full_name")} />
            <span>{formState.errors.full_name?.message}</span>
          </label>
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
          <label>
            Cidade
            <input {...register("city")} />
          </label>
          <label>
            Estado
            <input {...register("state")} />
          </label>
          <label>
            Pais
            <input {...register("country")} />
          </label>
        </div>
        <label className="check">
          <input type="checkbox" {...register("accepted_terms")} />
          Aceito os termos de uso
        </label>
        <label className="check">
          <input type="checkbox" {...register("privacy_consent")} />
          Aceito a politica de privacidade
        </label>
        {error && <p className="form-error">{error}</p>}
        <button className="button" type="submit" disabled={formState.isSubmitting}>
          Criar conta
        </button>
      </form>
    </main>
  );
}
