"use client";

import {
  useState,
} from "react";

type DemoResult = {
  success?: boolean;
  mode?: string;
  persisted?: boolean;
  cveId?: string;
  sourceAssessment?: {
    score?: number;
    vector?: string;
    nomenclature?: string;
  };
  environmentalAssessment?:
    | {
        score: number;
        vector: string;
        nomenclature: string;
        decision: string;
      }
    | {
        status: "ABSTAINED";
        reasons: string[];
      };
  inferenceAnalysis?: {
    abstentionReasons?: string[];
    candidateMetrics?: Record<
      string,
      string
    >;
  };
  error?: string;
};

export function EnvironmentSimulator() {
  const [cveId, setCveId] =
    useState("CVE-2024-4251");

  const [
    baseVector,
    setBaseVector,
  ] = useState(
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
  );

  const [provider, setProvider] =
    useState("CNA_PUBLISHED");

  const [
    reachability,
    setReachability,
  ] = useState(
    "INTERNAL_ROUTED",
  );

  const [
    evidenceQuality,
    setEvidenceQuality,
  ] = useState("SUFFICIENT");

  const [
    telemetryAgeDays,
    setTelemetryAgeDays,
  ] = useState("0");

  const [loading, setLoading] =
    useState(false);

  const [result, setResult] =
    useState<DemoResult | null>(
      null,
    );

  async function runAnalysis() {
    setLoading(true);
    setResult(null);

    try {
      const response =
        await fetch(
          "/api/analyze-environment",
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify({
              cveId,
              baseVector,
              sourceAssessmentMeta: {
                provider,
              },
              evidence: {
                evidenceQuality,
                telemetryAgeDays:
                  Number(
                    telemetryAgeDays,
                  ),
                telemetryProfile:
                  "dynamic",
                maxTelemetryAgeDays:
                  1,
                reachability,
              },
            }),
          },
        );

      const payload =
        await response.json();

      setResult(payload);
    } catch (error) {
      setResult({
        error:
          error instanceof Error
            ? error.message
            : "Falha inesperada.",
      });
    } finally {
      setLoading(false);
    }
  }

  const abstained =
    result?.environmentalAssessment &&
    "status" in
      result.environmentalAssessment;

  return (
    <section
      className="panel"
      style={{
        marginTop: "1.5rem",
      }}
    >
      <div className="section-heading">
        <div>
          <span className="section-kicker">
            Demo stateless
          </span>
          <h2>
            Teste o fluxo em poucos campos
          </h2>
        </div>
        <p>
          Esta demonstração não cria
          organização, avaliação ou
          histórico. Para uso real, entre
          no workspace.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gap: "1rem",
        }}
      >
        <div className="field">
          <label htmlFor="demo-cve">
            1. CVE
          </label>
          <input
            id="demo-cve"
            value={cveId}
            onChange={(event) =>
              setCveId(
                event.target.value
                  .toUpperCase(),
              )
            }
          />
        </div>

        <div className="field">
          <label htmlFor="demo-vector">
            2. Vetor CVSS-B de origem
          </label>
          <textarea
            id="demo-vector"
            rows={3}
            value={baseVector}
            onChange={(event) =>
              setBaseVector(
                event.target.value,
              )
            }
          />
          <small>
            Copie o vetor publicado pela
            fonte. O score de origem será
            preservado.
          </small>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "1rem",
          }}
        >
          <div className="field">
            <label htmlFor="demo-provider">
              Fonte
            </label>
            <select
              id="demo-provider"
              value={provider}
              onChange={(event) =>
                setProvider(
                  event.target.value,
                )
              }
            >
              <option value="CNA_PUBLISHED">
                CNA / fornecedor
              </option>
              <option value="NVD_INDEXED">
                NVD
              </option>
              <option value="OTHER_AUTHORITATIVE">
                Outra fonte
              </option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="demo-reachability">
              3. Alcançabilidade
            </label>
            <select
              id="demo-reachability"
              value={reachability}
              onChange={(event) =>
                setReachability(
                  event.target.value,
                )
              }
            >
              <option value="PUBLIC_ROUTED">
                Internet / rede pública
              </option>
              <option value="INTERNAL_ROUTED">
                Rede interna roteada
              </option>
              <option value="ADJACENT_ONLY">
                Rede adjacente
              </option>
              <option value="LOCAL_ONLY">
                Local
              </option>
              <option value="PHYSICAL_ONLY">
                Físico
              </option>
              <option value="UNKNOWN">
                Não sei
              </option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="demo-quality">
              Qualidade da evidência
            </label>
            <select
              id="demo-quality"
              value={evidenceQuality}
              onChange={(event) =>
                setEvidenceQuality(
                  event.target.value,
                )
              }
            >
              <option value="SUFFICIENT">
                Suficiente
              </option>
              <option value="INSUFFICIENT">
                Incompleta
              </option>
              <option value="CONFLICTING">
                Conflitante
              </option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="demo-age">
              Idade da evidência (dias)
            </label>
            <input
              id="demo-age"
              type="number"
              min="0"
              step="0.01"
              value={telemetryAgeDays}
              onChange={(event) =>
                setTelemetryAgeDays(
                  event.target.value,
                )
              }
            />
          </div>
        </div>

        <button
          className="button button--primary"
          type="button"
          disabled={loading}
          onClick={runAnalysis}
        >
          {loading
            ? "Calculando..."
            : "4. Executar demonstração"}
        </button>
      </div>

      {result ? (
        <div
          className="panel"
          style={{
            marginTop: "1.5rem",
          }}
        >
          <span className="section-kicker">
            Resultado
          </span>

          {result.error ? (
            <>
              <h3>
                Não foi possível calcular
              </h3>
              <p>{result.error}</p>
            </>
          ) : abstained ? (
            <>
              <h3>
                ABSTAIN — evidência
                insuficiente para afirmar o
                contexto
              </h3>
              <p>
                O score Base permanece
                disponível. Corrija as
                evidências antes de tentar
                contextualizar.
              </p>
              <pre
                style={{
                  whiteSpace:
                    "pre-wrap",
                }}
              >
                {JSON.stringify(
                  result
                    .inferenceAnalysis
                    ?.abstentionReasons ??
                    [],
                  null,
                  2,
                )}
              </pre>
            </>
          ) : (
            <>
              <h3>
                CVSS-B{" "}
                {result.sourceAssessment
                  ?.score?.toFixed(1)}
                {" → "}
                {
                  (
                    result.environmentalAssessment as {
                      score: number;
                    }
                  )?.score?.toFixed(1)
                }
              </h3>
              <p>
                O vetor de origem não foi
                sobrescrito. O resultado
                contextual é apresentado
                separadamente.
              </p>
              <pre
                style={{
                  whiteSpace:
                    "pre-wrap",
                  overflowWrap:
                    "anywhere",
                }}
              >
                {
                  (
                    result.environmentalAssessment as {
                      vector: string;
                    }
                  )?.vector
                }
              </pre>
            </>
          )}
        </div>
      ) : null}
    </section>
  );
}
