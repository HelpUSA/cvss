import json
from pathlib import Path

scenarios_path = Path(r"d:\AntiG\cvss\data\synthetic_expert_scenarios.json")
output_path = Path(r"d:\AntiG\cvss\portal-especialistas.html")

scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
# Purgar estritamente qualquer vazamento de resposta ou vetor de referência (Conforme CG-20261013-023 C1)
clean_scenarios = []
for s in scenarios:
    clean_s = {
        "scenario_id": s["scenario_id"],
        "cve_id": s["cve_id"],
        "summary": s["summary"],
        "asset_class": s["asset_class"],
        "deployment_context": s["deployment_context"],
        "controls": s["controls"]
    }
    clean_scenarios.append(clean_s)
scenarios_json_str = json.dumps(clean_scenarios, ensure_ascii=False)

html_content = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portal EDC — Validação Cega de Especialistas (G9) | HelpUS CVSS AI</title>
  <link rel="icon" type="image/jpeg" href="/helpus-logo.jpg">
  <link rel="shortcut icon" type="image/jpeg" href="/helpus-logo.jpg">
  <style>
    :root {{
      --bg-dark: #030712;
      --bg-card: #09101f;
      --bg-card-hover: #0f1c36;
      --border: #1e293b;
      --border-accent: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #0284c7;
      --primary-hover: #0369a1;
      --purple: #8b5cf6;
      --purple-hover: #7c3aed;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
    }}
    header {{
      background: rgba(9, 16, 31, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 24px;
    }}
    .header-inner {{
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: inherit;
    }}
    .brand-wrap img {{
      width: 38px;
      height: 38px;
      border-radius: 8px;
      border: 1px solid var(--border-accent);
    }}
    .brand-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
    }}
    .brand-title span {{
      color: var(--border-accent);
    }}
    .badge-edc {{
      display: inline-block;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(139, 92, 246, 0.2);
      color: #c084fc;
      border: 1px solid rgba(192, 132, 252, 0.4);
      padding: 2px 8px;
      border-radius: 999px;
      margin-left: 6px;
    }}
    .badge-mock {{
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }}
    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .btn {{
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      border: 1px solid transparent;
      transition: all 0.2s ease;
    }}
    .btn-primary {{
      background: var(--primary);
      color: #fff;
      border-color: #38bdf8;
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}
    .btn-purple {{
      background: var(--purple);
      color: #fff;
      border-color: #a855f7;
    }}
    .btn-purple:hover {{
      background: var(--purple-hover);
    }}
    .btn-outline {{
      background: #0b1528;
      border-color: var(--border);
      color: var(--text-muted);
    }}
    .btn-outline:hover {{
      background: #14233f;
      color: #fff;
      border-color: var(--text-muted);
    }}
    .btn-success {{
      background: #059669;
      color: #fff;
      border-color: #34d399;
    }}
    .btn-success:hover {{
      background: #047857;
    }}
    .lang-btn {{
      padding: 6px 12px;
      background: #0f172a;
      border: 1px solid var(--border);
      color: var(--text-main);
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
    }}
    .lang-btn.active {{
      border-color: var(--border-accent);
      color: var(--border-accent);
      font-weight: 700;
    }}
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px 16px 60px;
      width: 100%;
      flex: 1;
    }}
    /* TABS DE ETAPAS */
    .steps-nav {{
      display: flex;
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
      gap: 8px;
    }}
    .step-tab {{
      padding: 12px 20px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .step-tab.active {{
      color: var(--border-accent);
      border-bottom-color: var(--border-accent);
    }}
    .step-tab.completed {{
      color: #34d399;
    }}
    .step-tab-num {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #1e293b;
      font-size: 11px;
    }}
    .step-tab.active .step-tab-num {{
      background: var(--primary);
      color: #fff;
    }}
    .step-tab.completed .step-tab-num {{
      background: #059669;
      color: #fff;
    }}
    /* SEÇÕES DE ETAPA */
    .step-section {{
      display: none;
    }}
    .step-section.active {{
      display: block;
    }}
    /* CARDS */
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
    }}
    .card-title {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    /* ETAPA 1: TERMO TCLE / ICF */
    .tcle-box {{
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 24px;
      max-height: 440px;
      overflow-y: auto;
      font-size: 13px;
      line-height: 1.7;
      color: #cbd5e1;
      margin-bottom: 20px;
    }}
    .tcle-box h2, .tcle-box h3 {{
      color: #38bdf8;
      margin: 16px 0 8px;
    }}
    .tcle-box ul {{
      margin-left: 20px;
      margin-bottom: 12px;
    }}
    .tcle-check-wrap {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #1e3a5f;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
    }}
    .tcle-check-item {{
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 12px;
      cursor: pointer;
    }}
    .tcle-check-item input[type="checkbox"] {{
      margin-top: 4px;
      width: 18px;
      height: 18px;
      cursor: pointer;
    }}
    /* ETAPA 2: AVALIAÇÃO CEGA */
    .adjudication-layout {{
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 20px;
    }}
    @media (max-width: 992px) {{
      .adjudication-layout {{
        grid-template-columns: 1fr;
      }}
    }}
    /* SIDEBAR DO CENÁRIO */
    .scenario-sidebar {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      height: fit-content;
    }}
    .scenario-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 6px;
      margin-top: 12px;
      max-height: 380px;
      overflow-y: auto;
      padding-right: 4px;
    }}
    .scenario-item-btn {{
      padding: 8px 4px;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }}
    .scenario-item-btn:hover {{
      background: #1e293b;
      color: #fff;
    }}
    .scenario-item-btn.active {{
      background: var(--primary);
      border-color: #38bdf8;
      color: #fff;
    }}
    .scenario-item-btn.done {{
      background: rgba(16, 185, 129, 0.2);
      border-color: rgba(52, 211, 153, 0.4);
      color: #34d399;
    }}
    .scenario-item-btn.active.done {{
      background: #059669;
      color: #fff;
    }}
    /* ALERTA DE CEGAMENTO */
    .blinding-shield {{
      background: rgba(139, 92, 246, 0.1);
      border: 1px solid rgba(168, 85, 247, 0.3);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
      color: #e9d5ff;
    }}
    /* DETALHES DO CENÁRIO */
    .scenario-detail-card {{
      background: #050b17;
      border: 1px solid #1e3a5f;
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 20px;
    }}
    .detail-tag {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: #1e293b;
      color: #cbd5e1;
      margin-right: 6px;
    }}
    .tag-asset {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .vector-box {{
      background: #030712;
      border: 1px dashed #334155;
      padding: 8px 12px;
      border-radius: 6px;
      font-family: monospace;
      font-size: 12px;
      color: #38bdf8;
      margin-top: 8px;
      word-break: break-all;
    }}
    /* FORMULÁRIO DE PONTUAÇÃO CVSS */
    .metric-group-card {{
      background: #0a1324;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
    }}
    .metric-group-title {{
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }}
    .metric-field label {{
      display: block;
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
      font-weight: 600;
    }}
    .metric-select {{
      width: 100%;
      background: #030712;
      border: 1px solid #334155;
      color: #f8fafc;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 12px;
      outline: none;
      transition: border 0.2s;
    }}
    .metric-select:focus {{
      border-color: var(--border-accent);
    }}
    /* ETAPA 3: RESUMO E SELAGEM */
    .summary-table-wrap {{
      max-height: 450px;
      overflow-y: auto;
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }}
    th, td {{
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid #1e293b;
    }}
    th {{
      background: #0a1324;
      color: var(--text-muted);
      font-weight: 700;
      position: sticky;
      top: 0;
    }}
    tr:hover td {{
      background: rgba(15, 23, 42, 0.4);
    }}
    .receipt-box {{
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(52, 211, 153, 0.3);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      display: none;
    }}
    /* MÍDIA IMPRESSÃO PARA TCLE */
    @media print {{
      header, .steps-nav, .header-actions, .no-print {{
        display: none !important;
      }}
      body, main, .card, .tcle-box {{
        background: #fff !important;
        color: #000 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
      }}
      .tcle-box {{
        max-height: none !important;
        overflow: visible !important;
      }}
    }}
  </style>
</head>
<body>

<!-- BANNER PERSISTENTE DE DEMONSTRAÇÃO SINTÉTICA (EXIGÊNCIA CG-20261013-023 H1) -->
<div id="syntheticDemoBanner" style="background:#7f1d1d;border-bottom:2px solid #ef4444;color:#fef2f2;padding:10px 16px;text-align:center;font-size:12px;font-weight:700;letter-spacing:0.5px;position:sticky;top:0;z-index:99999;">
  ⚠️ SYNTHETIC DEMONSTRATION — NO REAL PARTICIPANT DATA COLLECTION — G9 PENDING ETHICS APPROVAL
</div>

<header style="top:38px;">
  <div class="header-inner">
    <a href="/" class="brand-wrap" id="brandWrapLink" title="Voltar ao site principal">
      <img src="/helpus-logo.jpg" onerror="this.src='helpus-logo.jpg'; this.onerror=null;" alt="Logo HelpUS">
      <div>
        <div class="brand-title">Help<span>US</span> CVSS <span class="badge-edc">G9 EDC Portal</span><span class="badge-edc badge-mock">Synthetic Demo</span></div>
        <div style="font-size:11px;color:var(--text-muted);" id="headerSub">Portal de Avaliação Cega de Especialistas Independentes</div>
      </div>
    </a>

    <div class="header-actions">
      <!-- Seletor do Avaliador (Simulação) -->
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="font-size:12px;color:var(--text-muted);">Avaliador:</span>
        <select id="expertSelector" onchange="onExpertChange()" style="background:#0f172a;border:1px solid var(--border);color:#38bdf8;padding:5px 8px;border-radius:6px;font-size:12px;font-weight:700;">
          <option value="EXP-01">EXP-01 (AppSec Senior)</option>
          <option value="EXP-02">EXP-02 (SecOps / SOC N3)</option>
          <option value="EXP-03">EXP-03 (CISSP Auditor)</option>
          <option value="EXP-04">EXP-04 (Cloud & OT Specialist)</option>
          <option value="EXP-05">EXP-05 (Adjudicator Lead)</option>
        </select>
      </div>

      <!-- Seletor de Idioma -->
      <div style="display:flex;gap:4px;">
        <button class="lang-btn active" id="btn-lang-pt" onclick="setLanguage('pt')">🇧🇷 PT</button>
        <button class="lang-btn" id="btn-lang-en" onclick="setLanguage('en')">🇺🇸 EN</button>
        <button class="lang-btn" id="btn-lang-es" onclick="setLanguage('es')">🇪🇸 ES</button>
      </div>

      <a href="/" class="btn btn-outline" id="btnBackToSite">← Voltar ao Site</a>
    </div>
  </div>
</header>

<main>
  <!-- NAVEGAÇÃO DE ETAPAS -->
  <div class="steps-nav no-print">
    <div class="step-tab active" id="tab-step-1" onclick="goToStep(1)">
      <span class="step-tab-num">1</span>
      <span id="tabLabel1">Consentimento (e-TCLE / e-ICF)</span>
    </div>
    <div class="step-tab" id="tab-step-2" onclick="goToStep(2)">
      <span class="step-tab-num">2</span>
      <span id="tabLabel2">Avaliação Cega (30 Cenários)</span>
    </div>
    <div class="step-tab" id="tab-step-3" onclick="goToStep(3)">
      <span class="step-tab-num">3</span>
      <span id="tabLabel3">Revisão & Submissão Selada</span>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- ETAPA 1: CONSENTIMENTO ELETRÔNICO (e-TCLE / e-ICF) & COI        -->
  <!-- ============================================================== -->
  <div class="step-section active" id="section-step-1">
    <div class="card">
      <div class="card-title">
        <span id="tcleTitle">Termo de Consentimento Livre e Esclarecido Eletrônico (e-TCLE)</span>
        <button class="btn btn-outline" onclick="window.print()" style="padding:4px 10px;font-size:12px;">🖨️ <span id="btnPrintTerm">Imprimir / Salvar PDF</span></button>
      </div>

      <div class="tcle-box" id="tcleContent">
        <!-- Injetado dinamicamente via JS de acordo com o idioma -->
      </div>

      <div class="tcle-check-wrap">
        <label class="tcle-check-item">
          <input type="checkbox" id="checkConsent">
          <span id="labelConsent">Declaro que li, compreendi integralmente os objetivos, riscos mitigados e procedimentos da pesquisa e <strong>CONCORDO voluntariamente</strong> em participar da avaliação científica como Especialista Avaliador.</span>
        </label>
        <label class="tcle-check-item">
          <input type="checkbox" id="checkCoi">
          <span id="labelCoi">Declaro formalmente <strong>AUSÊNCIA DE CONFLITO DE INTERESSES</strong>, atestando não possuir vínculo empregatício, societário ou de desenvolvimento de código com a HelpUS LLC nos últimos 36 meses.</span>
        </label>
      </div>

      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:12px;color:var(--text-muted);" id="supportNote">Dúvidas sobre o estudo? Contate: <strong style="color:#38bdf8;">pesquisa@helpus.adv.br</strong></span>
        <button class="btn btn-primary" id="btnStartAdjudication" onclick="confirmConsentAndProceed()">🚀 <span id="btnStartText">Iniciar Avaliação Cega (30 Cenários)</span></button>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- ETAPA 2: INTERFACE DE AVALIAÇÃO CEGA (30 CENÁRIOS)            -->
  <!-- ============================================================== -->
  <div class="step-section" id="section-step-2">
    <div class="adjudication-layout">
      <!-- SIDEBAR ESQUERDA: NAVEGAÇÃO DOS 30 CENÁRIOS -->
      <div class="scenario-sidebar">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <strong style="font-size:13px;color:#fff;" id="sidebarNavTitle">Navegador de Cenários</strong>
          <span style="font-size:11px;color:var(--border-accent);font-weight:700;" id="progressSummary">0 / 30</span>
        </div>
        <div style="height:6px;background:#1e293b;border-radius:999px;margin-bottom:12px;overflow:hidden;">
          <div id="progressBar" style="height:100%;width:0%;background:#38bdf8;transition:width 0.3s ease;"></div>
        </div>
        <div class="scenario-grid" id="scenarioGrid">
          <!-- 30 botões de cenário injetados via JS -->
        </div>

        <div style="margin-top:20px;border-top:1px solid var(--border);padding-top:14px;display:flex;flex-direction:column;gap:8px;">
          <button class="btn btn-purple" onclick="goToStep(3)" style="width:100%;justify-content:center;font-size:12px;">📊 <span id="btnGoToReview">Ir para Resumo Final</span></button>
        </div>
      </div>

      <!-- CONTEÚDO PRINCIPAL: AVALIAÇÃO DO CENÁRIO ATUAL -->
      <div class="scenario-workspace">
        <!-- BLINDING BANNER -->
        <div class="blinding-shield">
          <span style="font-size:18px;">🛡️</span>
          <div>
            <strong id="blindShieldTitle">Ambiente Cego Estrito (Blinded Review Protocol)</strong>
            <div style="font-size:11px;opacity:0.9;" id="blindShieldDesc">Zero exposição de predições da IA HelpUS e zero visibilidade das respostas de outros avaliadores. Apenas o pacote técnico do CVE e a topologia estão disponíveis.</div>
          </div>
        </div>

        <!-- CARTÃO TÉCNICO DO CENÁRIO -->
        <div class="scenario-detail-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
            <div>
              <span class="detail-tag tag-asset" id="cardAssetClass">public_web_application</span>
              <span class="detail-tag" id="cardScenarioId">SCN-NVD-001</span>
              <h3 style="display:inline;font-size:17px;color:#fff;margin-left:6px;" id="cardCveId">CVE-2026-4251</h3>
            </div>
            <div style="font-size:12px;color:var(--text-muted);">
              <span id="scenarioIndexBadge">Cenário 1 de 30</span>
            </div>
          </div>

          <p style="font-size:13px;color:#cbd5e1;margin-bottom:12px;line-height:1.6;" id="cardSummary">
            Carregando detalhes técnicos da vulnerabilidade...
          </p>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:12px;background:#030712;padding:12px;border-radius:6px;border:1px solid #16263d;">
            <div>
              <strong style="color:#94a3b8;display:block;margin-bottom:2px;" id="labelContextTitle">Topologia de Implantação:</strong>
              <span style="color:#cbd5e1;" id="cardContext">Ambiente corporativo padrão</span>
            </div>
            <div>
              <strong style="color:#94a3b8;display:block;margin-bottom:2px;" id="labelControlsTitle">Controles Compensatórios:</strong>
              <span style="color:#cbd5e1;" id="cardControls">Firewall, WAF ativo</span>
          </div>
        </div>

        <!-- FORMULÁRIO DAS 13 MÉTRICAS AMBIENTAIS CVSS v4.0 -->
        <div class="card">
          <div class="card-title" style="font-size:15px;">
            <span id="formTitle">Julgamento das Métricas Ambientais (FIRST CVSS v4.0)</span>
            <span style="font-size:11px;color:#34d399;font-weight:400;" id="draftStatusBadge">✓ Rascunho salvo</span>
          </div>

          <!-- GRUPO 1: REQUISITOS DE SEGURANÇA -->
          <div class="metric-group-card">
            <div class="metric-group-title" id="mGroup1Title">1. Requisitos de Segurança do Ativo (CR / IR / AR)</div>
            <div class="metric-grid">
              <div class="metric-field">
                <label>Confidentiality Requirement (CR):</label>
                <select class="metric-select" id="metric-CR" onchange="onMetricChange('CR')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="H">High (H) — Impacto Catastrófico</option>
                  <option value="M">Medium (M) — Impacto Significativo</option>
                  <option value="L">Low (L) — Impacto Limitado</option>
                  <option value="X">Not Defined (X)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Integrity Requirement (IR):</label>
                <select class="metric-select" id="metric-IR" onchange="onMetricChange('IR')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="H">High (H) — Impacto Catastrófico</option>
                  <option value="M">Medium (M) — Impacto Significativo</option>
                  <option value="L">Low (L) — Impacto Limitado</option>
                  <option value="X">Not Defined (X)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Availability Requirement (AR):</label>
                <select class="metric-select" id="metric-AR" onchange="onMetricChange('AR')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="H">High (H) — Impacto Catastrófico</option>
                  <option value="M">Medium (M) — Impacto Significativo</option>
                  <option value="L">Low (L) — Impacto Limitado</option>
                  <option value="X">Not Defined (X)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- GRUPO 2: MODIFICADORES DE EXPLORAÇÃO -->
          <div class="metric-group-card">
            <div class="metric-group-title" id="mGroup2Title">2. Modificadores de Exploração com Controles (MAC / MAT / MPR / MUI)</div>
            <div class="metric-grid">
              <div class="metric-field">
                <label>Modified Attack Complexity (MAC):</label>
                <select class="metric-select" id="metric-MAC" onchange="onMetricChange('MAC')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H) — Requer bypass de controles</option>
                  <option value="L">Low (L) — Sem complexidade adicional</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Attack Requirements (MAT):</label>
                <select class="metric-select" id="metric-MAT" onchange="onMetricChange('MAT')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="P">Present (P) — Condições de ataque necessárias</option>
                  <option value="N">None (N) — Sem requisitos prévios</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Privileges Required (MPR):</label>
                <select class="metric-select" id="metric-MPR" onchange="onMetricChange('MPR')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H) — Privilégios administrativos</option>
                  <option value="L">Low (L) — Privilégios básicos de usuário</option>
                  <option value="N">None (N) — Não autenticado</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified User Interaction (MUI):</label>
                <select class="metric-select" id="metric-MUI" onchange="onMetricChange('MUI')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="N">None (N) — Sem interação humana</option>
                  <option value="P">Passive (P) — Interação involuntária</option>
                  <option value="A">Active (A) — Ação direta exigida</option>
                </select>
              </div>
            </div>
          </div>

          <!-- GRUPO 3: IMPACTO MODIFICADO NO SISTEMA VULNERÁVEL -->
          <div class="metric-group-card">
            <div class="metric-group-title" id="mGroup3Title">3. Modificadores de Impacto no Sistema Vulnerável (MVC / MVI / MVA)</div>
            <div class="metric-grid">
              <div class="metric-field">
                <label>Modified Vulnerable Conf. (MVC):</label>
                <select class="metric-select" id="metric-MVC" onchange="onMetricChange('MVC')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Vulnerable Integ. (MVI):</label>
                <select class="metric-select" id="metric-MVI" onchange="onMetricChange('MVI')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Vulnerable Avail. (MVA):</label>
                <select class="metric-select" id="metric-MVA" onchange="onMetricChange('MVA')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- GRUPO 4: IMPACTO MODIFICADO SUBSEQUENTE (SUBSEQUENT SYSTEMS) -->
          <div class="metric-group-card">
            <div class="metric-group-title" id="mGroup4Title">4. Modificadores de Impacto em Sistemas Subsequentes (MSC / MSI / MSA)</div>
            <div class="metric-grid">
              <div class="metric-field">
                <label>Modified Subsequent Conf. (MSC):</label>
                <select class="metric-select" id="metric-MSC" onchange="onMetricChange('MSC')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Subsequent Integ. (MSI):</label>
                <select class="metric-select" id="metric-MSI" onchange="onMetricChange('MSI')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
              <div class="metric-field">
                <label>Modified Subsequent Avail. (MSA):</label>
                <select class="metric-select" id="metric-MSA" onchange="onMetricChange('MSA')">
                  <option value="" disabled selected>-- Selecione / Select --</option>
                  <option value="X">Not Defined (X / Inalterado)</option>
                  <option value="H">High (H)</option>
                  <option value="L">Low (L)</option>
                  <option value="N">None (N)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- JUSTIFICATIVA TÉCNICA -->
          <div style="margin-bottom:16px;">
            <label style="display:block;font-size:12px;color:#cbd5e1;margin-bottom:4px;font-weight:600;" id="labelRationale">Justificativa Técnica do Especialista (Obrigatória para Auditoria):</label>
            <textarea id="metric-rationale" rows="3" oninput="onRationaleInput()" style="width:100%;background:#030712;border:1px solid #334155;color:#f8fafc;padding:10px;border-radius:6px;font-size:12px;resize:vertical;" placeholder="Fundamente tecnicamente sua seleção com base na topologia e controles informados..."></textarea>
          </div>

          <!-- BOTÕES DE NAVEGAÇÃO -->
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <button class="btn btn-outline" id="btnPrevScenario" onclick="prevScenario()">◀ <span id="btnPrevText">Cenário Anterior</span></button>
            <div style="display:flex;gap:8px;">
              <button class="btn btn-outline" onclick="saveCurrentDraft(true)">💾 <span id="btnSaveText">Salvar Rascunho</span></button>
              <button class="btn btn-primary" id="btnNextScenario" onclick="nextScenario()"><span id="btnNextText">Salvar & Próximo</span> ▶</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- ETAPA 3: REVISÃO GERAL E SUBMISSÃO SELADA                      -->
  <!-- ============================================================== -->
  <div class="step-section" id="section-step-3">
    <div class="card">
      <div class="card-title">
        <span id="reviewTitle">Quadro de Revisão Geral & Selagem de Respostas</span>
        <button class="btn btn-outline" onclick="goToStep(2)" style="font-size:12px;">← <span id="btnBackToQuestions">Voltar às Questões</span></button>
      </div>

      <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;" id="reviewDesc">
        Revise suas escolhas antes da submissão final. Ao selar, um hash criptográfico SHA-256 será gerado e os registros se tornarão imutáveis para compor o Padrão-Ouro do estudo.
      </p>

      <!-- RECIBO DE CUSTÓDIA PÓS-SUBMISSÃO -->
      <div class="receipt-box" id="submissionReceipt">
        <h4 style="color:#34d399;font-size:16px;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
          <span>✓</span> <span id="receiptTitle">Avaliação Selada com Sucesso no Padrão de Custódia G9!</span>
        </h4>
        <div style="font-family:monospace;font-size:12px;color:#cbd5e1;line-height:1.7;">
          <div><strong>Avaliador:</strong> <span id="receiptExpert">EXP-01</span></div>
          <div><strong>Timestamp (UTC):</strong> <span id="receiptTime">2026-10-12T00:00:00Z</span></div>
          <div><strong>Hash de Custódia SHA-256:</strong> <span id="receiptHash" style="color:#38bdf8;word-break:break-all;"></span></div>
          <div><strong>Total de Cenários Julgados:</strong> <span id="receiptCount">30 / 30</span></div>
        </div>
        <div style="margin-top:14px;display:flex;gap:10px;">
          <button class="btn btn-success" onclick="downloadAuditJson()">📥 <span id="btnDownloadReceipt">Baixar Arquivo Canônico de Auditoria (.json)</span></button>
        </div>
      </div>

      <!-- TABELA RESUMO -->
      <div class="summary-table-wrap">
        <table>
          <thead>
            <tr>
              <th id="thNum">#</th>
              <th id="thScenarioId">Cenário ID</th>
              <th id="thCveId">CVE ID</th>
              <th id="thAssetClass">Classe do Ativo</th>
              <th id="thCrIrAr">CR / IR / AR</th>
              <th id="thModifiers">Modificadores</th>
              <th id="thStatus">Status</th>
              <th id="thAction">Ação</th>
            </tr>
          </thead>
          <tbody id="summaryTableBody">
            <!-- Injetado dinamicamente via JS -->
          </tbody>
        </table>
      </div>

      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;">
        <span style="font-size:12px;color:var(--text-muted);" id="sealWarning">Atenção: A submissão final fecha a janela individual de avaliação.</span>
        <button class="btn btn-purple" id="btnSealSubmission" onclick="sealAndSubmitAll()">🔒 <span id="btnSealText">Selar e Enviar Avaliação Definitiva (30/30)</span></button>
      </div>
    </div>
  </div>
</main>

<script>
// ==============================================================================
// BASE DE DADOS DOS 30 CENÁRIOS SINTÉTICOS DO BENCHMARK (DATASET B / G9 DEMO)
// ==============================================================================
var SCENARIOS = {scenarios_json_str};

// ESTADO DA APLICAÇÃO
var currentLang = "pt";
var currentStep = 1;
var currentScenarioIdx = 0;
var currentExpert = "EXP-01";
var isSealed = false;

// DICIONÁRIO I18N TRILÍNGUE COMPLETO (PT, EN, ES)
var I18N = {{
  pt: {{
    headerSub: "Portal de Avaliação Cega de Especialistas Independentes (G9)",
    btnBackToSite: "← Voltar ao Site CVSS",
    tabLabel1: "1. Consentimento (e-TCLE)",
    tabLabel2: "2. Avaliação Cega (30 Cenários)",
    tabLabel3: "3. Revisão & Submissão",
    tcleTitle: "Termo de Consentimento Livre e Esclarecido Eletrônico (e-TCLE)",
    btnPrintTerm: "Imprimir / Salvar PDF",
    labelConsent: "Declaro que li, compreendi integralmente os objetivos, metodologia, riscos mitigados e procedimentos da pesquisa e CONCORDO voluntariamente em participar da validação científica como Especialista Avaliador.",
    labelCoi: "Declaro formalmente AUSÊNCIA DE CONFLITO DE INTERESSES (COI), atestando não possuir vínculo societário, empregatício ou de desenvolvimento com a HelpUS LLC, nem parentesco com os autores nos últimos 36 meses.",
    supportNote: "Dúvidas técnicas ou éticas? Contate: pesquisa@helpus.adv.br",
    btnStartText: "Iniciar Avaliação Cega (30 Cenários)",
    sidebarNavTitle: "Navegador de Cenários",
    btnGoToReview: "Ir para Resumo Final",
    blindShieldTitle: "Ambiente Cego Estrito (Blinded Review Protocol)",
    blindShieldDesc: "Zero exposição de predições da IA HelpUS e zero visibilidade das respostas de outros avaliadores. Apenas o pacote técnico do CVE e a topologia estão disponíveis.",
    formTitle: "Julgamento das Métricas Ambientais (FIRST CVSS v4.0)",
    mGroup1Title: "1. Requisitos de Segurança do Ativo (CR / IR / AR)",
    mGroup2Title: "2. Modificadores de Exploração com Controles (MAC / MAT / MPR / MUI)",
    mGroup3Title: "3. Modificadores de Impacto no Sistema Vulnerável (MVC / MVI / MVA)",
    mGroup4Title: "4. Modificadores de Impacto em Sistemas Subsequentes (MSC / MSI / MSA)",
    labelRationale: "Justificativa Técnica do Especialista (Obrigatória para Auditoria):",
    btnPrevText: "Cenário Anterior",
    btnSaveText: "Salvar Rascunho",
    btnNextText: "Salvar & Próximo",
    reviewTitle: "Quadro de Revisão Geral & Selagem de Respostas",
    reviewDesc: "Revise suas escolhas antes da submissão final. Ao selar, um hash criptográfico SHA-256 será gerado e os registros se tornarão imutáveis para compor o Padrão-Ouro do estudo.",
    receiptTitle: "Avaliação Selada com Sucesso no Padrão de Custódia G9!",
    btnDownloadReceipt: "Baixar Arquivo Canônico de Auditoria (.json)",
    sealWarning: "Atenção: A submissão final fecha a janela individual de avaliação e torna as respostas imutáveis.",
    btnSealText: "Selar e Enviar Avaliação Definitiva",
    labelContextTitle: "Topologia de Implantação:",
    labelControlsTitle: "Controles Compensatórios:",
    btnBackToQuestions: "Voltar às Questões",
    thNum: "#",
    thScenarioId: "Cenário ID",
    thCveId: "CVE ID",
    thAssetClass: "Classe do Ativo",
    thCrIrAr: "CR / IR / AR",
    thModifiers: "Modificadores",
    thStatus: "Status",
    thAction: "Ação"
  }},
  en: {{
    headerSub: "Independent Expert Blinded Adjudication Portal (G9 EDC)",
    btnBackToSite: "← Back to CVSS Site",
    tabLabel1: "1. Consent (e-ICF)",
    tabLabel2: "2. Blinded Review (30 Scenarios)",
    tabLabel3: "3. Review & Submission",
    tcleTitle: "Electronic Informed Consent Form (e-ICF / Common Rule 45 CFR 46)",
    btnPrintTerm: "Print / Save PDF",
    labelConsent: "I state that I have read and fully understood the research objectives, methodology, mitigations, and procedures, and I VOLUNTARILY AGREE to participate as an Independent Expert Evaluator.",
    labelCoi: "I formally declare NO CONFLICT OF INTEREST (COI), certifying that I have had no employment, equity, or development relationship with HelpUS LLC, nor familial relationship with the authors over the past 36 months.",
    supportNote: "Technical or ethical inquiries? Contact: pesquisa@helpus.adv.br",
    btnStartText: "Start Blinded Adjudication (30 Scenarios)",
    sidebarNavTitle: "Scenario Navigator",
    btnGoToReview: "Go to Final Review",
    blindShieldTitle: "Strict Blinding Shield (Blinded Review Protocol)",
    blindShieldDesc: "Zero exposure to HelpUS AI inferences and zero visibility into peer evaluator votes. Only the CVE technical record and deployment topology are visible.",
    formTitle: "Environmental Metric Scoring (FIRST CVSS v4.0 Specification)",
    mGroup1Title: "1. Security Requirements (CR / IR / AR)",
    mGroup2Title: "2. Exploitability Modifiers with Compensating Controls (MAC / MAT / MPR / MUI)",
    mGroup3Title: "3. Vulnerable System Impact Modifiers (MVC / MVI / MVA)",
    mGroup4Title: "4. Subsequent System Impact Modifiers (MSC / MSI / MSA)",
    labelRationale: "Expert Technical Rationale (Mandatory for Audit Trail):",
    btnPrevText: "Previous Scenario",
    btnSaveText: "Save Draft",
    btnNextText: "Save & Next",
    reviewTitle: "Final Review & Sealed Cryptographic Submission",
    reviewDesc: "Review your choices before sealing. Upon submission, a SHA-256 cryptographic hash will be calculated, locking all records into the study Human Ground Truth.",
    receiptTitle: "Adjudication Successfully Sealed under Gate G9 Custody Protocol!",
    btnDownloadReceipt: "Download Canonical Audit Package (.json)",
    sealWarning: "Notice: Final submission closes your individual evaluation window and makes responses immutable.",
    btnSealText: "Cryptographically Seal & Submit All Responses",
    labelContextTitle: "Deployment Topology:",
    labelControlsTitle: "Compensating Controls:",
    btnBackToQuestions: "Back to Scenarios",
    thNum: "#",
    thScenarioId: "Scenario ID",
    thCveId: "CVE ID",
    thAssetClass: "Asset Class",
    thCrIrAr: "CR / IR / AR",
    thModifiers: "Modifiers",
    thStatus: "Status",
    thAction: "Action"
  }},
  es: {{
    headerSub: "Portal de Evaluación Ciega de Expertos Independientes (G9 EDC)",
    btnBackToSite: "← Volver al Sitio CVSS",
    tabLabel1: "1. Consentimiento (e-TCLE / e-ICF)",
    tabLabel2: "2. Evaluación Ciega (30 Escenarios)",
    tabLabel3: "3. Revisión & Envío",
    tcleTitle: "Formulario de Consentimiento Informado Electrónico (e-TCLE / e-ICF)",
    btnPrintTerm: "Imprimir / Guardar PDF",
    labelConsent: "Declaro que he leído y comprendido en su totalidad los objetivos, metodología, mitigaciones y procedimientos de la investigación, y ACEPTO VOLUNTARIAMENTE participar como Experto Evaluador Independiente.",
    labelCoi: "Declaro formalmente AUSENCIA DE CONFLICTO DE INTERESES (COI), certificando no poseer relación societaria, laboral o de desarrollo con HelpUS LLC, ni parentesco con los autores en los últimos 36 meses.",
    supportNote: "¿Dudas técnicas o éticas? Contacto: pesquisa@helpus.adv.br",
    btnStartText: "Iniciar Evaluación Ciega (30 Escenarios)",
    sidebarNavTitle: "Navegador de Escenarios",
    btnGoToReview: "Ir al Resumen Final",
    blindShieldTitle: "Blindaje Ciego Estricto (Blinded Review Protocol)",
    blindShieldDesc: "Cero exposición a inferencias de IA HelpUS y cero visibilidad de las respuestas de otros evaluadores. Solo el registro técnico del CVE y la topología están disponibles.",
    formTitle: "Evaluación de Métricas Ambientales (Especificación FIRST CVSS v4.0)",
    mGroup1Title: "1. Requisitos de Seguridad del Activo (CR / IR / AR)",
    mGroup2Title: "2. Modificadores de Explotación con Controles (MAC / MAT / MPR / MUI)",
    mGroup3Title: "3. Modificadores de Impacto en el Sistema Vulnerable (MVC / MVI / MVA)",
    mGroup4Title: "4. Modificadores de Impacto en Sistemas Subsecuentes (MSC / MSI / MSA)",
    labelRationale: "Justificación Técnica del Experto (Obligatoria para Auditoría):",
    btnPrevText: "Escenario Anterior",
    btnSaveText: "Guardar Borrador",
    btnNextText: "Guardar y Siguiente",
    reviewTitle: "Cuadro de Revisión General y Envío Criptográfico Sellado",
    reviewDesc: "Revise sus elecciones antes del envío final. Al sellar, se generará un hash criptográfico SHA-256 y los registros serán inmutables para conformar el Human Ground Truth del estudio.",
    receiptTitle: "¡Evaluación Sellada con Éxito bajo el Protocolo de Custodia G9!",
    btnDownloadReceipt: "Descargar Paquete Canónico de Auditoría (.json)",
    sealWarning: "Atención: El envío final cierra su ventana individual de evaluación y hace que las respuestas sean inmutables.",
    btnSealText: "Sellar Criptográficamente y Enviar Todas las Respuestas",
    labelContextTitle: "Topología de Despliegue:",
    labelControlsTitle: "Controles Compensatorios:",
    btnBackToQuestions: "Volver a los Escenarios",
    thNum: "#",
    thScenarioId: "Escenario ID",
    thCveId: "CVE ID",
    thAssetClass: "Clase de Activo",
    thCrIrAr: "CR / IR / AR",
    thModifiers: "Modificadores",
    thStatus: "Estado",
    thAction: "Acción"
  }}
}};

// TEXTO COMPLETO DO TCLE / ICF BILINGUE / TRILINGUE
function getTcleHtml(lang) {{
  if (lang === "en") {{
    return `
      <h2>INFORMED CONSENT FORM (e-ICF) — GATE G9</h2>
      <p><strong>Study Title:</strong> Empirical Validation and Human-in-the-Loop Benchmarking of Contextual Environmental Scoring for FIRST CVSS v4.0</p>
      <p><strong>Sponsor:</strong> HelpUS LLC (United States)</p>
      <p><strong>Operational Human-Study PI:</strong> U.S.-Resident Technical Collaborator (HelpUS LLC, USA)</p>
      <p><strong>Lead Intellectual Author & Technology Originator:</strong> Wagner Santos (HelpUS LLC)</p>
      <p><strong>Regulatory Framework:</strong> US Title 45 CFR Part 46 (Common Rule Minimal Risk Analysis), DHS/IEEE Menlo Report Principles, and Brazilian Law 14,874/2024 / Decree 12,651/2025.</p>
      <br>
      <h3>1. Study Purpose & Nature of Participation</h3>
      <p>You are invited to serve as an Independent Expert Evaluator to assess 30 synthetic and curated vulnerability scenarios under FIRST CVSS v4.0 specifications. Your professional scoring will establish the human reference ground truth against which an automated contextual reasoning engine will be benchmarked.</p>
      <br>
      <h3>2. Blinded Independent Review Safeguards</h3>
      <p>In accordance with scientific blinding protocols: (a) You will NOT be shown any AI model outputs or automated severity scores; (b) You will NOT see other evaluators' responses prior to the adjudication phase; (c) Your judgments must reflect solely your independent expertise and the provided technical deployment topology and compensating controls.</p>
      <br>
      <h3>3. Risks, Safeguards, and Confidentiality</h3>
      <p>The only anticipated risk is cognitive fatigue from reviewing technical records. You may take breaks at any time; your progress is auto-saved. All personal evaluator identity is strictly pseudonymized (EXP-01 through EXP-05). No individual identifiable private data is published.</p>
      <br>
      <h3>4. Voluntary Participation & Right to Withdraw</h3>
      <p>Your participation is entirely voluntary. You may withdraw at any moment prior to final cryptographic sealing without penalty.</p>
      <br>
      <h3>5. Regulatory Governance & Independent Oversight</h3>
      <p>This protocol adheres to the US Common Rule (45 CFR 46) minimal risk expert survey framework with no federal trigger requiring commercial IRB review, and operates under independent ethics review standards. HelpUS LLC conducts this research with transparent conflict-of-interest disclosures and strict double-blind evaluation controls.</p>
    `;
  }}
  if (lang === "es") {{
    return `
      <h2>FORMULARIO DE CONSENTIMIENTO INFORMADO ELECTRÓNICO (e-TCLE / e-ICF) — GATE G9</h2>
      <p><strong>Título del Estudio:</strong> Validación Empírica y Benchmarking Humano de Métricas Ambientales en el Estándar FIRST CVSS v4.0</p>
      <p><strong>Patrocinador:</strong> HelpUS LLC (Estados Unidos)</p>
      <p><strong>Investigador Principal Operativo (Fase Humana):</strong> Colaborador Técnico Residente en EE. UU. (HelpUS LLC)</p>
      <p><strong>Autor Intelectual Principal y Creador Tecnológico:</strong> Wagner Santos (HelpUS LLC)</p>
      <p><strong>Marco Regulatorio:</strong> Marco EE. UU. 45 CFR 46 (Common Rule Riesgo Mínimo), Principios del Informe Menlo, Ley Federal Brasileña 14.874/2024 y Decreto 12.651/2025.</p>
      <br>
      <h3>1. Objetivos del Estudio y Rol del Experto</h3>
      <p>Usted ha sido invitado(a) como Experto Evaluador Independiente para juzgar 30 escenarios técnicos de vulnerabilidades bajo la especificación oficial FIRST CVSS v4.0. Sus determinaciones conformarán el Patrón de Oro Humano de Referencia (Human Ground Truth) para la auditoría y calibración de precisión del motor contextual automatizado.</p>
      <br>
      <h3>2. Protocolo de Evaluación Ciega e Imparcial</h3>
      <p>Para resguardar la máxima imparcialidad científica: (a) Usted NO tendrá acceso a puntuaciones sugeridas por Inteligencia Artificial; (b) Usted NO verá los votos emitidos por los otros evaluadores antes de la sesión formal de adjudicación; (c) Sus elecciones deben fundamentarse estrictamente en su conocimiento técnico profesional y en las evidencias de red y controles compensatorios provistos.</p>
      <br>
      <h3>3. Riesgos Mitigados y Confidencialidad</h3>
      <p>El único riesgo previsto es la fatiga cognitiva por el análisis de registros técnicos. Dispone de guardado automático para realizar la evaluación en sesiones convenientes a su ritmo. Su identidad profesional está estrictamente seudonimizada (EXP-01 a EXP-05), garantizando la protección de datos conforme a estándares internacionales.</p>
      <br>
      <h3>4. Participación Voluntaria y Derecho de Revocación</h3>
      <p>Su participación es totalmente voluntaria y puede revocar su consentimiento en cualquier momento antes del sellado criptográfico definitivo de sus respuestas.</p>
      <br>
      <h3>5. Gobernanza Ética e Independencia Metodológica</h3>
      <p>Este protocolo se rige por el marco de riesgo mínimo de la Common Rule de EE. UU. (45 CFR 46) y normas éticas independientes, asegurando total rigor metodológico, declaración transparente de conflicto de intereses y ausencia de sesgo evaluador.</p>
    `;
  }}
  return `
    <h2>TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO ELETRÔNICO (e-TCLE)</h2>
    <p><strong>Título da Pesquisa:</strong> Validação Empírica e Benchmarking Humano de Métricas Ambientais no Padrão FIRST CVSS v4.0</p>
    <p><strong>Patrocinador Institucional:</strong> HelpUS LLC (Estados Unidos)</p>
    <p><strong>Investigador Principal Operativo (Fase Humana):</strong> Colaborador Técnico Residente nos EUA (HelpUS LLC)</p>
    <p><strong>Autor Intelectual Principal e Originador Tecnológico:</strong> Wagner Santos (HelpUS LLC)</p>
    <p><strong>Marco Regulatório:</strong> Lei Federal nº 14.874/2024, Decreto nº 12.651/2025 (SINEP/INAEP/CEP), Critérios de Risco Mínimo US 45 CFR 46 (Common Rule) e Princípios do Menlo Report / Declaração de Helsinki.</p>
    <br>
    <h3>1. Objetivos da Pesquisa e Papel do Especialista</h3>
    <p>Você foi convidado(a) como Especialista Independente para avaliar 30 cenários técnicos de vulnerabilidades sob a especificação oficial FIRST CVSS v4.0. Seus julgamentos formarão o Padrão-Ouro Humano de Referência para a auditoria de acurácia de modelos automatizados de priorização de risco.</p>
    <br>
    <h3>2. Protocolo de Avaliação Cega (Blinded Review)</h3>
    <p>Para resguardar a imparcialidade científica: (a) Você NÃO terá acesso a notas sugeridas por Inteligência Artificial; (b) Você NÃO verá votos emitidos pelos outros 4 especialistas antes da sessão formal de adjudicação; (c) Suas escolhas devem se basear estritamente na sua experiência profissional e nas evidências de rede e controles compensatórios informados.</p>
    <br>
    <h3>3. Riscos Mitigados e Confidencialidade</h3>
    <p>O único risco previsível é o cansaço cognitivo visual na leitura dos dados técnicos. Você dispõe de salvamento automático de rascunhos para realizar a análise em sessões convenientes. Seus dados de identificação são pseudonimizados sob estrita conformidade técnica (EXP-01 a EXP-05).</p>
    <br>
    <h3>4. Voluntariedade e Direito de Revocação</h3>
    <p>Sua participação é estritamente voluntária e você pode revogar seu consentimento a qualquer momento antes da selagem definitiva de suas respostas.</p>
    <br>
    <h3>5. Governança Ética e Independência Científica</h3>
    <p>Este protocolo segue a arquitetura regulatória da Lei 14.874/2024 e o enquadramento de consulta a especialistas de risco mínimo da Common Rule dos EUA (45 CFR 46), assegurando rigor metodológico, salvaguardas de conflito de interesses e blindagem algorítmica.</p>
  `;
}}

// RESPOSTAS DO ESPECIALISTA ARMAZENADAS NO LOCALSTORAGE
function getStorageKey() {{
  return "helpus_edc_responses_" + currentExpert;
}}

function loadResponses() {{
  try {{
    var data = localStorage.getItem(getStorageKey());
    return data ? JSON.parse(data) : {{}};
  }} catch (e) {{
    return {{}};
  }}
}}

function saveResponses(responses) {{
  try {{
    localStorage.setItem(getStorageKey(), JSON.stringify(responses));
  }} catch (e) {{
    console.error("Storage error:", e);
  }}
}}

// INICIALIZAÇÃO
function init() {{
  if (window.location.protocol === 'file:') {{
    var b = document.getElementById('btnBackToSite');
    if (b) b.href = 'index.html';
    var bw = document.getElementById('brandWrapLink');
    if (bw) bw.href = 'index.html';
  }}
  renderTcle();
  renderScenarioGrid();
  loadScenario(0);
  checkConsentState();
  updateProgress();
}}

function setLanguage(lang) {{
  currentLang = lang;
  document.getElementById("btn-lang-pt").classList.toggle("active", lang === "pt");
  document.getElementById("btn-lang-en").classList.toggle("active", lang === "en");
  document.getElementById("btn-lang-es").classList.toggle("active", lang === "es");
  
  var dict = I18N[lang];
  for (var key in dict) {{
    var el = document.getElementById(key);
    if (el) {{
      el.innerText = dict[key];
    }}
  }}
  renderTcle();
  loadScenario(currentScenarioIdx);
  renderSummaryTable();
}}

function renderTcle() {{
  document.getElementById("tcleContent").innerHTML = getTcleHtml(currentLang);
}}

function onExpertChange() {{
  currentExpert = document.getElementById("expertSelector").value;
  checkConsentState();
  updateProgress();
  loadScenario(currentScenarioIdx);
  renderSummaryTable();
}}

function checkConsentState() {{
  var consentKey = "helpus_edc_consent_" + currentExpert;
  var hasConsented = localStorage.getItem(consentKey) === "true";
  document.getElementById("checkConsent").checked = hasConsented;
  document.getElementById("checkCoi").checked = hasConsented;
  document.getElementById("tab-step-1").classList.toggle("completed", hasConsented);
}}

function confirmConsentAndProceed() {{
  var c1 = document.getElementById("checkConsent").checked;
  var c2 = document.getElementById("checkCoi").checked;
  if (!c1 || !c2) {{
    var msg = currentLang === "pt"
      ? "Por favor, marque o aceite do e-TCLE e a declaração de ausência de conflito de interesses para prosseguir."
      : currentLang === "es"
      ? "Por favor, marque la aceptación del e-TCLE/e-ICF y la declaración de ausencia de conflicto de intereses para continuar."
      : "Please check both the consent agreement and the conflict of interest disclosure to proceed.";
    alert(msg);
    return;
  }}
  localStorage.setItem("helpus_edc_consent_" + currentExpert, "true");
  document.getElementById("tab-step-1").classList.add("completed");
  goToStep(2);
}}

function goToStep(step) {{
  if (step > 1 && localStorage.getItem("helpus_edc_consent_" + currentExpert) !== "true") {{
    var msg = currentLang === "pt"
      ? "Você deve confirmar o e-TCLE antes de acessar os cenários de avaliação."
      : currentLang === "es"
      ? "Debe confirmar el e-TCLE/e-ICF antes de acceder a los escenarios de evaluación."
      : "You must accept the e-ICF before accessing evaluation scenarios.";
    alert(msg);
    return;
  }}
  currentStep = step;
  document.querySelectorAll(".step-tab").forEach(function(el, idx) {{
    el.classList.toggle("active", idx + 1 === step);
  }});
  document.querySelectorAll(".step-section").forEach(function(el, idx) {{
    el.classList.toggle("active", idx + 1 === step);
  }});
  if (step === 3) {{
    renderSummaryTable();
  }}
  window.scrollTo({{ top: 0, behavior: "smooth" }});
}}

// RENDERIZADOR DO GRID DE 30 CENÁRIOS
function renderScenarioGrid() {{
  var grid = document.getElementById("scenarioGrid");
  grid.innerHTML = "";
  var responses = loadResponses();
  
  SCENARIOS.forEach(function(scn, idx) {{
    var btn = document.createElement("button");
    btn.className = "scenario-item-btn";
    btn.innerText = (idx + 1).toString().padStart(2, "0");
    btn.id = "scn-btn-" + idx;
    
    var isDone = responses[scn.scenario_id] && responses[scn.scenario_id].saved;
    if (isDone) btn.classList.add("done");
    if (idx === currentScenarioIdx) btn.classList.add("active");
    
    btn.onclick = function() {{
      saveCurrentDraft(false);
      loadScenario(idx);
    }};
    grid.appendChild(btn);
  }});
}}

// CARREGAR UM CENÁRIO ESPECÍFICO
function loadScenario(idx) {{
  currentScenarioIdx = idx;
  var scn = SCENARIOS[idx];
  if (!scn) return;
  
  // Atualizar visual do grid
  document.querySelectorAll(".scenario-item-btn").forEach(function(el, i) {{
    el.classList.toggle("active", i === idx);
  }});
  
  // Preencher cartão do cenário
  document.getElementById("cardAssetClass").innerText = scn.asset_class;
  document.getElementById("cardScenarioId").innerText = scn.scenario_id;
  document.getElementById("cardCveId").innerText = scn.cve_id;
  document.getElementById("scenarioIndexBadge").innerText = (currentLang === "pt" ? "Cenário " : currentLang === "es" ? "Escenario " : "Scenario ") + (idx + 1) + " / " + SCENARIOS.length;
  document.getElementById("cardSummary").innerText = scn.summary;
  document.getElementById("cardContext").innerText = scn.deployment_context;
  document.getElementById("cardControls").innerText = scn.controls;
  
  // Preencher respostas salvas (ou vazio por padrão para evitar viés de ancoragem)
  var responses = loadResponses();
  var r = responses[scn.scenario_id] || {{}};
  
  var metrics = ["CR", "IR", "AR", "MAC", "MAT", "MPR", "MUI", "MVC", "MVI", "MVA", "MSC", "MSI", "MSA"];
  metrics.forEach(function(m) {{
    var sel = document.getElementById("metric-" + m);
    if (sel) {{
      sel.value = r[m] !== undefined ? r[m] : "";
    }}
  }});
  
  document.getElementById("metric-rationale").value = r.rationale || "";
  
  // Estado de navegação
  document.getElementById("btnPrevScenario").disabled = (idx === 0);
  var isLast = (idx === SCENARIOS.length - 1);
  document.getElementById("btnNextText").innerText = isLast
    ? (currentLang === "pt" ? "Concluir e Revisar" : currentLang === "es" ? "Concluir y Revisar" : "Finish & Review")
    : (currentLang === "pt" ? "Salvar & Próximo" : currentLang === "es" ? "Guardar y Siguiente" : "Save & Next");
}}

function onMetricChange(m) {{
  saveCurrentDraft(false);
}}

function onRationaleInput() {{
  saveCurrentDraft(false);
}}

function saveCurrentDraft(showFeedback) {{
  var scn = SCENARIOS[currentScenarioIdx];
  if (!scn) return;
  
  var responses = loadResponses();
  var item = responses[scn.scenario_id] || {{}};
  
  var metrics = ["CR", "IR", "AR", "MAC", "MAT", "MPR", "MUI", "MVC", "MVI", "MVA", "MSC", "MSI", "MSA"];
  metrics.forEach(function(m) {{
    var sel = document.getElementById("metric-" + m);
    if (sel) item[m] = sel.value;
  }});
  
  item.rationale = document.getElementById("metric-rationale").value;
  item.saved = true;
  item.lastModified = new Date().toISOString();
  
  responses[scn.scenario_id] = item;
  saveResponses(responses);
  
  var btn = document.getElementById("scn-btn-" + currentScenarioIdx);
  if (btn) btn.classList.add("done");
  
  updateProgress();
  
  var badge = document.getElementById("draftStatusBadge");
  badge.style.opacity = "1";
  badge.innerText = currentLang === "pt" ? "✓ Rascunho salvo localmente" : currentLang === "es" ? "✓ Borrador guardado localmente" : "✓ Draft saved locally";
  setTimeout(function() {{ badge.style.opacity = "0.7"; }}, 1500);
}}

function prevScenario() {{
  if (currentScenarioIdx > 0) {{
    saveCurrentDraft(false);
    loadScenario(currentScenarioIdx - 1);
  }}
}}

function nextScenario() {{
  saveCurrentDraft(false);
  if (currentScenarioIdx < SCENARIOS.length - 1) {{
    loadScenario(currentScenarioIdx + 1);
  }} else {{
    goToStep(3);
  }}
}}

function updateProgress() {{
  var responses = loadResponses();
  var count = 0;
  SCENARIOS.forEach(function(scn) {{
    if (responses[scn.scenario_id] && responses[scn.scenario_id].saved) count++;
  }});
  var pct = Math.round((count / SCENARIOS.length) * 100);
  document.getElementById("progressSummary").innerText = count + " / " + SCENARIOS.length + " (" + pct + "%)";
  document.getElementById("progressBar").style.width = pct + "%";
  
  if (count === SCENARIOS.length) {{
    document.getElementById("tab-step-2").classList.add("completed");
  }}
}}

// TABELA RESUMO (ETAPA 3)
function renderSummaryTable() {{
  var tbody = document.getElementById("summaryTableBody");
  tbody.innerHTML = "";
  var responses = loadResponses();
  
  SCENARIOS.forEach(function(scn, idx) {{
    var r = responses[scn.scenario_id] || {{}};
    var isDone = r.saved === true;
    
    var tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${{idx + 1}}</td>
      <td><strong>${{scn.scenario_id}}</strong></td>
      <td>${{scn.cve_id}}</td>
      <td>${{scn.asset_class}}</td>
      <td>${{r.CR || "-"}} / ${{r.IR || "-"}} / ${{r.AR || "-"}}</td>
      <td style="font-family:monospace;font-size:11px;">${{r.MAC || "X"}},${{r.MAT || "X"}},${{r.MPR || "X"}},${{r.MUI || "X"}}</td>
      <td><span style="color:${{isDone ? "#34d399" : "#f59e0b"}};">${{isDone ? (currentLang === "pt" ? "✓ Concluído" : currentLang === "es" ? "✓ Completado" : "✓ Completed") : (currentLang === "pt" ? "⏳ Pendente" : currentLang === "es" ? "⏳ Pendiente" : "⏳ Pending")}}</span></td>
      <td><button class="btn btn-outline" style="padding:2px 8px;font-size:11px;" onclick="goToStep(2); loadScenario(${{idx}});">${{currentLang === "pt" ? "Editar" : currentLang === "es" ? "Editar" : "Edit"}}</button></td>
    `;
    tbody.appendChild(tr);
  }});
}}

// CÁLCULO DE HASH SHA-256 E SELAGEM DE SUBMISSÃO
async function computeSha256(str) {{
  var buffer = new TextEncoder().encode(str);
  var hashBuffer = await crypto.subtle.digest("SHA-256", buffer);
  var hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}}

async function sealAndSubmitAll() {{
  var responses = loadResponses();
  var missing = [];
  var metrics = ["CR", "IR", "AR", "MAC", "MAT", "MPR", "MUI", "MVC", "MVI", "MVA", "MSC", "MSI", "MSA"];
  
  SCENARIOS.forEach(function(scn, idx) {{
    var r = responses[scn.scenario_id];
    if (!r || !r.saved) {{
      missing.push(idx + 1);
    }} else {{
      var allAnswered = true;
      for (var i = 0; i < metrics.length; i++) {{
        if (!r[metrics[i]]) {{
          allAnswered = false;
          break;
        }}
      }}
      if (!allAnswered) missing.push(idx + 1);
    }}
  }});
  
  // VALIDAÇÃO FAIL-CLOSED (EXIGÊNCIA CG-20261013-023 C4): Recusa submissão incompleta
  if (missing.length > 0) {{
    var msg = currentLang === "pt"
      ? "Avaliação Incompleta (Fail-Closed): Os seguintes cenários possuem métricas não respondidas: #" + missing.join(", #") + ". Todos os 30 cenários e suas 13 métricas devem ser preenchidos antes da selagem definitiva."
      : currentLang === "es"
      ? "Evaluación Incompleta (Fail-Closed): Los siguientes escenarios tienen métricas sin responder: #" + missing.join(", #") + ". Los 30 escenarios y sus 13 métricas deben responderse antes del sellado definitivo."
      : "Incomplete Evaluation (Fail-Closed): The following scenarios have unanswered metrics: #" + missing.join(", #") + ". All 30 scenarios and all 13 metrics must be answered before final sealing.";
    alert(msg);
    return;
  }}
  
  var payload = {{
    study: "HelpUS CVSS AI - Gate G9 Expert Reference Ground Truth",
    protocol_regulatory_framework: "Lei 14.874/2024 (SINEP) / US 45 CFR 46 / Menlo Report",
    expert_id: currentExpert,
    consent_timestamp_iso: localStorage.getItem("helpus_edc_consent_time_" + currentExpert) || new Date().toISOString(),
    submission_timestamp_iso: new Date().toISOString(),
    total_scenarios_evaluated: Object.keys(responses).length,
    responses: responses
  }};
  
  var canonicalJson = JSON.stringify(payload, Object.keys(payload).sort());
  var hash = await computeSha256(canonicalJson);
  payload.custody_sha256 = hash;
  
  // Salvar submissão selada
  localStorage.setItem("helpus_edc_sealed_" + currentExpert, JSON.stringify(payload));
  
  // Exibir recibo
  document.getElementById("receiptExpert").innerText = currentExpert;
  document.getElementById("receiptTime").innerText = payload.submission_timestamp_iso;
  document.getElementById("receiptHash").innerText = hash;
  document.getElementById("receiptCount").innerText = Object.keys(responses).length + " / " + SCENARIOS.length;
  document.getElementById("submissionReceipt").style.display = "block";
  document.getElementById("btnSealSubmission").disabled = true;
  document.getElementById("tab-step-3").classList.add("completed");
  
  window.lastSealedPayload = payload;
  var sealAlert = currentLang === "pt"
    ? "Submissão selada com sucesso! Hash SHA-256 gerado e registrado no protocolo de custódia."
    : currentLang === "es"
    ? "¡Evaluación sellada con éxito! Hash SHA-256 generado y registrado en el protocolo de custodia."
    : "Submission cryptographically sealed! SHA-256 hash registered in custody log.";
  alert(sealAlert);
}}

function downloadAuditJson() {{
  var payload = window.lastSealedPayload || JSON.parse(localStorage.getItem("helpus_edc_sealed_" + currentExpert) || "{{}}");
  var blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: "application/json" }});
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "RESPOSTAS_ESPECIALISTA_" + currentExpert + "_" + (payload.custody_sha256 ? payload.custody_sha256.slice(0, 8) : "G9") + ".json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

// Iniciar ao carregar página
window.addEventListener("DOMContentLoaded", init);
</script>
</body>
</html>
"""

output_path.write_text(html_content, encoding="utf-8")
print(f"Portal EDC generated successfully at {output_path}! Size: {output_path.stat().st_size} bytes")

experts_dir = Path(r"d:\AntiG\cvss\experts")
experts_dir.mkdir(parents=True, exist_ok=True)
experts_index = experts_dir / "index.html"
experts_index.write_text(html_content, encoding="utf-8")
print(f"Portal EDC generated successfully at {experts_index}! Size: {experts_index.stat().st_size} bytes")

logo_src = Path(r"d:\AntiG\cvss\helpus-logo.jpg")
if logo_src.exists():
    import shutil
    shutil.copy2(logo_src, experts_dir / "helpus-logo.jpg")
    print(f"Logo copied to {experts_dir / 'helpus-logo.jpg'}")
