import type { Metadata } from "next";
import { getDashboardData } from "@/lib/data";
import { DashboardClient } from "../DashboardClient";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Laboratório Interativo & Demonstração CVSS v4.0 — HelpUS",
  description:
    "Console operacional completo de demonstração da contextualização ambiental FIRST CVSS v4.0, telemetria, simulador de 5 camadas, explorador de riscos e governança HITL.",
};

export default async function DemoPage() {
  const data = await getDashboardData();

  return <DashboardClient data={data} />;
}
