import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "CVSS Environmental Dashboard", description: "AI Bridge / Watcher dashboard for CVSS Environmental evidence and before-after assessment runs" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
