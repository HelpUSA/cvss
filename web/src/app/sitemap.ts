import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified =
    new Date("2026-10-14T00:00:00.000Z");

  return [
    {
      url:
        "https://cvss.helpusbr.com/",
      lastModified,
      changeFrequency: "weekly",
      priority: 1,
    },
    {
      url:
        "https://cvss.helpusbr.com/demo",
      lastModified,
      changeFrequency: "monthly",
      priority: 0.6,
    },
  ];
}
