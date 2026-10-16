"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type CreatedProject = {
  id: string;
  name: string;
  slug: string;
  status: string;
};

export function ProjectCreateForm({
  organizationSlug,
}: {
  organizationSlug: string;
}) {
  const router = useRouter();

  const [name, setName] =
    useState("");

  const [slug, setSlug] =
    useState("");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [
    createdProjects,
    setCreatedProjects,
  ] = useState<CreatedProject[]>([]);

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
        )}/projects`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
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
            "O projeto não pôde ser criado.",
        );
      }

      if (payload?.project) {
        setCreatedProjects((prev) => [
          payload.project as CreatedProject,
          ...prev.filter(
            (item) =>
              item.id !==
              payload.project.id,
          ),
        ]);
      }

      setName("");
      setSlug("");
      setMessage(
        "Projeto criado com sucesso.",
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
          <label htmlFor="project-name">
            Nome do projeto
          </label>

          <input
            id="project-name"
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
          <label htmlFor="project-slug">
            Slug
          </label>

          <input
            id="project-slug"
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
          disabled={pending}
        >
          {pending
            ? "Criando..."
            : "Criar projeto"}
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

      {createdProjects.length > 0 ? (
        <section className="tenant-list">
          {createdProjects.map((project) => (
            <article
              className="tenant-list-card"
              key={project.id}
            >
              <div>
                <span className="section-kicker">
                  Projeto ativo
                </span>

                <h2>{project.name}</h2>

                <code>{project.slug}</code>
              </div>

              <dl>
                <div>
                  <dt>Ambientes</dt>
                  <dd>0</dd>
                </div>

                <div>
                  <dt>Status</dt>
                  <dd>{project.status}</dd>
                </div>
              </dl>
            </article>
          ))}
        </section>
      ) : null}
    </>
  );
}
