#!/usr/bin/env python3
"""Moderate marketing claims in web app (app.js) across PT, EN, and ES."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_JS = ROOT / "app.js"

content = APP_JS.read_text(encoding="utf-8")

replacements = [
    # PT
    ('chart2Sub: "30 Cenários Validados",', 'chart2Sub: "Dataset B (Benchmark, n=30)",'),
    ('pipeTitle: "🔬 Arquitetura Científica: Pipeline de Decisão Anti-Alucinação",', 'pipeTitle: "🔬 Arquitetura Científica: Pipeline de Decisão Auditável",'),
    ('pipeTag: "100% Determinístico",', 'pipeTag: "Determinístico (Regras Versionadas)",'),
    ('pipeCard1Title: "1. Contrato Tripartite Imutável",', 'pipeCard1Title: "1. Registro Canônico de Auditoria",'),
    ('pipeCard2Title: "2. Inferência Determinística Sem Alucinações",', 'pipeCard2Title: "2. Inferência Determinística de Métricas",'),
    ('dsTitle: "📋 Dataset Benchmark: 30 Cenários Empíricos do Estudo",', 'dsTitle: "📋 Dataset B: Benchmark de Desenvolvimento (12 CVEs Reais + 18 Sintéticos)",'),
    ('dsSub: "Navegue pelos cenários reais e sintéticos avaliados na pesquisa científica",', 'dsSub: "Navegue pelos cenários de desenvolvimento avaliados na pesquisa preliminar (validação confirmatória pendente)",'),

    # EN
    ('whyP2: "<strong>Our contribution:</strong> We automate evidence collection and metric population using explainable AI, reaching 100% audit traceability and reducing operational stress without math hallucinations.",',
     'whyP2: "<strong>Our contribution:</strong> We automate evidence collection and metric mapping under versioned deterministic rules, ensuring audit traceability and reducing operational overhead.",'),
    ('chart2Sub: "30 Validated Scenarios",', 'chart2Sub: "Dataset B (Benchmark, n=30)",'),
    ('pipeTitle: "🔬 Scientific Architecture: Anti-Hallucination Decision Pipeline",', 'pipeTitle: "🔬 Scientific Architecture: Auditable Decision Pipeline",'),
    ('pipeTag: "100% Deterministic",', 'pipeTag: "Deterministic (Versioned Rules)",'),
    ('pipeCard1Title: "1. Immutable Tripartite Contract",', 'pipeCard1Title: "1. Canonical Audit Record",'),
    ('pipeCard2Title: "2. Deterministic Inference Without Hallucinations",', 'pipeCard2Title: "2. Deterministic Metric Inference",'),
    ('dsTitle: "📋 Benchmark Dataset: 30 Empirical Study Scenarios",', 'dsTitle: "📋 Dataset B: Development Benchmark (12 Real CVEs + 18 Synthetic)",'),
    ('dsSub: "Browse real and synthetic scenarios evaluated in the scientific paper",', 'dsSub: "Browse development scenarios evaluated in exploratory benchmark (confirmatory validation pending)",'),

    # ES
    ('whyP2: "<strong>Nuestra contribución:</strong> Automatizamos la recolección de evidencias y el cálculo de métricas con IA explicable, alcanzando 100% de trazabilidad y reduciendo el estrés operacional sin alucinaciones matemáticas.",',
     'whyP2: "<strong>Nuestra contribución:</strong> Automatizamos la recolección de evidencias y el mapeo de métricas bajo reglas versionadas deterministas, asegurando trazabilidad auditable y reduciendo la sobrecarga operacional.",'),
    ('chart2Sub: "30 Escenarios Validados",', 'chart2Sub: "Dataset B (Benchmark, n=30)",'),
    ('pipeTitle: "🔬 Arquitectura Científica: Pipeline de Decisión Anti-Alucinación",', 'pipeTitle: "🔬 Arquitectura Científica: Pipeline de Decisión Auditable",'),
    ('pipeTag: "100% Determinístico",', 'pipeTag: "Determinista (Reglas Versionadas)",'),
    ('pipeCard1Title: "1. Contrato Tripartito Inmutable",', 'pipeCard1Title: "1. Registro Canónico de Auditoría",'),
    ('pipeCard2Title: "2. Inferencia Determinista Sin Alucinaciones",', 'pipeCard2Title: "2. Inferencia Determinista de Métricas",'),
    ('dsTitle: "📋 Dataset Benchmark: 30 Escenarios Empíricos del Estudio",', 'dsTitle: "📋 Dataset B: Benchmark de Desarrollo (12 CVEs Reales + 18 Sintéticos)",'),
    ('dsSub: "Navegue por los escenarios reales y sintéticos evaluados en la investigación científica",', 'dsSub: "Navegue por los escenarios de desarrollo evaluados en el estudio exploratorio (validación confirmatoria pendiente)",'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        print(f"Warning: pattern not found: {old[:40]}...")

APP_JS.write_text(content, encoding="utf-8")
print(f"Updated {count}/{len(replacements)} strings in app.js successfully!")
