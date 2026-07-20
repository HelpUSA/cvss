"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

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

      setName("");
      setSlug("");
      setMessage(
        "Projeto criado com sucesso.",
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
  );
}
