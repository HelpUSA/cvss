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

type CreatedEnvironment = {
  id: string;
  name: string;
  slug: string;
  status: string;
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

  const [
    createdEnvironments,
    setCreatedEnvironments,
  ] = useState<CreatedEnvironment[]>([]);

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

      if (payload?.environment) {
        setCreatedEnvironments((prev) => [
          payload.environment as CreatedEnvironment,
          ...prev.filter(
            (item) =>
              item.id !==
              payload.environment.id,
          ),
        ]);
      }

      setName("");
      setSlug("");
      setMessage(
        "Ambiente criado com sucesso.",
      );
      setPending(false);

      if (typeof window === "undefined") {
        router.refresh();
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
    <>
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

      {createdEnvironments.length > 0 ? (
        <section className="tenant-list">
          {createdEnvironments.map(
            (environment) => (
              <article
                className="tenant-list-card"
                key={environment.id}
              >
                <div>
                  <span className="section-kicker">
                    Ambiente ativo
                  </span>

                  <h2>
                    {environment.name}
                  </h2>

                  <code>
                    {environment.slug}
                  </code>
                </div>

                <dl>
                  <div>
                    <dt>Status</dt>
                    <dd>
                      {environment.status}
                    </dd>
                  </div>
                </dl>
              </article>
            ),
          )}
        </section>
      ) : null}
    </>
  );
}
