"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import {
  authClient,
} from "@/lib/auth-client";

export function SignOutButton() {
  const router = useRouter();

  const [pending, setPending] =
    useState(false);

  async function signOut() {
    if (pending) {
      return;
    }

    setPending(true);

    try {
      await authClient.signOut();
    } finally {
      router.replace("/login");
      router.refresh();
      setPending(false);
    }
  }

  return (
    <button
      className="operational-signout"
      type="button"
      onClick={signOut}
      disabled={pending}
    >
      {pending ? "Saindo..." : "Sair"}
    </button>
  );
}
