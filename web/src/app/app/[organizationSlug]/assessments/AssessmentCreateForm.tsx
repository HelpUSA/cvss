"use client";

import {
  useMemo,
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

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

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

      router.push(
        `/app/${organizationSlug}/assessments/${payload.assessment.id}`,
      );
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Falha inesperada.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <form
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
        <label htmlFor="assessment-title">
          Nome da avaliação
        </label>
        <input
          id="assessment-title"
          value={title}
          onChange={(event) =>
            setTitle(event.target.value)
          }
          placeholder="Ex.: CVE no ERP de Produção"
          minLength={2}
          maxLength={120}
          required
        />
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
