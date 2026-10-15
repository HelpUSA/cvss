export function CvssEvidenceHelp() {
  return (
    <section className="panel cvss-evidence-help">
      <span className="section-kicker">
        Como decidir sem adivinhar
      </span>
      <h2>
        Preencha apenas o que você consegue sustentar com evidência.
      </h2>

      <div className="cvss-evidence-help__grid">
        <details open>
          <summary>
            Vetor CVSS-B de origem
          </summary>
          <p>
            Copie o vetor publicado pela fonte responsável pela vulnerabilidade.
            Não altere o vetor Base para representar sua rede, controles ou
            criticidade interna.
          </p>
        </details>

        <details>
          <summary>
            Reachability / Modified Attack Vector
          </summary>
          <p>
            Informe como o sistema vulnerável realmente pode ser alcançado no
            seu ambiente. Se a topologia ainda não foi verificada, mantenha
            “Ainda não avaliei”.
          </p>
        </details>

        <details>
          <summary>
            Qualidade e frescor da evidência
          </summary>
          <p>
            Marque a evidência como suficiente somente quando a informação puder
            ser verificada e estiver dentro da janela de validade definida para
            aquela telemetria.
          </p>
        </details>

        <details>
          <summary>
            O que significa ABSTAIN?
          </summary>
          <p>
            ABSTAIN não é erro de cálculo. Significa que o sistema preferiu não
            afirmar uma métrica ambiental sem base suficiente. O CVSS-B de origem
            continua preservado.
          </p>
        </details>
      </div>

      <p className="cvss-evidence-help__note">
        Regra prática: desconhecido deve permanecer desconhecido até existir
        evidência. O sistema não precisa “preencher tudo” para ser útil.
      </p>
    </section>
  );
}
