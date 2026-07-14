import { ImageResponse } from "next/og";

export const alt =
  "HelpUS CVSS — priorização contextual de vulnerabilidades";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          padding: "74px",
          flexDirection: "column",
          justifyContent: "space-between",
          background:
            "radial-gradient(circle at 10% 0%, #0c6f8c 0%, transparent 44%), linear-gradient(135deg, #07111f 0%, #030812 100%)",
          color: "#f5f9ff",
          fontFamily: "Arial, sans-serif",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "18px",
            fontSize: "26px",
            fontWeight: 700,
          }}
        >
          <div
            style={{
              width: "58px",
              height: "58px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: "2px solid #59d7ff",
              borderRadius: "18px",
              color: "#59d7ff",
            }}
          >
            H
          </div>
          HelpUS CVSS
        </div>

        <div
          style={{
            display: "flex",
            maxWidth: "1010px",
            flexDirection: "column",
            gap: "24px",
          }}
        >
          <div
            style={{
              color: "#59d7ff",
              fontSize: "24px",
              fontWeight: 700,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
            }}
          >
            Contextual Risk Intelligence
          </div>

          <div
            style={{
              fontSize: "72px",
              fontWeight: 800,
              lineHeight: 1.02,
              letterSpacing: "-0.045em",
            }}
          >
            Contexto operacional sem distorcer o CVSS oficial.
          </div>

          <div
            style={{
              color: "#b6c5d6",
              fontSize: "28px",
            }}
          >
            Evidências, prioridade e auditoria em uma única experiência.
          </div>
        </div>
      </div>
    ),
    size,
  );
}
