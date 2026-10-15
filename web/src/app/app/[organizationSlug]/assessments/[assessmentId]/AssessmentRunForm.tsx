"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";
import {
  validateCvss40VectorInput,
} from "@/lib/cvss-vector-validation";

type ReusableEvidence = {
  id: string;
  sourceType: string;
  sourceReference: string | null;
  capturedAt: string;
  expiresAt: string | null;
  canonicalHash: string;
  reachability: string;
  evidenceQuality: string;
  firewallActive: boolean;
  maxTelemetryAgeDays: number;
};

type ActivePolicy = {
  id: string;
  policyId: string;
  version: string;
  effectiveFrom: string | null;
};

type Props = {
  organizationSlug: string;
  projectId: string;
  environmentId: string;
  assessmentId: string;
  cveId: string;
  reusableEvidence: ReusableEvidence[];
  activePolicies: ActivePolicy[];
};

export function AssessmentRunForm({
  organizationSlug,
  projectId,
  environmentId,
  assessmentId,
  cveId,
  reusableEvidence,
  activePolicies,
}: Props) {
  const router = useRouter();

  const [baseVector, setBaseVector] =
    useState("");

  const [provider, setProvider] =
    useState("CNA_PUBLISHED");

  const [
    reusedEvidenceSnapshotId,
    setReusedEvidenceSnapshotId,
  ] = useState("");

  const [sourceReference, setSourceReference] =
    useState("");

  const [capturedAt, setCapturedAt] =
    useState("");

  const [reachability, setReachability] =
    useState("UNKNOWN");

  const [evidenceQuality, setEvidenceQuality] =
    useState("UNKNOWN");

  const [
    telemetryAgeDays,
    setTelemetryAgeDays,
  ] = useState("");

  const [
    maxTelemetryAgeDays,
    setMaxTelemetryAgeDays,
  ] = useState("1");

  const [
    firewallActive,
    setFirewallActive,
  ] = useState(false);

  const [cr, setCr] =
    useState("X");

  const [ir, setIr] =
    useState("X");

  const [ar, setAr] =
    useState("X");

  const [
    selectedPolicyId,
    setSelectedPolicyId,
  ] = useState("");

  const [exploitMaturity, setExploitMaturity] =
    useState("X");

  const [
    threatIntelReference,
    setThreatIntelReference,
  ] = useState("");

  const [
    threatIntelObservedAt,
    setThreatIntelObservedAt,
  ] = useState("");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const vectorValidation =
    validateCvss40VectorInput(baseVector);

  function applyReusableEvidence(
    snapshotId: string,
  ) {
    setReusedEvidenceSnapshotId(
      snapshotId,
    );

    if (!snapshotId) {
      return;
    }

    const snapshot =
      reusableEvidence.find(
        (item) => item.id === snapshotId,
      );

    if (!snapshot) {
      return;
    }

    const captured =
      new Date(snapshot.capturedAt);

    const ageDays =
      Math.max(
        0,
        (Date.now() - captured.getTime()) /
          86_400_000,
      );

    setReachability(
      snapshot.reachability,
    );
    setEvidenceQuality(
      snapshot.evidenceQuality,
    );
    setFirewallActive(
      snapshot.firewallActive,
    );
    setMaxTelemetryAgeDays(
      String(
        snapshot.maxTelemetryAgeDays,
      ),
    );
    setTelemetryAgeDays(
      ageDays.toFixed(2),
    );
    setSourceReference(
      snapshot.sourceReference ?? "",
    );
    setCapturedAt(
      snapshot.capturedAt.slice(0, 16),
    );
  }

  async function submit(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!vectorValidation.valid) {
      setMessage(
        vectorValidation.errors[0] ||
          "Vetor CVSS v4.0 inválido.",
      );
      return;
    }

    const securityRequirementsUsed =
      [cr, ir, ar].some(
        (value) => value !== "X",
      );

    const selectedPolicy =
      activePolicies.find(
        (policy) =>
          policy.id === selectedPolicyId,
      );

    const threatMetricUsed =
      exploitMaturity !== "X";

    if (
      threatMetricUsed &&
      !threatIntelReference.trim()
    ) {
      setMessage(
        "Informe a referência de threat intelligence para definir Exploit Maturity (E).",
      );
      return;
    }

    if (
      threatMetricUsed &&
      !threatIntelObservedAt.trim()
    ) {
      setMessage(
        "Informe quando a threat intelligence foi observada para definir Exploit Maturity (E).",
      );
      return;
    }

    if (
      securityRequirementsUsed &&
      !selectedPolicy
    ) {
      setMessage(
        "Selecione uma política organizacional ativa antes de definir CR/IR/AR.",
      );
      return;
    }

    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/projects/${encodeURIComponent(
          projectId,
        )}/environments/${encodeURIComponent(
          environmentId,
        )}/assessments/${encodeURIComponent(
          assessmentId,
        )}/runs`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            cveId,
            baseVector:
              baseVector.trim(),
            sourceAssessmentMeta: {
              provider,
              ...(sourceReference.trim()
                ? {
                    sourceReference:
                      sourceReference.trim(),
                  }
                : {}),
            },
            sourceType:
              reusedEvidenceSnapshotId
                ? "GUIDED_REUSE"
                : "GUIDED_MANUAL_INPUT",
            reusedEvidenceSnapshotId:
              reusedEvidenceSnapshotId ||
              undefined,
            sourceReference:
              sourceReference.trim() ||
              undefined,
            capturedAt:
              capturedAt.trim()
                ? new Date(
                    capturedAt,
                  ).toISOString()
                : new Date().toISOString(),
            evidence: {
              evidenceQuality,
              ...(threatMetricUsed
                ? {
                    threatIntelligence: {
                      exploitMaturity,
                      sourceReference:
                        threatIntelReference.trim(),
                      observedAt:
                        new Date(
                          threatIntelObservedAt,
                        ).toISOString(),
                    },
                  }
                : {}),
              ...(securityRequirementsUsed &&
              selectedPolicy
                ? {
                    organizationPolicyId:
                      selectedPolicy.policyId,
                    policyVersion:
                      selectedPolicy.version,
                    securityRequirements: {
                      CR: cr,
                      IR: ir,
                      AR: ar,
                    },
                  }
                : {}),
              telemetryAgeDays:
                telemetryAgeDays.trim() === ""
                  ? null
                  : Number(telemetryAgeDays),
              maxTelemetryAgeDays:
                maxTelemetryAgeDays.trim() === ""
                  ? null
                  : Number(maxTelemetryAgeDays),
              telemetryProfile:
                "dynamic",
              reachability,
              firewallActive,
            },
          }),
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            payload?.error ??
            "A execução não pôde ser concluída.",
        );
      }

      router.push(
        `/app/${organizationSlug}/assessments/${assessmentId}/runs/${payload.run.id}`,
      );
      router.refresh();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Falha inesperada.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <form
      className="management-form"
      onSubmit={submit}
    >
      <div
        className="panel"
        style={{
          marginBottom: "1rem",
        }}
      >
        <span className="section-kicker">
          Etapa 4 de 5
        </span>
        <h2>
          Informe origem e evidências
        </h2>
        <p>
          A FIRST separa o score Base do
          contexto do consumidor. Aqui você
          preserva o vetor CVSS-B publicado
          e descreve somente fatos
          observáveis do ambiente.
        </p>
      </div>

      <div className="field">
        <label htmlFor="source-provider">
          Fonte do vetor
        </label>
        <select
          id="source-provider"
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
            Outra fonte autoritativa
          </option>
        </select>
        <small>
          Use o vetor publicado pela fonte;
          não o altere para representar o
          seu ambiente.
        </small>
      </div>

      <details className="panel">
        <summary>
          Reutilizar evidência existente (opcional)
        </summary>
        <p>
          Somente evidências do mesmo ambiente
          aparecem aqui. A seleção serve como
          ponto de partida; a nova execução
          cria um novo snapshot e preserva o
          original.
        </p>

        <div className="field">
          <label htmlFor="reuse-evidence">
            Snapshot preservado
          </label>
          <select
            id="reuse-evidence"
            value={reusedEvidenceSnapshotId}
            onChange={(event) =>
              applyReusableEvidence(
                event.target.value,
              )
            }
          >
            <option value="">
              Não reutilizar
            </option>
            {reusableEvidence.map(
              (snapshot) => {
                const expired =
                  snapshot.expiresAt !== null &&
                  new Date(
                    snapshot.expiresAt,
                  ).getTime() < Date.now();

                return (
                  <option
                    key={snapshot.id}
                    value={snapshot.id}
                    disabled={expired}
                  >
                    {snapshot.sourceReference ??
                      snapshot.sourceType}
                    {" · "}
                    {new Date(
                      snapshot.capturedAt,
                    ).toLocaleString(
                      "pt-BR",
                    )}
                    {expired
                      ? " · expirada"
                      : ""}
                  </option>
                );
              },
            )}
          </select>
          <small>
            Evidências expiradas aparecem
            apenas para contexto histórico e
            não podem ser selecionadas.
          </small>
        </div>
      </details>

      <details className="panel evidence-provenance-panel">
        <summary>
          Provenance da fonte (opcional)
        </summary>
        <p>
          Registre a referência original e,
          quando necessário, o momento em que
          a evidência foi capturada. Esses
          dados são preservados no snapshot,
          mas não alteram o score por si só.
        </p>

        <div className="field">
          <label htmlFor="source-reference">
            URL, advisory ou referência
          </label>
          <input
            id="source-reference"
            value={sourceReference}
            onChange={(event) =>
              setSourceReference(
                event.target.value,
              )
            }
            placeholder="https://... ou ADV-2026-001"
            maxLength={1000}
            autoComplete="off"
          />
        </div>

        <div className="field">
          <label htmlFor="captured-at">
            Capturada em
          </label>
          <input
            id="captured-at"
            type="datetime-local"
            value={capturedAt}
            onChange={(event) =>
              setCapturedAt(
                event.target.value,
              )
            }
          />
          <small>
            Deixe em branco para registrar o
            horário da execução.
          </small>
        </div>
      </details>

      <div className="field">
        <label htmlFor="base-vector">
          Vetor CVSS v4.0 de origem
        </label>
        <textarea
          id="base-vector"
          rows={3}
          value={baseVector}
          onChange={(event) =>
            setBaseVector(
              event.target.value,
            )
          }
          placeholder="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
          required
          aria-invalid={
            baseVector.trim() !== "" &&
            !vectorValidation.valid
          }
        />
        {baseVector.trim() !== "" ? (
          vectorValidation.valid ? (
            <small className="vector-validation vector-validation--ok">
              Vetor válido · {vectorValidation.nomenclature}
            </small>
          ) : (
            <small
              className="vector-validation vector-validation--error"
              role="alert"
            >
              {vectorValidation.errors[0]}
            </small>
          )
        ) : null}
        <small>
          Este é o CVSS-B de referência.
          O resultado contextual será
          exibido separadamente.
        </small>
      </div>

      <div className="field">
        <label htmlFor="reachability">
          Como o sistema vulnerável pode ser
          alcançado no seu ambiente?
        </label>
        <select
          id="reachability"
          value={reachability}
          onChange={(event) =>
            setReachability(
              event.target.value,
            )
          }
        >
          <option value="UNKNOWN">
            Ainda não avaliei
          </option>
          <option value="PUBLIC_ROUTED">
            Internet / rede pública roteada
          </option>
          <option value="INTERNAL_ROUTED">
            Rede interna roteada
          </option>
          <option value="ADJACENT_ONLY">
            Apenas rede adjacente
          </option>
          <option value="LOCAL_ONLY">
            Apenas acesso local
          </option>
          <option value="PHYSICAL_ONLY">
            Apenas acesso físico
          </option>
        </select>
        <small>
          Esta evidência pode sustentar uma
          decisão de Modified Attack Vector.
          Se não houver evidência suficiente,
          mantenha “Ainda não avaliei”.
        </small>
      </div>

      <div className="field">
        <label htmlFor="evidence-quality">
          Qualidade da evidência
        </label>
        <select
          id="evidence-quality"
          value={evidenceQuality}
          onChange={(event) =>
            setEvidenceQuality(
              event.target.value,
            )
          }
        >
          <option value="UNKNOWN">
            Ainda não avaliei
          </option>
          <option value="SUFFICIENT">
            Suficiente e verificável
          </option>
          <option value="INSUFFICIENT">
            Incompleta
          </option>
          <option value="CONFLICTING">
            Há conflito entre fontes
          </option>
        </select>
        <small>
          Evidência incompleta ou conflitante
          pode levar o motor a ABSTAIN, em
          vez de criar uma métrica sem base.
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
          <label htmlFor="telemetry-age">
            Idade da evidência (dias)
          </label>
          <input
            id="telemetry-age"
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

        <div className="field">
          <label htmlFor="telemetry-max-age">
            Validade máxima (dias)
          </label>
          <input
            id="telemetry-max-age"
            type="number"
            min="0.01"
            step="0.01"
            value={maxTelemetryAgeDays}
            onChange={(event) =>
              setMaxTelemetryAgeDays(
                event.target.value,
              )
            }
            required
          />
        </div>
      </div>

      <details className="panel advanced-security-requirements">
        <summary>
          Requisitos de Segurança do ambiente (avançado)
        </summary>
        <p>
          CR, IR e AR representam a importância
          da confidencialidade, integridade e
          disponibilidade do sistema vulnerável
          neste ambiente. Se a organização não
          definiu esses requisitos por política,
          mantenha X (Não definido).
        </p>

        <div className="field">
          <label htmlFor="security-policy">
            Política organizacional
          </label>
          <select
            id="security-policy"
            value={selectedPolicyId}
            onChange={(event) =>
              setSelectedPolicyId(
                event.target.value,
              )
            }
          >
            <option value="">
              Nenhuma política selecionada
            </option>
            {activePolicies.map(
              (policy) => (
                <option
                  key={policy.id}
                  value={policy.id}
                >
                  {policy.policyId}
                  {" · v"}
                  {policy.version}
                </option>
              ),
            )}
          </select>
          <small>
            Obrigatória somente se algum de
            CR/IR/AR for diferente de X.
          </small>
        </div>

        <div className="advanced-security-requirements__grid">
          {[
            {
              id: "security-cr",
              label: "Confidencialidade (CR)",
              value: cr,
              setValue: setCr,
            },
            {
              id: "security-ir",
              label: "Integridade (IR)",
              value: ir,
              setValue: setIr,
            },
            {
              id: "security-ar",
              label: "Disponibilidade (AR)",
              value: ar,
              setValue: setAr,
            },
          ].map((metric) => (
            <div
              className="field"
              key={metric.id}
            >
              <label htmlFor={metric.id}>
                {metric.label}
              </label>
              <select
                id={metric.id}
                value={metric.value}
                onChange={(event) =>
                  metric.setValue(
                    event.target.value,
                  )
                }
              >
                <option value="X">
                  X — Não definido
                </option>
                <option value="H">
                  H — Alto
                </option>
                <option value="M">
                  M — Médio
                </option>
                <option value="L">
                  L — Baixo
                </option>
              </select>
            </div>
          ))}
        </div>

        <p className="advanced-security-requirements__note">
          Esses valores descrevem a criticidade
          do sistema vulnerável, não a
          vulnerabilidade em si. A seleção não
          deve ser usada para compensar controles
          técnicos ou alterar o vetor Base.
        </p>
      </details>

      <label
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: ".75rem",
          padding: "1rem",
          border: "1px solid var(--border)",
          borderRadius:
            "var(--radius-sm)",
        }}
      >
        <input
          type="checkbox"
          checked={firewallActive}
          onChange={(event) =>
            setFirewallActive(
              event.target.checked,
            )
          }
        />
        <span>
          <strong>
            Há firewall/WAF registrado na
            evidência
          </strong>
          <small
            style={{
              display: "block",
              color:
                "var(--text-muted)",
            }}
          >
            Isto é registrado como contexto.
            A presença isolada do controle
            não altera automaticamente MAC
            ou outra métrica CVSS.
          </small>
        </span>
      </label>

      {message ? (
        <p
          className="management-feedback"
          role="alert"
        >
          {message}
        </p>
      ) : null}

      <button
        className="button button--primary"
        type="submit"
        disabled={
          pending ||
          (baseVector.trim() !== "" && !vectorValidation.valid)
        }
      >
        {pending
          ? "Executando..."
          : "Executar e ver resultado"}
      </button>
    </form>
  );
}
