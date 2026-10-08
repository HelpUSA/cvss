import re

file_path = r"D:\AntiG\cvss\app.js"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

new_sol4_es = "Traduce puntajes CVSS en ventanas de SLA operacionales auditables (alineadas con PCI-DSS, NIS2, DORA, ISO 27001) y emite recibos de procedencia con hash SHA-256 y Merkle Tree para auditorias."

content = re.sub(
    r'solCard4Desc:\s*"Traduce puntajes CVSS en plazos regulatorios[^"]+"',
    f'solCard4Desc: "{new_sol4_es}"',
    content
)

content = re.sub(r'kpiNoise:\s*"Filtro de Ruido[^"]+"', 'kpiNoise: "Transición Debajo de High"', content)
content = re.sub(r'kpiNoiseSub:\s*"De 10 a 4 alertas[^"]+"', 'kpiNoiseSub: "3 de 12 reclasificados < High"', content)
content = re.sub(r'pipeCard2Title:\s*"2\.\s*Cero Alucinaciones[^"]+"', 'pipeCard2Title: "2. Inferencia Determinista Sin Alucinaciones"', content)
content = re.sub(
    r'pipeCard2Text:\s*"La IA nunca calcula notas[^"]+"',
    'pipeCard2Text: "La IA nunca calcula notas directamente. Deduce únicamente métricas nominales canónicas (ej: MAV:Adjacent). El score se genera con la fórmula oficial de FIRST."',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Spanish translations in app.js successfully.")
