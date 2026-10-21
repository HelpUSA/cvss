"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

function slugify(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

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
  const formRef =
    useRef<HTMLFormElement>(null);

  const [projectId, setProjectId] =
    useState(
      projects[0]?.id ?? "",
    );

  const [template, setTemplate] =
    useState("");

  const [name, setName] =
    useState("");

  const [slug, setSlug] =
    useState("");

  const [
    slugManuallyEdited,
    setSlugManuallyEdited,
  ] = useState(false);

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [
    createdEnvironments,
    setCreatedEnvironments,
  ] = useState<CreatedEnvironment[]>([]);

  useEffect(() => {
    const syncFromDom = () => {
      const form = formRef.current;
      if (!form) {
        return;
      }
      const projEl =
        form.querySelector<HTMLSelectElement>(
          "#environment-project",
        );
      if (projEl && projEl.value !== "") {
        setProjectId((prev) =>
          prev === projEl.value
            ? prev
            : projEl.value,
        );
      }
      const nameEl =
        form.querySelector<HTMLInputElement>(
          "#environment-name",
        );
      const slugEl =
        form.querySelector<HTMLInputElement>(
          "#environment-slug",
        );
      if (nameEl && nameEl.value !== "") {
        setName((prev) =>
          prev === ""
            ? nameEl.value
            : prev,
        );
        if (!slugEl || slugEl.value === "") {
          setSlug((prev) =>
            prev === ""
              ? slugify(nameEl.value)
              : prev,
          );
        }
      }
      if (slugEl && slugEl.value !== "") {
        const normalized =
          slugEl.value.toLowerCase();
        setSlug((prev) =>
          prev === ""
            ? normalized
            : prev,
        );
      }
    };
    syncFromDom();
    const frame =
      window.requestAnimationFrame(
        syncFromDom,
      );
    return () =>
      window.cancelAnimationFrame(frame);
  }, []);

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

      setTemplate("");
      setName("");
      setSlug("");
      setSlugManuallyEdited(false);
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
        ref={formRef}
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
          <label htmlFor="environment-template">
            Tipo de ambiente (atalho)
          </label>
          <select
            id="environment-template"
            value={template}
            onChange={(event) => {
              const value = event.target.value;
              setTemplate(value);
              if (!value) return;
              setName(value);
              setSlug(slugify(value));
              setSlugManuallyEdited(false);
            }}
          >
            <option value="">
              Escolher tipo...
            </option>
            <option value="Produção">Produção</option>
            <option value="Homologação">Homologação</option>
            <option value="Desenvolvimento">Desenvolvimento</option>
            <option value="DMZ">DMZ</option>
            <option value="Rede interna">Rede interna</option>
            <option value="Cloud / Nuvem">Cloud / Nuvem</option>
          </select>
          <small>
            Selecione um tipo comum ou escreva um nome personalizado abaixo.
          </small>
        </div>

        <div className="field">
          <label htmlFor="environment-name">
            Nome do ambiente
          </label>

          <input
            id="environment-name"
            value={name}
            onChange={(event) => {
              const nextName = event.target.value;
              setName(nextName);
              setTemplate("");
              if (!slugManuallyEdited) {
                setSlug(slugify(nextName));
              }
            }}
            minLength={2}
            maxLength={120}
            required
          />
          <small>
            O slug é gerado automaticamente e continua editável.
          </small>
        </div>

        <div className="field">
          <label htmlFor="environment-slug">
            Slug
          </label>

          <input
            id="environment-slug"
            value={slug}
            onChange={(event) => {
              setSlug(
                event.target.value
                  .toLowerCase(),
              );
              setSlugManuallyEdited(true);
            }}
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
