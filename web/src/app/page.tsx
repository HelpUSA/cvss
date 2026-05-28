import { getDashboardData } from "@/lib/data";
import { DashboardClient } from "./DashboardClient";

export const dynamic = "force-dynamic";

export default async function Home() {
  const data = await getDashboardData();
  const curatedRuns = Array.isArray((data as any).curatedRuns) ? (data as any).curatedRuns : Object.values((data as any).curatedRuns ?? {});
 return (
 <>
 <section className='panel'>
 <h2>Curated validation runs</h2>
 <p>Engineering-validation scenarios generated from deterministic run artifacts.</p>
 <div>{curatedRuns.length} runs</div>
 <ul>{curatedRuns.map((run: any) => <li key={run.run_id}>{run.run_id} findings={run.findings} assessments={run.assessments} downgraded={run.downgraded} unchanged={run.unchanged} upgraded={run.upgraded} mean_delta={run.mean_delta}</li>)}</ul>
 </section>
 <DashboardClient data={data} />
 </>
 );
}

