import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
    },
    sitemap: "https://cvss.helpusbr.com/sitemap.xml",
    host: "https://cvss.helpusbr.com",
  };
}
