import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "HelpUS CVSS",
    short_name: "HelpUS CVSS",
    description:
      "Contextualização ambiental CVSS v4.0 com vetor de origem preservado, evidências rastreáveis e fluxo guiado.",
    start_url: "/",
    display: "standalone",
    background_color: "#07111f",
    theme_color: "#07111f",
    lang: "pt-BR",
    icons: [
      {
        src: "/icon.svg",
        sizes: "any",
        type: "image/svg+xml",
      },
    ],
  };
}
