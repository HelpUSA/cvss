import { getDashboardData } from "@/lib/data";
import { DashboardClient } from "./DashboardClient";

export const dynamic = "force-dynamic";

export default async function Home() {
  const data = await getDashboardData();
  return <DashboardClient data={data} />;
}
