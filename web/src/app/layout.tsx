import type { Metadata, Viewport } from "next";
import "./globals.css";

const siteUrl = "https://cvss.helpusbr.com";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: "HelpUS CVSS",
  title: {
    default: "HelpUS CVSS | Priorização contextual de vulnerabilidades",
    template: "%s | HelpUS CVSS",
  },
  description:
    "Compare CVSS oficial, evidências ambientais e priorização contextual sem alterar o score oficial da vulnerabilidade.",
  keywords: [
    "CVSS",
    "vulnerability management",
    "cybersecurity",
    "risk prioritization",
    "environmental score",
    "contextual prioritization",
    "HelpUS",
  ],
  alternates: {
    canonical: "/",
  },
  manifest: "/manifest.webmanifest",
  openGraph: {
    type: "website",
    url: siteUrl,
    locale: "pt_BR",
    siteName: "HelpUS CVSS",
    title: "HelpUS CVSS — contexto sem distorcer o score oficial",
    description:
      "Transforme evidências ambientais em decisões de priorização rastreáveis, mantendo o CVSS oficial separado do contexto operacional.",
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: "HelpUS CVSS — priorização contextual de vulnerabilidades",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "HelpUS CVSS — priorização contextual",
    description:
      "CVSS oficial, contexto operacional e evidências em uma experiência auditável.",
    images: ["/opengraph-image"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  colorScheme: "dark",
  themeColor: "#07111f",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
