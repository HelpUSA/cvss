"use client";

import {
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type EnvironmentOption = {
  id: string;
  name: string;
  project: {
    id: string;
    name: string;
  };
};

export function AssessmentCreateForm({
  organizationSlug,
  environments,
}: {
  organizationSlug: string;
  environments: EnvironmentOption[];
}) {
  const router = useRouter();
  const formRef =
    useRef<HTMLFormElement>(null);

  const [environmentId, setEnvironmentId] =
    useState(
      environments[0]?.id ?? "",
    );

  const [cve, setCve] =
    useState("");

  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");

  function suggestedTitle(
    mode: "cve-environment" | "assessment-cve" | "project-environment",
  ): string {
    const normalizedCve =
      cve.trim().toUpperCase() || "CVE";
    const environmentName =
      selectedEnvironment?.name || "ambiente";
    const projectName =
      selectedEnvironment?.project.name || "projeto";

    if (mode === "assessment-cve") {
      return `Avaliação ${normalizedCve} — ${environmentName}`;
    }

    if (mode === "project-environment") {
      return `${normalizedCve} — ${projectName} / ${environmentName}`;
    }

    return `${normalizedCve} no ${environmentName}`;
  }

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  useEffect(() => {
    const syncFromDom = () => {
      const form = formRef.current;
      if (!form) {
        return;
      }
      const envEl =
        form.querySelector<HTMLSelectElement>(
          "#assessment-environment",
        );
      if (envEl && envEl.value !== "") {
        setEnvironmentId((prev) =>
          prev === envEl.value
            ? prev
            : envEl.value,
        );
      }
      const cveEl =
        form.querySelector<HTMLInputElement>(
          "#assessment-cve",
        );
      if (cveEl && cveEl.value !== "") {
        const normalized =
          cveEl.value.toUpperCase();
        setCve((prev) =>
          prev === ""
            ? normalized
            : prev,
        );
      }
      const titleEl =
        form.querySelector<HTMLInputElement>(
          "#assessment-title",
        );
      if (titleEl && titleEl.value !== "") {
        setTitle((prev) =>
          prev === ""
            ? titleEl.value
            : prev,
        );
      }
    };
    syncFromDom();
    const timer = window.setInterval(
      syncFromDom,
      100,
    );
    return () =>
      window.clearInterval(timer);
  }, []);

  const selectedEnvironment =
    useMemo(
      () =>
        environments.find(
          (item) =>
            item.id === environmentId,
        ),
      [environmentId, environments],
    );

  async function submit(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setMessage("");

    try {
      const normalizedCve =
        cve.trim().toUpperCase();

      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/assessments`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            environmentId,
            vulnerabilityId:
              normalizedCve,
            cve: normalizedCve,
            title,
            description,
          }),
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            "A avaliação não pôde ser criada.",
        );
      }

      const nextUrl = `/app/${organizationSlug}/assessments/${payload.assessment.id}`;
      if (typeof window !== "undefined") {
        window.location.assign(nextUrl);
      } else {
        router.push(nextUrl);
      }
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Falha inesperada.",
      );
      setPending(false);
    }
  }

  return (
    <form
      ref={formRef}
      className="management-form"
      onSubmit={submit}
    >
      <div
        className="panel"
        style={{
          marginBottom: "1rem",
        }}
      >
        <span className="section-kicker">
          Etapa 3 de 5
        </span>
        <h2>
          Identifique a vulnerabilidade
        </h2>
        <p>
          Use o identificador CVE e um
          título que faça sentido para o
          ativo ou serviço avaliado. O vetor
          CVSS será informado na próxima
          etapa, junto com as evidências.
        </p>
      </div>

      <div className="field">
        <label htmlFor="assessment-environment">
          Ambiente
        </label>
        <select
          id="assessment-environment"
          value={environmentId}
          onChange={(event) =>
            setEnvironmentId(
              event.target.value,
            )
          }
          required
        >
          {environments.map(
            (environment) => (
              <option
                key={environment.id}
                value={environment.id}
              >
                {
                  environment.project
                    .name
                }{" "}
                / {environment.name}
              </option>
            ),
          )}
        </select>
        <small>
          {selectedEnvironment
            ? `Projeto: ${selectedEnvironment.project.name}`
            : ""}
        </small>
      </div>

      <div className="field">
        <label htmlFor="assessment-cve">
          CVE
        </label>
        <input
          id="assessment-cve"
          value={cve}
          onChange={(event) =>
            setCve(
              event.target.value
                .toUpperCase(),
            )
          }
          placeholder="CVE-2026-12345"
          pattern="CVE-[0-9]{4}-[0-9]{4,}"
          required
          autoComplete="off"
        />
        <small>
          Copie o identificador da fonte
          que publicou a vulnerabilidade.
        </small>
      </div>

      <div className="field">
        <label htmlFor="assessment-title-template">
          Modelo de nome (opcional)
        </label>
        <select
          id="assessment-title-template"
          defaultValue=""
          onChange={(event) => {
            const value = event.target.value;
            if (!value) return;
            setTitle(
              suggestedTitle(
                value as
                  | "cve-environment"
                  | "assessment-cve"
                  | "project-environment",
              ),
            );
          }}
        >
          <option value="">
            Escolher modelo...
          </option>
          <option value="cve-environment">
            CVE + ambiente
          </option>
          <option value="assessment-cve">
            “Avaliação” + CVE + ambiente
          </option>
          <option value="project-environment">
            CVE + projeto + ambiente
          </option>
        </select>
        <small>
          O nome gerado pode ser editado antes de continuar.
        </small>
      </div>

      <div className="field">
        <label htmlFor="assessment-title">
          Nome da avaliação
        </label>
        <input
          id="assessment-title"
          value={title}
          onChange={(event) =>
            setTitle(event.target.value)
          }
          placeholder="Ex.: CVE-2026-12345 no Produção"
          minLength={2}
          maxLength={120}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="assessment-description-template">
          Observação rápida (opcional)
        </label>
        <select
          id="assessment-description-template"
          defaultValue=""
          onChange={(event) => {
            const value = event.target.value;
            if (!value) return;

            const templates: Record<string, string> = {
              internet:
                "Serviço acessível pela Internet. Confirmar exposição e controles aplicáveis.",
              internal:
                "Serviço acessível apenas pela rede interna. Confirmar rotas e segmentação.",
              critical:
                "Ativo ou serviço crítico para a operação. Validar requisitos de segurança do ambiente.",
              none:
                "",
            };

            setDescription(
              templates[value] ?? description,
            );
          }}
        >
          <option value="">
            Escolher modelo...
          </option>
          <option value="internet">
            Serviço acessível pela Internet
          </option>
          <option value="internal">
            Somente rede interna
          </option>
          <option value="critical">
            Ativo/serviço crítico
          </option>
          <option value="none">
            Sem observação
          </option>
        </select>
        <small>
          O texto é apenas um ponto de partida e deve ser ajustado aos fatos reais.
        </small>
      </div>

      <div className="field">
        <label htmlFor="assessment-description">
          Observação opcional
        </label>
        <textarea
          id="assessment-description"
          value={description}
          onChange={(event) =>
            setDescription(
              event.target.value,
            )
          }
          rows={4}
          maxLength={4000}
          placeholder="Ex.: serviço financeiro exposto apenas pela rede interna."
        />
      </div>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}

      <button
        className="button button--primary"
        type="submit"
        disabled={
          pending ||
          environments.length === 0
        }
      >
        {pending
          ? "Criando..."
          : "Criar e continuar para evidências"}
      </button>
    </form>
  );
}
