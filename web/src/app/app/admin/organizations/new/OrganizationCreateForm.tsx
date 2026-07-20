"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type Feedback = {
  tone: "success" | "error";
  message: string;
};

export function OrganizationCreateForm() {
  const router = useRouter();

  const [name, setName] =
    useState("");

  const [slug, setSlug] =
    useState("");

  const [pending, setPending] =
    useState(false);

  const [feedback, setFeedback] =
    useState<Feedback | null>(null);

  async function submit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setFeedback(null);

    try {
      const response = await fetch(
        "/api/platform/organizations",
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
            "A organização não pôde ser criada.",
        );
      }

      setFeedback({
        tone: "success",
        message:
          "Organização criada com sucesso.",
      });

      router.push(
        `/app/${payload.organization.slug}`,
      );

      router.refresh();
    } catch (error) {
      setFeedback({
        tone: "error",

        message:
          error instanceof Error
            ? error.message
            : "Falha inesperada.",
      });
    } finally {
      setPending(false);
    }
  }

  return (
    <form
      className="management-form"
      onSubmit={submit}
    >
      <div className="field">
        <label htmlFor="organization-name">
          Nome
        </label>

        <input
          id="organization-name"
          value={name}
          onChange={(event) =>
            setName(event.target.value)
          }
          minLength={2}
          maxLength={120}
          required
          autoComplete="organization"
        />
      </div>

      <div className="field">
        <label htmlFor="organization-slug">
          Slug
        </label>

        <input
          id="organization-slug"
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
          autoComplete="off"
        />
      </div>

      {feedback ? (
        <p
          className={
            `management-feedback ` +
            `management-feedback--${feedback.tone}`
          }
          role="status"
        >
          {feedback.message}
        </p>
      ) : null}

      <button
        className="button button--primary"
        type="submit"
        disabled={pending}
      >
        {pending
          ? "Criando..."
          : "Criar organização"}
      </button>
    </form>
  );
}
