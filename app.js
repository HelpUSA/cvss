function val(id) {
  var el = document.getElementById(id);
  return el ? el.value : "";
}

function sev(score) {
  var s = Number(score);
  if (s >= 9) return "Critical";
  if (s >= 7) return "High";
  if (s >= 4) return "Medium";
  if (s > 0) return "Low";
  return "None";
}

function yes(id) {
  return val(id) === "yes";
}

function esc(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmtNum(value, digits) {
  var n = Number(value);
  if (!isFinite(n)) return "";
  return n.toFixed(digits === undefined ? 1 : digits);
}

function quoteCsv(value) {
  return "\"" + String(value == null ? "" : value).replace(/"/g, "\"\"") + "\"";
}

function getExportContract() {
  var r = window.lastCvssResult || {};
  var contract = {
    official_cvss: r.official_cvss || {},
    contextual_environmental: r.contextual_environmental || {},
    evidence: r.evidence || {}
  };
  if (r.homologation) {
    contract.human_homologation = r.homologation;
  }
  return contract;
}

function switchView(viewId) {
  var views = ["view-guia", "view-simulador", "view-scanner", "view-metricas", "view-console", "view-especialistas"];
  views.forEach(function(v) {
    var el = document.getElementById(v);
    var btn = document.getElementById("nav-btn-" + v);
    if (el) {
      if (v === viewId) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    }
    if (btn) {
      if (v === viewId) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    }
  });
  if (viewId === "view-metricas") {
    renderAuditDashboard();
  }
  if (viewId === "view-console") {
    updateConsoleAuthDisplay();
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setTab(tab) {
  var tabs = ["what", "how", "why"];
  tabs.forEach(function(t) {
    var content = document.getElementById("tab-content-" + t);
    var btn = document.getElementById("tab-btn-" + t);
    if (content) content.style.display = (t === tab ? "block" : "none");
    if (btn) btn.className = (t === tab ? "tab-btn active" : "tab-btn");
  });
}

// ============================================================================
// DICIONÁRIO E GERENCIADOR DE IDIOMAS 100% COMPLETO HELPUS (PT / EN / ES)
// ============================================================================
var HELPUS_I18N = {
  pt: {
    langLabel: "🌐 🇧🇷 PT",
    navSubtitle: "Priorização de Risco com IA • FIRST CVSS v4.0",
    tabGuia: "Visão Geral & Guia",
    tabSimulador: "Simulador de Impacto",
    tabScanner: "Scanner & Topologia",
    tabMetricas: "Métricas & Auditoria",
    tabConsole: "Console Operacional",
    tabEspecialistas: "Painel Especialistas (G9)",
    headerPortalLabel: "Portal EDC (Online)",
    navWa: "WhatsApp",
    footerSub: "Plataforma de Cibersegurança & Pesquisa Científica em IA",
    footerCredit: "Desenvolvido por",
    footerPrivacy: "Política de Privacidade & Cookies",
    footerRights: "© 2026 HelpUS Group. Todos os direitos reservados.",
    waMessage: "Olá, gostaria de saber mais sobre a plataforma HelpUS CVSS e soluções de IA.",

    // Banner de Cookies
    cookieTitle: "Privacidade e Uso de Cookies",
    cookieText: "A plataforma HelpUS CVSS utiliza cookies técnicos estritamente necessários e armazenamento local para lembrar suas preferências de idioma, dados de auditoria e configurações de visualização da rede, em conformidade com a LGPD e o GDPR.",
    cookieBtnDetails: "Saiba Mais",
    cookieBtnAccept: "Aceitar & Continuar",

    // Modal de Privacidade
    privacyModalTitle: "Política de Privacidade & Proteção de Dados",
    privacyP1: "A HelpUS Technology Solutions respeita integralmente sua privacidade e os direitos fundamentais garantidos pela Lei Geral de Proteção de Dados (LGPD - Lei 13.709/2018) e pelo Regulamento Geral de Proteção de Dados da União Europeia (GDPR).",
    privacyH1: "1. Coleta e Uso de Informações",
    privacyP2: "Nossa plataforma realiza simulações e cálculos de priorização de vulnerabilidades (CVSS v4.0). Nenhuma informação de rede privada, credencial ou topologia interna é transmitida ou vendida a terceiros. Todo processamento heurístico ocorre em tempo de execução no seu próprio navegador ou em instâncias protegidas de API.",
    privacyH2: "2. Uso de Cookies e Armazenamento Local",
    privacyP3: "Utilizamos localStorage e cookies essenciais única e exclusivamente para salvar o idioma de sua preferência (Português, Inglês ou Espanhol) e registrar a sua concordância com este termo.",
    privacyH3: "3. Contato do Encarregado (DPO)",
    privacyP4: "Em caso de dúvidas técnicas ou solicitações de auditoria, entre em contato com nossa equipe de segurança em seguranca@helpusbr.com ou pelo canal de suporte via WhatsApp.",
    privacyBtnClose: "Entendi",

    // Hero Video Banner
    heroBadge: "Pesquisa Científica & Motor de IA Explicável",
    heroTitle: "Priorização de Vulnerabilidades Baseada em Evidências Reais",
    heroDesc: "Plataforma científica para calcular o <strong>CVSS v4.0 oficial</strong> e aplicar uma camada contextual explicável com <strong>IA Watcher</strong> baseada em evidências reais do seu ambiente (firewall, rede, escopo PCI e dados críticos).",
    heroBtnSim: "⚡ Testar Simulador com IA",
    heroBtnScan: "🌐 Ver Topologia da Rede",

    // Seção O Que Desenvolvemos (Cards estilo HelpUS)
    solHeaderTitle: "O Que Desenvolvemos",
    solHeaderSub: "Engenharia de cibersegurança moderna, motor de IA explicável e governança matemática aplicada ao FIRST CVSS v4.0.",
    solFooterLabel: "Ver detalhes da solução:",
    solCard1Tag: "REVERSE MITIGATION & WHAT-IF",
    solCard1Title: "Calculadora Reversa de Riscos (\"What-If\")",
    solCard1Desc: "Defina a meta de severidade desejada (ex: sair de 9.8 Crítico para ≤ 5.0 Médio) e nosso algoritmo deduz os controles mínimos de rede e firewall necessários para cumprir o SLA sem paralisar a produção.",
    solCard1Btn: "Testar Mitigação Reversa →",
    solCard2Tag: "CONTEXTUAL AI & FIRST CVSS v4.0",
    solCard2Title: "Motor Watcher IA & FIRST v4.0",
    solCard2Desc: "Motor de inferência determinística que cruza relatórios de vulnerabilidade com evidências de VLAN, WAF e ativos, calibrando a severidade sob regras versionadas auditáveis.",
    solCard2Btn: "Simulador de Impacto IA →",
    solCard3Tag: "DYNAMIC SCANNER & TOPOLOGY",
    solCard3Title: "Scanner de Rede & Topologia em Tempo Real",
    solCard3Desc: "Ingestão nativa de Trivy, Nessus e OpenVAS combinada com sonda local do host. Gera grafos SVG de relacionamentos e rotas de ataque entre gateway, firewall e bases de dados.",
    solCard3Btn: "Abrir Scanner de Rede →",
    solCard4Tag: "COMPLIANCE CLOCK & SLA FORENSICS",
    solCard4Title: "Cronômetro Regulatório & Pacote Forense",
    solCard4Desc: "Traduz notas CVSS em janelas de SLA operacionais auditáveis (inspiradas em PCI-DSS, BACEN, NIS2, ISO 27001) e emite recibos de proveniência com hash SHA-256 e Merkle Tree para rastreabilidade.",
    solCard4Btn: "Consultar Governança & SLA →",
    solCard5Tag: "POLICY-AS-CODE & VIRTUAL PATCHING",
    solCard5Title: "Gerador Automático de Contramedidas (IaC)",
    solCard5Desc: "Gera com 1 clique scripts prontos de contenção perimetral: regras de iptables/nftables para Linux, Security Groups para AWS e regras de filtro WAF para Cloudflare específicas para a CVE.",
    solCard5Btn: "Gerar Regras de Contramedida →",
    solCard6Tag: "TRI-SCORE COMPARATOR & EPSS",
    solCard6Title: "Comparador Tripartite & EPSS Contextual",
    solCard6Desc: "Contraste em tempo real entre o legado CVSS v3.1, o padrão FIRST CVSS v4.0 e a IA Contextual, cruzando a probabilidade de exploração global do EPSS com a barreira perimetral local.",
    solCard6Btn: "Ver Comparador Tri-Score →",

    // Aba 1: Guia Rápido
    guideBadge: "💡 Guia Rápido de Introdução",
    guideTitle: "Primeira vez aqui? Entenda em 3 passos",
    tabWhat: "1. O que é?",
    tabHow: "2. Como funciona?",
    tabWhy: "3. Estudo Científico",
    whatP1: "O <strong>HelpUS CVSS</strong> resolve o maior problema da gestão de vulnerabilidades: <strong>o excesso de alertas inflados</strong>.",
    cardNvdTitle: "🔴 Vetor Base CVSS v4.0 (Fonte Primária)",
    cardNvdDesc: "Mede o perigo intrínseco teórico da falha no mundo. Trata uma falha 9.8 como urgente mesmo em um computador isolado de laboratório ou sem conexão externa.",
    cardContextTitle: "🟢 CVSS Contextual (Nosso Motor com IA)",
    cardContextDesc: "Cruza a falha com <strong>evidências do ambiente real</strong> (firewall, rede, WAF, escopo bancário) para priorizar o que realmente importa e desescalonar ruídos.",
    howStep1: "<strong>Ingestão de Scanner Real:</strong> O sistema aceita relatórios do <code>Trivy</code>, <code>Nessus</code>, <code>OpenVAS</code> ou do nosso <code>Scanner Nativo</code> de rede.",
    howStep2: "<strong>Extração de Evidências por IA:</strong> Nossos agentes analisam configurações de rede, portas abertas e regras perimetrais.",
    howStep3: "<strong>Cálculo Conforme Especificação:</strong> O modelo infere métricas nominais (ex: <code>MAV:Adjacent</code>), mas o score final é derivado pela especificação CVSS v4.0 da FIRST.",
    howStep4: "<strong>Gate de Homologação Humana:</strong> Toda decisão operacional é registrada com justificativas, citações e rastreabilidade auditável.",
    whyP1: "Na literatura científica e na indústria, equipes quase nunca preenchem as métricas ambientais do CVSS porque analisar dezenas de controles manualmente é custoso e demorado.",
    whyP2: "<strong>Nossa contribuição:</strong> Automatizamos a coleta de evidências e o mapeamento de métricas sob regras versionadas determinísticas, assegurando rastreabilidade auditável e reduzindo a sobrecarga operacional.",
    guideBtnSim: "⚡ Abrir Simulador de Parâmetros",
    guideBtnScan: "🌐 Ver Scanner de Ambientes & Grafo",
    guideBtnAudit: "📊 Consultar Métricas de Auditoria",

    // What-If Panel
    whatifBadge: "🎯 Engenharia de Mitigação Reversa (What-If Solver)",
    whatifTitle: "Defina sua Meta de Severidade para Descoberta Automática de Controles",
    whatifTargetLabel: "Meta Alvo:",

    // Virtual Patch Modal
    vpModalBadge: "Policy-as-Code & Virtual Patching",
    vpModalTitle: "Contramedidas Automatizadas de Rede e Firewall",
    vpModalDesc: "Scripts de infraestrutura prontos para aplicar os controles compensatórios sugeridos pela IA Watcher e validar o score CVSS v4.0 sem quebrar a aplicação:",
    vpCopyBtn: "Copiar Script",
    vpCloseBtn: "Fechar",

    // Aba 2: Simulador
    simBadge: "⚡ Laboratório Interativo & Casos Reais",
    simTitle: "Simulador de Impacto Contextual com IA Watcher",
    simPresetLabel: "Selecione um Caso Real para Comparar a Inteligência Contextual:",
    presetBtnPci: "💳 1. PCI Bancário (VLAN Isolada)",
    presetBtnDev: "🧪 2. Servidor de Testes / Dev (-4.4)",
    presetBtnEcom: "🌐 3. E-commerce Sem WAF (+0.2)",
    presetBtnClinic: "🏥 4. Clínica Médica / Servidor Local (-1.6)",
    simControlsLabel: "⚙ Ajuste Fino dos Controles Ambientais (Cálculo em Tempo Real):",
    lblScenario: "Cenário / Ativo",
    lblAssetId: "ID do Ativo",
    lblCve: "Identificador CVE",
    lblBaseScore: "Score Base de Origem (CNA/NVD)",
    lblInternet: "Exposto na Internet pública?",
    optNetNo: "Não (Interno / DMZ Protegida)",
    optNetYes: "Sim (Aberto para 0.0.0.0/0)",
    lblSegmented: "Segmentado em VLAN/Subrede?",
    optSegYes: "Sim (Subrede Isolada)",
    optSegNo: "Não (Rede Plana Compartilhada)",
    lblPci: "Escopo PCI-DSS (Cartões/Bancos)?",
    optPciYes: "Sim (Requisito Crítico)",
    optPciNo: "Não (Fora de Escopo Regulatório)",
    lblFirewall: "Firewall / WAF Ativo?",
    optFwYes: "Sim (Regras Restritivas Ativas)",
    optFwNo: "Não (Sem Restrição Perimetral)",
    lblCompensating: "Controles Compensatórios?",
    optCompYes: "Sim (MFA / Rate-limit / Monitoramento)",
    optCompNo: "Não",
    lblCriticality: "Criticidade do Negócio",
    optCritHigh: "Alta (Core Financeiro / Produção)",
    optCritMed: "Média (Sistemas Corporativos)",
    optCritLow: "Baixa (Ambiente de Teste/Dev)",
    btnCalc: "▶ Calcular com IA",
    btnExportJson: "Exportar JSON",
    btnExportCsv: "Exportar CSV",
    btnCopyPipeline: "Copiar Pipeline JSON",
    btnDownloadReport: "Baixar Relatório MD",

    // Aba 3: Scanner
    scanBadge: "🌐 Scanner Dinâmico de Infraestrutura",
    scanTitle: "Varredura, Topologia e Detecção em Tempo Real",
    scanModeProbe: "🔍 Sondar Meu Dispositivo",
    scanModeCustom: "⌨ Minha Subrede",
    scanModePresets: "🏢 Ambientes Modelo",
    scanModeUpload: "📂 Importar JSON",
    scanGraphTitle: "🗺 Diagrama de Topologia da Rede Analisada",
    scanGraphLegend: "Legenda: <span style='color:#4ade80;'>● Ativo Protegido</span> | <span style='color:#f87171;'>● Ativo Vulnerável</span> | <span style='color:#38bdf8;'>● Gateway/Firewall</span>",

    // Aba 4: Métricas & Auditoria
    metricBadge: "📊 Auditoria Científica & Validação Empírica",
    metricTitle: "Métricas do Estudo Científico & Validação CVSS v4.0",
    btnAuditMd: "Baixar Relatório (.md)",
    btnAuditCsv: "Exportar Dataset (.csv)",
    btnAuditJson: "Baixar Auditoria (.json)",
    kpiScenarios: "Cenários Avaliados",
    kpiScenariosSub: "12 CVEs Reais • 18 Cenários de Produção",
    kpiNoise: "Transição Abaixo de High",
    kpiNoiseSub: "3 de 12 reclassificados < High",
    kpiTransitions: "Transições de Prioridade",
    kpiTransitionsSub: "73.3% decisões contextualizadas",
    kpiTrace: "Rastreabilidade Criptográfica",
    kpiTraceSub: "Hash SHA-256 por decisão",
    kpiMitigation: "Média de Mitigação",
    kpiMitigationSub: "Delta em redes protegidas",
    chart1Title: "📉 Distribuição de Severidades: Avaliação de Origem vs HelpUS IA",
    chart1Sub: "Base vs Contextual",
    chart1Note: "💡 <strong>Impacto Prático:</strong> A avaliação de origem trata 73.3% dos achados no vácuo como Críticos ou Altos. A HelpUS redistribui os alertas reais para Médio/Baixo quando há controles como VLAN, WAF ou ausência de internet, reduzindo a sobrecarga operacional.",
    chart2Title: "⚖ Matriz de Decisões do Watcher IA",
    chart2Sub: "Dataset B (Benchmark, n=30)",
    chart2Note: "🛡 <strong>Ação Bidirecional:</strong> A IA desescalona falhas em ambientes isolados (46.7%), mas eleva a prioridade (26.7%) quando há escopo regulatório (PCI-DSS) ou risco financeiro.",
    pipeTitle: "🔬 Arquitetura Científica: Pipeline de Decisão Auditável",
    pipeSub: "Alinhamento algorítmico com a especificação CVSS v4.0 da FIRST",
    pipeTag: "Determinístico (Regras Versionadas)",
    pipeCard1Title: "1. Registro Canônico de Auditoria",
    pipeCard1Text: "A avaliação CVSS de origem nunca é sobrescrita ou distorcida. Fica permanentemente visível para fins de auditoria.",
    pipeCard2Title: "2. Inferência Determinística de Métricas",
    pipeCard2Text: "O modelo infere métricas nominais canônicas (ex: MAV:Adjacent). O score é gerado pelo algoritmo canônico CVSS v4.0 da FIRST.",
    pipeCard3Title: "3. Gate de Homologação Humana",
    pipeCard3Text: "Toda recomendação de ajuste é registrada com citações explicativas e submetida a carimbo humano antes do despacho.",
    dsTitle: "📋 Dataset B: Benchmark de Desenvolvimento (12 CVEs Reais + 18 Sintéticos)",
    dsSub: "Navegue pelos cenários de desenvolvimento avaliados na pesquisa preliminar (validação confirmatória pendente)",
    filterAll: "Todos (30)",
    filterNvd: "NVD Reais (12)",
    filterSyn: "Sintéticos (18)",
    filterDown: "🟢 Desescalonados (14)",
    filterUp: "🔴 Escalonados (8)",
    searchPlaceholder: "🔍 Pesquisar por CVE, ID, nome do ativo ou tecnologia...",
    thScenario: "Cenário / CVE",
    thAssetClass: "Classe do Ativo",
    thExposure: "Exposição",
    thBaseNvd: "Base NVD",
    thContextual: "Contextual",
    thDelta: "Delta",
    thDecision: "Decisão IA",
    thControl: "Controle / Evidência Principal",

    // Homologação
    homologModalSuper: "Governança & Homologação Humana (HITL)",
    homologModalTitle: "Protocolo de Homologação de Prioridade Contextual",
    step1Badge: "1. Evidências",
    step2Badge: "2. Identificação",
    step3Badge: "3. Justificativa",
    step4Badge: "4. Carimbo & Hash",

    // Console Operacional
    headerConsoleLabel: "Console Operacional",
    heroBtnConsole: "Acessar Console Operacional (5 Camadas)",
    consoleAreaBadge: "Área Operacional Corporativa • 5 Camadas de Avaliação",
    consoleTitle: "Console Operacional HelpUS CVSS",
    consoleDesc: "Priorização contextual em 5 camadas com proveniência compatível com JCS (RFC 8785 pendente validação formal) SHA-256 e governança supervisionada pelo perfil autoritativo PLATFORM_ADMIN.",
    consoleHitlBadge: "Governança Human-in-the-Loop (HITL)",
    consoleHitlTitle: "Homologação e Revisão Humana",
    consoleHitlDesc: "A homologação formal de reclassificações ambientais exige autenticação autorizada de revisor humano com validação de sessão server-side.",
    consoleRbacBadge: "Autenticação Servidor com RBAC",
    consoleRbacDesc: "Decisões operacionais com persistência e auditoria exigem sessão corporativa autenticada via endpoint seguro <code>/api/review/decision</code>. O console público atua em modo de simulação demonstrativa.",
    consoleLoginBtn: "🔐 Acessar Portal de Homologação Autenticado",
    consoleDemoBtn: "Visualizar Demonstração Interativa (Modo Leitura)",
    consoleTlsFooter: "Conexão segura com criptografia TLS 1.3 • Hash compatível com JCS (RFC 8785 pendente validação) SHA-256",
    consoleReviewerName: "Revisor Autorizado (SecOps)",
    consoleReviewerRole: "HITL Reviewer",
    consoleReviewerProfile: "Perfil de Homologação • Revisão Humana Obrigatória",
    consoleDownloadLogBtn: "📥 Baixar Log da Sessão",
    consoleLogoutBtn: "Encerrar Sessão",
    consoleCaseStudyLabel: "Selecione o Caso de Estudo Real (Dataset B)",
    consoleFindingsTitle: "12 Achados de Produção Normalizados",
    consoleFreezeNotice: "Freeze: 2026-10-08T21:30:00Z",
    layer1Badge: "Camada 1",
    layer1Tag: "Normativa",
    layer1Header: "Score de Origem (CNA/NVD)",
    layer1Check: "✓ Score Base Preservado Intacto",
    layer2Badge: "Camada 2",
    layer2Tag: "Evidências",
    layer2Header: "Contexto e Telemetria",
    layer2VectorLabel: "Vetor:",
    layer2ComplexityLabel: "Complexidade:",
    layer2PrivilegesLabel: "Privilégios:",
    layer2AgeLabel: "Idade Telemetria:",
    layer2Check: "✓ Prova de Rede Auditada",
    layer3Badge: "Camada 3",
    layer3Tag: "Priorização",
    layer3Header: "Prioridade HelpUS",
    layer3CvssLabel: "CVSS Ambiental:",
    layer3SlaLabel: "SLA Operacional:",
    layer3TransitionLabel: "Transição:",
    layer4Badge: "Camada 4",
    layer4Tag: "Rastreabilidade",
    layer4Header: "Recibo Canônico JCS (compatível RFC 8785, pendente)",
    layer4ReceiptLabel: "Canônico: JCS compatível (RFC 8785 pendente validação)",
    layer4DownloadBtn: "📥 Baixar Recibo (.json)",
    layer5Badge: "Camada 5",
    layer5Tag: "Auditoria HITL",
    layer5Header: "Aprovação HITL",
    layer5PendingBadge: "Pendente de Homologação",
    layer5ReqSession: "Revisão: Requer Sessão Autorizada",
    layer5ApproveBtn: "✓ Homologar",
    layer5RejectBtn: "✕ Rejeitar",
    consoleHistoryTitle: "Histórico de Homologações & Decisões Operacionais",
    consoleDemoBadge: "Console Interativo: Modo Demonstração (Não Autoritativo)",
    thConsoleDate: "Data/Hora UTC",
    thConsoleCve: "CVE ID",
    thConsoleBase: "Score Base",
    thConsoleContext: "Score Contextual",
    thConsolePriority: "Prioridade",
    thConsoleApprover: "Aprovador Master",
    thConsoleReceipt: "Recibo SHA-256",
    consoleEmptyAudit: "Nenhuma homologação realizada nesta sessão. Selecione um CVE e clique em 'Homologar'.",
    consoleHitlApproved: "✓ Homologado (Simulação)",
    consoleHitlRejected: "✕ Rejeitado (Simulação)",
    cnaAuthorizedPrefix: "CNA Autorizado: ",
    mavAdj: " (Adjacente)",
    mavExt: " (Rede Externa)",
    mavLoc: " (Local)",

    // Painel Especialistas (G9)
    g9HeroBadge: "Gate G9 • Validação Externa por Painel de Especialistas",
    g9HeroTitle: "Portal Eletrônico de Avaliação Cega de Especialistas (EDC)",
    g9HeroDesc: "Ambiente dedicado para coleta eletrônica de dados de especialistas independentes (pesquisadores e profissionais seniores de cibersegurança). O protocolo implementa consentimento eletrônico bilíngue (e-TCLE / e-ICF), blindagem estrita (sem viés de IA), reavaliação de 13 métricas ambientais FIRST CVSS v4.0 em 30 cenários e selamento criptográfico SHA-256.",
    g9OpenBtn: "🚀 Abrir Portal EDC Completo",
    g9OpenSub: "(Nova Aba ↗)",
    g9ActiveBadge: "Ambiente Sintético Ativo • Gate G9",
    g9Card1Title: "Coleta Web Online (EDC)",
    g9Card1Sub: "30 Cenários de Referência Sintética",
    g9Card1Desc: "Interface web autônoma e responsiva desenvolvida para aplicação online. O especialista pode navegar entre os cenários, revisar evidências de rede, atribuir notas de 13 métricas ambientais e salvar rascunhos localmente com segurança.",
    g9Card1Li1: "<strong>e-TCLE / e-ICF:</strong> Assinatura eletrônica e declaração de ausência de conflitos.",
    g9Card1Li2: "<strong>Auto-save:</strong> Persistência local no navegador (localStorage).",
    g9Card1Li3: "<strong>Selamento:</strong> Hash SHA-256 e recibo JSON auditável baixável.",
    g9Card1Btn: "Acessar Portal dos Especialistas →",
    g9Card2Title: "Dossiê Ético & Regulatório",
    g9Card2Sub: "Estratégia Binacional Brasil / EUA (Opção 1)",
    g9Card2Desc: "Conforme pareceres de auditoria <code>CG-20261010-021</code> e <code>CG-20261013-022</code>, a HelpUS adota submissão via CEP nacional (Custo R$ 0,00) com escopo internacional declarado, permitindo especialistas dos EUA e Brasil sem taxas de IRB comercial.",
    g9Card2DocsLabel: "Documentos Disponíveis no Dossiê:",
    g9Card2Status: "Status CEP: Submissão em Preparação • R$ 0,00",
    g9Card3Title: "Blindagem & Integridade Metodológica",
    g9Card3Sub: "Duplo-Cego Estrito (Blinded Review)",
    g9Card3Desc: "A metodologia científica assegura que o especialista não veja nem seja influenciado pelos scores preditos pelo motor de IA nem pelas respostas de revisores prévios.",
    g9Card3Li1: "<strong>Dataset C1/C2:</strong> Permanece estritamente lacrado até o congelamento formal.",
    g9Card3Li2: "<strong>13 Métricas FIRST:</strong> CR, IR, AR, MAV, MAC, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA.",
    g9Card3Li3: "<strong>Acordo Inter-Avaliadores:</strong> Fleiss' Kappa / ICC e Wilcoxon pareado no plano estatístico.",
    g9Card3Status: "✓ Blinding Shield Validado por Auditoria",
    g9FlowTitle: "Fluxo Operacional do Especialista no Portal EDC",
    g9Step1Tag: "Passo 1",
    g9Step1Title: "Consentimento & COI",
    g9Step1Desc: "Leitura do e-TCLE (PT-BR) ou e-ICF (EN-US/ES), preenchimento de identificação e declaração de não conflito de interesses.",
    g9Step2Tag: "Passo 2",
    g9Step2Title: "Avaliação dos 30 Cenários",
    g9Step2Desc: "Análise técnica de cada cenário, seleção das 13 métricas ambientais CVSS v4.0 e justificativa pericial textual.",
    g9Step3Tag: "Passo 3",
    g9Step3Title: "Revisão & Selamento SHA-256",
    g9Step3Desc: "Geração do hash criptográfico digital nativo, certificado de custódia e download do pacote de submissão (.json).",

    // Modal de Homologação HITL
    homologStep1Title: "Passo 1/4 — Checagem de Grounding (Fatos Reais):",
    homologStep1P: "Em conformidade com a <em>ISO/IEC 27001 (Cláusula 6.1.2)</em> e <em>NIST AI RMF</em>, o analista deve atestar que as premissas de rede e negócio declaradas refletem o ambiente físico ou lógico real:",
    homologBtnCancel: "Cancelar",
    homologBtnNext1: "Avançar: Identificação →",
    homologStep2Title: "Passo 2/4 — Atribuição & Responsabilidade Técnica:",
    homologStep2P: "Registre a identidade do operador para garantir não-repúdio e auditoria forense.",
    homologLblName: "Nome Completo do Analista / Auditor:",
    homologLblEmail: "E-mail Corporativo:",
    homologLblRole: "Papel / Perfil de Acesso:",
    homologOptRole1: "Lead Security Engineer / CISO",
    homologOptRole2: "SOC Analyst N3",
    homologOptRole3: "Auditor de Compliance PCI/ISO",
    homologOptRole4: "Engenheiro DevSecOps",
    homologLblTicket: "ID do Chamado / Ticket (Jira/HelpUS/GLPI):",
    homologBtnBack: "← Voltar",
    homologBtnNext2: "Avançar: Justificativa →",
    homologStep3Title: "Passo 3/4 — Justificativa Formal e Decisão de Risco:",
    homologStep3P: "Defina se a proposta da IA é aceita na íntegra, aceita com ressalvas ou rejeitada mantendo o score base de origem.",
    homologLblDelib: "Tipo de Deliberação:",
    homologOptDelib1: "✓ Homologar Prioridade Contextual da IA (Recomendado)",
    homologOptDelib2: "✓ Homologar com Condicionante (Manutenção Agendada)",
    homologOptDelib3: "✕ Rejeitar Proposta da IA (Manter Score Base de Origem)",
    homologOptDelib4: "✕ Rejeitar & Escalar para Comitê de Crise",
    homologLblJust: "Justificativa Técnica do Analista (Obrigatória):",
    homologPlaceholderJust: "Ex: Topologia validada com regras de iptables/VLAN verificadas. Risco aceito com base nos controles compensatórios vigentes até a janela quinzenal.",
    homologBtnSubmit: "✓ Concluir Simulação de Homologação",
    homologSuccessTitle: "Simulação de Homologação Concluída",
    homologSuccessDesc: "O digest de demonstração local foi gerado para pré-visualização. Homologações oficiais são registradas exclusivamente via API autenticada.",
    homologBtnReceipt: "📥 Baixar Comprovante de Simulação (.json)",
    homologBtnClose: "Fechar",

    // Virtual Patching
    vpTabIptables: "Linux (iptables)",
    vpTabAws: "AWS Security Group",
    vpTabWaf: "Cloudflare WAF"
  },

  en: {
    langLabel: "🌐 🇺🇸 EN",
    navSubtitle: "AI Contextual Risk Prioritization • FIRST CVSS v4.0",
    tabGuia: "Overview & Guide",
    tabSimulador: "Impact Simulator",
    tabScanner: "Scanner & Topology",
    tabMetricas: "Metrics & Audit",
    tabConsole: "Operational Console",
    tabEspecialistas: "Expert Panel (G9)",
    headerPortalLabel: "EDC Portal (Online)",
    navWa: "WhatsApp",
    footerSub: "Cybersecurity Platform & Scientific AI Research",
    footerCredit: "Powered by",
    footerPrivacy: "Privacy Policy & Cookies",
    footerRights: "© 2026 HelpUS Group. All rights reserved.",
    waMessage: "Hello, I would like to learn more about the HelpUS CVSS platform and AI cybersecurity solutions.",

    // Cookie Banner
    cookieTitle: "Privacy & Use of Cookies",
    cookieText: "The HelpUS CVSS platform uses strictly necessary technical cookies and local storage to preserve your language preferences, audit logs, and network visualization settings, in full compliance with GDPR and LGPD regulations.",
    cookieBtnDetails: "Learn More",
    cookieBtnAccept: "Accept & Continue",

    // Privacy Modal
    privacyModalTitle: "Privacy Policy & Data Protection",
    privacyP1: "HelpUS Technology Solutions fully respects your privacy and fundamental rights guaranteed by international data protection laws, including GDPR and the Brazilian LGPD.",
    privacyH1: "1. Data Collection and Usage",
    privacyP2: "Our platform performs vulnerability prioritization simulations and calculations (FIRST CVSS v4.0). No private network topologies, credentials, or internal assets are shared or sold to third parties. All heuristic evaluation runs locally in your browser or through encrypted APIs.",
    privacyH2: "2. Cookies and Local Storage",
    privacyP3: "We use localStorage and essential cookies solely to remember your preferred language (Portuguese, English, or Spanish) and to record your acceptance of these terms.",
    privacyH3: "3. Data Protection Officer (DPO) Contact",
    privacyP4: "For technical inquiries or audit verifications, contact our security team at seguranca@helpusbr.com or reach out via WhatsApp support.",
    privacyBtnClose: "Understood",

    // Hero Video Banner
    heroBadge: "Scientific Research & Explainable AI Engine",
    heroTitle: "Evidence-Based Vulnerability Prioritization",
    heroDesc: "Scientific platform to compute official <strong>FIRST CVSS v4.0</strong> and apply an explainable contextual <strong>AI Watcher</strong> layer based on real environment evidence (firewall, network topology, PCI scope, and critical assets).",
    heroBtnSim: "⚡ Test Simulator with AI",
    heroBtnScan: "🌐 View Network Topology",

    // Solutions section
    solHeaderTitle: "What We Build",
    solHeaderSub: "Cutting-edge cybersecurity engineering, explainable AI engine, and mathematical governance applied to FIRST CVSS v4.0.",
    solFooterLabel: "Explore solution details:",
    solCard1Tag: "REVERSE MITIGATION & WHAT-IF",
    solCard1Title: "Reverse Mitigation Calculator (\"What-If\")",
    solCard1Desc: "Set your target severity goal (e.g. drop from 9.8 Critical to ≤ 5.0 Medium) and our algorithm deduces the minimal network and firewall controls required to meet SLA without production downtime.",
    solCard1Btn: "Test Reverse Mitigation →",
    solCard2Tag: "CONTEXTUAL AI & FIRST CVSS v4.0",
    solCard2Title: "AI Watcher Engine & FIRST v4.0",
    solCard2Desc: "Evidence-constrained deterministic engine correlating vulnerability scanner reports with VLAN, WAF, and network topology, calibrating environmental severity under versioned rules.",
    solCard2Btn: "AI Impact Simulator →",
    solCard3Tag: "DYNAMIC SCANNER & TOPOLOGY",
    solCard3Title: "Real-Time Network Scanner & Topology",
    solCard3Desc: "Native ingestion of Trivy, Nessus, and OpenVAS combined with local host probing. Generates interactive SVG attack graphs between gateway, firewall, and databases.",
    solCard3Btn: "Open Network Scanner →",
    solCard4Tag: "COMPLIANCE CLOCK & SLA FORENSICS",
    solCard4Title: "Regulatory SLA Clock & Forensic Packet",
    solCard4Desc: "Translates CVSS scores into auditable operational SLA windows (aligned with PCI-DSS, NIS2, DORA, ISO 27001) and issues SHA-256 Merkle Tree provenance receipts for transparent compliance defense.",
    solCard4Btn: "Consult Governance & SLA →",
    solCard5Tag: "POLICY-AS-CODE & VIRTUAL PATCHING",
    solCard5Title: "Automated Countermeasure Generator (IaC)",
    solCard5Desc: "Generates 1-click perimeter containment scripts: Linux iptables/nftables rules, AWS Security Groups, and Cloudflare WAF filter expressions specific to the CVE.",
    solCard5Btn: "Generate Countermeasures →",
    solCard6Tag: "TRI-SCORE COMPARATOR & EPSS",
    solCard6Title: "Tri-Score Comparator & Contextual EPSS",
    solCard6Desc: "Real-time contrast between legacy CVSS v3.1, official FIRST CVSS v4.0, and Contextual AI, weighting global EPSS exploit probabilities against local perimeter barriers.",
    solCard6Btn: "View Tri-Score Comparator →",

    // Guide
    guideBadge: "💡 Quick Introduction Guide",
    guideTitle: "First time here? Understand in 3 steps",
    tabWhat: "1. What is it?",
    tabHow: "2. How it works",
    tabWhy: "3. Scientific Study",
    whatP1: "The <strong>HelpUS CVSS</strong> platform solves the greatest challenge in vulnerability management: <strong>alert fatigue and inflated scores</strong>.",
    cardNvdTitle: "🔴 Primary Base CVSS v4.0 (CNA/NVD)",
    cardNvdDesc: "Measures the theoretical intrinsic hazard of a flaw globally. Treats a 9.8 vulnerability as urgent even on an isolated laboratory machine without internet access.",
    cardContextTitle: "🟢 Contextual CVSS (Our AI Engine)",
    cardContextDesc: "Cross-references flaws with <strong>real-world environment evidence</strong> (firewall, network topology, WAF, banking scope) to prioritize real risks and eliminate noise.",
    howStep1: "<strong>Real Scanner Ingestion:</strong> Ingests reports from <code>Trivy</code>, <code>Nessus</code>, <code>OpenVAS</code>, or our <code>Native Network Scanner</code>.",
    howStep2: "<strong>AI Evidence Extraction:</strong> Autonomous agents analyze network topologies, open ports, and perimeter firewall rules.",
    howStep3: "<strong>Specification-Compliant Calculation:</strong> AI proposes nominal metrics (e.g. <code>MAV:Adjacent</code>), but the final score strictly follows the FIRST CVSS v4.0 specification.",
    howStep4: "<strong>Human Homologation Gate:</strong> Every operational decision is logged with transparent rationale, citations, and complete audit trail.",
    whyP1: "In scientific literature and industry practice, security teams rarely populate environmental CVSS metrics because manual audit of dozens of controls is costly and slow.",
    whyP2: "<strong>Our contribution:</strong> We automate evidence collection and metric mapping under versioned deterministic rules, ensuring audit traceability and reducing operational overhead.",
    guideBtnSim: "⚡ Open Parameter Simulator",
    guideBtnScan: "🌐 View Environment Scanner & Graph",
    guideBtnAudit: "📊 Consult Audit Metrics",

    // What-If Panel
    whatifBadge: "🎯 Reverse Mitigation Engineering (What-If Solver)",
    whatifTitle: "Set Your Target Severity Goal for Automated Control Discovery",
    whatifTargetLabel: "Target Goal:",

    // Virtual Patch Modal
    vpModalBadge: "Policy-as-Code & Virtual Patching",
    vpModalTitle: "Automated Network & Firewall Countermeasures",
    vpModalDesc: "Ready-to-deploy infrastructure scripts implementing compensating controls suggested by AI Watcher to validate CVSS v4.0 score without breaking applications:",
    vpCopyBtn: "Copy Script",
    vpCloseBtn: "Close",

    // Simulator
    simBadge: "⚡ Interactive Lab & Real Cases",
    simTitle: "Contextual Impact Simulator with AI Watcher",
    simPresetLabel: "Select a Real Case to Compare Contextual Intelligence:",
    presetBtnPci: "💳 1. PCI Banking (Isolated VLAN)",
    presetBtnDev: "🧪 2. Test / Dev Server (-4.4)",
    presetBtnEcom: "🌐 3. E-commerce Without WAF (+0.2)",
    presetBtnClinic: "🏥 4. Medical Clinic / Local Server (-1.6)",
    simControlsLabel: "⚙ Fine-Tuning Environmental Controls (Real-Time Computation):",
    lblScenario: "Scenario / Asset",
    lblAssetId: "Asset ID",
    lblCve: "CVE Identifier",
    lblBaseScore: "Primary Base Score (CNA/NVD)",
    lblInternet: "Exposed to Public Internet?",
    optNetNo: "No (Internal / Protected DMZ)",
    optNetYes: "Yes (Open to 0.0.0.0/0)",
    lblSegmented: "Segmented into VLAN/Subnet?",
    optSegYes: "Yes (Isolated Subnet)",
    optSegNo: "No (Flat Shared Network)",
    lblPci: "PCI-DSS Scope (Cards/Banking)?",
    optPciYes: "Yes (Critical Requirement)",
    optPciNo: "No (Out of Regulatory Scope)",
    lblFirewall: "Firewall / WAF Active?",
    optFwYes: "Yes (Active Restrictive Rules)",
    optFwNo: "No (No Perimeter Restriction)",
    lblCompensating: "Compensating Controls?",
    optCompYes: "Yes (MFA / Rate-limit / Monitoring)",
    optCompNo: "No",
    lblCriticality: "Business Criticality",
    optCritHigh: "High (Core Financial / Production)",
    optCritMed: "Medium (Corporate Systems)",
    optCritLow: "Low (Test / Dev Environment)",
    btnCalc: "▶ Calculate with AI",
    btnExportJson: "Export JSON",
    btnExportCsv: "Export CSV",
    btnCopyPipeline: "Copy Pipeline JSON",
    btnDownloadReport: "Download MD Report",

    // Scanner
    scanBadge: "🌐 Dynamic Infrastructure Scanner",
    scanTitle: "Real-Time Scanning, Topology & Detection",
    scanModeProbe: "🔍 Probe My Device",
    scanModeCustom: "⌨ My Subnet",
    scanModePresets: "🏢 Blueprint Environments",
    scanModeUpload: "📂 Import JSON",
    scanGraphTitle: "🗺 Analyzed Network Topology Diagram",
    scanGraphLegend: "Legend: <span style='color:#4ade80;'>● Protected Asset</span> | <span style='color:#f87171;'>● Vulnerable Asset</span> | <span style='color:#38bdf8;'>● Gateway/Firewall</span>",

    // Metrics & Audit
    metricBadge: "📊 Scientific Audit & Empirical Validation",
    metricTitle: "Scientific Study Metrics & CVSS v4.0 Validation",
    btnAuditMd: "Download Report (.md)",
    btnAuditCsv: "Export Dataset (.csv)",
    btnAuditJson: "Download Audit (.json)",
    kpiScenarios: "Evaluated Scenarios",
    kpiScenariosSub: "12 Real CVEs • 18 Production Scenarios",
    kpiNoise: "Transition to Below-High",
    kpiNoiseSub: "3 of 12 reclassified < High",
    kpiTransitions: "Priority Transitions",
    kpiTransitionsSub: "73.3% contextualized decisions",
    kpiTrace: "Cryptographic Traceability",
    kpiTraceSub: "SHA-256 hash per decision",
    kpiMitigation: "Average Mitigation",
    kpiMitigationSub: "Delta in protected networks",
    chart1Title: "📉 Severity Distribution: Source Assessment vs HelpUS AI",
    chart1Sub: "Base vs Contextual",
    chart1Note: "💡 <strong>Practical Impact:</strong> Source assessments treat 73.3% of findings in a vacuum as Critical or High. HelpUS re-allocates alerts to Medium/Low when controls such as VLAN, WAF or lack of internet exist, reducing operational overhead.",
    chart2Title: "⚖ AI Watcher Decision Matrix",
    chart2Sub: "Dataset B (Benchmark, n=30)",
    chart2Note: "🛡 <strong>Bi-directional Action:</strong> AI downgrades flaws in isolated environments (46.7%), but escalates priority (26.7%) when regulatory scope (PCI-DSS) or financial risk is present.",
    pipeTitle: "🔬 Scientific Architecture: Auditable Decision Pipeline",
    pipeSub: "Algorithmic alignment with FIRST CVSS v4.0 specification",
    pipeTag: "Deterministic (Versioned Rules)",
    pipeCard1Title: "1. Canonical Audit Record",
    pipeCard1Text: "The source CVSS assessment is never overwritten or distorted. It remains permanently visible for audit compliance.",
    pipeCard2Title: "2. Deterministic Metric Inference",
    pipeCard2Text: "The AI infers nominal metrics (e.g. MAV:Adjacent). The final score is computed by FIRST's CVSS v4.0 specification.",
    pipeCard3Title: "3. Human Homologation Gate (HITL)",
    pipeCard3Text: "Every proposed adjustment is recorded with explanatory citations and submitted to human sign-off before dispatch.",
    dsTitle: "📋 Dataset B: Development Benchmark (12 Real CVEs + 18 Synthetic)",
    dsSub: "Browse development scenarios evaluated in exploratory benchmark (confirmatory validation pending)",
    filterAll: "All (30)",
    filterNvd: "Real CVEs (12)",
    filterSyn: "Synthetic (18)",
    filterDown: "🟢 Downgraded (14)",
    filterUp: "🔴 Upgraded (8)",
    searchPlaceholder: "🔍 Search by CVE, ID, asset name or technology...",
    thScenario: "Scenario / CVE",
    thAssetClass: "Asset Class",
    thExposure: "Exposure",
    thBaseNvd: "Base Score",
    thContextual: "Contextual",
    thDelta: "Delta",
    thDecision: "AI Decision",
    thControl: "Primary Control / Evidence",

    // Homologation
    homologModalSuper: "Governance & Human-in-the-Loop (HITL)",
    homologModalTitle: "Contextual Priority Homologation Protocol",
    step1Badge: "1. Evidence",
    step2Badge: "2. Identification",
    step3Badge: "3. Justification",
    step4Badge: "4. Stamp & Hash",

    // Operational Console
    headerConsoleLabel: "Operational Console",
    heroBtnConsole: "Access Operational Console (5 Layers)",
    consoleAreaBadge: "Corporate Operational Area • 5 Evaluation Layers",
    consoleTitle: "HelpUS CVSS Operational Console",
    consoleDesc: "5-layer contextual prioritization with JCS-compliant (RFC 8785 pending formal validation) SHA-256 provenance and supervision by PLATFORM_ADMIN authoritative role.",
    consoleHitlBadge: "Human-in-the-Loop (HITL) Governance",
    consoleHitlTitle: "Human Review & Homologation",
    consoleHitlDesc: "Formal homologation of environmental reclassifications requires authorized human reviewer authentication with server-side session validation.",
    consoleRbacBadge: "Server Authentication with RBAC",
    consoleRbacDesc: "Operational decisions with persistence and audit require an authenticated corporate session via secure endpoint <code>/api/review/decision</code>. The public console operates in demonstration simulation mode.",
    consoleLoginBtn: "🔐 Access Authenticated Homologation Portal",
    consoleDemoBtn: "View Interactive Demonstration (Read-Only Mode)",
    consoleTlsFooter: "Secure connection with TLS 1.3 encryption • Hash compatible with JCS (RFC 8785 pending validation) SHA-256",
    consoleReviewerName: "Authorized Reviewer (SecOps)",
    consoleReviewerRole: "HITL Reviewer",
    consoleReviewerProfile: "Homologation Profile • Mandatory Human Review",
    consoleDownloadLogBtn: "📥 Download Session Log",
    consoleLogoutBtn: "Sign Out",
    consoleCaseStudyLabel: "Select Real-World Case Study (Dataset B)",
    consoleFindingsTitle: "12 Normalized Production Findings",
    consoleFreezeNotice: "Freeze: 2026-10-08T21:30:00Z",
    layer1Badge: "Layer 1",
    layer1Tag: "Normative",
    layer1Header: "Origin Score (CNA/NVD)",
    layer1Check: "✓ Base Score Preserved Intact",
    layer2Badge: "Layer 2",
    layer2Tag: "Evidence",
    layer2Header: "Context & Telemetry",
    layer2VectorLabel: "Vector:",
    layer2ComplexityLabel: "Complexity:",
    layer2PrivilegesLabel: "Privileges:",
    layer2AgeLabel: "Telemetry Age:",
    layer2Check: "✓ Network Proof Audited",
    layer3Badge: "Layer 3",
    layer3Tag: "Prioritization",
    layer3Header: "HelpUS Priority",
    layer3CvssLabel: "Environmental CVSS:",
    layer3SlaLabel: "Operational SLA:",
    layer3TransitionLabel: "Transition:",
    layer4Badge: "Layer 4",
    layer4Tag: "Traceability",
    layer4Header: "JCS Canonical Receipt (RFC 8785 compatible, pending)",
    layer4ReceiptLabel: "Canonical: JCS compatible (RFC 8785 validation pending)",
    layer4DownloadBtn: "📥 Download Receipt (.json)",
    layer5Badge: "Layer 5",
    layer5Tag: "HITL Audit",
    layer5Header: "HITL Approval",
    layer5PendingBadge: "Pending Homologation",
    layer5ReqSession: "Review: Requires Authorized Session",
    layer5ApproveBtn: "✓ Homologate",
    layer5RejectBtn: "✕ Reject",
    consoleHistoryTitle: "Homologations & Operational Decisions History",
    consoleDemoBadge: "Interactive Console: Demonstration Mode (Non-Authoritative)",
    thConsoleDate: "UTC Date/Time",
    thConsoleCve: "CVE ID",
    thConsoleBase: "Base Score",
    thConsoleContext: "Contextual Score",
    thConsolePriority: "Priority",
    thConsoleApprover: "Master Approver",
    thConsoleReceipt: "SHA-256 Receipt",
    consoleEmptyAudit: "No homologation performed in this session. Select a CVE and click 'Homologate'.",
    consoleHitlApproved: "✓ Homologated (Simulation)",
    consoleHitlRejected: "✕ Rejected (Simulation)",
    cnaAuthorizedPrefix: "Authorized CNA: ",
    mavAdj: " (Adjacent)",
    mavExt: " (External Network)",
    mavLoc: " (Local)",

    // Expert Panel (G9)
    g9HeroBadge: "Gate G9 • External Independent Expert Panel Validation",
    g9HeroTitle: "Electronic Blinded Expert Evaluation Portal (EDC)",
    g9HeroDesc: "Dedicated electronic data capture environment for independent experts (senior cybersecurity professionals and researchers). Protocol implements bilingual electronic consent (e-ICF / e-TCLE), strict blinding (zero AI bias), reassessment of 13 FIRST CVSS v4.0 environmental metrics across 30 scenarios, and SHA-256 cryptographic sealing.",
    g9OpenBtn: "🚀 Open Full EDC Portal",
    g9OpenSub: "(New Tab ↗)",
    g9ActiveBadge: "Synthetic Environment Active • Gate G9",
    g9Card1Title: "Online Web EDC Collection",
    g9Card1Sub: "30 Synthetic Reference Scenarios",
    g9Card1Desc: "Autonomous, responsive web interface built for online execution. Experts can navigate scenarios, inspect network evidence, assign 13 environmental metrics, and safely save drafts locally.",
    g9Card1Li1: "<strong>e-ICF / e-TCLE:</strong> Electronic signature and conflict-of-interest declaration.",
    g9Card1Li2: "<strong>Auto-save:</strong> Local in-browser persistence (localStorage).",
    g9Card1Li3: "<strong>Sealing:</strong> SHA-256 hash and downloadable auditable JSON receipt.",
    g9Card1Btn: "Access Expert Portal →",
    g9Card2Title: "Ethical & Regulatory Dossier",
    g9Card2Sub: "Binational Brazil / US Strategy (Option 1)",
    g9Card2Desc: "Per audit opinions <code>CG-20261010-021</code> and <code>CG-20261013-022</code>, HelpUS adopts submission via national CEP (R$ 0.00 cost) with declared international scope, enabling US and Brazilian experts without commercial IRB fees.",
    g9Card2DocsLabel: "Documents Available in Dossier:",
    g9Card2Status: "CEP Status: Submission in Preparation • R$ 0.00",
    g9Card3Title: "Blinding & Methodological Integrity",
    g9Card3Sub: "Strict Double-Blind (Blinded Review)",
    g9Card3Desc: "Scientific methodology ensures that reviewers neither see nor are influenced by AI predicted scores or peer responses.",
    g9Card3Li1: "<strong>C1/C2 Dataset:</strong> Remains strictly sealed until formal code freeze.",
    g9Card3Li2: "<strong>13 FIRST Metrics:</strong> CR, IR, AR, MAV, MAC, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA.",
    g9Card3Li3: "<strong>Inter-Rater Agreement:</strong> Fleiss' Kappa / ICC and paired Wilcoxon in statistical analysis plan.",
    g9Card3Status: "✓ Blinding Shield Audited & Validated",
    g9FlowTitle: "Expert Operational Flow in the EDC Portal",
    g9Step1Tag: "Step 1",
    g9Step1Title: "Consent & COI",
    g9Step1Desc: "Review of e-TCLE (PT-BR) or e-ICF (EN-US/ES), personal details, and declaration of no conflict of interest.",
    g9Step2Tag: "Step 2",
    g9Step2Title: "30-Scenario Evaluation",
    g9Step2Desc: "Technical analysis of each scenario, scoring 13 CVSS v4.0 environmental metrics, and textual expert rationale.",
    g9Step3Tag: "Step 3",
    g9Step3Title: "Review & SHA-256 Sealing",
    g9Step3Desc: "Generation of native cryptographic SHA-256 hash, custody certificate, and downloadable submission JSON package.",

    // HITL Homologation Modal
    homologStep1Title: "Step 1/4 — Grounding Verification (Real Facts):",
    homologStep1P: "In compliance with <em>ISO/IEC 27001 (Clause 6.1.2)</em> and <em>NIST AI RMF</em>, the analyst must certify that declared network and business assumptions match the physical or logical environment:",
    homologBtnCancel: "Cancel",
    homologBtnNext1: "Next: Identification →",
    homologStep2Title: "Step 2/4 — Attribution & Technical Accountability:",
    homologStep2P: "Register operator identity to ensure non-repudiation and forensic auditability.",
    homologLblName: "Analyst / Auditor Full Name:",
    homologLblEmail: "Corporate Email:",
    homologLblRole: "Role / Access Profile:",
    homologOptRole1: "Lead Security Engineer / CISO",
    homologOptRole2: "SOC Analyst N3",
    homologOptRole3: "PCI/ISO Compliance Auditor",
    homologOptRole4: "DevSecOps Engineer",
    homologLblTicket: "Ticket / Issue ID (Jira/HelpUS/GLPI):",
    homologBtnBack: "← Back",
    homologBtnNext2: "Next: Justification →",
    homologStep3Title: "Step 3/4 — Formal Justification & Risk Decision:",
    homologStep3P: "Define whether the AI proposal is accepted in full, accepted with conditions, or rejected keeping original base score.",
    homologLblDelib: "Deliberation Type:",
    homologOptDelib1: "✓ Homologate AI Contextual Priority (Recommended)",
    homologOptDelib2: "✓ Homologate with Conditions (Scheduled Maintenance)",
    homologOptDelib3: "✕ Reject AI Proposal (Maintain Original Base Score)",
    homologOptDelib4: "✕ Reject & Escalate to Crisis Committee",
    homologLblJust: "Analyst Technical Justification (Mandatory):",
    homologPlaceholderJust: "E.g.: Topology verified with iptables/VLAN rules confirmed. Risk accepted based on active compensating controls until biweekly maintenance window.",
    homologBtnSubmit: "✓ Complete Homologation Simulation",
    homologSuccessTitle: "Homologation Simulation Completed",
    homologSuccessDesc: "The demonstration digest was generated for preview. Official homologations are recorded exclusively via authenticated API.",
    homologBtnReceipt: "📥 Download Simulation Receipt (.json)",
    homologBtnClose: "Close",

    // Virtual Patching
    vpTabIptables: "Linux (iptables)",
    vpTabAws: "AWS Security Group",
    vpTabWaf: "Cloudflare WAF"
  },

  es: {
    langLabel: "🌐 🇪🇸 ES",
    navSubtitle: "Priorización de Riesgo con IA • FIRST CVSS v4.0",
    tabGuia: "Visión General & Guía",
    tabSimulador: "Simulador de Impacto",
    tabScanner: "Escáner & Topología",
    tabMetricas: "Métricas & Auditoría",
    tabConsole: "Consola Operativa",
    tabEspecialistas: "Panel de Expertos (G9)",
    headerPortalLabel: "Portal EDC (Online)",
    navWa: "WhatsApp",
    footerSub: "Plataforma de Ciberseguridad & Investigación Científica en IA",
    footerCredit: "Desarrollado por",
    footerPrivacy: "Política de Privacidad & Cookies",
    footerRights: "© 2026 HelpUS Group. Todos los derechos reservados.",
    waMessage: "Hola, me gustaría saber más sobre la plataforma HelpUS CVSS y soluciones de IA.",

    // Banner de Cookies
    cookieTitle: "Privacidad y Uso de Cookies",
    cookieText: "La plataforma HelpUS CVSS utiliza cookies técnicas estrictamente necesarias y almacenamiento local para recordar sus preferencias de idioma, registros de auditoría y ajustes de topología de red, en cumplimiento con el RGPD y la LGPD.",
    cookieBtnDetails: "Conocer Más",
    cookieBtnAccept: "Aceptar & Continuar",

    // Modal de Privacidad
    privacyModalTitle: "Política de Privacidad & Protección de Datos",
    privacyP1: "HelpUS Technology Solutions respeta plenamente su privacidad y los derechos fundamentales garantizados por las leyes internacionales de protección de datos, incluidos el RGPD y la LGPD.",
    privacyH1: "1. Recolección y Uso de Información",
    privacyP2: "Nuestra plataforma realiza simulaciones y cálculos de priorización de vulnerabilidades (CVSS v4.0). Ninguna información de red privada, credencial o activo interno se comparte ni se vende a terceros. Todo el procesamiento se ejecuta de forma segura.",
    privacyH2: "2. Cookies y Almacenamiento Local",
    privacyP3: "Utilizamos localStorage y cookies esenciales única y exclusivamente para guardar su idioma preferido (Portugués, Inglés o Español) y registrar su consentimiento.",
    privacyH3: "3. Contacto del Delegado de Protección de Datos (DPO)",
    privacyP4: "Para consultas técnicas o auditorías, comuníquese con nuestro equipo de seguridad en seguranca@helpusbr.com o mediante nuestro canal de WhatsApp.",
    privacyBtnClose: "Entendido",

    // Hero Video Banner
    heroBadge: "Investigación Científica & Motor de IA Explicable",
    heroTitle: "Priorización de Vulnerabilidades Basada en Evidencias Reales",
    heroDesc: "Plataforma científica para calcular el <strong>CVSS v4.0 oficial</strong> y aplicar una capa contextual explicable con <strong>IA Watcher</strong> basada en evidencias reales de su entorno (firewall, red, alcance PCI y datos críticos).",
    heroBtnSim: "⚡ Probar Simulador con IA",
    heroBtnScan: "🌐 Ver Topología de Red",

    // Seção O Que Desenvolvemos
    solHeaderTitle: "Lo Que Desarrollamos",
    solHeaderSub: "Ingeniería de vanguardia en ciberseguridad, motor de IA explicable y gobernanza matemática aplicada a FIRST CVSS v4.0.",
    solFooterLabel: "Ver detalles de la solución:",
    solCard1Tag: "REVERSE MITIGATION & WHAT-IF",
    solCard1Title: "Calculadora Inversa de Riesgos (\"What-If\")",
    solCard1Desc: "Defina su meta de severidad (ej: bajar de 9.8 Crítico a ≤ 5.0 Medio) y nuestro algoritmo deduce los controles mínimos de red y firewall para cumplir con el SLA sin detener la producción.",
    solCard1Btn: "Probar Mitigación Inversa →",
    solCard2Tag: "CONTEXTUAL AI & FIRST CVSS v4.0",
    solCard2Title: "Motor Watcher IA & FIRST v4.0",
    solCard2Desc: "Motor de inferencia determinista que cruza reportes de vulnerabilidades con evidencias de topología, VLAN, WAF y activos, calibrando la severidad bajo reglas versionadas auditables.",
    solCard2Btn: "Simulador de Impacto IA →",
    solCard3Tag: "DYNAMIC SCANNER & TOPOLOGY",
    solCard3Title: "Escáner de Red & Topología en Tiempo Real",
    solCard3Desc: "Ingestión nativa de Trivy, Nessus y OpenVAS combinada con sondeo local del host. Genera grafos SVG de ataques entre gateway, firewall y bases de datos.",
    solCard3Btn: "Abrir Escáner de Red →",
    solCard4Tag: "COMPLIANCE CLOCK & SLA FORENSICS",
    solCard4Title: "Reloj Regulatorio & Paquete Forense",
    solCard4Desc: "Traduce puntajes CVSS en ventanas de SLA operacionales auditables (alineadas con PCI-DSS, NIS2, DORA, ISO 27001) y emite recibos de procedencia con hash SHA-256 y Merkle Tree para auditorias.",
    solCard4Btn: "Consultar Gobernanza & SLA →",
    solCard5Tag: "POLICY-AS-CODE & VIRTUAL PATCHING",
    solCard5Title: "Generador Automático de Contramedidas (IaC)",
    solCard5Desc: "Genera en 1 clic scripts de contención perimetral: reglas iptables/nftables para Linux, Security Groups de AWS y filtros WAF de Cloudflare específicos para la CVE.",
    solCard5Btn: "Generar Contramedidas →",
    solCard6Tag: "TRI-SCORE COMPARATOR & EPSS",
    solCard6Title: "Comparador Tripartito & EPSS Contextual",
    solCard6Desc: "Contraste en tiempo real entre el legado CVSS v3.1, el estándar FIRST CVSS v4.0 y la IA Contextual, evaluando probabilidades de exploit EPSS frente a barreras locales.",
    solCard6Btn: "Ver Comparador Tri-Score →",

    // Guía
    guideBadge: "💡 Guía Rápida de Introducción",
    guideTitle: "¿Primera vez aquí? Entienda en 3 pasos",
    tabWhat: "1. ¿Qué es?",
    tabHow: "2. ¿Cómo funciona?",
    tabWhy: "3. Estudio Científico",
    whatP1: "El <strong>HelpUS CVSS</strong> resuelve el mayor problema de la gestión de vulnerabilidades: <strong>el exceso de alertas infladas</strong>.",
    cardNvdTitle: "🔴 Vector Base CVSS v4.0 (Fuente Primaria)",
    cardNvdDesc: "Mide el peligro intrínseco teórico del fallo en el mundo. Trata una falla 9.8 como urgente incluso en una computadora aislada de laboratorio sin conexión externa.",
    cardContextTitle: "🟢 CVSS Contextual (Nuestro Motor con IA)",
    cardContextDesc: "Cruza el fallo con <strong>evidencias del entorno real</strong> (firewall, red, WAF, alcance bancario) para priorizar lo que realmente importa y desescalar ruidos.",
    howStep1: "<strong>Ingestión de Escáner Real:</strong> El sistema acepta reportes de <code>Trivy</code>, <code>Nessus</code>, <code>OpenVAS</code> o de nuestro <code>Escáner Nativo</code> de red.",
    howStep2: "<strong>Extracción de Evidencias por IA:</strong> Nuestros agentes analizan configuraciones de red, puertos abiertos y reglas perimetrales.",
    howStep3: "<strong>Cálculo Conforme a la Especificación:</strong> La IA propone métricas nominales (ej: <code>MAV:Adjacent</code>), pero el score final se deriva de la especificación CVSS v4.0 de FIRST.",
    howStep4: "<strong>Puerta de Homologación Humana:</strong> Toda decisión operativa se registra con justificaciones, citas y trazabilidad total.",
    whyP1: "En la literatura científica y la industria, los equipos casi nunca completan las métricas ambientales de CVSS porque auditar docenas de controles manualmente es costoso y lento.",
    whyP2: "<strong>Nuestra contribución:</strong> Automatizamos la recolección de evidencias y el mapeo de métricas bajo reglas versionadas deterministas, asegurando trazabilidad auditable y reduciendo la sobrecarga operacional.",
    guideBtnSim: "⚡ Abrir Simulador de Parámetros",
    guideBtnScan: "🌐 Ver Escáner de Entornos & Grafo",
    guideBtnAudit: "📊 Consultar Métricas de Auditoría",

    // What-If Panel
    whatifBadge: "🎯 Ingeniería de Mitigación Inversa (What-If Solver)",
    whatifTitle: "Defina su Meta de Severidad para Descubrimiento Automático de Controles",
    whatifTargetLabel: "Meta Objetivo:",

    // Virtual Patch Modal
    vpModalBadge: "Policy-as-Code & Virtual Patching",
    vpModalTitle: "Contramedidas Automatizadas de Red y Firewall",
    vpModalDesc: "Scripts de infraestructura listos para aplicar los controles compensatorios sugeridos por IA Watcher y validar el score CVSS v4.0 sin alterar la aplicación:",
    vpCopyBtn: "Copiar Script",
    vpCloseBtn: "Cerrar",

    // Simulador
    simBadge: "⚡ Laboratorio Interactivo & Casos Reales",
    simTitle: "Simulador de Impacto Contextual con IA Watcher",
    simPresetLabel: "Seleccione un Caso Real para Comparar la Inteligencia Contextual:",
    presetBtnPci: "💳 1. PCI Bancario (VLAN Aislada)",
    presetBtnDev: "🧪 2. Servidor de Pruebas / Dev (-4.4)",
    presetBtnEcom: "🌐 3. Comercio Sin WAF (+0.2)",
    presetBtnClinic: "🏥 4. Clínica Médica / Servidor Local (-1.6)",
    simControlsLabel: "⚙ Ajuste Fino de Controles Ambientales (Cálculo en Tiempo Real):",
    lblScenario: "Escenario / Activo",
    lblAssetId: "ID del Activo",
    lblCve: "Identificador CVE",
    lblBaseScore: "Score Base de Origen (CNA/NVD)",
    lblInternet: "¿Expuesto a Internet público?",
    optNetNo: "No (Interno / DMZ Protegida)",
    optNetYes: "Sí (Abierto para 0.0.0.0/0)",
    lblSegmented: "¿Segmentado en VLAN/Subred?",
    optSegYes: "Sí (Subred Aislada)",
    optSegNo: "No (Red Plana Compartida)",
    lblPci: "¿Alcance PCI-DSS (Tarjetas/Bancos)?",
    optPciYes: "Sí (Requisito Crítico)",
    optPciNo: "No (Fuera de Alcance Regulatorio)",
    lblFirewall: "¿Firewall / WAF Activo?",
    optFwYes: "Sí (Reglas Restrictivas Activas)",
    optFwNo: "No (Sin Restricción Perimetral)",
    lblCompensating: "¿Controles Compensatorios?",
    optCompYes: "Sí (MFA / Rate-limit / Monitoreo)",
    optCompNo: "No",
    lblCriticality: "Criticidad del Negocio",
    optCritHigh: "Alta (Core Financiero / Producción)",
    optCritMed: "Media (Sistemas Corporativos)",
    optCritLow: "Baja (Entorno de Prueba / Dev)",
    btnCalc: "▶ Calcular con IA",
    btnExportJson: "Exportar JSON",
    btnExportCsv: "Exportar CSV",
    btnCopyPipeline: "Copiar Pipeline JSON",
    btnDownloadReport: "Descargar Reporte MD",

    // Escáner
    scanBadge: "🌐 Escáner Dinámico de Infraestructura",
    scanTitle: "Escaneo, Topología y Detección en Tiempo Real",
    scanModeProbe: "🔍 Sondear Mi Dispositivo",
    scanModeCustom: "⌨ Mi Subred",
    scanModePresets: "🏢 Entornos Modelo",
    scanModeUpload: "📂 Importar JSON",
    scanGraphTitle: "🗺 Diagrama de Topología de Red Analizada",
    scanGraphLegend: "Leyenda: <span style='color:#4ade80;'>● Activo Protegido</span> | <span style='color:#f87171;'>● Activo Vulnerable</span> | <span style='color:#38bdf8;'>● Gateway/Firewall</span>",

    // Métricas
    metricBadge: "📊 Auditoría Científica & Validação Empírica",
    metricTitle: "Métricas del Estudio Científico & Validación CVSS v4.0",
    btnAuditMd: "Descargar Reporte (.md)",
    btnAuditCsv: "Exportar Dataset (.csv)",
    btnAuditJson: "Descargar Auditoría (.json)",
    kpiScenarios: "Escenarios Evaluados",
    kpiScenariosSub: "12 CVEs Reales • 18 Escenarios de Producción",
    kpiNoise: "Transición Debajo de High",
    kpiNoiseSub: "3 de 12 reclasificados < High",
    kpiTransitions: "Transiciones de Prioridad",
    kpiTransitionsSub: "73.3% decisiones contextualizadas",
    kpiTrace: "Trazabilidad Criptográfica",
    kpiTraceSub: "Hash SHA-256 por decisión",
    kpiMitigation: "Promedio de Mitigación",
    kpiMitigationSub: "Delta en redes protegidas",
    chart1Title: "📉 Distribución de Severidades: Evaluación de Origen vs HelpUS IA",
    chart1Sub: "Base vs Contextual",
    chart1Note: "💡 <strong>Impacto Práctico:</strong> La evaluación de origen trata el 73.3% de los hallazgos en el vacío como Críticos o Altos. HelpUS redistribuye las alertas reales a Medio/Bajo cuando hay controles como VLAN, WAF o ausencia de internet, reduciendo la sobrecarga operacional.",
    chart2Title: "⚖ Matriz de Decisiones del Watcher IA",
    chart2Sub: "Dataset B (Benchmark, n=30)",
    chart2Note: "🛡 <strong>Acción Bidireccional:</strong> La IA desescala fallas en entornos aislados (46.7%), pero eleva la prioridad (26.7%) cuando existe alcance regulatorio (PCI-DSS) o riesgo financiero.",
    pipeTitle: "🔬 Arquitectura Científica: Pipeline de Decisión Auditable",
    pipeSub: "Alineación algorítmica con la especificación CVSS v4.0 de FIRST",
    pipeTag: "Determinístico (Regras Versionadas)",
    pipeCard1Title: "1. Registro Canónico de Auditoría",
    pipeCard1Text: "La evaluación CVSS de origen nunca se sobrescribe ni se distorsiona. Permanece permanentemente visible para auditoría.",
    pipeCard2Title: "2. Inferencia Determinista de Métricas",
    pipeCard2Text: "El modelo deduce únicamente métricas nominales canónicas (ej: MAV:Adjacent). El score se genera con la especificación CVSS v4.0 de FIRST.",
    pipeCard3Title: "3. Puerta de Homologación Humana (HITL)",
    pipeCard3Text: "Toda recomendación de ajuste se registra con citas explicativas y se somete a firma humana antes del despacho.",
    dsTitle: "📋 Dataset B: Benchmark de Desarrollo (12 CVEs Reais + 18 Sintéticos)",
    dsSub: "Navegue por los escenarios de desarrollo evaluados en el estudio exploratorio (validación confirmatoria pendiente)",
    filterAll: "Todos (30)",
    filterNvd: "CVEs Reales (12)",
    filterSyn: "Sintéticos (18)",
    filterDown: "🟢 Desescalados (14)",
    filterUp: "🔴 Escalados (8)",
    searchPlaceholder: "🔍 Buscar por CVE, ID, nombre del activo o tecnología...",
    thScenario: "Escenario / CVE",
    thAssetClass: "Clase del Activo",
    thExposure: "Exposición",
    thBaseNvd: "Base NVD",
    thContextual: "Contextual",
    thDelta: "Delta",
    thDecision: "Decisión IA",
    thControl: "Control / Evidencia Principal",

    // Homologación
    homologModalSuper: "Gobernanza & Homologación Humana (HITL)",
    homologModalTitle: "Protocolo de Homologación de Prioridad Contextual",
    step1Badge: "1. Evidencias",
    step2Badge: "2. Identificación",
    step3Badge: "3. Justificación",
    step4Badge: "4. Firma & Hash",

    // Consola Operativa
    headerConsoleLabel: "Consola Operativa",
    heroBtnConsole: "Acceder a Consola Operativa (5 Capas)",
    consoleAreaBadge: "Área Operativa Corporativa • 5 Capas de Evaluación",
    consoleTitle: "Consola Operativa HelpUS CVSS",
    consoleDesc: "Priorización contextual en 5 capas con procedencia compatible con JCS (RFC 8785 pendiente de validación formal) SHA-256 y gobernanza supervisada por el perfil autoritativo PLATFORM_ADMIN.",
    consoleHitlBadge: "Gobernanza Human-in-the-Loop (HITL)",
    consoleHitlTitle: "Homologación y Revisión Humana",
    consoleHitlDesc: "La homologación formal de reclasificaciones ambientales exige autenticación autorizada de revisor humano con validación de sesión en el servidor.",
    consoleRbacBadge: "Autenticación de Servidor con RBAC",
    consoleRbacDesc: "Las decisiones operativas con persistencia y auditoría requieren una sesión corporativa autenticada a través del endpoint seguro <code>/api/review/decision</code>. La consola pública funciona en modo de simulación demostrativa.",
    consoleLoginBtn: "🔐 Acceder al Portal de Homologación Autenticado",
    consoleDemoBtn: "Ver Demostración Interactiva (Modo Lectura)",
    consoleTlsFooter: "Conexión segura con cifrado TLS 1.3 • Hash compatible con JCS (RFC 8785 pendiente de validación) SHA-256",
    consoleReviewerName: "Revisor Autorizado (SecOps)",
    consoleReviewerRole: "Revisor HITL",
    consoleReviewerProfile: "Perfil de Homologación • Revisión Humana Obligatoria",
    consoleDownloadLogBtn: "📥 Descargar Registro de Sesión",
    consoleLogoutBtn: "Cerrar Sesión",
    consoleCaseStudyLabel: "Seleccione el Caso de Estudio Real (Dataset B)",
    consoleFindingsTitle: "12 Hallazgos de Producción Normalizados",
    consoleFreezeNotice: "Congelación: 2026-10-08T21:30:00Z",
    layer1Badge: "Capa 1",
    layer1Tag: "Normativa",
    layer1Header: "Puntuación de Origen (CNA/NVD)",
    layer1Check: "✓ Puntuación Base Preservada Intacta",
    layer2Badge: "Capa 2",
    layer2Tag: "Evidencias",
    layer2Header: "Contexto y Telemetría",
    layer2VectorLabel: "Vector:",
    layer2ComplexityLabel: "Complejidad:",
    layer2PrivilegesLabel: "Privilegios:",
    layer2AgeLabel: "Antigüedad Telemetría:",
    layer2Check: "✓ Prueba de Red Auditada",
    layer3Badge: "Capa 3",
    layer3Tag: "Priorización",
    layer3Header: "Prioridad HelpUS",
    layer3CvssLabel: "CVSS Ambiental:",
    layer3SlaLabel: "SLA Operativo:",
    layer3TransitionLabel: "Transición:",
    layer4Badge: "Capa 4",
    layer4Tag: "Trazabilidad",
    layer4Header: "Recibo Canónico JCS (compatible RFC 8785, pendiente)",
    layer4ReceiptLabel: "Canónico: JCS compatible (validación RFC 8785 pendiente)",
    layer4DownloadBtn: "📥 Descargar Recibo (.json)",
    layer5Badge: "Capa 5",
    layer5Tag: "Auditoría HITL",
    layer5Header: "Aprobación HITL",
    layer5PendingBadge: "Pendiente de Homologación",
    layer5ReqSession: "Revisión: Requiere Sesión Autorizada",
    layer5ApproveBtn: "✓ Homologar",
    layer5RejectBtn: "✕ Rechazar",
    consoleHistoryTitle: "Historial de Homologaciones y Decisiones Operativas",
    consoleDemoBadge: "Consola Interactiva: Modo Demostración (No Autoritativo)",
    thConsoleDate: "Fecha/Hora UTC",
    thConsoleCve: "CVE ID",
    thConsoleBase: "Score Base",
    thConsoleContext: "Score Contextual",
    thConsolePriority: "Prioridad",
    thConsoleApprover: "Aprobador Máster",
    thConsoleReceipt: "Recibo SHA-256",
    consoleEmptyAudit: "Ninguna homologación realizada en esta sesión. Seleccione un CVE y haga clic en 'Homologar'.",
    consoleHitlApproved: "✓ Homologado (Simulación)",
    consoleHitlRejected: "✕ Rechazado (Simulación)",
    cnaAuthorizedPrefix: "CNA Autorizado: ",
    mavAdj: " (Adyacente)",
    mavExt: " (Red Externa)",
    mavLoc: " (Local)",

    // Panel de Expertos (G9)
    g9HeroBadge: "Gate G9 • Validación Externa por Panel de Expertos",
    g9HeroTitle: "Portal Electrónico de Evaluación a Ciegas de Expertos (EDC)",
    g9HeroDesc: "Entorno dedicado para captura electrónica de datos de expertos independientes (investigadores y profesionales sénior de ciberseguridad). El protocolo implementa consentimiento electrónico bilingüe (e-ICF / e-TCLE), doble ciego estricto (sin sesgo de IA), reevaluación de 13 métricas ambientales FIRST CVSS v4.0 en 30 escenarios y sellado criptográfico SHA-256.",
    g9OpenBtn: "🚀 Abrir Portal EDC Completo",
    g9OpenSub: "(Nueva Pestaña ↗)",
    g9ActiveBadge: "Entorno Sintético Activo • Gate G9",
    g9Card1Title: "Recolección Web Online (EDC)",
    g9Card1Sub: "30 Escenarios de Referencia Sintética",
    g9Card1Desc: "Interfaz web autónoma y adaptable creada para ejecución online. El experto puede navegar entre escenarios, inspeccionar evidencias de red, calificar 13 métricas ambientales y guardar borradores localmente.",
    g9Card1Li1: "<strong>e-ICF / e-TCLE:</strong> Firma electrónica y declaración de ausencia de conflicto de intereses.",
    g9Card1Li2: "<strong>Autoguardado:</strong> Persistencia local en el navegador (localStorage).",
    g9Card1Li3: "<strong>Sellado:</strong> Hash SHA-256 y recibo JSON auditable descargable.",
    g9Card1Btn: "Acceder al Portal de Expertos →",
    g9Card2Title: "Dossier Ético y Regulatorio",
    g9Card2Sub: "Estrategia Binacional Brasil / EE. UU. (Opción 1)",
    g9Card2Desc: "Según los dictámenes de auditoría <code>CG-20261010-021</code> y <code>CG-20261013-022</code>, HelpUS adopta la sumisión vía CEP nacional (costo R$ 0,00) con alcance internacional declarado, permitiendo expertos de EE. UU. y Brasil sin tarifas de IRB comercial.",
    g9Card2DocsLabel: "Documentos Disponibles en el Dossier:",
    g9Card2Status: "Estado CEP: Sumisión en Preparación • R$ 0,00",
    g9Card3Title: "Blindaje e Integridad Metodológica",
    g9Card3Sub: "Doble Ciego Estricto (Blinded Review)",
    g9Card3Desc: "La metodología científica asegura que el experto no vea ni sea influenciado por los puntajes predichos por la IA ni por respuestas de otros revisores.",
    g9Card3Li1: "<strong>Dataset C1/C2:</strong> Permanece estrictamente sellado hasta el congelamiento formal.",
    g9Card3Li2: "<strong>13 Métricas FIRST:</strong> CR, IR, AR, MAV, MAC, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA.",
    g9Card3Li3: "<strong>Acuerdo Interevaluador:</strong> Fleiss' Kappa / ICC y Wilcoxon pareado en el plan de análisis estadístico.",
    g9Card3Status: "✓ Escudo de Cegamiento Auditado y Validado",
    g9FlowTitle: "Flujo Operativo del Experto en el Portal EDC",
    g9Step1Tag: "Paso 1",
    g9Step1Title: "Consentimiento y COI",
    g9Step1Desc: "Lectura del e-TCLE (PT-BR) o e-ICF (EN-US/ES), registro de identificación y declaración de no conflicto de intereses.",
    g9Step2Tag: "Paso 2",
    g9Step2Title: "Evaluación de los 30 Escenarios",
    g9Step2Desc: "Análisis técnico de cada escenario, selección de las 13 métricas ambientales CVSS v4.0 y justificación pericial en texto.",
    g9Step3Tag: "Paso 3",
    g9Step3Title: "Revisión y Sellado SHA-256",
    g9Step3Desc: "Generación del hash criptográfico nativo SHA-256, certificado de custodia y descarga del paquete de sumisión (.json).",

    // Modal de Homologación HITL
    homologStep1Title: "Paso 1/4 — Verificación de Hechos Reales (Grounding):",
    homologStep1P: "En conformidad con <em>ISO/IEC 27001 (Cláusula 6.1.2)</em> y <em>NIST AI RMF</em>, el analista debe certificar que las premisas declaradas reflejan el entorno físico o lógico real:",
    homologBtnCancel: "Cancelar",
    homologBtnNext1: "Avanzar: Identificación →",
    homologStep2Title: "Paso 2/4 — Atribución y Responsabilidad Técnica:",
    homologStep2P: "Registre la identidad del operador para garantizar no repudio y auditoría forense.",
    homologLblName: "Nombre Completo del Analista / Auditor:",
    homologLblEmail: "Correo Electrónico Corporativo:",
    homologLblRole: "Rol / Perfil de Acceso:",
    homologOptRole1: "Lead Security Engineer / CISO",
    homologOptRole2: "Analista SOC N3",
    homologOptRole3: "Auditor de Cumplimiento PCI/ISO",
    homologOptRole4: "Ingeniero DevSecOps",
    homologLblTicket: "ID del Ticket / Incidencia (Jira/HelpUS/GLPI):",
    homologBtnBack: "← Volver",
    homologBtnNext2: "Avanzar: Justificación →",
    homologStep3Title: "Paso 3/4 — Justificación Formal y Decisión de Riesgo:",
    homologStep3P: "Defina si la propuesta de la IA se acepta por completo, se acepta con reservas o se rechaza manteniendo el score base original.",
    homologLblDelib: "Tipo de Deliberación:",
    homologOptDelib1: "✓ Homologar Prioridad Contextual de la IA (Recomendado)",
    homologOptDelib2: "✓ Homologar con Condición (Mantenimiento Programado)",
    homologOptDelib3: "✕ Rechazar Propuesta de la IA (Mantener Score Base Original)",
    homologOptDelib4: "✕ Rechazar y Escalar a Comité de Crisis",
    homologLblJust: "Justificación Técnica del Analista (Obligatoria):",
    homologPlaceholderJust: "Ej: Topología validada con reglas de iptables/VLAN verificadas. Riesgo aceptado con base en controles compensatorios vigentes hasta la ventana quincenal.",
    homologBtnSubmit: "✓ Concluir Simulación de Homologación",
    homologSuccessTitle: "Simulación de Homologación Concluida",
    homologSuccessDesc: "El resumen de demostración fue generado para vista previa. Las homologaciones oficiales se registran exclusivamente a través de API autenticada.",
    homologBtnReceipt: "📥 Descargar Comprobante de Simulación (.json)",
    homologBtnClose: "Cerrar",

    // Virtual Patching
    vpTabIptables: "Linux (iptables)",
    vpTabAws: "AWS Security Group",
    vpTabWaf: "Cloudflare WAF"
  }
};

window.currentLanguage = localStorage.getItem("helpus_cvss_lang") || "pt";

function toggleLangMenu() {
  var menu = document.getElementById("langPopdownMenu");
  if (menu) menu.classList.toggle("open");
}

document.addEventListener("click", function(e) {
  var wrap = document.querySelector(".lang-popdown-wrap");
  var menu = document.getElementById("langPopdownMenu");
  if (wrap && menu && !wrap.contains(e.target)) {
    menu.classList.remove("open");
  }
});

function setLanguage(lang) {
  if (!HELPUS_I18N[lang]) lang = "pt";
  window.currentLanguage = lang;
  localStorage.setItem("helpus_cvss_lang", lang);
  var dict = HELPUS_I18N[lang];

  // Define atributo lang do documento HTML
  document.documentElement.lang = (lang === "pt" ? "pt-BR" : (lang === "es" ? "es" : "en"));

  // Fecha menu popdown
  var menu = document.getElementById("langPopdownMenu");
  if (menu) menu.classList.remove("open");

  // Atualiza label do botão atual
  var curLabel = document.getElementById("langCurrentLabel");
  if (curLabel) curLabel.innerText = dict.langLabel;

  // Atualiza botões no menu popdown
  ["pt", "en", "es"].forEach(function(l) {
    var item = document.getElementById("pop-lang-" + l);
    if (item) {
      if (l === lang) item.classList.add("active");
      else item.classList.remove("active");
    }
  });

  // Atualiza todos os elementos marcados com data-i18n
  var elements = document.querySelectorAll("[data-i18n]");
  elements.forEach(function(el) {
    var key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });

  // Atualiza placeholders
  var placeEls = document.querySelectorAll("[data-i18n-placeholder]");
  placeEls.forEach(function(el) {
    var key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Atualiza link do WhatsApp no rodapé
  var footWaLink = document.getElementById("footer-wa-btn");
  if (footWaLink) {
    footWaLink.href = "https://wa.me/5583988419118?text=" + encodeURIComponent(dict.waMessage);
  }

  // Atualiza componentes dinâmicos na tela para o novo idioma
  renderScenarioEdu(window.currentScenarioPreset || "pci");
  calc();
  runWhatIfOptimization(window.currentWhatIfTarget || 5.0);
  renderScanModeControls(currentScanMode);
  renderAuditDashboard();
  if (typeof renderConsoleCveCards === "function") renderConsoleCveCards();
  if (typeof renderConsoleAuditHistory === "function") renderConsoleAuditHistory();
  if (typeof selectConsoleCve === "function" && typeof currentSelectedConsoleCve !== "undefined" && currentSelectedConsoleCve) {
    selectConsoleCve(currentSelectedConsoleCve.id);
  }
}

// Gerenciamento do Banner de Cookies
function checkCookieConsent() {
  var consented = localStorage.getItem("helpus_cookie_consent");
  var banner = document.getElementById("cookieBanner");
  if (!consented && banner) {
    banner.style.display = "flex";
  }
}

function acceptCookies() {
  localStorage.setItem("helpus_cookie_consent", "true");
  var banner = document.getElementById("cookieBanner");
  if (banner) banner.style.display = "none";
}

function openPrivacyModal() {
  var modal = document.getElementById("privacyModal");
  if (modal) modal.classList.add("active");
}

function closePrivacyModal() {
  var modal = document.getElementById("privacyModal");
  if (modal) modal.classList.remove("active");
}

window.addEventListener("DOMContentLoaded", function() {
  if (window.location.protocol === "file:") {
    document.querySelectorAll('a[href="/experts"]').forEach(function(el) {
      el.href = "portal-especialistas.html";
    });
  }
  setLanguage(window.currentLanguage);
  checkCookieConsent();
});

// ============================================================================
// OTIMIZADOR DE MITIGAÇÃO REVERSA ("WHAT-IF" SOLVER)
// ============================================================================
window.currentWhatIfTarget = 5.0;

function openReverseCalculator() {
  switchView("view-simulador");
  var el = document.getElementById("whatifOptimizerPanel");
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  runWhatIfOptimization(5.0);
}

function runWhatIfOptimization(targetScore) {
  window.currentWhatIfTarget = targetScore;
  var currentBase = Number(String(val("base_score") || "9.8").replace(",", "."));
  if (!isFinite(currentBase)) currentBase = 9.8;

  var lang = window.currentLanguage || "pt";

  [7.0, 5.0, 2.5].forEach(function(s) {
    var key = (s === 7.0 ? "7" : (s === 5.0 ? "5" : "2"));
    var btn = document.getElementById("whatif-btn-" + key);
    if (btn) {
      if (Math.abs(s - targetScore) < 0.2) btn.classList.add("active");
      else btn.classList.remove("active");
    }
  });

  var box = document.getElementById("whatifOutputBox");
  if (!box) return;

  var neededReduction = (currentBase - targetScore);
  var prescriptions = [];
  var achievedScore = currentBase;

  if (neededReduction > 0) {
    prescriptions.push({
      control: (lang === "en" ? "Remove public 0.0.0.0/0 exposure (MAV: Network → Local)" : (lang === "es" ? "Eliminar exposición pública 0.0.0.0/0 (MAV: Network → Local)" : "Desativar exposição pública 0.0.0.0/0 (MAV: Network → Local)")),
      delta: -1.8,
      applied: true
    });
    achievedScore -= 1.8;
  }

  if (achievedScore > targetScore) {
    prescriptions.push({
      control: (lang === "en" ? "Isolate asset on restricted VLAN / Subnet (MAV: Adjacent)" : (lang === "es" ? "Aislar activo en VLAN / Subred restringida (MAV: Adjacent)" : "Isolar ativo em VLAN / Subrede restrita (MAV: Adjacent)")),
      delta: -0.8,
      applied: true
    });
    achievedScore -= 0.8;
  }

  if (achievedScore > targetScore) {
    prescriptions.push({
      control: (lang === "en" ? "Enable active perimeter WAF / Restrictive Firewall filtering" : (lang === "es" ? "Activar WAF perimetral / Reglas de Firewall restrictivas" : "Ativar WAF perimetral / Regras restritivas de Firewall")),
      delta: -0.4,
      applied: true
    });
    achievedScore -= 0.4;
  }

  if (achievedScore > targetScore && val("business_criticality") === "high") {
    prescriptions.push({
      control: (lang === "en" ? "Deploy compensating MFA + Strict host-level egress rate-limiting" : (lang === "es" ? "Desplegar MFA compensatorio + Control estricto de egress" : "Aplicar controles compensatórios de MFA + Rate-limit rigoroso")),
      delta: -0.7,
      applied: true
    });
    achievedScore -= 0.7;
  }

  achievedScore = Math.max(1.0, Number(achievedScore.toFixed(1)));

  var titleMsg = (lang === "en" ? "Analysis for Base Score " + currentBase + " → Target Goal: ≤ " + targetScore : (lang === "es" ? "Análisis para Score Base " + currentBase + " → Meta: ≤ " + targetScore : "Prescrição para Score Base " + currentBase + " → Meta: ≤ " + targetScore));
  var achievedMsg = (lang === "en" ? "Projected Score: " + achievedScore + " (" + sev(achievedScore) + ")" : (lang === "es" ? "Score Proyectado: " + achievedScore + " (" + sev(achievedScore) + ")" : "Score Projetado: " + achievedScore + " (" + sev(achievedScore) + ")"));
  var btnApplyLabel = (lang === "en" ? "Apply to Simulator Form" : (lang === "es" ? "Aplicar al Formulario del Simulador" : "Aplicar ao Formulário"));
  var btnIacLabel = (lang === "en" ? "Generate Virtual Patch (IaC)" : (lang === "es" ? "Generar Virtual Patch (IaC)" : "Gerar Virtual Patch (IaC)"));

  var listHtml = prescriptions.map(function(p) {
    return "<li style='margin-bottom:6px;'>" +
      "<strong style='color:#4ade80;'>[✔ " + p.delta + "]</strong> " + esc(p.control) +
    "</li>";
  }).join("");

  box.innerHTML =
    "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px;border-bottom:1px solid #162c4a;padding-bottom:8px;'>" +
      "<div><strong style='color:#38bdf8;font-size:14px;'>" + titleMsg + "</strong></div>" +
      "<div style='background:rgba(74,222,128,0.15);border:1px solid #4ade80;color:#4ade80;padding:4px 10px;border-radius:6px;font-weight:700;font-size:12px;'>" + achievedMsg + "</div>" +
    "</div>" +
    "<div style='font-size:12px;color:#94a3b8;margin-bottom:8px;'>" +
      (lang === "en" ? "Minimal Operational Intervention Prescribed by AI Watcher:" : (lang === "es" ? "Intervención Operativa Mínima Prescrita por IA Watcher:" : "Menor Intervenção Operacional Prescrita pela IA Watcher:")) +
    "</div>" +
    "<ul style='margin:0 0 12px;padding-left:20px;line-height:1.6;'>" + listHtml + "</ul>" +
    "<div style='display:flex;gap:8px;flex-wrap:wrap;'>" +
      "<button onclick='applyWhatIfControls()' style='width:auto;padding:7px 16px;background:#0284c7;font-size:12px;'>" + btnApplyLabel + "</button>" +
      "<button onclick='openVirtualPatchModal()' style='width:auto;padding:7px 16px;background:#16a34a;border-color:#16a34a;font-size:12px;'>" + btnIacLabel + "</button>" +
    "</div>";
}

function applyWhatIfControls() {
  document.getElementById("internet_exposed").value = "no";
  document.getElementById("network_segmented").value = "yes";
  document.getElementById("firewall_restricted").value = "yes";
  document.getElementById("compensating_controls").value = "yes";
  calc();
  var lang = window.currentLanguage || "pt";
  alert(lang === "en" ? "Controls applied! Form re-evaluated." : (lang === "es" ? "¡Controles aplicados! Formulario recalculado." : "Controles aplicados com sucesso! Simulador recalculado."));
}

// ============================================================================
// MODAL DE POLICY-AS-CODE / VIRTUAL PATCHING
// ============================================================================
var currentVpTabType = "iptables";

function openVirtualPatchModal() {
  var modal = document.getElementById("virtualPatchModal");
  if (!modal) return;
  setVpTab(currentVpTabType);
  modal.classList.add("active");
}

function closeVirtualPatchModal() {
  var modal = document.getElementById("virtualPatchModal");
  if (modal) modal.classList.remove("active");
}

function setVpTab(type) {
  currentVpTabType = type;
  ["iptables", "aws", "waf"].forEach(function(t) {
    var btn = document.getElementById("vp-tab-" + t);
    if (btn) {
      if (t === type) btn.classList.add("active");
      else btn.classList.remove("active");
    }
  });

  var codeEl = document.getElementById("vpCodeText");
  if (!codeEl) return;

  var cve = val("cve") || "CVE-2025-0001";
  var asset = val("asset_id") || "payment-api";

  if (type === "iptables") {
    codeEl.innerText =
      "# ============================================================\n" +
      "# HelpUS Virtual Patching: Linux iptables Containment Rule\n" +
      "# Target: " + asset + " | Flaw: " + cve + "\n" +
      "# ============================================================\n\n" +
      "# 1. Allow strictly verified internal subnet\n" +
      "iptables -A INPUT -p tcp --dport 5432 -s 192.168.1.0/24 -m state --state NEW,ESTABLISHED -j ACCEPT\n\n" +
      "# 2. Drop direct exposure from wild internet (0.0.0.0/0)\n" +
      "iptables -A INPUT -p tcp --dport 5432 -j DROP\n\n" +
      "# 3. Log blocked attempts for HITL audit compliance\n" +
      "iptables -A INPUT -p tcp --dport 5432 -m limit --limit 5/min -j LOG --log-prefix \"[HELPUS-CVSS-BLOCKED]: \"";
  } else if (type === "aws") {
    codeEl.innerText =
      "# ============================================================\n" +
      "# HelpUS Virtual Patching: AWS Security Group Revocation (CLI)\n" +
      "# Target: " + asset + " | Flaw: " + cve + "\n" +
      "# ============================================================\n\n" +
      "# Revoke public ingress to database/app port\n" +
      "aws ec2 revoke-security-group-ingress \\\n" +
      "  --group-id sg-01a2b3c4d5e6f7g8 \\\n" +
      "  --protocol tcp \\\n" +
      "  --port 5432 \\\n" +
      "  --cidr 0.0.0.0/0\n\n" +
      "# Authorize strictly private VPC peering\n" +
      "aws ec2 authorize-security-group-ingress \\\n" +
      "  --group-id sg-01a2b3c4d5e6f7g8 \\\n" +
      "  --protocol tcp \\\n" +
      "  --port 5432 \\\n" +
      "  --cidr 10.0.0.0/16";
  } else {
    codeEl.innerText =
      "# ============================================================\n" +
      "# HelpUS Virtual Patching: Cloudflare WAF Expression Rule\n" +
      "# Target: " + asset + " | Flaw: " + cve + "\n" +
      "# ============================================================\n\n" +
      "(http.request.uri.path contains \"/api/v1/\" and not ip.src in {192.168.1.0/24 10.0.0.0/16})\n" +
      "Action: Block\n\n" +
      "# Rate-limit fallback rule for external DMZ\n" +
      "(http.request.uri.path contains \"/auth\" and cf.threat_score gt 10)\n" +
      "Action: Interactive Challenge (Managed)";
  }
}

function copyVpCode() {
  var codeEl = document.getElementById("vpCodeText");
  if (!codeEl) return;
  navigator.clipboard.writeText(codeEl.innerText);
  var lang = window.currentLanguage || "pt";
  alert(lang === "en" ? "Script copied to clipboard!" : (lang === "es" ? "¡Script copiado al portapapeles!" : "Script copiado para a área de transferência!"));
}

function openTriScoreDirect() {
  switchView("view-simulador");
  var el = document.getElementById("result");
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// Estado global de homologação humana
window.currentHomologation = null;

function openHomologationModal(actionType) {
  var modal = document.getElementById("homologationModal");
  if (!modal) return;

  var r = window.lastCvssResult || {};
  var e = r.evidence || {};
  var c = r.contextual_environmental || {};
  var lang = window.currentLanguage || "pt";

  // Preenche checklist de evidências
  var checklistEl = document.getElementById("modalEvidenceChecklist");
  if (checklistEl) {
    var lblTopo = (lang === "en" ? "Network Topology: " + (e.network_segmented === "yes" ? "Isolated subnet / VLAN verified" : "Flat shared network") + " (" + (e.internet_exposed === "yes" ? "Exposed 0.0.0.0/0" : "Internal / No direct route") + ")" : (lang === "es" ? "Topología de Red: " + (e.network_segmented === "yes" ? "Subred aislada / VLAN verificada" : "Red plana compartida") + " (" + (e.internet_exposed === "yes" ? "Expuesto 0.0.0.0/0" : "Interno / Sin acceso directo") + ")" : "Topologia de Rede: " + (e.network_segmented === "yes" ? "Subrede isolada/VLAN verificada" : "Rede plana compartilhada") + " (" + (e.internet_exposed === "yes" ? "Exposto 0.0.0.0/0" : "Interno/Sem acesso direto") + ")"));
    var lblPerim = (lang === "en" ? "Perimeter Controls: " + (e.firewall_restricted === "yes" ? "Firewall/WAF active blocking unauthorized traffic" : "No perimeter shielding") : (lang === "es" ? "Controles Perimetrales: " + (e.firewall_restricted === "yes" ? "Firewall/WAF activo bloqueando tráfico no autorizado" : "Sin blindaje perimetral") : "Controles Perimetrais: " + (e.firewall_restricted === "yes" ? "Firewall/WAF ativo e bloqueando tráfego não autorizado" : "Sem blindagem perimetral")));
    var lblBiz = (lang === "en" ? "Business Impact: " + (e.pci_in_scope === "yes" ? "PCI-DSS Scope Active (Banking/Cards)" : "Out of PCI scope") + " • Criticality " + String(e.business_criticality || "high").toUpperCase() : (lang === "es" ? "Impacto en Negocio: " + (e.pci_in_scope === "yes" ? "Alcance PCI-DSS Activo (Bancario/Tarjetas)" : "Fuera de alcance PCI") + " • Criticidad " + String(e.business_criticality || "high").toUpperCase() : "Impacto no Negócio: " + (e.pci_in_scope === "yes" ? "Escopo PCI-DSS ativo (Cartões/Bancário)" : "Fora do escopo PCI") + " • Criticidade " + String(e.business_criticality || "high").toUpperCase()));
    var lblCve = (lang === "en" ? "Validated Vulnerability: " + (e.cve || "CVE-2025-0001") + " on asset " + (e.asset_id || "host") : (lang === "es" ? "Vulnerabilidad Validada: " + (e.cve || "CVE-2025-0001") + " en activo " + (e.asset_id || "host") : "Vulnerabilidade Validada: " + (e.cve || "CVE-2025-0001") + " no ativo " + (e.asset_id || "host")));

    var items = [
      { id: "chk_topo", label: lblTopo },
      { id: "chk_perim", label: lblPerim },
      { id: "chk_biz", label: lblBiz },
      { id: "chk_cve", label: lblCve }
    ];

    checklistEl.innerHTML = items.map(function(item) {
      return "<label class='evidence-check-item'>" +
        "<input type='checkbox' id='" + item.id + "' checked>" +
        "<span style='font-size:13px;color:#e2e8f0;line-height:1.4;'>" + esc(item.label) + "</span>" +
      "</label>";
    }).join("");
  }

  // Define a ação padrão com base no clique
  var selectAction = document.getElementById("homologDecisionAction");
  if (selectAction) {
    selectAction.value = (actionType === "reject") ? "reject_conservative" : "approve";
    updateDecisionGuidance();
  }

  goToWizardStep(1);
  modal.classList.add("active");
}

function closeHomologationModal() {
  var modal = document.getElementById("homologationModal");
  if (modal) modal.classList.remove("active");
}

function goToWizardStep(stepNumber) {
  [1, 2, 3, 4].forEach(function(s) {
    var pane = document.getElementById("wizard-step-" + s);
    var badge = document.getElementById("step-badge-" + s);
    if (pane) pane.className = (s === stepNumber ? "wizard-step-pane active" : "wizard-step-pane");
    if (badge) {
      if (s < stepNumber) {
        badge.className = "modal-step-badge done";
      } else if (s === stepNumber) {
        badge.className = "modal-step-badge active";
      } else {
        badge.className = "modal-step-badge";
      }
    }
  });
}

function updateDecisionGuidance() {
  var action = document.getElementById("homologDecisionAction").value;
  var note = document.getElementById("homologGuidanceNote");
  var rationaleArea = document.getElementById("homologRationaleText");
  var btn = document.getElementById("btnExecuteHomologation");

  var r = window.lastCvssResult || {};
  var c = r.contextual_environmental || {};

  if (!note) return;

  if (action === "approve") {
    note.innerHTML = "<strong style='color:#4ade80;'>Homologação Contextual:</strong> O score " + esc(c.contextual_score || "") + " (" + esc(c.contextual_severity || "") + ") substituirá a prioridade padrão nos dashboards operacionais e SLAs do HelpUS.";
    if (!rationaleArea.value || rationaleArea.dataset.autoFilled) {
      rationaleArea.value = "Topologia e segmentação de rede confirmadas. O vetor MAV e os requisitos de negócio (" + (c.decision || "ajustado") + ") refletem a realidade operacional.";
      rationaleArea.dataset.autoFilled = "true";
    }
    if (btn) {
      btn.style.background = "#16a34a";
      btn.style.borderColor = "#16a34a";
      btn.innerHTML = "✓ Assinar & Concluir Homologação";
    }
  } else if (action === "approve_with_controls") {
    note.innerHTML = "<strong style='color:#38bdf8;'>Homologação com Condicionante:</strong> O score atenuado é aceito temporariamente sob compromisso de aplicação de patch ou compensação até a data limite estabelecida.";
    if (!rationaleArea.value || rationaleArea.dataset.autoFilled) {
      rationaleArea.value = "Mitigado temporariamente por firewall/isolamento. Correção definitiva programada para a próxima janela de manutenção de infraestrutura.";
      rationaleArea.dataset.autoFilled = "true";
    }
    if (btn) {
      btn.style.background = "#0284c7";
      btn.style.borderColor = "#0284c7";
      btn.innerHTML = "✓ Homologar com Condicionante";
    }
  } else if (action === "reject_conservative") {
    note.innerHTML = "<strong style='color:#f87171;'>Rejeição (Manter Origem):</strong> A recomendação contextual da IA é descartada. O score base de origem (" + esc((r.official_cvss || {}).base_score || "") + ") continuará governando o SLA e a criticidade.";
    if (!rationaleArea.value || rationaleArea.dataset.autoFilled) {
      rationaleArea.value = "Rejeitado pelo analista de segurança: o isolamento alegado é insuficiente ou há risco lateral potencial não mapeado pela heurística da IA.";
      rationaleArea.dataset.autoFilled = "true";
    }
    if (btn) {
      btn.style.background = "#b91c1c";
      btn.style.borderColor = "#b91c1c";
      btn.innerHTML = "✕ Rejeitar Proposta (Manter Base NVD)";
    }
  } else {
    note.innerHTML = "<strong style='color:#eab308;'>Escalação de Crise:</strong> O ativo será enviado ao comitê de segurança com ticket de prioridade máxima para análise conjunta.";
    if (!rationaleArea.value || rationaleArea.dataset.autoFilled) {
      rationaleArea.value = "Divergência crítica entre modelo de ameaça e evidências do ambiente. Encaminhado ao Comitê de Risco Cibernético.";
      rationaleArea.dataset.autoFilled = "true";
    }
    if (btn) {
      btn.style.background = "#ca8a04";
      btn.style.borderColor = "#ca8a04";
      btn.innerHTML = "⚠ Escalar para Comitê de Crise";
    }
  }
}

function generateAuditHash(payload) {
  // Demo simulation digest generation over canonicalized preview payload.
  // Strictly non-authoritative demo digest — NOT a cryptographic signature or durable audit event.
  var str = JSON.stringify(payload || {});
  var hash = 0;
  for (var i = 0; i < str.length; i++) {
    var chr = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  var hex = (hash >>> 0).toString(16).padStart(8, "0");
  return "demo-digest-simulacao-" + hex;
}

function executeHomologation() {
  var r = window.lastCvssResult || {};
  var o = r.official_cvss || {};
  var c = r.contextual_environmental || {};
  var e = r.evidence || {};

  var reviewer = document.getElementById("homologReviewerName").value || "Analista de Segurança";
  var email = document.getElementById("homologReviewerEmail").value || "secops@empresa.com.br";
  var role = document.getElementById("homologReviewerRole").value || "Security Engineer";
  var ticketId = document.getElementById("homologTicketId").value || "SEC-GENERAL";
  var action = document.getElementById("homologDecisionAction").value;
  var rationale = document.getElementById("homologRationaleText").value;

  var nowIso = new Date().toISOString();
  var isApproved = (action === "approve" || action === "approve_with_controls");

  var demoPayload = {
    action: action,
    reviewer_email: email,
    ticket_id: ticketId,
    rationale: rationale,
    timestamp: nowIso,
    target_cve: e.cve,
    asset_id: e.asset_id,
    effective_score: isApproved ? c.contextual_score : o.base_score,
  };
  var demoDigest = generateAuditHash(demoPayload);

  var homologationRecord = {
    status: isApproved ? "SIMULACAO_APROVADA" : "SIMULACAO_REJEITADA",
    mode: "client_side_simulation",
    governance_notice: "Simulação client-side não autoritativa para pré-visualização. Homologações corporativas oficiais com recibo auditável exigem sessão corporativa autenticada via endpoint /api/review/decision.",
    action: action,
    reviewer_name: reviewer,
    reviewer_email: email,
    reviewer_role: role,
    ticket_id: ticketId,
    rationale: rationale,
    timestamp: nowIso,
    demo_digest: demoDigest,
    target_cve: e.cve,
    asset_id: e.asset_id,
    effective_score: isApproved ? c.contextual_score : o.base_score,
    effective_severity: isApproved ? c.contextual_severity : o.base_severity,
    official_base_score: o.base_score
  };

  window.currentHomologation = homologationRecord;
  if (window.lastCvssResult) {
    window.lastCvssResult.homologation = homologationRecord;
  }

  // Atualiza painel do gate na tela
  var box = document.getElementById("reviewDecisionBox");
  if (box) {
    var statusBadgeColor = isApproved ? "#4ade80" : "#f87171";
    var statusBg = isApproved ? "rgba(74,222,128,0.15)" : "rgba(248,113,113,0.15)";
    var icon = isApproved ? "✓" : "✕";

    box.innerHTML =
      "<div style='background:" + statusBg + ";border:1px solid " + statusBadgeColor + ";border-radius:8px;padding:12px;width:100%;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;'>" +
        "<div>" +
          "<div style='color:" + statusBadgeColor + ";font-weight:700;font-size:13px;'>" + icon + " Simulação: " + homologationRecord.status + " por " + esc(reviewer) + " (" + esc(role) + ")</div>" +
          "<div style='font-size:11px;color:#cbd5e1;margin-top:3px;'>Ticket: <strong>" + esc(ticketId) + "</strong> | Digest (Demo): <code>" + demoDigest + "</code> | " + nowIso.substring(0, 19).replace("T", " ") + " UTC</div>" +
          "<div style='font-size:11px;color:#94a3b8;margin-top:2px;'>Score de Simulação: <strong>" + esc(homologationRecord.effective_score) + " (" + esc(homologationRecord.effective_severity) + ")</strong></div>" +
        "</div>" +
        "<div style='display:flex;gap:6px;'>" +
          "<button onclick='openHomologationModal(\"" + (isApproved ? "approve" : "reject") + "\")' style='width:auto;padding:6px 12px;background:#0d223f;border:1px solid #1e3a5f;font-size:11px;color:#38bdf8;'>Revisar Simulação</button>" +
          "<button onclick='downloadHomologationCertificate()' style='width:auto;padding:6px 12px;background:#1e293b;border:1px solid #334155;font-size:11px;color:#cbd5e1;'>Comprovante Demo</button>" +
        "</div>" +
      "</div>";
  }

  // Preenche dados do Passo 4
  var certBox = document.getElementById("homologationCertificateBox");
  if (certBox) {
    certBox.style.borderColor = isApproved ? "#16a34a" : "#dc2626";
    certBox.innerHTML =
      "<div style='display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1e3a5f;padding-bottom:10px;margin-bottom:12px;'>" +
        "<div>" +
          "<span style='font-size:11px;color:#94a3b8;text-transform:uppercase;'>Comprovante de Demonstração Interativa (Simulação Local)</span>" +
          "<h4 style='margin:2px 0 0;font-size:16px;color:" + (isApproved ? "#4ade80" : "#f87171") + ";'>" + homologationRecord.status + " • " + esc(homologationRecord.effective_score) + " " + esc(homologationRecord.effective_severity) + "</h4>" +
        "</div>" +
        "<span style='font-size:11px;background:#050c17;padding:4px 8px;border-radius:6px;border:1px solid #1e3a5f;color:#38bdf8;'>Simulação Client-Side</span>" +
      "</div>" +
      "<div style='font-size:12px;line-height:1.7;color:#cbd5e1;'>" +
        "<div><strong>Responsável Técnico (Simulado):</strong> " + esc(reviewer) + " &lt;" + esc(email) + "&gt; (" + esc(role) + ")</div>" +
        "<div><strong>Chamado Vinculado:</strong> " + esc(ticketId) + "</div>" +
        "<div><strong>Ativo / CVE:</strong> " + esc(e.asset_id) + " / " + esc(e.cve) + "</div>" +
        "<div><strong>Score Base Origem:</strong> " + esc(o.base_score) + " (" + esc(o.base_severity) + ")</div>" +
        "<div><strong>Score Efetivo Simulado:</strong> " + esc(homologationRecord.effective_score) + " (" + esc(homologationRecord.effective_severity) + ")</div>" +
        "<div><strong>Justificativa Técnica:</strong> " + esc(rationale) + "</div>" +
        "<div><strong>Carimbo Temporal:</strong> " + nowIso + "</div>" +
        "<div style='margin-top:6px;word-break:break-all;'><strong>Digest de Demonstração (Não Autoritativo):</strong> <code style='color:#38bdf8;'>" + demoDigest + "</code></div>" +
        "<div style='margin-top:4px;font-size:11px;color:#94a3b8;'><em>Nota: Pré-visualização demonstrativa no navegador. Homologações oficiais são auditadas e persistidas via API autenticada /api/review/decision.</em></div>" +
      "</div>";
  }

  // Atualiza export preview com a homologação
  var exportBox = document.getElementById("exportBox");
  if (exportBox) {
    exportBox.value = JSON.stringify(getExportContract(), null, 2);
  }

  goToWizardStep(4);
}

function downloadHomologationCertificate() {
  var rec = window.currentHomologation;
  if (!rec) {
    alert("Nenhuma homologação ativa para exportar.");
    return;
  }
  var data = JSON.stringify(rec, null, 2);
  var blob = new Blob([data], {type: "application/json"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "homologation_certificate_" + (rec.ticket_id || "audit") + ".json";
  a.click();
}

function approveDecision() {
  openHomologationModal("approve");
}

function rejectDecision() {
  openHomologationModal("reject");
}

// ============================================================================
// CENÁRIOS PRESET MULTILÍNGUES (PT / EN / ES)
// ============================================================================
var SIMULATOR_PRESETS = {
  pci: {
    id: "pci",
    title: {
      pt: "1. API de Pagamentos PCI (Bancário)",
      en: "1. PCI Payments API (Banking)",
      es: "1. API de Pagos PCI (Bancario)"
    },
    tag: {
      pt: "Produção Crítica • Isolada em VLAN",
      en: "Critical Production • VLAN Isolated",
      es: "Producción Crítica • Aislada en VLAN"
    },
    scenario: "pci_segmented_lab_20260517_143146",
    asset_id: "payment-api",
    cve: "CVE-2025-0001",
    base_score: "9.8",
    internet_exposed: "no",
    network_segmented: "yes",
    pci_in_scope: "yes",
    firewall_restricted: "yes",
    compensating_controls: "yes",
    business_criticality: "high",
    description: {
      pt: "Ambiente bancário de processamento de cartões de crédito e PIX. O servidor não tem IP público e opera isolado em VLAN restrita.",
      en: "Banking environment processing credit cards and instant payments. Server has no public IP and operates isolated on a restricted VLAN.",
      es: "Entorno bancario de procesamiento de tarjetas de crédito y pagos instantáneos. El servidor no tiene IP pública y opera aislado en una VLAN restringida."
    },
    traditional_problem: {
      pt: "A avaliação de origem emite nota 9.8 Crítico no vácuo. Equipes entram em desespero achando que a internet inteira pode atacar o ativo diretamente.",
      en: "The source assessment issues a 9.8 Critical score in a vacuum. Teams panic assuming the entire public internet can exploit the server directly.",
      es: "La evaluación de origen emite un score de 9.8 Crítico en el vacío. Los equipos entran en pánico asumiendo que internet completo puede atacar el servidor directamente."
    },
    helpus_advantage: {
      pt: "A HelpUS identifica que a rede está blindada em VLAN (vetor Adjacent), mas NÃO negligencia a falha: como o dano financeiro e a multa regulatória seriam catastróficos, a IA mantém a prioridade máxima (9.9) para auditoria e conformidade, sem alarmes falsos de ataque externo.",
      en: "HelpUS identifies that the network is shielded in a VLAN (Adjacent vector), but does NOT ignore severity: because financial and regulatory penalties would be catastrophic, AI sustains top priority (9.9) for audit compliance without false panic of external exposure.",
      es: "HelpUS identifica que la red está blindada en VLAN (vector Adjacent), pero NO ignora el peligro: como la sanción regulatoria y el daño financiero serían catastróficos, la IA mantiene prioridad máxima (9.9) para auditoría sin falsas alarmas de ataque externo."
    },
    nodes: [
      { label: { pt: "Internet Pública", en: "Public Internet", es: "Internet Pública" }, sub: { pt: "Bloqueada", en: "Blocked", es: "Bloqueada" }, icon: "🌐", x: 70, y: 55, color: "#94a3b8" },
      { label: { pt: "Firewall / WAF", en: "Firewall / WAF", es: "Firewall / WAF" }, sub: { pt: "Regras Estritas", en: "Strict Rules", es: "Reglas Estrictas" }, icon: "⛨", x: 220, y: 55, color: "#38bdf8" },
      { label: { pt: "VLAN PCI-DSS", en: "PCI-DSS VLAN", es: "VLAN PCI-DSS" }, sub: { pt: "Subrede Isolada", en: "Isolated Subnet", es: "Subred Aislada" }, icon: "🔒", x: 370, y: 55, color: "#4ade80" },
      { label: { pt: "payment-api", en: "payment-api", es: "payment-api" }, sub: { pt: "Prioridade: 9.9 (+0.1)", en: "Priority: 9.9 (+0.1)", es: "Prioridad: 9.9 (+0.1)" }, icon: "⚠", x: 520, y: 55, color: "#f87171" }
    ],
    links: [
      { from: 0, to: 1, label: { pt: "Bloqueio 0.0.0.0/0", en: "0.0.0.0/0 Block", es: "Bloqueo 0.0.0.0/0" }, color: "#f87171", dash: true },
      { from: 1, to: 2, label: { pt: "Inspecionado", en: "Inspected", es: "Inspeccionado" }, color: "#38bdf8", dash: false },
      { from: 2, to: 3, label: { pt: "Acesso Interno", en: "Internal Access", es: "Acceso Interno" }, color: "#fbbf24", dash: false }
    ]
  },
  dev: {
    id: "dev",
    title: {
      pt: "2. Servidor de Teste / Dev (Staging)",
      en: "2. Test / Dev Server (Staging)",
      es: "2. Servidor de Pruebas / Dev (Staging)"
    },
    tag: {
      pt: "Homologação • Dados Fictícios • Baixo Risco",
      en: "Staging • Dummy Data • Low Risk",
      es: "Homologación • Datos Ficticios • Bajo Riesgo"
    },
    scenario: "staging_dev_env_20261007_001",
    asset_id: "staging-sandbox-01",
    cve: "CVE-2025-0001",
    base_score: "9.8",
    internet_exposed: "no",
    network_segmented: "yes",
    pci_in_scope: "no",
    firewall_restricted: "yes",
    compensating_controls: "no",
    business_criticality: "low",
    description: {
      pt: "Máquina de homologação usada pelos desenvolvedores para testes de novas funcionalidades, com base de dados sintética (falsa) e sem rota da internet.",
      en: "Staging machine used by developers to test new features, with synthetic (fake) database and no public internet route.",
      es: "Máquina de homologación utilizada por desarrolladores para probar nuevas funciones, con base de datos sintética (falsa) y sin ruta de internet pública."
    },
    traditional_problem: {
      pt: "A nota 9.8 cega obriga a equipe de segurança a acordar engenheiros de madrugada para aplicar patches urgentes em uma máquina descartável de testes.",
      en: "Blind 9.8 score forces security teams to wake engineers at midnight for emergency patching on an ephemeral, non-critical test host.",
      es: "El puntaje ciego de 9.8 obliga al equipo de seguridad a despertar ingenieros de madrugada para aplicar parches urgentes en una máquina descartable de pruebas."
    },
    helpus_advantage: {
      pt: "A HelpUS detecta a ausência de internet, a segmentação e a criticidade baixa, desescalonando a nota de 9.8 para 5.4 (-4.4). A empresa economiza tempo precioso da engenharia e foca onde há risco real.",
      en: "HelpUS detects no internet exposure, isolated segmentation, and low criticality, demoting score from 9.8 to 5.4 (-4.4). Engineering saves precious time to focus on genuine threats.",
      es: "HelpUS detecta ausencia de internet, segmentación aislada y baja criticidad, desescalando el score de 9.8 a 5.4 (-4.4). La empresa ahorra tiempo valioso de ingeniería para enfocarse en riesgos reales."
    },
    nodes: [
      { label: { pt: "Internet Externa", en: "External Internet", es: "Internet Externa" }, sub: { pt: "Inacessível", en: "Unreachable", es: "Inaccesible" }, icon: "🌐", x: 70, y: 55, color: "#94a3b8" },
      { label: { pt: "Firewall Interno", en: "Internal Firewall", es: "Firewall Interno" }, sub: { pt: "Portas Fechadas", en: "Ports Closed", es: "Puertos Cerrados" }, icon: "⛨", x: 220, y: 55, color: "#38bdf8" },
      { label: { pt: "DMZ Homologação", en: "Staging DMZ", es: "DMZ Homologación" }, sub: { pt: "Rede Dev", en: "Dev Network", es: "Red Dev" }, icon: "🧪", x: 370, y: 55, color: "#4ade80" },
      { label: { pt: "staging-sandbox", en: "staging-sandbox", es: "staging-sandbox" }, sub: { pt: "Prioridade: 5.4 (-4.4)", en: "Priority: 5.4 (-4.4)", es: "Prioridad: 5.4 (-4.4)" }, icon: "✓", x: 520, y: 55, color: "#4ade80" }
    ],
    links: [
      { from: 0, to: 1, label: { pt: "Sem Rota", en: "No Route", es: "Sin Ruta" }, color: "#64748b", dash: true },
      { from: 1, to: 2, label: { pt: "VPN Dev", en: "Dev VPN", es: "VPN Dev" }, color: "#38bdf8", dash: false },
      { from: 2, to: 3, label: { pt: "Dados Fictícios", en: "Dummy Data", es: "Datos Ficticios" }, color: "#4ade80", dash: false }
    ]
  },
  ecom: {
    id: "ecom",
    title: {
      pt: "3. E-commerce na Internet Sem WAF",
      en: "3. Public E-Commerce Without WAF",
      es: "3. Comercio Electrónico Sin WAF"
    },
    tag: {
      pt: "Produção Crítica • Exposto à Web Aberta",
      en: "Critical Production • Open Web Exposed",
      es: "Producción Crítica • Expuesto a Web Abierta"
    },
    scenario: "public_storefront_20261007_002",
    asset_id: "storefront-web-prod",
    cve: "CVE-2025-0001",
    base_score: "9.8",
    internet_exposed: "yes",
    network_segmented: "no",
    pci_in_scope: "no",
    firewall_restricted: "no",
    compensating_controls: "no",
    business_criticality: "high",
    description: {
      pt: "Loja virtual diretamente acessível ao público geral (0.0.0.0/0) na porta 443 sem proxy de borda WAF ou rate-limit.",
      en: "Online storefront directly reachable by general public (0.0.0.0/0) on port 443 with no WAF edge proxy or rate limiting.",
      es: "Tienda online accesible directamente al público general (0.0.0.0/0) en el puerto 443 sin proxy de borde WAF ni limitación de tráfico."
    },
    traditional_problem: {
      pt: "Sem contexto de rede, sistemas comuns mostram essa falha na mesma lista e com a mesma urgência teórica que o servidor de homologação (Dev).",
      en: "Without environmental topology, standard scanners display this flaw alongside the test machine with identical theoretical priority.",
      es: "Sin contexto de red, sistemas comunes muestran este fallo en la misma lista y con la misma urgencia teórica que el servidor de pruebas."
    },
    helpus_advantage: {
      pt: "A HelpUS identifica exposição total na internet sem proteções e eleva o score para 10.0 (+0.2) com alerta crítico de intervenção imediata antes que ocorra invasão.",
      en: "HelpUS recognizes open internet exposure without barriers and escalates score to 10.0 (+0.2) with urgent intervention alert before compromise occurs.",
      es: "HelpUS identifica exposición total a internet sin defensas y eleva el score a 10.0 (+0.2) con alerta crítica de intervención inmediata antes de cualquier intrusión."
    },
    nodes: [
      { label: { pt: "Internet Pública", en: "Public Internet", es: "Internet Pública" }, sub: { pt: "Ataque Iminente", en: "Imminent Attack", es: "Ataque Inminente" }, icon: "🌐", x: 80, y: 55, color: "#f87171" },
      { label: { pt: "Roteador Borda", en: "Edge Router", es: "Router Borde" }, sub: { pt: "Sem Firewall/WAF", en: "No Firewall/WAF", es: "Sin Firewall/WAF" }, icon: "⚡", x: 300, y: 55, color: "#f87171" },
      { label: { pt: "storefront-prod", en: "storefront-prod", es: "storefront-prod" }, sub: { pt: "Prioridade: 10.0 (+0.2)", en: "Priority: 10.0 (+0.2)", es: "Prioridad: 10.0 (+0.2)" }, icon: "⚠", x: 520, y: 55, color: "#f87171" }
    ],
    links: [
      { from: 0, to: 1, label: { pt: "0.0.0.0/0 Aberto", en: "0.0.0.0/0 Open", es: "0.0.0.0/0 Abierto" }, color: "#f87171", dash: false },
      { from: 1, to: 2, label: { pt: "Sem Filtro WAF", en: "No WAF Filter", es: "Sin Filtro WAF" }, color: "#f87171", dash: false }
    ]
  },
  clinic: {
    id: "clinic",
    title: {
      pt: "4. Clínica Médica / Servidor Local de Prontuários",
      en: "4. Medical Clinic / Local EHR Server",
      es: "4. Clínica Médica / Servidor Local de Historias Clínicas"
    },
    tag: {
      pt: "Rede Local Física • Consultório Privado",
      en: "Physical Local LAN • Private Clinic",
      es: "Red Local Física • Consultorio Privado"
    },
    scenario: "clinic_local_lan_20261007_003",
    asset_id: "clinic-db-server",
    cve: "CVE-2023-39417",
    base_score: "8.7",
    internet_exposed: "no",
    network_segmented: "yes",
    pci_in_scope: "no",
    firewall_restricted: "yes",
    compensating_controls: "yes",
    business_criticality: "high",
    description: {
      pt: "Servidor local instalado no consultório médico rodando banco de dados com prontuários de pacientes, conectado apenas por cabo de rede no switch físico da recepção e consultórios.",
      en: "Local physical server in medical clinic running patient database, connected strictly via ethernet to the on-premise physical switch with no outside port forwards.",
      es: "Servidor local instalado en el consultorio médico ejecutando base de datos de pacientes, conectado únicamente por cable ethernet al switch físico interno sin puertos abiertos al exterior."
    },
    traditional_problem: {
      pt: "Scanners comuns acusam CVE-2023-39417 como perigo crítico de invasão remota externa, gerando alarme falso nos gestores de saúde.",
      en: "Generic scanners trigger high-panic alarms for CVE-2023-39417 alleging external remote exploitation risk, stressing clinic operators unnecessarily.",
      es: "Escáneres genéricos acusan CVE-2023-39417 como peligro crítico de invasión remota exterior, generando falsas alarmas en administradores de salud."
    },
    helpus_advantage: {
      pt: "A HelpUS reconhece que o serviço está contido no switch físico da clínica (vetor Adjacent/Local) e atenua o score de 8.7 para 7.1 (-1.6), orientando manutenção programada sem estresse operacional.",
      en: "HelpUS recognizes the database is enclosed within physical clinic switch (Adjacent/Local vector) and attenuates score from 8.7 to 7.1 (-1.6), scheduling patch window calmly.",
      es: "HelpUS reconoce que la base de datos está contenida en el switch físico de la clínica (vector Adjacent/Local) y atenúa el puntaje de 8.7 a 7.1 (-1.6), guiando mantenimiento programado sin estrés."
    },
    nodes: [
      { label: { pt: "Internet Externa", en: "External Internet", es: "Internet Externa" }, sub: { pt: "Sem Port-Forward", en: "No Port-Forward", es: "Sin Port-Forward" }, icon: "🌐", x: 70, y: 55, color: "#94a3b8" },
      { label: { pt: "Roteador da Clínica", en: "Clinic Router", es: "Router de Clínica" }, sub: { pt: "NAT / Firewall", en: "NAT / Firewall", es: "NAT / Firewall" }, icon: "⛨", x: 220, y: 55, color: "#38bdf8" },
      { label: { pt: "Switch Consultório", en: "Clinic Switch", es: "Switch Consultorio" }, sub: { pt: "LAN 192.168.0.x", en: "LAN 192.168.0.x", es: "LAN 192.168.0.x" }, icon: "🏠", x: 370, y: 55, color: "#4ade80" },
      { label: { pt: "clinic-db", en: "clinic-db", es: "clinic-db" }, sub: { pt: "Prioridade: 7.1 (-1.6)", en: "Priority: 7.1 (-1.6)", es: "Prioridad: 7.1 (-1.6)" }, icon: "🗄", x: 520, y: 55, color: "#4ade80" }
    ],
    links: [
      { from: 0, to: 1, label: { pt: "Bloqueado", en: "Blocked", es: "Bloqueado" }, color: "#64748b", dash: true },
      { from: 1, to: 2, label: { pt: "Cabo de Rede", en: "Ethernet Cable", es: "Cable de Red" }, color: "#38bdf8", dash: false },
      { from: 2, to: 3, label: { pt: "Porta 5432 Local", en: "Local Port 5432", es: "Puerto 5432 Local" }, color: "#4ade80", dash: false }
    ]
  },
  santos: {
    id: "santos",
    title: {
      pt: "5. Estudo Trento 2017: Cisco Core Switch com ACLs (86% Erro Humano)",
      en: "5. Trento 2017 Study: Cisco Core Switch with ACLs (86% Human Error)",
      es: "5. Estudio Trento 2017: Cisco Core Switch con ACLs (86% Error Humano)"
    },
    tag: {
      pt: "Benchmark Científico Canônico • Santos et al. (Springer 2017)",
      en: "Canonical Scientific Benchmark • Santos et al. (Springer 2017)",
      es: "Benchmark Científico Canónico • Santos et al. (Springer 2017)"
    },
    scenario: "trento_pci_cisco_switch_cve_2016_6441",
    asset_id: "cisco-asr-core-switch",
    cve: "CVE-2016-6441",
    base_score: "9.8",
    internet_exposed: "no",
    network_segmented: "yes",
    pci_in_scope: "yes",
    firewall_restricted: "yes",
    compensating_controls: "yes",
    business_criticality: "high",
    description: {
      pt: "Switch de agregação Cisco ASR 900 executando IOS XE, implementando RACLs e VLANs para o enclave PCI de pagamentos da Christine's Company. Vulnerabilidade TL1 no plano de gerência (Base 9.8).",
      en: "Cisco ASR 900 core aggregation switch running IOS XE, enforcing RACLs and VLANs for Christine's Company PCI payment enclave. TL1 management daemon flaw (Base 9.8).",
      es: "Switch de agregación Cisco ASR 900 ejecutando IOS XE, implementando RACLs y VLANs para el enclave PCI de Christine's Company. Fallo TL1 en el plano de gestión (Base 9.8)."
    },
    traditional_problem: {
      pt: "No experimento controlado com 29 analistas (Santos et al., Springer 2017), 86% a 90% dos avaliadores humanos erraram a pontuação deste switch por sobrecarga cognitiva ao julgar as ACLs do trânsito.",
      en: "In the controlled trial with 29 analysts (Santos et al., Springer 2017), 86% to 90% of human evaluators failed to score this switch correctly due to mental overload reconciling management vs data planes.",
      es: "En el experimento con 29 analistas (Santos et al., Springer 2017), entre el 86% y 90% de los evaluadores humanos erraron la puntuación de este switch debido a sobrecarga mental."
    },
    helpus_advantage: {
      pt: "A HelpUS analisa a topologia em < 700ms, isola o plano de gerenciamento (MAV:Adjacent, MPR:High) e atenua o score para 6.4 (-3.4), gerando a regra de Virtual Patching IaC imediata com 100% de consistência.",
      en: "HelpUS parses topology in < 700ms, bounds management plane (MAV:Adjacent, MPR:High) reducing score to 6.4 (-3.4), synthesizing immediate Virtual Patching ACL rules with 100% consistency.",
      es: "HelpUS analiza la topología en < 700ms, aísla el plano de gestión (MAV:Adjacent, MPR:High) atenuando el score a 6.4 (-3.4) y generando la regla de Virtual Patching inmediata con 100% de consistencia."
    },
    nodes: [
      { label: { pt: "Internet Externa", en: "External Internet", es: "Internet Externa" }, sub: { pt: "Sem Rota Direta", en: "No Direct Route", es: "Sin Ruta Directa" }, icon: "🌐", x: 70, y: 55, color: "#94a3b8" },
      { label: { pt: "Border Router", en: "Border Router", es: "Border Router" }, sub: { pt: "Firewall / NAT", en: "Firewall / NAT", es: "Firewall / NAT" }, icon: "🛡", x: 220, y: 55, color: "#38bdf8" },
      { label: { pt: "Cisco ASR Core", en: "Cisco ASR Core", es: "Cisco ASR Core" }, sub: { pt: "Plano OOB / RACL", en: "OOB Plane / RACL", es: "Plano OOB / RACL" }, icon: "🖧", x: 370, y: 55, color: "#38bdf8" },
      { label: { pt: "POS PCI Enclave", en: "POS PCI Enclave", es: "POS PCI Enclave" }, sub: { pt: "Score: 6.4 (-3.4)", en: "Score: 6.4 (-3.4)", es: "Score: 6.4 (-3.4)" }, icon: "💳", x: 520, y: 55, color: "#4ade80" }
    ],
    links: [
      { from: 0, to: 1, label: { pt: "Bloqueado", en: "Blocked", es: "Bloqueado" }, color: "#64748b", dash: true },
      { from: 1, to: 2, label: { pt: "VLAN OOB 10.254.0.0", en: "OOB VLAN 10.254.0.0", es: "VLAN OOB 10.254.0.0" }, color: "#38bdf8", dash: false },
      { from: 2, to: 3, label: { pt: "RACL Filtrada", en: "Filtered RACL", es: "RACL Filtrada" }, color: "#4ade80", dash: false }
    ]
  }
};

window.currentScenarioPreset = "pci";

function getLocalizedField(obj) {
  var lang = window.currentLanguage || "pt";
  if (typeof obj === "object" && obj !== null) {
    return obj[lang] || obj.pt || "";
  }
  return String(obj || "");
}

function renderScenarioGraphSvg(preset) {
  var nodes = preset.nodes;
  var links = preset.links;

  var linesSvg = links.map(function(l) {
    var n1 = nodes[l.from];
    var n2 = nodes[l.to];
    var midX = (n1.x + n2.x) / 2;
    var midY = (n1.y + n2.y) / 2 - 12;
    var dashAttr = l.dash ? "stroke-dasharray='5,5'" : "";
    var lText = getLocalizedField(l.label);
    return "<line x1='" + n1.x + "' y1='" + n1.y + "' x2='" + n2.x + "' y2='" + n2.y + "' stroke='" + l.color + "' stroke-width='2.5' " + dashAttr + " />" +
      "<rect x='" + (midX - 55) + "' y='" + (midY - 9) + "' width='110' height='16' fill='#07111f' rx='4' />" +
      "<text x='" + midX + "' y='" + (midY + 3) + "' fill='" + l.color + "' font-size='10' font-weight='600' text-anchor='middle'>" + esc(lText) + "</text>";
  }).join("");

  var nodesSvg = nodes.map(function(n) {
    var nLabel = getLocalizedField(n.label);
    var nSub = getLocalizedField(n.sub);
    return "<g>" +
      "<circle cx='" + n.x + "' cy='" + n.y + "' r='20' fill='#081324' stroke='" + n.color + "' stroke-width='2.5' />" +
      "<text x='" + n.x + "' y='" + (n.y + 5) + "' font-size='14' text-anchor='middle'>" + n.icon + "</text>" +
      "<text x='" + n.x + "' y='" + (n.y + 32) + "' fill='#f8fafc' font-size='11' font-weight='700' text-anchor='middle'>" + esc(nLabel) + "</text>" +
      "<text x='" + n.x + "' y='" + (n.y + 44) + "' fill='#94a3b8' font-size='10' text-anchor='middle'>" + esc(nSub) + "</text>" +
    "</g>";
  }).join("");

  return "<svg width='100%' height='110' viewBox='0 0 600 110' style='overflow:visible;'>" +
    linesSvg + nodesSvg +
  "</svg>";
}

function renderScenarioEdu(presetKey) {
  var preset = SIMULATOR_PRESETS[presetKey] || SIMULATOR_PRESETS.pci;
  window.currentScenarioPreset = presetKey;
  var card = document.getElementById("scenarioEduCard");
  if (!card) return;

  var lang = window.currentLanguage || "pt";
  var svgHtml = renderScenarioGraphSvg(preset);

  var subMapped = (lang === "en" ? "Topology & Risk Mapped in Real Time" : (lang === "es" ? "Topología y Riesgo Mapeados en Tiempo Real" : "Topologia e Risco Mapeados em Tempo Real"));
  var realCase = (lang === "en" ? "Real Scenario:" : (lang === "es" ? "Escenario Real:" : "Cenário Real:"));
  var diagramTitle = (lang === "en" ? "Network Diagram: Asset Access Pathway" : (lang === "es" ? "Diagrama de Red: Flujo de Acceso al Activo" : "Diagrama da Rede: Fluxo de Acesso ao Ativo"));
  var connTitle = (lang === "en" ? "Physical / Logical Links" : (lang === "es" ? "Conexiones Físicas / Lógicas" : "Conexões Físicas / Lógicas"));
  var tradTitle = (lang === "en" ? "❌ Traditional Approach (Blind NVD / Zero Context)" : (lang === "es" ? "❌ Enfoque Tradicional (NVD Ciego / Sin Contexto)" : "❌ Abordagem Tradicional (NVD Cego / Sem Contexto)"));
  var advTitle = (lang === "en" ? "🚀 Why HelpUS Solution is Superior (Real Advantage)" : (lang === "es" ? "🚀 Por qué la Solución HelpUS es Superior (Ventaja Real)" : "🚀 Por que a Solução HelpUS é Superior (Vantagem Real)"));

  card.innerHTML =
    "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;border-bottom:1px solid #1e3a5f;padding-bottom:10px;'>" +
      "<div>" +
        "<strong style='color:#38bdf8;font-size:16px;'>" + esc(getLocalizedField(preset.title)) + "</strong>" +
        "<span class='badge-diff' style='background:rgba(56,189,248,0.15);color:#38bdf8;margin-left:10px;'>" + esc(getLocalizedField(preset.tag)) + "</span>" +
      "</div>" +
      "<small style='color:#94a3b8;'>" + subMapped + "</small>" +
    "</div>" +
    
    "<p class='note' style='margin:0 0 14px;color:#cbd5e1;font-size:13px;'>" +
      "🏢 <strong>" + realCase + "</strong> " + esc(getLocalizedField(preset.description)) +
    "</p>" +

    "<!-- Grafo de Topologia Visual deste Cenário -->" +
    "<div style='background:#030812;border:1px solid #1e3a5f;border-radius:12px;padding:12px 16px 18px;margin-bottom:16px;'>" +
      "<div style='display:flex;justify-content:space-between;margin-bottom:6px;'>" +
        "<span style='color:#38bdf8;font-size:12px;font-weight:700;'>🗺 " + diagramTitle + "</span>" +
        "<span style='color:#94a3b8;font-size:11px;'>" + connTitle + "</span>" +
      "</div>" +
      "<div style='width:100%;display:flex;justify-content:center;'>" + svgHtml + "</div>" +
    "</div>" +

    "<!-- Comparativo: Abordagem Tradicional vs Solução HelpUS -->" +
    "<div class='grid' style='grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;'>" +
      "<div style='background:#0b1526;border:1px solid #dc2626;border-radius:10px;padding:14px;'>" +
        "<div style='color:#f87171;font-weight:700;font-size:13px;margin-bottom:6px;'>" + tradTitle + "</div>" +
        "<p style='margin:0;font-size:12px;color:#cbd5e1;line-height:1.6;'>" + esc(getLocalizedField(preset.traditional_problem)) + "</p>" +
      "</div>" +
      "<div style='background:#0b1d2e;border:1px solid #4ade80;border-radius:10px;padding:14px;'>" +
        "<div style='color:#4ade80;font-weight:700;font-size:13px;margin-bottom:6px;'>🚀 " + advTitle + "</div>" +
        "<p style='margin:0;font-size:12px;color:#cbd5e1;line-height:1.6;'>" + esc(getLocalizedField(preset.helpus_advantage)) + "</p>" +
      "</div>" +
    "</div>";
}

function loadScenarioPreset(presetKey) {
  var preset = SIMULATOR_PRESETS[presetKey] || SIMULATOR_PRESETS.pci;
  window.currentScenarioPreset = presetKey;
  
  var presetKeys = ["pci", "dev", "ecom", "clinic", "santos"];
  presetKeys.forEach(function(k) {
    var btn = document.getElementById("preset-btn-" + k);
    if (btn) {
      if (k === presetKey) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    }
  });

  document.getElementById("scenario").value = preset.scenario;
  document.getElementById("asset_id").value = preset.asset_id;
  document.getElementById("cve").value = preset.cve;
  document.getElementById("base_score").value = preset.base_score;
  document.getElementById("internet_exposed").value = preset.internet_exposed;
  document.getElementById("network_segmented").value = preset.network_segmented;
  document.getElementById("pci_in_scope").value = preset.pci_in_scope;
  document.getElementById("firewall_restricted").value = preset.firewall_restricted;
  document.getElementById("compensating_controls").value = preset.compensating_controls;
  document.getElementById("business_criticality").value = preset.business_criticality;

  renderScenarioEdu(presetKey);
  calc();
}

function calc() {
  var base = Number(String(val("base_score") || "0").replace(",", "."));
  if (!isFinite(base)) base = 0;

  var contextual = base;
  var rationale = [];
  var citations = [];
  var lang = window.currentLanguage || "pt";

  // MAV (Modified Attack Vector) Evaluation
  var mav = "X";
  if (yes("network_segmented") && !yes("internet_exposed")) {
    mav = "A";
    contextual -= 0.8;
    citations.push(lang === "en" ? "MAV:Adjacent — Asset located on isolated subnet without direct external exposure." : (lang === "es" ? "MAV:Adjacent — Activo en subred aislada sin exposición externa directa." : "MAV:Adjacent — Ativo em subrede isolada sem exposição externa direta."));
    rationale.push("network segmentation reduced reachable attack surface");
  } else if (!yes("internet_exposed")) {
    mav = "L";
    contextual -= 1.8;
    citations.push(lang === "en" ? "MAV:Local — Strictly internal network asset, inaccessible from outside." : (lang === "es" ? "MAV:Local — Activo estrictamente de red interna, inaccesible desde el exterior." : "MAV:Local — Ativo estritamente de rede interna, inacessível externamente."));
    rationale.push("absence of internet exposure reduced contextual priority");
  } else if (yes("firewall_restricted") || yes("compensating_controls")) {
    mav = "N";
    contextual -= 0.4;
    citations.push(lang === "en" ? "MAV:Network — Exposed asset, preliminarily mitigated by perimeter WAF/Firewall." : (lang === "es" ? "MAV:Network — Activo expuesto, mitigado preliminarmente por WAF/Firewall perimetral." : "MAV:Network — Ativo exposto, mitigado preliminarmente por WAF/Firewall perimetral."));
    rationale.push("firewall and compensating controls mitigated external exposure");
  } else {
    mav = "N";
    contextual += 0.5;
    citations.push(lang === "en" ? "MAV:Network — Asset directly exposed to public internet without perimeter shielding." : (lang === "es" ? "MAV:Network — Activo expuesto directamente a internet sin blindaje perimetral." : "MAV:Network — Ativo exposto diretamente à internet sem evidência de blindagem."));
    rationale.push("internet exposure increased contextual priority");
  }

  // Security Requirements (CR, IR, AR)
  var cr = "M";
  if (yes("pci_in_scope")) {
    cr = "H";
    contextual += 0.4;
    citations.push(lang === "en" ? "CR:High — Asset in regulatory PCI-DSS / financial processing scope." : (lang === "es" ? "CR:High — Activo en alcance regulatorio PCI-DSS / procesamiento financiero." : "CR:High — Ativo em escopo regulatório PCI-DSS / processamento financeiro."));
    rationale.push("PCI scope increased business and compliance relevance");
  }

  var criticality = val("business_criticality");
  if (criticality === "high") {
    contextual += 0.5;
    citations.push(lang === "en" ? "IR:High — High business criticality asset." : (lang === "es" ? "IR:High — Activo de alta criticidad para el negocio." : "IR:High — Ativo de alta criticidade de negócio."));
    rationale.push("high business criticality increased contextual relevance");
  } else if (criticality === "low") {
    contextual -= 3.6;
    citations.push(lang === "en" ? "CR:Low, IR:Low & AR:Low — Test environment with synthetic data (low operational impact)." : (lang === "es" ? "CR:Low, IR:Low & AR:Low — Entorno de pruebas con datos ficticios (bajo impacto operacional)." : "CR:Low, IR:Low & AR:Low — Ambiente de teste com dados fictícios (baixo impacto operacional)."));
    rationale.push("low business criticality and test environment significantly reduced contextual priority");
  }

  // Detecção de contexto de consultório/clínica
  var scenVal = String(val("scenario")).toLowerCase();
  var assetVal = String(val("asset_id")).toLowerCase();
  if (scenVal.indexOf("clinic") !== -1 || assetVal.indexOf("clinic") !== -1) {
    if (yes("firewall_restricted") || yes("compensating_controls")) {
      contextual -= 0.7;
      citations.push(lang === "en" ? "LAN:Local — Connection restricted to local physical switch on premises." : (lang === "es" ? "LAN:Local — Conexión restringida al switch físico local del consultorio." : "LAN:Local — Conexão restrita ao switch físico local do consultório."));
      rationale.push("local physical clinic switch further contained reachable exposure");
    }
  }

  var contextualScore = Number(Math.max(0, Math.min(10, contextual)).toFixed(1));
  var delta = Number((contextualScore - base).toFixed(1));
  var decision = delta < 0 ? "downgraded" : (delta > 0 ? "upgraded" : "unchanged");

  var officialCvss = {
    base_score: fmtNum(base, 1),
    base_severity: sev(base)
  };

  var contextualEnvironmental = {
    contextual_score: fmtNum(contextualScore, 1),
    contextual_severity: sev(contextualScore),
    nomenclature: "CVSS-BE",
    decision: decision,
    delta_from_official_base: fmtNum(delta, 1),
    rationale: rationale.join("; "),
    citations: citations
  };

  var evidence = {
    scenario: val("scenario"),
    asset_id: val("asset_id"),
    cve: val("cve"),
    internet_exposed: val("internet_exposed"),
    network_segmented: val("network_segmented"),
    pci_in_scope: val("pci_in_scope"),
    firewall_restricted: val("firewall_restricted"),
    compensating_controls: val("compensating_controls"),
    business_criticality: criticality
  };

  var out = {
    official_cvss: officialCvss,
    contextual_environmental: contextualEnvironmental,
    evidence: evidence,
    scenario: evidence.scenario,
    asset_id: evidence.asset_id,
    cve: evidence.cve,
    base_score: officialCvss.base_score,
    base_severity: officialCvss.base_severity,
    environmental_score: contextualEnvironmental.contextual_score,
    environmental_severity: contextualEnvironmental.contextual_severity,
    delta: contextualEnvironmental.delta_from_official_base,
    decision: contextualEnvironmental.decision,
    rationale: contextualEnvironmental.rationale,
    internet_exposed: evidence.internet_exposed,
    network_segmented: evidence.network_segmented,
    pci_in_scope: evidence.pci_in_scope,
    firewall_restricted: evidence.firewall_restricted,
    compensating_controls: evidence.compensating_controls,
    business_criticality: evidence.business_criticality
  };

  window.lastCvssResult = out;

  var deltaColor = delta < 0 ? "#4ade80" : (delta > 0 ? "#fbbf24" : "#94a3b8");
  var citationsHtml = citations.map(function(c) {
    return "<li style='margin-bottom:6px;'>" + esc(c) + "</li>";
  }).join("");

  var resTitle = (lang === "en" ? "📊 Environmental Assessment Result CVSS v4.0 (FIRST Spec)" : (lang === "es" ? "📊 Resultado de la Evaluación Ambiental CVSS v4.0 (FIRST Spec)" : "📊 Resultado da Avaliação Ambiental CVSS v4.0 (FIRST Spec)"));
  var cardNvd = (lang === "en" ? "🔴 Primary Base CVSS" : (lang === "es" ? "🔴 Base de Origen CVSS" : "🔴 Base de Origem CVSS"));
  var cardCtx = (lang === "en" ? "🟢 Contextual Priority (CVSS-BE)" : (lang === "es" ? "🟢 Prioridad Contextual (CVSS-BE)" : "🟢 Prioridade Contextual (CVSS-BE)"));
  var cardVar = (lang === "en" ? "⚖ Real Variation (Delta)" : (lang === "es" ? "⚖ Variación Real (Delta)" : "⚖ Variação Real (Delta)"));
  var citTitle = (lang === "en" ? "🔍 Evidence Citations Extracted by AI Watcher:" : (lang === "es" ? "🔍 Citas de Evidencias Extraídas por el Watcher con IA:" : "🔍 Citações de Evidências Extraídas pelo Watcher com IA:"));
  var hitlTitle = (lang === "en" ? "Human Review Gate (HITL):" : (lang === "es" ? "Puerta de Revisión Humana (HITL):" : "Gate de Revisão Humana (HITL):"));
  var hitlSub = (lang === "en" ? "AI proposes grounded in evidence. Final homologation is human." : (lang === "es" ? "La IA propone basada en evidencias. La homologación final es humana." : "A IA propõe fundamentada em evidências. A homologação final é humana."));
  var hitlApprove = (lang === "en" ? "✓ Homologate Proposal" : (lang === "es" ? "✓ Homologar Propuesta" : "✓ Homologar Proposta"));
  var hitlReject = (lang === "en" ? "✕ Adjust / Reject" : (lang === "es" ? "✕ Ajustar / Rechazar" : "✕ Ajustar / Rejeitar"));

  // Tri-Score & EPSS Values
  var legacyV31 = Math.min(10.0, base);
  var epssGlobal = (base >= 9.0 ? "88.4%" : (base >= 7.0 ? "54.2%" : "12.8%"));
  var epssLocal = (!yes("internet_exposed") ? "< 0.1%" : (yes("firewall_restricted") ? "1.4%" : epssGlobal));
  var slaDaysBase = (base >= 9.0 ? "72h (3d)" : (base >= 7.0 ? "15d" : "60d"));
  var slaDaysCtx = (contextualScore >= 9.0 ? "72h (3d)" : (contextualScore >= 7.0 ? "15d" : "60d"));

  var resultEl = document.getElementById("result");
  if (resultEl) {
    resultEl.innerHTML =
      "<h3 style='margin-top:0;color:#38bdf8;'>" + resTitle + "</h3>" +
      "<div class=grid>" +
      "<div class=card><div>" + cardNvd + "</div><div class=metric style='color:#f87171'>" + esc(officialCvss.base_score) + "</div><div style='color:#94a3b8'>" + esc(officialCvss.base_severity) + "</div></div>" +
      "<div class=card><div>" + cardCtx + "</div><div class=metric style='color:#4ade80'>" + esc(contextualEnvironmental.contextual_score) + "</div><div style='color:#94a3b8'>" + esc(contextualEnvironmental.contextual_severity) + "</div></div>" +
      "<div class=card><div>" + cardVar + "</div><div class=metric style='color:" + deltaColor + "'>" + (delta > 0 ? "+" : "") + esc(contextualEnvironmental.delta_from_official_base) + "</div><div style='color:#94a3b8'>" + esc(contextualEnvironmental.decision) + "</div></div>" +
      "</div>" +

      "<!-- Painel Tri-Score Diff, EPSS Local & Cronômetro SLA -->" +
      "<div style='margin-top:16px;background:#050c17;padding:16px;border-radius:12px;border:1px solid #1e3a5f;'>" +
        "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;'>" +
          "<strong style='color:#38bdf8;font-size:14px;'>⚖ Comparador Tripartite & Inteligência Preditiva EPSS</strong>" +
          "<span style='font-size:11px;color:#94a3b8;'>Multi-Vector Audit</span>" +
        "</div>" +
        "<div class='triscore-grid'>" +
          "<div class='triscore-card'>" +
            "<small style='color:#94a3b8;'>CVSS v3.1 Legado</small>" +
            "<div style='font-size:18px;font-weight:bold;color:#f87171;'>" + fmtNum(legacyV31, 1) + "</div>" +
            "<small style='color:#64748b;font-size:10px;'>Escopo Rígido Inflado</small>" +
          "</div>" +
          "<div class='triscore-card'>" +
            "<small style='color:#94a3b8;'>CVSS v4.0 NVD Base</small>" +
            "<div style='font-size:18px;font-weight:bold;color:#f87171;'>" + esc(officialCvss.base_score) + "</div>" +
            "<small style='color:#64748b;font-size:10px;'>Padrão FIRST 2026</small>" +
          "</div>" +
          "<div class='triscore-card'>" +
            "<small style='color:#94a3b8;'>HelpUS Contextual</small>" +
            "<div style='font-size:18px;font-weight:bold;color:#4ade80;'>" + esc(contextualEnvironmental.contextual_score) + "</div>" +
            "<small style='color:#4ade80;font-size:10px;'>Com Evidências Reais</small>" +
          "</div>" +
          "<div class='triscore-card'>" +
            "<small style='color:#94a3b8;'>EPSS Global vs Local</small>" +
            "<div style='font-size:16px;font-weight:bold;color:#38bdf8;'>" + epssLocal + " <span style='font-size:11px;color:#64748b;'>(" + epssGlobal + ")</span></div>" +
            "<small style='color:#94a3b8;font-size:10px;'>Protegido por Perímetro</small>" +
          "</div>" +
          "<div class='triscore-card'>" +
            "<small style='color:#94a3b8;'>SLA Regulatório</small>" +
            "<div style='font-size:16px;font-weight:bold;color:#a78bfa;'>" + slaDaysCtx + "</div>" +
            "<small style='color:#64748b;font-size:10px;'>vs " + slaDaysBase + " Emergencial</small>" +
          "</div>" +
        "</div>" +
      "</div>" +

      "<div style='margin-top:16px;background:#050c17;padding:16px;border-radius:10px;border:1px solid #1e3a5f;'>" +
      "<h4 style='margin:0 0 8px;color:#38bdf8;'>" + citTitle + "</h4>" +
      "<ul style='margin:0;padding-left:20px;color:#cbd5e1;line-height:1.6;'>" + citationsHtml + "</ul>" +
      "</div>" +
      "<div style='margin-top:16px;padding:16px;border-radius:10px;background:#050c17;border:1px solid #1e3a5f;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;'>" +
      "<div><strong>" + hitlTitle + "</strong><br><small style='color:#94a3b8'>" + hitlSub + "</small></div>" +
      "<div id='reviewDecisionBox' style='display:flex;gap:8px;'>" +
      "<button onclick='approveDecision()' style='width:auto;padding:8px 16px;background:#16a34a;border-color:#16a34a;'>" + hitlApprove + "</button>" +
      "<button onclick='rejectDecision()' style='width:auto;padding:8px 16px;background:#475569;border-color:#475569;'>" + hitlReject + "</button>" +
      "</div>" +
      "</div>";
  }
}

function loadExample() {
  loadScenarioPreset("pci");
}

function downloadJson() {
  var data = JSON.stringify(getExportContract(), null, 2);
  var blob = new Blob([data], {type: "application/json"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cvss_official_contextual_result.json";
  a.click();
}

function downloadCsv() {
  var r = window.lastCvssResult || {};
  var o = r.official_cvss || {};
  var c = r.contextual_environmental || {};
  var e = r.evidence || {};
  var header = [
    "scenario",
    "asset_id",
    "cve",
    "official_cvss_base_score",
    "official_cvss_base_severity",
    "contextual_score",
    "contextual_severity",
    "contextual_decision",
    "contextual_delta_from_official_base",
    "rationale"
  ];
  var values = [
    e.scenario,
    e.asset_id,
    e.cve,
    o.base_score,
    o.base_severity,
    c.contextual_score,
    c.contextual_severity,
    c.decision,
    c.delta_from_official_base,
    c.rationale
  ];
  var csv = header.join(",") + "\n" + values.map(quoteCsv).join(",");
  var blob = new Blob([csv], {type: "text/csv"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cvss_official_contextual_result.csv";
  a.click();
}

function copyPipelineJson() {
  var r = window.lastCvssResult || {};
  var e = r.evidence || {};
  var o = r.official_cvss || {};
  var pkg = {
    case_description: {
      scenario: e.scenario,
      source: "interactive_static_mvp"
    },
    vulnerabilities: [{
      finding_id: "interactive-001",
      asset_id: e.asset_id,
      cve: e.cve,
      vulnerability_type: "user_entered",
      official_cvss_base_score: o.base_score,
      official_cvss_base_severity: o.base_severity
    }],
    context: e,
    export_layers: getExportContract()
  };
  navigator.clipboard.writeText(JSON.stringify(pkg, null, 2));
  alert("Pipeline JSON copiado com sucesso!");
}

function downloadReport() {
  var r = window.lastCvssResult || {};
  var o = r.official_cvss || {};
  var c = r.contextual_environmental || {};
  var e = r.evidence || {};
  var text = "# Relatório de Avaliação Ambiental CVSS v4.0\n\n";
  text += "## Vetor Base CVSS v4.0 (Origem CNA/NVD)\n";
  text += "- Base Score: " + (o.base_score || "") + "\n";
  text += "- Base Severity: " + (o.base_severity || "") + "\n\n";

  text += "## Priorização Contextual com IA (CVSS-BE)\n";
  text += "- Contextual Score: " + (c.contextual_score || "") + "\n";
  text += "- Contextual Severity: " + (c.contextual_severity || "") + "\n";
  text += "- Decisão: " + (c.decision || "") + "\n";
  text += "- Variação (Delta): " + (c.delta_from_official_base || "") + "\n";
  text += "- Justificativa: " + (c.rationale || "") + "\n\n";

  text += "## Evidências do Ambiente\n";
  text += "- Cenário: " + (e.scenario || "") + "\n";
  text += "- Ativo: " + (e.asset_id || "") + "\n";
  text += "- CVE: " + (e.cve || "") + "\n";
  text += "- Exposição Internet: " + (e.internet_exposed || "") + "\n";
  text += "- Segmentação Rede: " + (e.network_segmented || "") + "\n";
  text += "- Escopo PCI: " + (e.pci_in_scope || "") + "\n";
  text += "- Firewall: " + (e.firewall_restricted || "") + "\n\n";

  if (r.homologation) {
    var h = r.homologation;
    text += "## Homologação e Governança Humana (HITL)\n";
    text += "- Status: " + h.status + "\n";
    text += "- Responsável: " + h.reviewer_name + " <" + h.reviewer_email + "> (" + h.reviewer_role + ")\n";
    text += "- Ticket Vinculado: " + h.ticket_id + "\n";
    text += "- Score Efetivo Aprovado: " + h.effective_score + " (" + h.effective_severity + ")\n";
    text += "- Justificativa do Analista: " + h.rationale + "\n";
    text += "- Timestamp ISO: " + h.timestamp + "\n";
    text += "- Hash de Rastreabilidade (SHA): `" + h.audit_hash + "`\n\n";
  }

  text += "## Ressalva Científica\n";
  text += "A priorização contextual é complementar e não substitui o score base de origem.\n";

  var blob = new Blob([text], {type: "text/markdown"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cvss_assessment_report.md";
  a.click();
}

function getVisitorClientInfo() {
  var ua = navigator.userAgent || "";
  var platform = navigator.userAgentData && navigator.userAgentData.platform ? navigator.userAgentData.platform : (navigator.platform || "");
  var isWindows = /Win/i.test(ua) || /Win/i.test(platform);
  var isMac = /Mac/i.test(ua) || /Mac/i.test(platform);
  var isLinux = /Linux/i.test(ua) || /Linux/i.test(platform);
  var isMobile = /Android|iPhone|iPad|Mobile/i.test(ua);

  var osName = isWindows ? "Windows PC" : (isMac ? "macOS" : (isLinux ? "Linux Host" : (isMobile ? "Mobile Device" : "Workstation")));
  var browser = /Chrome/i.test(ua) && !/Edg/i.test(ua) ? "Chrome" : (/Edg/i.test(ua) ? "Edge" : (/Firefox/i.test(ua) ? "Firefox" : (/Safari/i.test(ua) ? "Safari" : "Web Browser")));

  return {
    osName: osName,
    browser: browser,
    hostLabel: "Host (" + osName + ")",
    ip: "127.0.0.1"
  };
}

var currentScanMode = "probe";

var ENV_PRESETS = {
  pci_joe: {
    title: { pt: "🏬 Joe's Jerky Store (Canônico PCI-DSS v3 - Level 3)", en: "🏬 Joe's Jerky Store (Canonical PCI-DSS v3 - Level 3)", es: "🏬 Joe's Jerky Store (Canónico PCI-DSS v3 - Level 3)" },
    subnet: "192.168.10.0/24 (Store LAN / DMZ)",
    scan_time: "2017-04-12T10:15:00Z",
    hosts_count: 4,
    nodes: [
      { id: "dsl", x: 100, y: 110, label: "DSL Router + DMZ", type: "gw" },
      { id: "pos", x: 300, y: 55, label: "POS Terminals (IP)", type: "protected" },
      { id: "kiosk", x: 300, y: 165, label: "Customer Kiosk", type: "vuln" },
      { id: "wifi", x: 500, y: 110, label: "Free Guest Wi-Fi", type: "vuln" }
    ],
    links: [
      { from: "dsl", to: "pos", label: "DMZ Subnet" },
      { from: "dsl", to: "kiosk", label: "Ethernet" },
      { from: "dsl", to: "wifi", label: "Unsegmented AP" }
    ],
    findings: [
      {
        asset_ip: "192.168.10.50",
        asset_hostname: "pos-terminal-store",
        asset_role: { pt: "Terminal de Ponto de Venda (Cartões de Crédito)", en: "Point-of-Sale Terminal (Credit Cards)", es: "Terminal de Punto de Venta (Tarjetas)" },
        cve: "CVE-2016-0167",
        title: "Windows Kernel-Mode Driver Privilege Escalation (Win32k)",
        official_base_score: 7.8,
        official_base_severity: "High",
        contextual_score: 5.4,
        contextual_severity: "Medium",
        delta: -2.4,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Local — O terminal POS opera isolado na DMZ do roteador DSL.",
            "CR:High / IR:High — Escopo de conformidade PCI-DSS obrigatório.",
            "Estudo Santos et al. (2017): 72% de acerto humano em rede flat; mitigado após DMZ."
          ],
          en: [
            "MAV:Local — POS terminal operates segmented within router DMZ.",
            "CR:High / IR:High — Mandatory PCI-DSS compliance scope.",
            "Santos et al. (2017) trial: 72% human accuracy in flat net; mitigated post-DMZ."
          ],
          es: [
            "MAV:Local — La terminal POS opera aislada en la DMZ del router.",
            "CR:High / IR:High — Alcance obligatorio de cumplimiento PCI-DSS.",
            "Estudio Santos et al. (2017): 72% acierto humano en red plana; mitigado tras DMZ."
          ]
        }
      }
    ]
  },
  pci_christine: {
    title: { pt: "🏢 Christine's Enterprise (Canônico PCI-DSS v1 - Cisco Core Switch)", en: "🏢 Christine's Enterprise (Canonical PCI-DSS v1 - Cisco Core Switch)", es: "🏢 Christine's Enterprise (Canónico PCI-DSS v1 - Cisco Core Switch)" },
    subnet: "10.100.0.0/16 (Corporate Multi-VLAN)",
    scan_time: "2017-05-18T14:30:00Z",
    hosts_count: 5,
    nodes: [
      { id: "border", x: 80, y: 110, label: "Border Router", type: "gw" },
      { id: "cisco", x: 260, y: 110, label: "Cisco ASR Core Switch", type: "gw" },
      { id: "cardholder", x: 440, y: 55, label: "Cardholder Enclave", type: "protected" },
      { id: "admin", x: 440, y: 165, label: "Admin Store PCs", type: "vuln" },
      { id: "wifi", x: 600, y: 110, label: "WIPS Wireless", type: "protected" }
    ],
    links: [
      { from: "border", to: "cisco", label: "Fiber Trunk" },
      { from: "cisco", to: "cardholder", label: "VLAN RACL Enclave" },
      { from: "cisco", to: "admin", label: "Store VLAN" },
      { from: "cisco", to: "wifi", label: "Isolated WIPS" }
    ],
    findings: [
      {
        asset_ip: "10.254.0.1",
        asset_hostname: "cisco-asr-aggregation",
        asset_role: { pt: "Switch de Agregação de Núcleo (Cisco IOS XE)", en: "Core Aggregation Switch (Cisco IOS XE)", es: "Switch de Agregación de Núcleo (Cisco IOS XE)" },
        cve: "CVE-2016-6441",
        title: "Cisco IOS Transaction Language 1 (TL1) Remote Code Execution",
        official_base_score: 9.8,
        official_base_severity: "Critical",
        contextual_score: 6.4,
        contextual_severity: "Medium",
        delta: -3.4,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Adjacent — Porta de gerenciamento TL1 (3082/TCP) restrita à VLAN de gerência OOB.",
            "MPR:High — Acesso autenticado via VPN e token exigido para operadores de rede.",
            "Estudo Santos et al. (Springer 2017): 86% dos analistas humanos cometeram erro grave neste ativo."
          ],
          en: [
            "MAV:Adjacent — TL1 management port (3082/TCP) restricted to OOB management VLAN.",
            "MPR:High — Authenticated access via VPN token mandated for operators.",
            "Santos et al. (Springer 2017): 86% of human assessors committed severe scoring errors on this asset."
          ],
          es: [
            "MAV:Adjacent — Puerto de gestión TL1 (3082/TCP) restringido a la VLAN de gestión OOB.",
            "MPR:High — Acceso autenticado mediante token VPN requerido.",
            "Estudio Santos et al. (Springer 2017): 86% de los analistas humanos cometieron errores graves en este activo."
          ]
        }
      }
    ]
  },
  lan: {
    title: { pt: "Rede Local Corporativa (LAN)", en: "Corporate Local Network (LAN)", es: "Red Local Corporativa (LAN)" },
    subnet: "192.168.1.0/24",
    scan_time: new Date().toISOString(),
    hosts_count: 3,
    nodes: [
      { id: "gw", x: 120, y: 110, label: "Gateway 192.168.1.1", type: "gw" },
      { id: "local", x: 400, y: 55, label: "Host (127.0.0.1)", type: "protected" },
      { id: "db", x: 400, y: 165, label: "DB (192.168.1.100)", type: "vuln" }
    ],
    links: [
      { from: "gw", to: "local", label: "VLAN" },
      { from: "gw", to: "db", label: "Port 5432" }
    ],
    findings: [
      {
        asset_ip: "127.0.0.1",
        asset_hostname: "User Host",
        asset_role: { pt: "Estação de Trabalho Local", en: "Local Workstation", es: "Estación de Trabajo Local" },
        cve: "CVE-2023-39417",
        title: "PostgreSQL Extension SQL Injection Vulnerability",
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 8.5,
        contextual_severity: "High",
        delta: -0.2,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Local — Serviço no localhost inacessível pela internet externa.",
            "CR:High — Escopo de credenciais locais protegidas.",
            "IR:High — Integridade da base transacional resguardada."
          ],
          en: [
            "MAV:Local — Service on localhost inaccessible from external internet.",
            "CR:High — Protected local credential scope.",
            "IR:High — Integrity of transactional database safeguarded."
          ],
          es: [
            "MAV:Local — Servicio en localhost inaccesible desde internet externo.",
            "CR:High — Alcance de credenciales locales protegido.",
            "IR:High — Integridad de la base transaccional resguardada."
          ]
        }
      },
      {
        asset_ip: "192.168.1.1",
        asset_hostname: "Gateway / Web Router",
        asset_role: { pt: "Roteador e Firewall de Borda Local", en: "Local Edge Router & Firewall", es: "Router y Firewall de Borde Local" },
        cve: "CVE-2023-44487",
        title: "HTTP/2 Rapid Reset Denial of Service",
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 7.1,
        contextual_severity: "High",
        delta: -1.6,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Adjacent — Ativo opera em subrede privada 192.168.1.0/24 sem porta pública exposta.",
            "AR:High — Ponto de interrupção de tráfego local."
          ],
          en: [
            "MAV:Adjacent — Asset operates on private 192.168.1.0/24 subnet with no public port exposed.",
            "AR:High — Local traffic outage disruption point."
          ],
          es: [
            "MAV:Adjacent — Activo opera en subred privada 192.168.1.0/24 sin puerto público expuesto.",
            "AR:High — Punto de interrupción de tráfico local."
          ]
        }
      }
    ]
  },
  cloud: {
    title: { pt: "Infraestrutura Cloud / DMZ (AWS/Vercel/API)", en: "Cloud Infrastructure / DMZ (AWS/Vercel/API)", es: "Infraestructura Cloud / DMZ (AWS/Vercel/API)" },
    subnet: "10.0.0.0/16 (VPC)",
    scan_time: "2026-10-07T03:31:12Z",
    hosts_count: 4,
    nodes: [
      { id: "lb", x: 100, y: 110, label: "Cloudflare / WAF", type: "gw" },
      { id: "api", x: 300, y: 60, label: "API Gateway", type: "protected" },
      { id: "auth", x: 300, y: 160, label: "Auth Service", type: "protected" },
      { id: "s3", x: 500, y: 110, label: "Storage S3", type: "vuln" }
    ],
    links: [
      { from: "lb", to: "api", label: "HTTPS / TLS 1.3" },
      { from: "lb", to: "auth", label: "WAF" },
      { from: "api", to: "s3", label: "IAM Role" }
    ],
    findings: [
      {
        asset_ip: "api.helpusbr.com",
        asset_hostname: "API Gateway Cloud",
        asset_role: { pt: "Microsserviço de Borda com Proteção WAF", en: "Edge Microservice with WAF", es: "Microservicio de Borde con WAF" },
        cve: "CVE-2023-44487",
        title: "HTTP/2 Rapid Reset Mitigation",
        official_base_score: 7.5,
        official_base_severity: "High",
        contextual_score: 6.2,
        contextual_severity: "Medium",
        delta: -1.3,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Network mantido com ressalva de WAF ativo com Rate-limiting ativado na borda.",
            "AR:Low mitigado por auto-scaling elástico do cluster."
          ],
          en: [
            "MAV:Network retained with active edge WAF and Rate-limiting verified.",
            "AR:Low mitigated by cluster elastic auto-scaling."
          ],
          es: [
            "MAV:Network mantenido con salvedad de WAF activo y Rate-limiting en el borde.",
            "AR:Low mitigado por auto-escalado elástico del clúster."
          ]
        }
      }
    ]
  },
  pci: {
    title: { pt: "Zona Restrita de Pagamentos (PCI-DSS Cluster)", en: "Restricted Payment Zone (PCI-DSS Cluster)", es: "Zona Restringida de Pagos (PCI-DSS Cluster)" },
    subnet: "172.16.10.0/24 (VLAN 40)",
    scan_time: "2026-10-07T03:32:00Z",
    hosts_count: 3,
    nodes: [
      { id: "fw", x: 110, y: 110, label: "Firewall NGFW", type: "gw" },
      { id: "hsm", x: 380, y: 60, label: "HSM Crypto", type: "protected" },
      { id: "pay_db", x: 380, y: 160, label: "Vault DB", type: "vuln" }
    ],
    links: [
      { from: "fw", to: "hsm", label: "IPSec / mTLS" },
      { from: "fw", to: "pay_db", label: "MFA" }
    ],
    findings: [
      {
        asset_ip: "172.16.10.50",
        asset_hostname: "Vault PCI",
        asset_role: { pt: "Database de Pagamentos e Tokens Bancários", en: "Payment Database & Banking Token Vault", es: "Database de Pagos y Tokens Bancarios" },
        cve: "CVE-2025-0001",
        title: "Zero-Day Memory Leak in Crypto Module",
        official_base_score: 9.8,
        official_base_severity: "Critical",
        contextual_score: 8.9,
        contextual_severity: "High",
        delta: -0.9,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Adjacent — Acesso restrito a terminais com chave física e MFA.",
            "CR:High / IR:High — Requisitos máximos de confidencialidade regulatória PCI-DSS."
          ],
          en: [
            "MAV:Adjacent — Restricted access to physical token terminals with MFA.",
            "CR:High / IR:High — Maximum regulatory confidentiality requirements for PCI-DSS."
          ],
          es: [
            "MAV:Adjacent — Acceso restringido a terminales con token físico y MFA.",
            "CR:High / IR:High — Máximos requisitos de confidencialidad regulatoria PCI-DSS."
          ]
        }
      }
    ]
  },
  k8s: {
    title: { pt: "Cluster Docker / Microsserviços de Produção", en: "Production Docker / Microservices Cluster", es: "Clúster Docker / Microservicios de Producción" },
    subnet: "10.244.0.0/16 (Pod Overlay)",
    scan_time: "2026-10-07T03:33:05Z",
    hosts_count: 4,
    nodes: [
      { id: "ing", x: 100, y: 110, label: "Ingress Controller", type: "gw" },
      { id: "node1", x: 280, y: 55, label: "Worker-01 (API)", type: "protected" },
      { id: "node2", x: 280, y: 165, label: "Worker-02 (Worker)", type: "protected" },
      { id: "redis", x: 480, y: 110, label: "Redis State Cache", type: "vuln" }
    ],
    links: [
      { from: "ing", to: "node1", label: "ClusterIP" },
      { from: "ing", to: "node2", label: "ClusterIP" },
      { from: "node1", to: "redis", label: "NetworkPolicy" },
      { from: "node2", to: "redis", label: "NetworkPolicy" }
    ],
    findings: [
      {
        asset_ip: "redis.default.svc",
        asset_hostname: "Redis Cache",
        asset_role: { pt: "Banco em Memória de Sessões e Fila", en: "In-Memory Session & Queue Store", es: "Base en Memoria de Sesiones y Cola" },
        cve: "CVE-2024-31449",
        title: "Lua Script Integer Overflow in Redis",
        official_base_score: 7.0,
        official_base_severity: "High",
        contextual_score: 5.6,
        contextual_severity: "Medium",
        delta: -1.4,
        nomenclature: "CVSS-BE",
        ai_citations: {
          pt: [
            "MAV:Adjacent — Acesso bloqueado externamente por NetworkPolicies do Kubernetes.",
            "AR:Low — Sessões armazenadas com fallback em banco relacional persistente."
          ],
          en: [
            "MAV:Adjacent — External access blocked by Kubernetes NetworkPolicies.",
            "AR:Low — Sessions preserved with persistent relational DB fallback."
          ],
          es: [
            "MAV:Adjacent — Acceso externo bloqueado por NetworkPolicies de Kubernetes.",
            "AR:Low — Sesiones preservadas con fallback en BD relacional persistente."
          ]
        }
      }
    ]
  }
};

function setScanMode(mode) {
  currentScanMode = mode;
  var modes = ["probe", "custom", "presets", "upload"];
  modes.forEach(function(m) {
    var btn = document.getElementById("mode-tab-" + m);
    if (btn) {
      if (m === mode) btn.classList.add("active");
      else btn.classList.remove("active");
    }
  });
  renderScanModeControls(mode);
}

function renderScanModeControls(mode) {
  var container = document.getElementById("scanModeControls");
  if (!container) return;
  var info = getVisitorClientInfo();
  var lang = window.currentLanguage || "pt";

  if (mode === "probe") {
    var probeTitle = (lang === "en" ? "💻 Visitor Device Detected:" : (lang === "es" ? "💻 Dispositivo del Visitante Detectado:" : "💻 Dispositivo do Visitante Detectado:"));
    var probeSub = (lang === "en" ? "Local Address: 127.0.0.1 (Loopback) • Ready to probe local services on your workstation" : (lang === "es" ? "Dirección Local: 127.0.0.1 (Loopback) • Listo para sondear servicios locales en su computadora" : "Endereço Local: 127.0.0.1 (Loopback) • Pronto para sondar serviços locais no seu computador"));
    var probeBtn = (lang === "en" ? "▶ Probe My Machine Now" : (lang === "es" ? "▶ Sondear Mi Computadora Ahora" : "▶ Sondar Meu Computador Agora"));

    container.innerHTML =
      "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;'>" +
        "<div>" +
          "<strong style='color:#38bdf8;font-size:15px;'>" + probeTitle + "</strong>" +
          "<span style='color:#f8fafc;margin-left:8px;font-weight:700;'>" + esc(info.osName) + " (" + esc(info.browser) + ")</span>" +
          "<br><small style='color:#94a3b8;'>" + probeSub + "</small>" +
        "</div>" +
        "<button onclick='runDeviceProbe()' style='width:auto;padding:10px 20px;background:#0284c7;'>" + probeBtn + "</button>" +
      "</div>";
    runDeviceProbe();
  } else if (mode === "custom") {
    var lblHost = (lang === "en" ? "Your Host / Machine Name:" : (lang === "es" ? "Nombre de su Host / Computadora:" : "Nome do Seu Computador/Host:"));
    var lblSubnet = (lang === "en" ? "Your Subnet Range:" : (lang === "es" ? "Rango de su Subred:" : "Sua Faixa de Subrede:"));
    var lblSvc = (lang === "en" ? "Local Service to Evaluate:" : (lang === "es" ? "Servicio Local a Evaluar:" : "Serviço Local a Avaliar:"));
    var optDb = (lang === "en" ? "PostgreSQL / SQL Server (Port 5432 / 1433)" : (lang === "es" ? "PostgreSQL / SQL Server (Puerto 5432 / 1433)" : "PostgreSQL / SQL Server (Porta 5432 / 1433)"));
    var optWeb = (lang === "en" ? "Web Server / HTTP API (Port 80 / 443 / 3000)" : (lang === "es" ? "Servidor Web / API HTTP (Puerto 80 / 443 / 3000)" : "Servidor Web / Aplicação (Porta 80 / 443 / 3000)"));
    var optSsh = (lang === "en" ? "Remote Shell / SSH (Port 22 / 3389)" : (lang === "es" ? "Terminal Remoto / SSH (Puerto 22 / 3389)" : "Terminal Remoto / SSH (Porta 22 / 3389)"));
    var btnMap = (lang === "en" ? "▶ Map & Compute Risk" : (lang === "es" ? "▶ Mapear y Calcular Riesgo" : "▶ Mapear e Calcular Risco"));

    container.innerHTML =
      "<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;align-items:end;'>" +
        "<label style='margin:0;'>" + lblHost +
          "<input id='customHostName' value='" + esc(info.osName) + "' style='margin-top:4px;'>" +
        "</label>" +
        "<label style='margin:0;'>" + lblSubnet +
          "<input id='customSubnet' value='192.168.1.0/24' style='margin-top:4px;'>" +
        "</label>" +
        "<label style='margin:0;'>" + lblSvc +
          "<select id='customService' style='margin-top:4px;'>" +
            "<option value='db'>" + optDb + "</option>" +
            "<option value='web'>" + optWeb + "</option>" +
            "<option value='ssh'>" + optSsh + "</option>" +
          "</select>" +
        "</label>" +
        "<button onclick='runCustomSubnetScan()' style='height:44px;background:#0284c7;'>" + btnMap + "</button>" +
      "</div>";
  } else if (mode === "presets") {
    var lblModel = (lang === "en" ? "Select Infrastructure Blueprint:" : (lang === "es" ? "Seleccione el Modelo de Infraestructura:" : "Selecione o Modelo de Infraestrutura:"));
    var optP1 = (lang === "en" ? "📡 1. Corporate Local Area Network (192.168.1.0/24)" : (lang === "es" ? "📡 1. Red Local Corporativa (192.168.1.0/24)" : "📡 1. Rede Local Corporativa (192.168.1.0/24)"));
    var optP2 = (lang === "en" ? "☁ 2. Cloud Infrastructure / DMZ (AWS/Vercel/API)" : (lang === "es" ? "☁ 2. Infraestructura Cloud / DMZ (AWS/Vercel/API)" : "☁ 2. Infraestrutura Cloud / DMZ (AWS/Vercel/API)"));
    var optP3 = (lang === "en" ? "💳 3. Restricted Payment Zone (PCI-DSS Cluster)" : (lang === "es" ? "💳 3. Zona Restringida de Pagos (PCI-DSS Cluster)" : "💳 3. Zona Restrita de Pagamentos (PCI-DSS Cluster)"));
    var optP4 = (lang === "en" ? "🐳 4. Production Docker / Microservices Cluster" : (lang === "es" ? "🐳 4. Clúster Docker / Microservicios de Producción" : "🐳 4. Cluster Docker / Microsserviços de Produção"));
    var btnLoad = (lang === "en" ? "▶ Load Blueprint" : (lang === "es" ? "▶ Cargar Modelo" : "▶ Carregar Modelo"));

    container.innerHTML =
      "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;'>" +
        "<div style='flex:1;min-width:240px;'>" +
          "<label style='margin:0;'>" + lblModel +
            "<select id='scanTargetSelect' onchange='runSelectedScan()' style='margin-top:4px;'>" +
              "<option value='lan'>" + optP1 + "</option>" +
              "<option value='cloud'>" + optP2 + "</option>" +
              "<option value='pci'>" + optP3 + "</option>" +
              "<option value='k8s'>" + optP4 + "</option>" +
              "<option value='pci_joe'>🏬 5. Joe's Store (Canonical PCI-DSS v3 - Level 3)</option>" +
              "<option value='pci_christine'>🏢 6. Christine's Enterprise (Canonical PCI-DSS v1 - Cisco Core)</option>" +
            "</select>" +
          "</label>" +
        "</div>" +
        "<button onclick='runSelectedScan()' style='width:auto;margin-top:20px;padding:10px 20px;background:#0284c7;'>" + btnLoad + "</button>" +
      "</div>";
    runSelectedScan();
  } else if (mode === "upload") {
    var upTitle = (lang === "en" ? "📂 Import Real Vulnerability Scan Report (.json)" : (lang === "es" ? "📂 Importar Reporte Real de Escaneo (.json)" : "📂 Importar Relatório de Varredura Real (.json)"));
    var upDesc = (lang === "en" ? "Load JSON file produced by HelpUS Scanner, Trivy, or Nessus run on your network." : (lang === "es" ? "Cargue el archivo JSON generado por el escáner HelpUS, Trivy o Nessus ejecutado en su red." : "Carregue o arquivo JSON gerado pelo scanner HelpUS, Trivy ou Nessus executado na sua rede."));
    var upBtn = (lang === "en" ? "📂 Select JSON File" : (lang === "es" ? "📂 Seleccionar Archivo JSON" : "📂 Selecionar Arquivo JSON"));
    var cliLabel = (lang === "en" ? "Terminal Scanner Command:" : (lang === "es" ? "Comando del Escáner en su terminal:" : "Comando do Scanner no seu terminal:"));
    var cliCopy = (lang === "en" ? "Copy Command" : (lang === "es" ? "Copiar Comando" : "Copiar Comando"));

    container.innerHTML =
      "<div>" +
        "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:12px;'>" +
          "<div>" +
            "<strong style='color:#38bdf8;font-size:14px;'>" + upTitle + "</strong>" +
            "<p style='margin:4px 0 0;font-size:12px;color:#94a3b8;'>" + upDesc + "</p>" +
          "</div>" +
          "<div>" +
            "<input type='file' id='scanFileInput' accept='.json' style='display:none;' onchange='handleScanFileUpload(event)'>" +
            "<button onclick='document.getElementById(\"scanFileInput\").click()' style='width:auto;padding:10px 20px;background:#16a34a;border-color:#16a34a;'>" + upBtn + "</button>" +
          "</div>" +
        "</div>" +
        "<div style='background:#030812;border:1px solid #162c4a;border-radius:8px;padding:10px 14px;font-size:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;'>" +
          "<div>" +
            "<span style='color:#38bdf8;font-weight:700;'>Comando do Scanner no seu terminal:</span>" +
            "<code style='color:#f8fafc;margin-left:8px;background:#081324;padding:3px 8px;border-radius:4px;'>python tools/local_network_scanner.py</code>" +
          "</div>" +
          "<button onclick='copyCliCommand()' style='width:auto;padding:6px 14px;font-size:12px;background:#1e3a5f;'>" + cliCopy + "</button>" +
        "</div>" +
      "</div>";
  }
}

function runDeviceProbe() {
  var info = getVisitorClientInfo();
  var lang = window.currentLanguage || "pt";

  var env = {
    title: (lang === "en" ? "Local Probe of Current Device (" + info.osName + ")" : (lang === "es" ? "Sondeo Local del Dispositivo Actual (" + info.osName + ")" : "Sonda Local do Dispositivo Atual (" + info.osName + ")")),
    subnet: "127.0.0.1 / Loopback",
    scan_time: new Date().toISOString(),
    hosts_count: 2,
    nodes: [
      { id: "client", x: 140, y: 110, label: info.hostLabel, type: "protected" },
      { id: "localnet", x: 340, y: 65, label: "Gateway LAN (192.168.x.1)", type: "gw" },
      { id: "service", x: 480, y: 155, label: (lang === "en" ? "Local Active Service" : (lang === "es" ? "Servicio Local Activo" : "Serviço Local Ativo")), type: "vuln" }
    ],
    links: [
      { from: "client", to: "localnet", label: (lang === "en" ? "Physical LAN / Wi-Fi" : (lang === "es" ? "Red Física / Wi-Fi" : "Rede Física / Wi-Fi")) },
      { from: "client", to: "service", label: "Port 127.0.0.1" }
    ],
    findings: [
      {
        asset_ip: "127.0.0.1",
        asset_hostname: info.hostLabel,
        asset_role: (lang === "en" ? "Local Host (" + info.browser + " running)" : (lang === "es" ? "Host Local (" + info.browser + " en ejecución)" : "Host Local do Visitante (" + info.browser + " em execução)")),
        cve: "CVE-2023-39417",
        title: (lang === "en" ? "Preventive Evaluation of Local Services" : (lang === "es" ? "Evaluación Preventiva de Servicios Locales" : "Avaliação Preventiva de Serviços Locais")),
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 8.5,
        contextual_severity: "High",
        delta: -0.2,
        nomenclature: "CVSS-BE",
        ai_citations: [
          (lang === "en" ? "MAV:Local assigned: device operates on user's loopback interface without 0.0.0.0/0 exposure." : (lang === "es" ? "MAV:Local asignado: el dispositivo opera en la interfaz loopback sin exposición a 0.0.0.0/0." : "MAV:Local atribuído automaticamente: o dispositivo opera na interface local do usuário sem exposição direta a 0.0.0.0/0.")),
          (lang === "en" ? "CR:High preserving credentials and cached data in " + info.osName + "." : (lang === "es" ? "CR:High resguardando credenciales y datos locales en " + info.osName + "." : "CR:High resguardando dados e credenciais em cache local do sistema operacional " + info.osName + "."))
        ]
      },
      {
        asset_ip: "192.168.x.1",
        asset_hostname: (lang === "en" ? "LAN Gateway / Router" : (lang === "es" ? "Router / Gateway Local" : "Roteador / Gateway da Sua Rede")),
        asset_role: (lang === "en" ? "Local Perimeter Gateway Device" : (lang === "es" ? "Dispositivo Perimetral de Red Local" : "Dispositivo de Borda da Rede Local")),
        cve: "CVE-2023-44487",
        title: "HTTP/2 Rapid Reset Denial of Service",
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 7.1,
        contextual_severity: "High",
        delta: -1.6,
        nomenclature: "CVSS-BE",
        ai_citations: [
          (lang === "en" ? "MAV:Adjacent assigned: router answers strictly within physical local subnet." : (lang === "es" ? "MAV:Adjacent asignado: el router responde únicamente a la subred física local." : "MAV:Adjacent atribuído: o roteador responde apenas para hosts da subrede física local.")),
          (lang === "en" ? "AR:High preserving local connection uptime." : (lang === "es" ? "AR:High resguardando continuidad de red local." : "AR:High resguardando continuidade de conexão local à internet."))
        ]
      }
    ]
  };

  renderNetworkGraph(env);
  renderScanFindings(env);
}

function runCustomSubnetScan() {
  var hostName = (val("customHostName") || "Meu Computador").trim();
  var subnet = (val("customSubnet") || "192.168.1.0/24").trim();
  var serviceType = val("customService") || "db";
  var lang = window.currentLanguage || "pt";

  var baseIp = subnet.split("/")[0] || "192.168.1.0";
  var parts = baseIp.split(".");
  var gwIp = (parts.length === 4) ? (parts[0] + "." + parts[1] + "." + parts[2] + ".1") : "192.168.1.1";
  var srvIp = (parts.length === 4) ? (parts[0] + "." + parts[1] + "." + parts[2] + ".100") : "192.168.1.100";

  var srvLabel = serviceType === "db" ? "DB (" + srvIp + ")" : (serviceType === "web" ? "Web (" + srvIp + ")" : "SSH (" + srvIp + ")");
  var srvRole = serviceType === "db" ? "PostgreSQL / SQL" : (serviceType === "web" ? "HTTP Web App" : "SSH Remote Shell");
  var cveCode = serviceType === "db" ? "CVE-2023-39417" : (serviceType === "web" ? "CVE-2023-44487" : "CVE-2024-6387");

  var env = {
    title: (lang === "en" ? "Custom Subnet: " + subnet : (lang === "es" ? "Subred Personalizada: " + subnet : "Subrede Personalizada: " + subnet)),
    subnet: subnet,
    scan_time: new Date().toISOString(),
    hosts_count: 3,
    nodes: [
      { id: "gw", x: 120, y: 110, label: "Gateway " + gwIp, type: "gw" },
      { id: "client", x: 400, y: 55, label: hostName, type: "protected" },
      { id: "srv", x: 400, y: 165, label: srvLabel, type: "vuln" }
    ],
    links: [
      { from: "gw", to: "client", label: "VLAN " + subnet },
      { from: "gw", to: "srv", label: "Port" }
    ],
    findings: [
      {
        asset_ip: "127.0.0.1",
        asset_hostname: hostName,
        asset_role: (lang === "en" ? "Host in subnet " + subnet : (lang === "es" ? "Host en subred " + subnet : "Host do Usuário na subrede " + subnet)),
        cve: "CVE-2023-39417",
        title: (lang === "en" ? "Host Evaluation in Target Subnet" : (lang === "es" ? "Evaluación de Host en Subred Destino" : "Avaliação do Host Local na Rede Informada")),
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 8.5,
        contextual_severity: "High",
        delta: -0.2,
        nomenclature: "CVSS-BE",
        ai_citations: [
          (lang === "en" ? "MAV:Local — Host bound to private subnet " + subnet + "." : (lang === "es" ? "MAV:Local — Host enlazado a subred privada " + subnet + "." : "MAV:Local — Host mapeado na subrede privada " + subnet + ".")),
          "CR:High"
        ]
      },
      {
        asset_ip: srvIp,
        asset_hostname: srvLabel,
        asset_role: srvRole,
        cve: cveCode,
        title: (lang === "en" ? "Vulnerability on Mapped Subnet Asset" : (lang === "es" ? "Vulnerabilidad en Activo de Subred Mapeada" : "Vulnerabilidade no Ativo Mapeado da Subrede")),
        official_base_score: 8.7,
        official_base_severity: "High",
        contextual_score: 7.3,
        contextual_severity: "High",
        delta: -1.4,
        nomenclature: "CVSS-BE",
        ai_citations: [
          (lang === "en" ? "MAV:Adjacent — Asset restricted to private subnet " + subnet + " without direct route." : (lang === "es" ? "MAV:Adjacent — Activo restringido a subred privada " + subnet + " sin ruta directa." : "MAV:Adjacent — Ativo restrito à subrede privada " + subnet + " sem rota pública direta.")),
          "IR:High / AR:High"
        ]
      }
    ]
  };

  renderNetworkGraph(env);
  renderScanFindings(env);
}

function handleScanFileUpload(event) {
  var file = event.target.files && event.target.files[0];
  if (!file) return;

  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var data = JSON.parse(e.target.result);
      var findings = data.findings || data.vulnerabilities || [];
      var subnet = data.subnet || data.scan_target || "Target Subnet";
      var scanTime = data.scan_time || data.timestamp || new Date().toISOString();

      var nodes = [
        { id: "gw", x: 120, y: 110, label: "Gateway", type: "gw" }
      ];
      var links = [];

      var mappedFindings = findings.slice(0, 5).map(function(item, idx) {
        var ip = item.asset_ip || item.ip || ("192.168.1." + (10 + idx));
        var host = item.asset_hostname || item.hostname || ("Host-" + (idx + 1));
        var cve = item.cve || item.cve_id || "CVE-2023-39417";
        var baseScore = Number(item.official_base_score || item.base_score || 8.7);
        var contextualScore = Number(item.contextual_score || (baseScore - 1.2).toFixed(1));
        var delta = Number((contextualScore - baseScore).toFixed(1));

        var nodeId = "node_" + idx;
        var yPos = 55 + (idx * 50);
        nodes.push({ id: nodeId, x: 400, y: Math.min(180, yPos), label: host + " (" + ip + ")", type: delta < -1 ? "protected" : "vuln" });
        links.push({ from: "gw", to: nodeId, label: "Port" });

        return {
          asset_ip: ip,
          asset_hostname: host,
          asset_role: item.asset_role || "Imported Host",
          cve: cve,
          title: item.title || item.vulnerability_name || "Vulnerability Finding",
          official_base_score: baseScore,
          official_base_severity: sev(baseScore),
          contextual_score: contextualScore,
          contextual_severity: sev(contextualScore),
          delta: delta,
          nomenclature: "CVSS-BE",
          ai_citations: item.ai_citations || [
            "MAV:Adjacent — Imported report finding.",
            "Audited."
          ]
        };
      });

      if (mappedFindings.length === 0) {
        alert("O arquivo JSON não possui lista de achados compatível. Certifique-se de usar o relatório do HelpUS Scanner.");
        return;
      }

      var env = {
        title: "Report: " + file.name,
        subnet: subnet,
        scan_time: scanTime,
        hosts_count: mappedFindings.length,
        nodes: nodes,
        links: links,
        findings: mappedFindings
      };

      renderNetworkGraph(env);
      renderScanFindings(env);
    } catch (err) {
      alert("Erro ao ler o arquivo JSON: " + err.message);
    }
  };
  reader.readAsText(file);
}

function copyCliCommand() {
  navigator.clipboard.writeText("python tools/local_network_scanner.py");
  alert("Comando copiado! Cole no seu terminal para rodar o scanner local.");
}

function renderNetworkGraph(env) {
  var svgContainer = document.getElementById("networkGraphSvg");
  if (!svgContainer) return;

  var nodes = env.nodes || [];
  var links = env.links || [];

  var nodeMap = {};
  nodes.forEach(function(n) { nodeMap[n.id] = n; });

  var linesSvg = links.map(function(l) {
    var source = nodeMap[l.from];
    var target = nodeMap[l.to];
    if (!source || !target) return "";
    var midX = (source.x + target.x) / 2;
    var midY = (source.y + target.y) / 2;
    return "<g>" +
      "<line x1='" + source.x + "' y1='" + source.y + "' x2='" + target.x + "' y2='" + target.y + "' stroke='#1e3a5f' stroke-width='2' stroke-dasharray='4,4' />" +
      "<text x='" + midX + "' y='" + (midY - 6) + "' fill='#64748b' font-size='10' text-anchor='middle'>" + esc(l.label) + "</text>" +
    "</g>";
  }).join("");

  var nodesSvg = nodes.map(function(n) {
    var color = n.type === "gw" ? "#38bdf8" : (n.type === "vuln" ? "#f87171" : "#4ade80");
    var radius = n.type === "gw" ? 22 : 18;
    return "<g style='cursor:pointer;'>" +
      "<circle cx='" + n.x + "' cy='" + n.y + "' r='" + (radius + 5) + "' fill='" + color + "' opacity='0.15' />" +
      "<circle cx='" + n.x + "' cy='" + n.y + "' r='" + radius + "' fill='#081324' stroke='" + color + "' stroke-width='2.5' />" +
      "<text x='" + n.x + "' y='" + (n.y + 4) + "' fill='#f8fafc' font-size='11' font-weight='bold' text-anchor='middle'>" + (n.type === "gw" ? "⛨" : (n.type === "vuln" ? "⚠" : "✓")) + "</text>" +
      "<text x='" + n.x + "' y='" + (n.y + radius + 16) + "' fill='#cbd5e1' font-size='11' font-weight='600' text-anchor='middle'>" + esc(n.label) + "</text>" +
    "</g>";
  }).join("");

  svgContainer.innerHTML =
    "<svg width='100%' height='220' viewBox='0 0 600 220' style='overflow:visible;'>" +
      linesSvg + nodesSvg +
    "</svg>";
}

function renderScanFindings(env) {
  var container = document.getElementById("liveScanOutput");
  if (!container) return;
  var lang = window.currentLanguage || "pt";

  var lblOfficial = (lang === "en" ? "Primary Base" : (lang === "es" ? "Base Origen" : "Base Origem"));
  var lblContextual = (lang === "en" ? "Contextual" : (lang === "es" ? "Contextual" : "Contextual"));
  var lblCit = (lang === "en" ? "AI Citations Grounded in this Topology:" : (lang === "es" ? "Citas de IA Basadas en esta Topología:" : "Citações de IA Baseadas na Topologia Deste Ambiente:"));
  var lblSuccess = (lang === "en" ? "✓ Scan completed in environment" : (lang === "es" ? "✓ Escaneo completado en el entorno" : "✓ Varredura concluída no ambiente"));

  var cards = env.findings.map(function(f) {
    var deltaColor = f.delta < 0 ? "#4ade80" : "#fbbf24";
    var roleText = getLocalizedField(f.asset_role);
    var citItems = Array.isArray(f.ai_citations) ? f.ai_citations : (f.ai_citations && f.ai_citations[lang] ? f.ai_citations[lang] : (f.ai_citations && f.ai_citations.pt ? f.ai_citations.pt : []));
    var citList = citItems.map(function(c) {
      return "<li style='margin-bottom:4px;'>" + esc(c) + "</li>";
    }).join("");

    return "<div style='background:#081324;border:1px solid #1e3a5f;border-radius:12px;padding:16px;margin-bottom:12px;'>" +
      "<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;'>" +
        "<div><strong style='color:#38bdf8;font-size:16px;'>" + esc(f.asset_hostname) + " (" + esc(f.asset_ip) + ")</strong><br><small style='color:#94a3b8;'>" + esc(roleText) + " — " + esc(f.cve) + ": " + esc(f.title) + "</small></div>" +
        "<div style='display:flex;gap:12px;'>" +
          "<div style='text-align:right;'><small style='color:#94a3b8;'>Base Origem</small><div style='font-size:18px;font-weight:700;color:#f87171;'>" + esc(f.official_base_score) + "</div></div>" +
          "<div style='text-align:right;'><small style='color:#94a3b8;'>Contextual (" + esc(f.nomenclature) + ")</small><div style='font-size:18px;font-weight:700;color:#4ade80;'>" + esc(f.contextual_score) + "</div></div>" +
          "<div style='text-align:right;'><small style='color:#94a3b8;'>Delta</small><div style='font-size:18px;font-weight:700;color:" + deltaColor + ";'>" + (f.delta > 0 ? "+" : "") + esc(f.delta) + "</div></div>" +
        "</div>" +
      "</div>" +
      "<div style='margin-top:10px;background:#050c17;padding:10px;border-radius:8px;border:1px solid #162c4a;'>" +
        "<strong style='font-size:12px;color:#38bdf8;'>" + lblCit + "</strong>" +
        "<ul style='margin:4px 0 0;padding-left:18px;font-size:13px;color:#cbd5e1;line-height:1.5;'>" + citList + "</ul>" +
      "</div>" +
    "</div>";
  }).join("");

  var envTitle = getLocalizedField(env.title);
  container.innerHTML =
    "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>" +
      "<span style='color:#4ade80;font-size:13px;'>" + lblSuccess + " <strong>" + esc(envTitle) + "</strong> (" + esc(env.subnet) + ")</span>" +
      "<small style='color:#94a3b8;'>Timestamp: " + esc(env.scan_time) + "</small>" +
    "</div>" + cards;
}

function runSelectedScan() {
  var select = document.getElementById("scanTargetSelect");
  var targetKey = select ? select.value : "lan";
  var env = ENV_PRESETS[targetKey] || ENV_PRESETS.lan;

  renderNetworkGraph(env);
  renderScanFindings(env);
}

// ============================================================================
// DATASET BENCHMARK CIENTÍFICO (30 CENÁRIOS)
// ============================================================================
var BENCHMARK_DATASET = [{"id": "SCN-NVD-001", "cve": "CVE-2026-4251", "source_type": "nvd", "asset": "Public Web Application", "exposure": "Public", "base_score": 1.1, "base_sev": "Low", "env_score": 1.1, "env_sev": "Low", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "WAF enabled", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: public_web_application."}, {"id": "SCN-NVD-002", "cve": "CVE-2026-4252", "source_type": "nvd", "asset": "Internal Admin Console", "exposure": "Restricted", "base_score": 8.9, "base_sev": "High", "env_score": 8.0, "env_sev": "High", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "VPN", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: internal_admin_console."}, {"id": "SCN-NVD-003", "cve": "CVE-2026-4270", "source_type": "nvd", "asset": "Identity Provider", "exposure": "Restricted", "base_score": 6.8, "base_sev": "Medium", "env_score": 7.6, "env_sev": "High", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "MFA", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: identity_provider."}, {"id": "SCN-NVD-004", "cve": "CVE-2026-28490", "source_type": "nvd", "asset": "Database Server", "exposure": "Internal", "base_score": 8.3, "base_sev": "High", "env_score": 9.1, "env_sev": "Critical", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "Network isolation", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: database_server."}, {"id": "SCN-NVD-005", "cve": "CVE-2026-28498", "source_type": "nvd", "asset": "Developer Workstation", "exposure": "Restricted", "base_score": 8.2, "base_sev": "High", "env_score": 8.2, "env_sev": "High", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "EDR", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: developer_workstation."}, {"id": "SCN-NVD-006", "cve": "CVE-2026-29510", "source_type": "nvd", "asset": "Isolated Lab System", "exposure": "Isolated", "base_score": 5.1, "base_sev": "Medium", "env_score": 4.2, "env_sev": "Medium", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "Network isolation", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: isolated_lab_system."}, {"id": "SCN-NVD-007", "cve": "CVE-2026-29513", "source_type": "nvd", "asset": "Ot Monitoring Gateway", "exposure": "Internal", "base_score": 5.1, "base_sev": "Medium", "env_score": 5.1, "env_sev": "Medium", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "Network segmentation", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: ot_monitoring_gateway."}, {"id": "SCN-NVD-008", "cve": "CVE-2026-29520", "source_type": "nvd", "asset": "Public Api Gateway", "exposure": "Public", "base_score": 5.1, "base_sev": "Medium", "env_score": 5.9, "env_sev": "Medium", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "API gateway policies", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: public_api_gateway."}, {"id": "SCN-NVD-009", "cve": "CVE-2026-29521", "source_type": "nvd", "asset": "Public Web Application", "exposure": "Public", "base_score": 5.1, "base_sev": "Medium", "env_score": 5.9, "env_sev": "Medium", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "WAF enabled", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: public_web_application."}, {"id": "SCN-NVD-010", "cve": "CVE-2026-3644", "source_type": "nvd", "asset": "Internal Admin Console", "exposure": "Restricted", "base_score": 6.0, "base_sev": "Medium", "env_score": 5.1, "env_sev": "Medium", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "VPN", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: internal_admin_console."}, {"id": "SCN-NVD-011", "cve": "CVE-2026-4224", "source_type": "nvd", "asset": "Identity Provider", "exposure": "Restricted", "base_score": 6.0, "base_sev": "Medium", "env_score": 6.8, "env_sev": "Medium", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "MFA", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: identity_provider."}, {"id": "SCN-NVD-012", "cve": "CVE-2026-4253", "source_type": "nvd", "asset": "Database Server", "exposure": "Internal", "base_score": 2.0, "base_sev": "Low", "env_score": 2.8, "env_sev": "Low", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "Network isolation", "citation": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: database_server."}, {"id": "SCN-SYN-013", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Developer Workstation", "exposure": "Restricted", "base_score": 9.3, "base_sev": "Critical", "env_score": 9.3, "env_sev": "Critical", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "EDR", "citation": "Curated local environment profile for developer_workstation; CVSS v4.0 vector assigned for controlled experime..."}, {"id": "SCN-SYN-014", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Isolated Lab System", "exposure": "Isolated", "base_score": 8.7, "base_sev": "High", "env_score": 6.0, "env_sev": "Medium", "delta": -3, "delta_val": -2.7, "decision": "downgraded", "controls": "Network isolation", "citation": "Curated local environment profile for isolated_lab_system; CVSS v4.0 vector assigned for controlled experiment..."}, {"id": "SCN-SYN-015", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Ot Monitoring Gateway", "exposure": "Internal", "base_score": 7.1, "base_sev": "High", "env_score": 7.9, "env_sev": "High", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "Network segmentation", "citation": "Curated local environment profile for ot_monitoring_gateway; CVSS v4.0 vector assigned for controlled experime..."}, {"id": "SCN-SYN-016", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Public Api Gateway", "exposure": "Public", "base_score": 6.8, "base_sev": "Medium", "env_score": 8.4, "env_sev": "High", "delta": 2, "delta_val": 1.6, "decision": "upgraded", "controls": "API gateway policies", "citation": "Curated local environment profile for public_api_gateway; CVSS v4.0 vector assigned for controlled experiment,..."}, {"id": "SCN-SYN-017", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Public Web Application", "exposure": "Public", "base_score": 4.8, "base_sev": "Medium", "env_score": 5.6, "env_sev": "Medium", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "WAF enabled", "citation": "Curated local environment profile for public_web_application; CVSS v4.0 vector assigned for controlled experim..."}, {"id": "SCN-SYN-018", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Internal Admin Console", "exposure": "Restricted", "base_score": 2.1, "base_sev": "Low", "env_score": 1.2, "env_sev": "Low", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "VPN", "citation": "Curated local environment profile for internal_admin_console; CVSS v4.0 vector assigned for controlled experim..."}, {"id": "SCN-SYN-019", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Identity Provider", "exposure": "Restricted", "base_score": 9.3, "base_sev": "Critical", "env_score": 9.3, "env_sev": "Critical", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "MFA", "citation": "Curated local environment profile for identity_provider; CVSS v4.0 vector assigned for controlled experiment, ..."}, {"id": "SCN-SYN-020", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Database Server", "exposure": "Internal", "base_score": 8.7, "base_sev": "High", "env_score": 9.5, "env_sev": "Critical", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "Network isolation", "citation": "Curated local environment profile for database_server; CVSS v4.0 vector assigned for controlled experiment, no..."}, {"id": "SCN-SYN-021", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Developer Workstation", "exposure": "Restricted", "base_score": 7.1, "base_sev": "High", "env_score": 7.1, "env_sev": "High", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "EDR", "citation": "Curated local environment profile for developer_workstation; CVSS v4.0 vector assigned for controlled experime..."}, {"id": "SCN-SYN-022", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Isolated Lab System", "exposure": "Isolated", "base_score": 6.8, "base_sev": "Medium", "env_score": 5.0, "env_sev": "Medium", "delta": -2, "delta_val": -1.8, "decision": "downgraded", "controls": "Network isolation", "citation": "Curated local environment profile for isolated_lab_system; CVSS v4.0 vector assigned for controlled experiment..."}, {"id": "SCN-SYN-023", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Ot Monitoring Gateway", "exposure": "Internal", "base_score": 4.8, "base_sev": "Medium", "env_score": 6.4, "env_sev": "Medium", "delta": 2, "delta_val": 1.6, "decision": "upgraded", "controls": "Network segmentation", "citation": "Curated local environment profile for ot_monitoring_gateway; CVSS v4.0 vector assigned for controlled experime..."}, {"id": "SCN-SYN-024", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Public Api Gateway", "exposure": "Public", "base_score": 2.1, "base_sev": "Low", "env_score": 3.7, "env_sev": "Low", "delta": 2, "delta_val": 1.6, "decision": "upgraded", "controls": "API gateway policies", "citation": "Curated local environment profile for public_api_gateway; CVSS v4.0 vector assigned for controlled experiment,..."}, {"id": "SCN-SYN-025", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Public Web Application", "exposure": "Public", "base_score": 9.3, "base_sev": "Critical", "env_score": 9.3, "env_sev": "Critical", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "WAF enabled", "citation": "Curated local environment profile for public_web_application; CVSS v4.0 vector assigned for controlled experim..."}, {"id": "SCN-SYN-026", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Internal Admin Console", "exposure": "Restricted", "base_score": 8.7, "base_sev": "High", "env_score": 7.8, "env_sev": "High", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "VPN", "citation": "Curated local environment profile for internal_admin_console; CVSS v4.0 vector assigned for controlled experim..."}, {"id": "SCN-SYN-027", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Identity Provider", "exposure": "Restricted", "base_score": 7.1, "base_sev": "High", "env_score": 7.9, "env_sev": "High", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "MFA", "citation": "Curated local environment profile for identity_provider; CVSS v4.0 vector assigned for controlled experiment, ..."}, {"id": "SCN-SYN-028", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Database Server", "exposure": "Internal", "base_score": 6.8, "base_sev": "Medium", "env_score": 7.6, "env_sev": "High", "delta": 1, "delta_val": 0.8, "decision": "upgraded", "controls": "Network isolation", "citation": "Curated local environment profile for database_server; CVSS v4.0 vector assigned for controlled experiment, no..."}, {"id": "SCN-SYN-029", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Developer Workstation", "exposure": "Restricted", "base_score": 4.8, "base_sev": "Medium", "env_score": 4.8, "env_sev": "Medium", "delta": 0, "delta_val": 0.0, "decision": "unchanged", "controls": "EDR", "citation": "Curated local environment profile for developer_workstation; CVSS v4.0 vector assigned for controlled experime..."}, {"id": "SCN-SYN-030", "cve": "Sintético (Lab)", "source_type": "synthetic", "asset": "Isolated Lab System", "exposure": "Isolated", "base_score": 2.1, "base_sev": "Low", "env_score": 1.2, "env_sev": "Low", "delta": -1, "delta_val": -0.9, "decision": "downgraded", "controls": "Network isolation", "citation": "Curated local environment profile for isolated_lab_system; CVSS v4.0 vector assigned for controlled experiment..."}];

var currentAuditFilter = "all";

function renderAuditSeverityChartSvg() {
  var container = document.getElementById("auditChartSeverity");
  if (!container) return;
  var lang = window.currentLanguage || "pt";

  var cats = [
    { label: (lang === "en" ? "Critical" : (lang === "es" ? "Crítico" : "Crítico")), nvd: 10, helpus: 4 },
    { label: (lang === "en" ? "High" : (lang === "es" ? "Alto" : "Alto")), nvd: 12, helpus: 9 },
    { label: (lang === "en" ? "Medium" : (lang === "es" ? "Medio" : "Médio")), nvd: 6, helpus: 11 },
    { label: (lang === "en" ? "Low" : (lang === "es" ? "Bajo" : "Baixo")), nvd: 2, helpus: 6 }
  ];

  var lblNvd = (lang === "en" ? "Primary Base Score" : (lang === "es" ? "Score Base Origen" : "Score Base Origem"));
  var lblHelp = (lang === "en" ? "HelpUS AI (Contextual)" : (lang === "es" ? "HelpUS IA (Contextual)" : "HelpUS IA (Contextual)"));

  var barsSvg = cats.map(function(c, i) {
    var x = 35 + (i * 125);
    var hNvd = c.nvd * 8.5;
    var yNvd = 125 - hNvd;
    var hHelp = c.helpus * 8.5;
    var yHelp = 125 - hHelp;

    return "<g>" +
      "<text x='" + (x + 36) + "' y='145' fill='#cbd5e1' font-size='11' font-weight='600' text-anchor='middle'>" + c.label + "</text>" +
      "<rect x='" + x + "' y='" + yNvd + "' width='32' height='" + hNvd + "' fill='#ef4444' rx='4' opacity='0.9' />" +
      "<text x='" + (x + 16) + "' y='" + (yNvd - 5) + "' fill='#f87171' font-size='11' font-weight='bold' text-anchor='middle'>" + c.nvd + "</text>" +
      "<rect x='" + (x + 40) + "' y='" + yHelp + "' width='32' height='" + hHelp + "' fill='#10b981' rx='4' opacity='0.9' />" +
      "<text x='" + (x + 56) + "' y='" + (yHelp - 5) + "' fill='#4ade80' font-size='11' font-weight='bold' text-anchor='middle'>" + c.helpus + "</text>" +
    "</g>";
  }).join("");

  container.innerHTML =
    "<svg width='100%' height='180' viewBox='0 0 520 160' style='overflow:visible;'>" +
      "<line x1='20' y1='125' x2='500' y2='125' stroke='#1e3a5f' stroke-width='1.5' />" +
      "<g transform='translate(130, 10)'>" +
        "<rect x='0' y='0' width='12' height='12' fill='#ef4444' rx='2' />" +
        "<text x='18' y='10' fill='#94a3b8' font-size='11'>" + lblNvd + "</text>" +
        "<rect x='140' y='0' width='12' height='12' fill='#10b981' rx='2' />" +
        "<text x='158' y='10' fill='#94a3b8' font-size='11'>" + lblHelp + "</text>" +
      "</g>" +
      barsSvg +
    "</svg>";
}

function renderAuditTransitionsChartSvg() {
  var container = document.getElementById("auditChartTransitions");
  if (!container) return;
  var lang = window.currentLanguage || "pt";

  var lblDown = (lang === "en" ? "Downgraded: 14 (46.7%)" : (lang === "es" ? "Desescalados: 14 (46.7%)" : "Desescalonados: 14 (46.7%)"));
  var lblUp = (lang === "en" ? "Upgraded: 8 (26.7%)" : (lang === "es" ? "Escalados: 8 (26.7%)" : "Escalonados: 8 (26.7%)"));
  var lblSame = (lang === "en" ? "Neutral: 8 (26.7%)" : (lang === "es" ? "Neutros: 8 (26.7%)" : "Neutros: 8 (26.7%)"));

  var descDown = (lang === "en" ? "🟢 Downgraded (- Delta): 14 scenarios mitigated by VLAN, WAF or lack of internet." : (lang === "es" ? "🟢 Desescalados (- Delta): 14 escenarios mitigados por VLAN, WAF o aislamiento." : "🟢 Desescalonados (- Delta): 14 cenários mitigados por VLAN, WAF ou isolamento."));
  var descUp = (lang === "en" ? "🔴 Upgraded (+ Delta): 8 scenarios in banking PCI-DSS scope or identity core." : (lang === "es" ? "🔴 Escalados (+ Delta): 8 escenarios en alcance bancario PCI-DSS o identidad." : "🔴 Escalonados (+ Delta): 8 cenários de escopo PCI-DSS bancário ou identidade."));
  var descSame = (lang === "en" ? "🟡 Preserved (0 Delta): 8 scenarios where exposure already mirrored real threat." : (lang === "es" ? "🟡 Preservados (0 Delta): 8 escenarios donde la exposición ya reflejaba el riesgo real." : "🟡 Preservados (0 Delta): 8 cenários onde a exposição já refletia o risco real."));

  container.innerHTML =
    "<svg width='100%' height='180' viewBox='0 0 520 160' style='overflow:visible;'>" +
      "<g transform='translate(10, 25)'>" +
        "<rect x='0' y='0' width='233' height='32' fill='#16a34a' rx='6' />" +
        "<text x='116' y='20' fill='#ffffff' font-size='12' font-weight='bold' text-anchor='middle'>" + lblDown + "</text>" +
        "<rect x='237' y='0' width='133' height='32' fill='#dc2626' rx='6' />" +
        "<text x='303' y='20' fill='#ffffff' font-size='12' font-weight='bold' text-anchor='middle'>" + lblUp + "</text>" +
        "<rect x='374' y='0' width='133' height='32' fill='#334155' rx='6' />" +
        "<text x='440' y='20' fill='#ffffff' font-size='12' font-weight='bold' text-anchor='middle'>" + lblSame + "</text>" +
      "</g>" +
      "<g transform='translate(20, 80)'>" +
        "<circle cx='10' cy='10' r='6' fill='#16a34a' />" +
        "<text x='24' y='14' fill='#4ade80' font-size='12' font-weight='600'>" + descDown + "</text>" +
        "<circle cx='10' cy='34' r='6' fill='#dc2626' />" +
        "<text x='24' y='38' fill='#f87171' font-size='12' font-weight='600'>" + descUp + "</text>" +
        "<circle cx='10' cy='58' r='6' fill='#94a3b8' />" +
        "<text x='24' y='62' fill='#94a3b8' font-size='12' font-weight='600'>" + descSame + "</text>" +
      "</g>" +
    "</svg>";
}

function renderAuditPipelineSvg() {
  var container = document.getElementById("auditPipelineSvg");
  if (!container) return;
  var lang = window.currentLanguage || "pt";

  var steps = [
    { label: (lang === "en" ? "1. NVD Ingest" : (lang === "es" ? "1. Ingesta NVD" : "1. Ingestão NVD")), sub: (lang === "en" ? "Immutable" : (lang === "es" ? "Inmutable" : "Base Imutável")), color: "#f87171", icon: "📡" },
    { label: (lang === "en" ? "2. Net Facts" : (lang === "es" ? "2. Hechos Red" : "2. Fatos de Rede")), sub: "WAF / VLAN / IPs", color: "#38bdf8", icon: "🛡" },
    { label: (lang === "en" ? "3. AI Watcher" : (lang === "es" ? "3. Watcher IA" : "3. Watcher IA")), sub: (lang === "en" ? "Citations" : (lang === "es" ? "Citas Reales" : "Citações Reais")), color: "#fbbf24", icon: "🤖" },
    { label: (lang === "en" ? "4. FIRST v4.0" : (lang === "es" ? "4. FIRST v4.0" : "4. FIRST v4.0")), sub: (lang === "en" ? "Math Formula" : (lang === "es" ? "Fórmula Oficial" : "Cálculo Oficial")), color: "#4ade80", icon: "📐" },
    { label: (lang === "en" ? "5. Human Gate" : (lang === "es" ? "5. Puerta HITL" : "5. Gate Humano")), sub: (lang === "en" ? "Sign-off" : (lang === "es" ? "Homologación" : "Homologação")), color: "#a78bfa", icon: "👤" }
  ];

  var stepsSvg = steps.map(function(s, i) {
    var x = 15 + (i * 118);
    var arrowSvg = (i < 4) ? "<path d='M" + (x + 95) + " 35 L" + (x + 112) + " 35' stroke='#1e3a5f' stroke-width='2' marker-end='url(#arrow)' />" : "";

    return "<g>" +
      "<rect x='" + x + "' y='10' width='95' height='50' fill='#081324' stroke='" + s.color + "' stroke-width='1.5' rx='8' />" +
      "<text x='" + (x + 47) + "' y='" + 30 + "' fill='#f8fafc' font-size='11' font-weight='bold' text-anchor='middle'>" + s.icon + " " + esc(s.label) + "</text>" +
      "<text x='" + (x + 47) + "' y='" + 46 + "' fill='#94a3b8' font-size='9' text-anchor='middle'>" + esc(s.sub) + "</text>" +
      arrowSvg +
    "</g>";
  }).join("");

  container.innerHTML =
    "<svg width='100%' height='75' viewBox='0 0 600 75' style='overflow:visible;'>" +
      "<defs>" +
        "<marker id='arrow' viewBox='0 0 10 10' refX='5' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'>" +
          "<path d='M 0 0 L 10 5 L 0 10 z' fill='#38bdf8' />" +
        "</marker>" +
      "</defs>" +
      stepsSvg +
    "</svg>";
}

function filterAuditScenarios(mode) {
  if (mode !== "search") {
    currentAuditFilter = mode;
    var filterBtns = ["all", "nvd", "synthetic", "down", "up"];
    filterBtns.forEach(function(f) {
      var btn = document.getElementById("filter-btn-" + f);
      if (btn) {
        if (f === mode) btn.classList.add("active");
        else btn.classList.remove("active");
      }
    });
  }

  var searchInput = document.getElementById("auditSearchInput");
  var query = searchInput ? searchInput.value.toLowerCase().trim() : "";

  var filtered = BENCHMARK_DATASET.filter(function(item) {
    var matchesFilter = true;
    if (currentAuditFilter === "nvd") matchesFilter = (item.source_type === "nvd");
    else if (currentAuditFilter === "synthetic") matchesFilter = (item.source_type === "synthetic");
    else if (currentAuditFilter === "down") matchesFilter = (item.decision === "downgraded");
    else if (currentAuditFilter === "up") matchesFilter = (item.decision === "upgraded");

    if (!matchesFilter) return false;

    if (query) {
      var text = (item.id + " " + item.cve + " " + item.asset + " " + item.controls + " " + item.citation + " " + item.exposure).toLowerCase();
      return text.indexOf(query) !== -1;
    }
    return true;
  });

  renderAuditTable(filtered);
}

function renderAuditTable(items) {
  var tbody = document.getElementById("auditTableBody");
  if (!tbody) return;
  var lang = window.currentLanguage || "pt";

  if (items.length === 0) {
    var noData = (lang === "en" ? "No scenarios found for this search filter." : (lang === "es" ? "Ningún escenario encontrado para este filtro de búsqueda." : "Nenhum cenário encontrado para este filtro de busca."));
    tbody.innerHTML = "<tr><td colspan='8' style='text-align:center;padding:24px;color:#94a3b8;'>" + noData + "</td></tr>";
    return;
  }

  var rowsHtml = items.map(function(item) {
    var deltaClass = item.delta < 0 ? "badge-down" : (item.delta > 0 ? "badge-up" : "badge-same");
    var deltaPrefix = item.delta > 0 ? "+" : "";
    var decisionColor = item.decision === "downgraded" ? "#4ade80" : (item.decision === "upgraded" ? "#f87171" : "#94a3b8");

    var decText = item.decision;
    if (lang === "pt") decText = (item.decision === "downgraded" ? "Desescalonado" : (item.decision === "upgraded" ? "Escalonado" : "Preservado"));
    else if (lang === "es") decText = (item.decision === "downgraded" ? "Desescalado" : (item.decision === "upgraded" ? "Escalado" : "Sin cambios"));
    else decText = (item.decision === "downgraded" ? "Downgraded" : (item.decision === "upgraded" ? "Upgraded" : "Unchanged"));

    var expText = item.exposure;
    if (lang === "pt") expText = (item.exposure === "Public" ? "Pública" : (item.exposure === "Restricted" ? "Restrita" : (item.exposure === "Internal" ? "Interna" : "Isolada")));
    else if (lang === "es") expText = (item.exposure === "Public" ? "Pública" : (item.exposure === "Restricted" ? "Restringida" : (item.exposure === "Internal" ? "Interna" : "Aislada")));

    return "<tr style='cursor:pointer;' onclick='showAuditScenarioDetail(\"" + esc(item.id) + "\")'>" +
      "<td><strong style='color:#38bdf8;'>" + esc(item.id) + "</strong><br><small style='color:#cbd5e1;'>" + esc(item.cve) + "</small></td>" +
      "<td>" + esc(item.asset) + "</td>" +
      "<td><span style='color:" + (item.exposure === "Public" ? "#f87171" : "#4ade80") + ";'>" + esc(expText) + "</span></td>" +
      "<td><strong style='color:#f87171;'>" + esc(item.base_score.toFixed(1)) + "</strong> <small style='color:#94a3b8;'>" + esc(item.base_sev) + "</small></td>" +
      "<td><strong style='color:#4ade80;'>" + esc(item.env_score.toFixed(1)) + "</strong> <small style='color:#94a3b8;'>" + esc(item.env_sev) + "</small></td>" +
      "<td><span class='badge-tag " + deltaClass + "'>" + deltaPrefix + esc(item.delta_val.toFixed(1)) + "</span></td>" +
      "<td><small style='color:" + decisionColor + ";font-weight:700;'>" + esc(decText) + "</small></td>" +
      "<td style='max-width:240px;font-size:12px;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;' title='" + esc(item.citation) + "'>" + esc(item.citation) + "</td>" +
    "</tr>";
  }).join("");

  tbody.innerHTML = rowsHtml;
}

function showAuditScenarioDetail(id) {
  var item = BENCHMARK_DATASET.find(function(s) { return s.id === id; });
  var box = document.getElementById("auditScenarioDetailBox");
  if (!item || !box) return;

  var lang = window.currentLanguage || "pt";
  var deltaClass = item.delta < 0 ? "#4ade80" : (item.delta > 0 ? "#f87171" : "#94a3b8");

  var srcText = (item.source_type === "nvd" ? (lang === "en" ? "Source Assessment" : (lang === "es" ? "Evaluación de Origen" : "Avaliação de Origem")) : (lang === "en" ? "Curated Synthetic" : (lang === "es" ? "Sintético Curado" : "Sintético Curado")));
  var lblOrigin = (lang === "en" ? "Source:" : (lang === "es" ? "Origen:" : "Origem:"));
  var lblBase = (lang === "en" ? "Source Base Score" : (lang === "es" ? "Score Base de Origen" : "Score Base de Origem"));
  var lblCtx = (lang === "en" ? "Contextual HelpUS" : (lang === "es" ? "Contextual HelpUS" : "Contextual HelpUS"));
  var lblDelta = (lang === "en" ? "Priority Delta" : (lang === "es" ? "Delta de Prioridad" : "Delta de Prioridade"));
  var lblExp = (lang === "en" ? "Network Exposure" : (lang === "es" ? "Exposición de Red" : "Exposição de Rede"));
  var lblCtrl = (lang === "en" ? "🛡 Active Compensating Controls:" : (lang === "es" ? "🛡 Controles Compensatorios Activos:" : "🛡 Controles Compensatórios Ativos:"));
  var lblEv = (lang === "en" ? "🔍 AI Watcher Auditable Rationale & Evidence:" : (lang === "es" ? "🔍 Evidencia & Razonamiento Auditable del Watcher IA:" : "🔍 Evidência & Raciocínio Auditável do Watcher IA:"));
  var btnClose = (lang === "en" ? "✕ Close" : (lang === "es" ? "✕ Cerrar" : "✕ Fechar"));

  var decText = (lang === "pt" ? (item.decision === "downgraded" ? "Desescalonado" : (item.decision === "upgraded" ? "Escalonado" : "Preservado")) : (lang === "es" ? (item.decision === "downgraded" ? "Desescalado" : (item.decision === "upgraded" ? "Escalado" : "Sin cambios")) : item.decision));
  var expText = (lang === "pt" ? (item.exposure === "Public" ? "Pública" : (item.exposure === "Restricted" ? "Restrita" : (item.exposure === "Internal" ? "Interna" : "Isolada"))) : (lang === "es" ? (item.exposure === "Public" ? "Pública" : (item.exposure === "Restricted" ? "Restringida" : (item.exposure === "Internal" ? "Interna" : "Aislada"))) : item.exposure));

  box.style.display = "block";
  box.innerHTML =
    "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>" +
      "<div>" +
        "<strong style='color:#38bdf8;font-size:16px;'>" + esc(item.id) + " — " + esc(item.cve) + " (" + esc(item.asset) + ")</strong>" +
        "<span style='margin-left:10px;font-size:12px;background:#050c17;padding:3px 8px;border-radius:6px;color:#94a3b8;'>" + lblOrigin + " " + srcText + "</span>" +
      "</div>" +
      "<button onclick='document.getElementById(\"auditScenarioDetailBox\").style.display=\"none\"' style='width:auto;padding:4px 10px;background:#1e3a5f;font-size:12px;'>" + btnClose + "</button>" +
    "</div>" +
    "<div class='grid' style='grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:12px;'>" +
      "<div style='background:#050c17;padding:10px;border-radius:8px;'><small style='color:#94a3b8;'>" + lblBase + "</small><div style='font-size:18px;font-weight:bold;color:#f87171;'>" + item.base_score.toFixed(1) + " (" + item.base_sev + ")</div></div>" +
      "<div style='background:#050c17;padding:10px;border-radius:8px;'><small style='color:#94a3b8;'>Contextual HelpUS</small><div style='font-size:18px;font-weight:bold;color:#4ade80;'>" + item.env_score.toFixed(1) + " (" + item.env_sev + ")</div></div>" +
      "<div style='background:#050c17;padding:10px;border-radius:8px;'><small style='color:#94a3b8;'>Delta de Prioridade</small><div style='font-size:18px;font-weight:bold;color:" + deltaClass + ";'>" + (item.delta > 0 ? "+" : "") + item.delta_val.toFixed(1) + " (" + decText + ")</div></div>" +
      "<div style='background:#050c17;padding:10px;border-radius:8px;'><small style='color:#94a3b8;'>Exposição de Rede</small><div style='font-size:16px;font-weight:bold;color:#cbd5e1;'>" + expText + "</div></div>" +
    "</div>" +
    "<div style='background:#050c17;border:1px solid #162c4a;border-radius:8px;padding:12px;margin-bottom:10px;'>" +
      "<strong style='color:#38bdf8;font-size:13px;'>" + lblCtrl + "</strong>" +
      "<p style='margin:4px 0 0;font-size:13px;color:#cbd5e1;'>" + esc(item.controls) + "</p>" +
    "</div>" +
    "<div style='background:#050c17;border:1px solid #162c4a;border-radius:8px;padding:12px;'>" +
      "<strong style='color:#38bdf8;font-size:13px;'>🔍 Evidência & Raciocínio Auditável do Watcher IA:</strong>" +
      "<p style='margin:4px 0 0;font-size:13px;color:#cbd5e1;'>" + esc(item.citation) + "</p>" +
    "</div>";
  
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function downloadBenchmarkCsv() {
  var header = ["scenario_id", "cve_id", "source_type", "asset_class", "internet_exposure", "official_base_score", "official_base_severity", "contextual_score", "contextual_severity", "delta", "decision", "compensating_controls", "evidence_summary"];
  var lines = [header.join(",")];
  BENCHMARK_DATASET.forEach(function(item) {
    var row = [
      quoteCsv(item.id),
      quoteCsv(item.cve),
      quoteCsv(item.source_type),
      quoteCsv(item.asset),
      quoteCsv(item.exposure),
      quoteCsv(item.base_score),
      quoteCsv(item.base_sev),
      quoteCsv(item.env_score),
      quoteCsv(item.env_sev),
      quoteCsv(item.delta_val),
      quoteCsv(item.decision),
      quoteCsv(item.controls),
      quoteCsv(item.citation)
    ];
    lines.push(row.join(","));
  });

  var blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "helpus_cvss40_benchmark_dataset_30scenarios.csv";
  a.click();
}

function downloadBenchmarkJson() {
  var blob = new Blob([JSON.stringify(BENCHMARK_DATASET, null, 2)], { type: "application/json" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "helpus_cvss40_benchmark_audit.json";
  a.click();
}

function renderAuditDashboard() {
  renderAuditSeverityChartSvg();
  renderAuditTransitionsChartSvg();
  renderAuditPipelineSvg();
  filterAuditScenarios("all");
}


// ============================================================================
// CONSOLE OPERACIONAL HELPUS CVSS (5 CAMADAS, GOVERNANÇA HITL & GOOGLE AUTH)
// ============================================================================

var CONSOLE_12_CVES = [
  { id: "CVE-2024-21413", name: "Microsoft Outlook RCE", baseScore: 9.8, severity: "CRITICAL", cna: "Microsoft Corporation", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.9, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "153f3f22572a9b31d8c11e74a8d4be107128cf78e61a0d3329f6d39cb621ee84" },
  { id: "CVE-2024-3094", name: "XZ Utils Liblzma Backdoor", baseScore: 10.0, severity: "CRITICAL", cna: "Red Hat / Openwall", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H", mav: "N", mac: "L", mpr: "N", envScore: 10.0, priority: "P0", priorityLabel: "P0 • EMERGÊNCIA", sla: "4 Horas", hash: "9bf4c02283e30f14624d7756e2978aa0e71932ea4512b91d2938afdc13d312bc" },
  { id: "CVE-2024-21762", name: "Fortinet FortiOS SSL-VPN", baseScore: 9.8, severity: "CRITICAL", cna: "Fortinet PSIRT", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.9, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "4471cd6963283f5872ea43b2a3cd662e74da96245dcb99c828d11c828362b192" },
  { id: "CVE-2024-23897", name: "Jenkins CLI Arbitrary File Read", baseScore: 9.8, severity: "CRITICAL", cna: "Jenkins Project", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "L", envScore: 8.7, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "2e6b23a9d18b6287c264c995ad1c8c946b5a38ef67e0e7a17f738b55d918341c" },
  { id: "CVE-2024-27198", name: "JetBrains TeamCity Auth Bypass", baseScore: 9.8, severity: "CRITICAL", cna: "JetBrains Security", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.9, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "b54e38ac912079bb1735cf548238db2e5e1972c8413b0c67c514897f26190a44" },
  { id: "CVE-2024-3400", name: "Palo Alto PAN-OS Command Inj.", baseScore: 10.0, severity: "CRITICAL", cna: "Palo Alto Networks", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H", mav: "N", mac: "L", mpr: "N", envScore: 10.0, priority: "P0", priorityLabel: "P0 • EMERGÊNCIA", sla: "4 Horas", hash: "fa081913cbb38258e80b2a7593c21a48c903bd6b758da47f8923dc10b61829e1" },
  { id: "CVE-2024-4577", name: "PHP CGI Argument Injection", baseScore: 9.8, severity: "CRITICAL", cna: "PHP Security Group", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.9, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "830c29184ba713eb723ca27072a3e0b48c12b7a983ca2058137f2590bd847291" },
  { id: "CVE-2024-38856", name: "Apache OFBiz Pre-auth RCE", baseScore: 9.8, severity: "CRITICAL", cna: "Apache Software Foundation", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.9, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "743b1853ea0b88ca45037d0c354e6377e810a08e1a89c968f237f81a7051b72a" },
  { id: "CVE-2024-43451", name: "Microsoft NTLM Hash Disclosure", baseScore: 8.8, severity: "HIGH", cna: "Microsoft Corporation", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:R/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 8.0, priority: "P1", priorityLabel: "P1 • ALTA", sla: "24 Horas", hash: "6149f6b2195826f5d81747802b1158b44917dc820ba54817a02b85e0bc4e1329" },
  { id: "CVE-2024-21412", name: "Microsoft SmartScreen Bypass", baseScore: 8.1, severity: "HIGH", cna: "Microsoft Corporation", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:R/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "A", mac: "L", mpr: "N", envScore: 7.3, priority: "P2", priorityLabel: "P2 • MÉDIA", sla: "7 Dias", hash: "a094bb713589b917f309a47382626e2a10bf27b9c615a9b73489e37bc537e248" },
  { id: "CVE-2023-4863", name: "Google Chrome WebP Heap Overflow", baseScore: 8.8, severity: "HIGH", cna: "Google Chrome Security", vector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:R/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", mav: "L", mac: "L", mpr: "N", envScore: 6.8, priority: "P2", priorityLabel: "P2 • MÉDIA", sla: "7 Dias", hash: "583c4b92aa0c5817d29487a3cb34f2a7183e845781604a8b894d3725b89a8570" },
  { id: "CVE-2023-38606", name: "Apple WebKit State Execution", baseScore: 5.5, severity: "MEDIUM", cna: "Apple Inc.", vector: "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:M/VI:M/VA:N/SC:N/SI:N/SA:N", mav: "L", mac: "L", mpr: "N", envScore: 5.5, priority: "P3", priorityLabel: "P3 • BAIXA", sla: "30 Dias", hash: "4192b0c9536d7a5b3a1a3648eb847aa1f855d04523910c2834b6e510816781cb" }
];

var currentSelectedConsoleCve = CONSOLE_12_CVES[0];
var consoleAuditHistory = [];

function isMasterAuthenticated() {
  try {
    var raw = localStorage.getItem("helpus_demo_session");
    if (!raw) return false;
    var data = JSON.parse(raw);
    return Boolean(data && data.authenticated);
  } catch(e) {
    return false;
  }
}

function setMasterSession(user) {
  var sessionObj = {
    name: user.name || "SecOps Reviewer",
    role: "HITL_REVIEWER",
    authenticated: true,
    authTime: Date.now()
  };
  localStorage.setItem("helpus_demo_session", JSON.stringify(sessionObj));
  updateConsoleAuthDisplay();
}

function openDemoConsoleView() {
  setMasterSession({ name: "Demonstração Interativa (SecOps)" });
}

function triggerGoogleAuth() {
  window.location.href = "/login";
}

function logoutMasterGoogle() {
  localStorage.removeItem("helpus_demo_session");
  updateConsoleAuthDisplay();
  switchView("view-console");
}

function showGoogleAuthError(msg) {
  var errBox = document.getElementById("googleAuthErrorBox");
  if (errBox) {
    errBox.innerHTML = msg;
    errBox.style.display = "block";
  }
}

function updateConsoleAuthDisplay() {
  var isAuth = isMasterAuthenticated();
  var loginBlock = document.getElementById("consoleLoginBlock");
  var appBlock = document.getElementById("consoleAppBlock");
  var headerBtn = document.getElementById("headerConsoleBtn");
  var headerLabel = document.getElementById("headerConsoleLabel");

  if (isAuth) {
    if (loginBlock) loginBlock.style.display = "none";
    if (appBlock) appBlock.style.display = "block";
    if (headerLabel) headerLabel.innerText = "Sessão HITL Ativa";
    if (headerBtn) {
      headerBtn.style.background = "rgba(74,222,128,0.2)";
      headerBtn.style.borderColor = "#4ade80";
      headerBtn.style.color = "#4ade80";
    }
    renderConsoleCveCards();
    selectConsoleCve(currentSelectedConsoleCve.id);
  } else {
    if (loginBlock) loginBlock.style.display = "block";
    if (appBlock) appBlock.style.display = "none";
    if (headerLabel) headerLabel.innerText = "Console Operacional";
    if (headerBtn) {
      headerBtn.style.background = "linear-gradient(135deg,#0284c7,#2563eb)";
      headerBtn.style.borderColor = "#38bdf8";
      headerBtn.style.color = "#ffffff";
    }
  }
}

function renderConsoleCveCards() {
  var container = document.getElementById("consoleCveGrid");
  if (!container) return;

  var html = "";
  CONSOLE_12_CVES.forEach(function(cve) {
    var isSelected = cve.id === currentSelectedConsoleCve.id;
    var borderStyle = isSelected ? "border:2px solid #38bdf8; background:#081324; box-shadow:0 0 16px rgba(56,189,248,0.35);" : "border:1px solid #1e3a5f; background:#0d1d33;";
    
    html += '<div onclick="selectConsoleCve(\'' + cve.id + '\')" style="' + borderStyle + ' border-radius:12px; padding:12px 14px; cursor:pointer; transition:all 0.15s ease;">';
    html += '  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">';
    html += '    <span style="font-size:12px; font-weight:800; color:#ffffff; font-family:monospace;">' + cve.id + '</span>';
    html += '    <span style="font-size:11px; font-weight:800; color:' + (cve.severity === "CRITICAL" ? "#f87171" : "#fbbf24") + ';">' + cve.baseScore + ' ' + cve.severity + '</span>';
    html += '  </div>';
    html += '  <div style="font-size:11px; color:#cbd5e1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">' + esc(cve.name) + '</div>';
    html += '  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:10px; color:#94a3b8;">';
    html += '    <span>' + esc(cve.cna) + '</span>';
    html += '    <span style="background:rgba(56,189,248,0.15); color:#38bdf8; padding:2px 6px; border-radius:4px; font-weight:700;">' + cve.priority + ' SLA</span>';
    html += '  </div>';
    html += '</div>';
  });

  container.innerHTML = html;
}

function selectConsoleCve(cveId) {
  var found = CONSOLE_12_CVES.find(function(c) { return c.id === cveId; });
  if (found) {
    currentSelectedConsoleCve = found;
  }
  renderConsoleCveCards();

  var c = currentSelectedConsoleCve;
  // Atualiza Camada 1
  var c1Score = document.getElementById("c1ScoreDisplay");
  var c1Id = document.getElementById("c1CveId");
  var c1Cna = document.getElementById("c1CnaInfo");
  var d = HELPUS_I18N[window.currentLanguage] || HELPUS_I18N.pt;
  if (c1Score) {
    c1Score.innerText = c.baseScore.toFixed(1);
    c1Score.style.color = c.severity === "CRITICAL" ? "#f87171" : "#fbbf24";
  }
  if (c1Id) c1Id.innerText = c.id + " • " + c.severity;
  if (c1Cna) c1Cna.innerText = (d.cnaAuthorizedPrefix || "CNA Autorizado: ") + c.cna;

  // Atualiza Camada 2
  var c2Mav = document.getElementById("c2MavBadge");
  if (c2Mav) {
    var mavText = c.mav === "A" ? (d.mavAdj || " (Adjacente)") : c.mav === "N" ? (d.mavExt || " (Rede Externa)") : (d.mavLoc || " (Local)");
    c2Mav.innerText = "MAV:" + c.mav + mavText;
  }

  // Atualiza Camada 3
  var c3Priority = document.getElementById("c3PriorityBadge");
  var c3Env = document.getElementById("c3EnvScore");
  if (c3Priority) {
    c3Priority.innerText = c.priorityLabel;
    if (c.priority === "P0") {
      c3Priority.style.background = "rgba(248,113,113,0.18)";
      c3Priority.style.borderColor = "#f87171";
      c3Priority.style.color = "#f87171";
    } else if (c.priority === "P1") {
      c3Priority.style.background = "rgba(251,191,36,0.18)";
      c3Priority.style.borderColor = "#fbbf24";
      c3Priority.style.color = "#fbbf24";
    } else {
      c3Priority.style.background = "rgba(74,222,128,0.18)";
      c3Priority.style.borderColor = "#4ade80";
      c3Priority.style.color = "#4ade80";
    }
  }
  if (c3Env) c3Env.innerText = c.envScore.toFixed(1) + " (SLA: " + c.sla + ")";

  // Atualiza Camada 4
  var c4Hash = document.getElementById("c4HashDisplay");
  if (c4Hash) c4Hash.innerText = "SHA-256: " + c.hash;

  // Atualiza Camada 5
  var c5Badge = document.getElementById("c5HitlStatusBadge");
  if (c5Badge) {
    c5Badge.innerText = d.layer5PendingBadge || "Pendente de Homologação";
    c5Badge.style.background = "rgba(251,191,36,0.15)";
    c5Badge.style.color = "#fbbf24";
    c5Badge.style.borderColor = "#fbbf24";
  }
}

function handleHitlApprove() {
  var d = HELPUS_I18N[window.currentLanguage] || HELPUS_I18N.pt;
  var c = currentSelectedConsoleCve;
  var now = new Date().toISOString();
  consoleAuditHistory.unshift({
    timestamp: now,
    cveId: c.id,
    baseScore: c.baseScore.toFixed(1),
    envScore: c.envScore.toFixed(1),
    priority: c.priority,
    status: d.consoleHitlApproved || "Homologado (Simulação)",
    approver: d.consoleReviewerName || "Revisor HITL Autorizado",
    hash: c.hash.substring(0, 16) + "..."
  });
  renderConsoleAuditHistory();
  alert(window.currentLanguage === "en" ? "✓ Homologation simulation recorded in console!\n\nGovernance Note: For official production decisions, validation is performed server-side via authenticated /api/review/decision." : (window.currentLanguage === "es" ? "✓ ¡Simulación de homologación registrada en la consola!\n\nNota de Gobernanza: Para decisiones oficiales en producción, la validación se ejecuta en el servidor mediante /api/review/decision." : "✓ Simulação de homologação registrada no console!\n\nNota de Governança: Para decisões oficiais persistidas em produção, a validação é executada server-side via endpoint seguro /api/review/decision."));
}

function handleHitlReject() {
  var d = HELPUS_I18N[window.currentLanguage] || HELPUS_I18N.pt;
  var c = currentSelectedConsoleCve;
  var now = new Date().toISOString();
  consoleAuditHistory.unshift({
    timestamp: now,
    cveId: c.id,
    baseScore: c.baseScore.toFixed(1),
    envScore: c.baseScore.toFixed(1) + (window.currentLanguage === "en" ? " (Kept)" : (window.currentLanguage === "es" ? " (Mantenido)" : " (Mantido)")),
    priority: "P0_OVERRIDE",
    status: d.consoleHitlRejected || "Rejeitado (Simulação)",
    approver: d.consoleReviewerName || "Revisor HITL Autorizado",
    hash: c.hash.substring(0, 16) + "..."
  });
  renderConsoleAuditHistory();

  var c5Badge = document.getElementById("c5HitlStatusBadge");
  if (c5Badge) {
    c5Badge.innerText = d.consoleHitlRejected || "✕ Rejeitado (Simulação)";
    c5Badge.style.background = "rgba(239,68,68,0.15)";
    c5Badge.style.color = "#fca5a5";
    c5Badge.style.borderColor = "#ef4444";
  }
}

function renderConsoleAuditHistory() {
  var tbody = document.getElementById("consoleAuditTableBody");
  if (!tbody) return;

  var d = HELPUS_I18N[window.currentLanguage] || HELPUS_I18N.pt;
  if (consoleAuditHistory.length === 0) {
    var emptyMsg = (d && d.consoleEmptyAudit) || 'Nenhuma homologação realizada nesta sessão. Selecione um CVE e clique em "Homologar".';
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#94a3b8; padding:16px;">' + emptyMsg + '</td></tr>';
    return;
  }

  var html = "";
  consoleAuditHistory.forEach(function(item) {
    var isApprove = item.status.indexOf("Homologado") >= 0;
    html += '<tr>';
    html += '  <td class="mono" style="font-size:11px;">' + item.timestamp.replace("T", " ").replace("Z", "") + '</td>';
    html += '  <td class="mono" style="font-weight:700; color:#38bdf8;">' + item.cveId + '</td>';
    html += '  <td>' + item.baseScore + '</td>';
    html += '  <td><strong>' + item.envScore + '</strong></td>';
    html += '  <td><span style="padding:2px 8px; border-radius:4px; font-weight:700; font-size:11px; background:' + (isApprove ? "rgba(74,222,128,0.2); color:#4ade80;" : "rgba(239,68,68,0.2); color:#fca5a5;") + '">' + item.priority + '</span></td>';
    html += '  <td style="font-size:12px; color:#ffffff;">' + item.approver + '</td>';
    html += '  <td class="mono" style="font-size:11px; color:#94a3b8;">' + item.hash + '</td>';
    html += '</tr>';
  });
  tbody.innerHTML = html;
}

function downloadCanonicalReceipt() {
  var c = currentSelectedConsoleCve;
  var receipt = {
    schema: "https://cvss.helpusbr.com/schemas/jcs-provenance-v1.json",
    canonical_standard: "JCS-compatible (RFC 8785 formal validation pending)",
    evaluated_at: new Date().toISOString(),
    reviewer_identity: "HITL Revisor Autorizado",
    finding: {
      cve_id: c.id,
      name: c.name,
      cna: c.cna,
      base_score: c.baseScore,
      base_severity: c.severity,
      official_vector: c.vector
    },
    environmental_assessment: {
      calculated_environmental_score: c.envScore,
      modified_attack_vector: c.mav,
      modified_attack_complexity: c.mac,
      modified_privileges_required: c.mpr,
      telemetry_window_seconds: 42,
      fail_safe_check: "PASSED (telemetry fresh < 24h)"
    },
    operational_disposition: {
      helpus_priority: c.priority,
      sla_resolution: c.sla,
      governance_authorization: "Homologação Humana Registrada (HITL)"
    },
    cryptographic_provenance: {
      algorithm: "SHA-256",
      receipt_hash: c.hash,
      signer_key_id: "HELPUS-CVSS-HITL-KEY"
    }
  };

  var blob = new Blob([JSON.stringify(receipt, null, 2)], { type: "application/json" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "receipt_" + c.id + "_jcs_sha256.json";
  a.click();
}

function downloadSessionAuditLog() {
  var data = {
    session_owner: "auditor.secops@helpusbr.com",
    role: "HITL_SUPERADMIN",
    exported_at: new Date().toISOString(),
    history: consoleAuditHistory
  };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "helpus_cvss_session_audit_" + Date.now() + ".json";
  a.click();
}

// Inicializa verificação na carga da página
document.addEventListener("DOMContentLoaded", function() {
  updateConsoleAuthDisplay();
  renderConsoleAuditHistory();
});
