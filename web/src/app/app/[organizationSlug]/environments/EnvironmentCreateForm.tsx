"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type ProjectOption = {
  id: string;
  name: string;
};

export function EnvironmentCreateForm({
  organizationSlug,
  projects,
}: {
  organizationSlug: string;
  projects: ProjectOption[];
}) {
  const router = useRouter();

  const [projectId, setProjectId] =
    useState(
      projects[0]?.id ?? "",
    );

  const [name, setName] =
    useState("");

  const [slug, setSlug] =
    useState("");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function submit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/environments`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            projectId,
            name,
            slug,
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
            "O ambiente não pôde ser criado.",
        );
      }

      setName("");
      setSlug("");
      setMessage(
        "Ambiente criado com sucesso.",
      );

      router.refresh();
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
      className="management-form management-form--inline"
      onSubmit={submit}
    >
      <div className="field">
        <label htmlFor="environment-project">
          Projeto
        </label>

        <select
          id="environment-project"
          value={projectId}
          onChange={(event) =>
            setProjectId(
              event.target.value,
            )
          }
          required
        >
          {projects.map((project) => (
            <option
              value={project.id}
              key={project.id}
            >
              {project.name}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="environment-name">
          Nome do ambiente
        </label>

        <input
          id="environment-name"
          value={name}
          onChange={(event) =>
            setName(event.target.value)
          }
          minLength={2}
          maxLength={120}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="environment-slug">
          Slug
        </label>

        <input
          id="environment-slug"
          value={slug}
          onChange={(event) =>
            setSlug(
              event.target.value
                .toLowerCase(),
            )
          }
          pattern="[a-z0-9]+(?:-[a-z0-9]+)*"
          minLength={2}
          maxLength={80}
          required
        />
      </div>

      <button
        className="button button--primary"
        type="submit"
        disabled={
          pending ||
          projects.length === 0
        }
      >
        {pending
          ? "Criando..."
          : "Criar ambiente"}
      </button>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}
    </form>
  );
}
