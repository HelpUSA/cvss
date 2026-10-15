import type { Metadata, Viewport } from "next";
import "./globals.css";

const siteUrl = "https://cvss.helpusbr.com";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: "HelpUS CVSS",
  title: {
    default: "HelpUS CVSS | Contextualização ambiental CVSS v4.0",
    template: "%s | HelpUS CVSS",
  },
  description:
    "Aplique contexto ambiental ao CVSS v4.0 com fluxo guiado, evidências rastreáveis e cálculo determinístico sem sobrescrever o vetor de origem.",
  keywords: [
    "CVSS",
    "vulnerability management",
    "cybersecurity",
    "environmental metrics",
    "CVSS-BE",
    "vulnerability severity",
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
    title: "HelpUS CVSS — contextualização ambiental CVSS v4.0",
    description:
      "Preserve o CVSS-B de origem, registre evidências do ambiente e acompanhe resultados CVSS ambientais com rastreabilidade.",
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: "HelpUS CVSS — contextualização ambiental CVSS v4.0",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "HelpUS CVSS — CVSS v4.0 ambiental",
    description:
      "CVSS-B preservado, contexto ambiental e evidências em um fluxo guiado e auditável.",
    images: ["/opengraph-image"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
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
