"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { authClient } from "@/lib/auth-client";

export function LoginForm({
  callbackURL,
}: {
  callbackURL: string;
}) {
  const router = useRouter();

  const [googleLoading, setGoogleLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  async function handleGoogleLogin() {
    if (googleLoading) return;

    setGoogleLoading(true);
    setErrorMessage("");
    setSuccessMessage("");

    try {
      await authClient.signIn.social({
        provider: "google",
        callbackURL: callbackURL || "/",
      });
    } catch (e: any) {
      setErrorMessage(
        e?.message || "Erro ao conectar com a conta Google."
      );
      setGoogleLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "100%" }}>
      {/* Botão Oficial Padronizado HelpUS Google Sign-In */}
      <button
        type="button"
        onClick={handleGoogleLogin}
        disabled={googleLoading}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "12px",
          width: "100%",
          padding: "13px 18px",
          borderRadius: "14px",
          background: "rgba(13, 29, 51, 0.95)",
          color: "#f5f9ff",
          border: "1px solid rgba(56, 189, 248, 0.4)",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.4)",
          fontWeight: 700,
          fontSize: "14px",
          cursor: googleLoading ? "wait" : "pointer",
          transition: "all 0.2s ease",
        }}
      >
        {googleLoading ? (
          <span style={{ display: "inline-flex", alignItems: "center", gap: "8px" }}>
            <svg
              style={{
                width: "18px",
                height: "18px",
                animation: "spin 1s linear infinite",
              }}
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                strokeOpacity="0.25"
              />
              <path
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            Conectando ao Google...
          </span>
        ) : (
          <>
            {/* SVG Oficial 4-Cores do Google */}
            <svg style={{ width: "20px", height: "20px", flexShrink: 0 }} viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
            <span>Continuar com o Google</span>
          </>
        )}
      </button>

      {successMessage ? (
        <p
          style={{
            padding: "10px 14px",
            borderRadius: "8px",
            background: "rgba(74, 222, 128, 0.15)",
            border: "1px solid #4ade80",
            color: "#4ade80",
            fontSize: "13px",
            fontWeight: 600,
            textAlign: "center",
          }}
          role="status"
        >
          {successMessage}
        </p>
      ) : null}

      {errorMessage ? (
        <p className="auth-error" role="alert" aria-live="polite">
          {errorMessage}
        </p>
      ) : null}

      <div style={{ textAlign: "center", fontSize: "11px", color: "#64748b", marginTop: "4px" }}>
        🔒 Acesso via Google • permissões definidas por organização
      </div>
    </div>
  );
}
