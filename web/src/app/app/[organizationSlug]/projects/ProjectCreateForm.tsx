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
  const formRef =
    useRef<HTMLFormElement>(null);

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
    createdProjects,
    setCreatedProjects,
  ] = useState<CreatedProject[]>([]);

  useEffect(() => {
    const syncFromDom = () => {
      const form = formRef.current;
      if (!form) {
        return;
      }
      const nameEl =
        form.querySelector<HTMLInputElement>(
          "#project-name",
        );
      if (nameEl && nameEl.value !== "") {
        setName((prev) =>
          prev === ""
            ? nameEl.value
            : prev,
        );
      }
      const slugEl =
        form.querySelector<HTMLInputElement>(
          "#project-slug",
        );
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
      setSlugManuallyEdited(false);
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
        ref={formRef}
        className="management-form management-form--inline"
        onSubmit={submit}
      >
        <div className="field">
          <label htmlFor="project-template">
            Começar por um modelo (opcional)
          </label>
          <select
            id="project-template"
            defaultValue=""
            onChange={(event) => {
              const value = event.target.value;
              if (!value) return;
              setName(value);
              setSlug(slugify(value));
              setSlugManuallyEdited(false);
            }}
          >
            <option value="">
              Escolher modelo...
            </option>
            <option value="ERP / Aplicação">
              ERP / Aplicação
            </option>
            <option value="Portal / API">
              Portal / API
            </option>
            <option value="Infraestrutura">
              Infraestrutura
            </option>
            <option value="Serviço em nuvem">
              Serviço em nuvem
            </option>
            <option value="Projeto geral">
              Projeto geral
            </option>
          </select>
          <small>
            O modelo apenas preenche um nome inicial; você pode editar.
          </small>
        </div>

        <div className="field">
          <label htmlFor="project-name">
            Nome do projeto
          </label>

          <input
            id="project-name"
            value={name}
            onChange={(event) => {
              const nextName = event.target.value;
              setName(nextName);
              if (!slugManuallyEdited) {
                setSlug(slugify(nextName));
              }
            }}
            minLength={2}
            maxLength={120}
            required
          />
          <small>
            O slug é gerado automaticamente a partir do nome.
          </small>
        </div>

        <div className="field">
          <label htmlFor="project-slug">
            Slug
          </label>

          <input
            id="project-slug"
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
