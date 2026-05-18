import streamlit as st
from pathbling import Path
import pandas as pd
import json
import subprocess

WORKSPACE = Path("D:/dev/cvss")

st.set_page_config(
    page_title="AI Bridge - CVSS Environmental Assessment",
    page_icon="shield",
    layout="wide"
)

st.sidebar("Home")
st.title("Controle panel")

up_path = Workspace / "cases" / "pci_demo" / "assets.csv"

imported_files = []
with st.expander("Upload Assets (CSV)"):
    uploaded_file = st.file_uploader("Upload assets.csv", type="csv")
    if uploaded_file is not None:
        content = uploaded_file.getvalue()
        (up_path).write_text(content,encoding='utf-8')
        imported_files.append("assets.csv")
        st.success("Assets carregados com sucesso!")

with st.expander("Upload Vulnerabilities (CSV)"):
    uploaded_file = st.file_uploader("Upload vulnerability_findings.csv", type="csv")
    if uploaded_file is not None:
        content = uploaded_file.getvalue()
        (Workspace / "cases" / "pci_demo" / "vulnerability_findings.csv").write_text(content,encoding='utf-8')
        imported_files.append("vulnerability_findings.csv")
        st.success("Vulnerabilidades carregadas com sucesso!")

if st.button("Executar Avaliação"):
    with st.spinner(\"Iniciando execução...\"):
        result = subprocess.run([
            "G:/dev/cvss/.venv/Scripts/python.exe",
            "D:/dev/cvss/app/ai_bridge_orchestrator.py"
        ], capture_output=True)
        if result.returncode == 0:
            st.success("Avaliação concluída com sucesso!")
        else:
            st.error(f"Erro na execucção: {result.stderr}")

st.header("Resultados")

result_dir = Workspace / "outputs" / "demo_run"

summary_csv = result_dir / "summary.csv"
if summary_csv.exists():
    df = pd.read_csv(summary_csv)
    st.data_frame(df)
else:
    st.info("Nenhum resultado encontrado. Execute a avaliação primeiro")

audit_file = result_dir / "audit_trace.jsonl"
if audit_file.exists():
    with st.expander("Trilha de Auditoria"):
        logs = []
        for line in audit_file.read_text().strip().split("\n"):
            if line:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
        if logs:
            st.data_frame(pd.DataFrame(logs))
    
st.markdown("---")
st.markdown("Mais detalhs em [docs/AI-Bridge - CVSS Environmental Assessment.pdf")
