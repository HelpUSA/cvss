import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de caminhos
base_dir = r"D:\AntiG\cvss"
csv_path = os.path.join(base_dir, "data", "article", "cvss40_environmental_scenarios.csv")
figures_dir = os.path.join(base_dir, "book_latex", "figures")
chapters_dir = os.path.join(base_dir, "book_latex", "chapters")

os.makedirs(figures_dir, exist_ok=True)
os.makedirs(chapters_dir, exist_ok=True)

df = pd.read_csv(csv_path)
print(f"Carregados {len(df)} cenarios de {csv_path}")

# Normalizar capitalização
df['base_sev'] = df['cvss_b_severity'].str.capitalize()
df['env_sev'] = df['environmental_priority'].str.capitalize()

order_sev = ['Critical', 'High', 'Medium', 'Low']
order_env = ['Critical', 'High', 'Medium', 'Low', 'Defer']

# Matriz de transição
crosstab = pd.crosstab(df['base_sev'], df['env_sev'])
crosstab = crosstab.reindex(index=order_sev, columns=order_env, fill_value=0)

# 1. Gerar Tabela 6.1 LaTeX automaticamente
table_tex_path = os.path.join(chapters_dir, "table_6_1_generated.tex")
with open(table_tex_path, "w", encoding="utf-8") as f:
    f.write("% Auto-generated from cvss40_environmental_scenarios.csv (Do not edit manually)\n")
    f.write("\\begin{table}[htbp]\n\\centering\n")
    f.write("\\caption{Cross-Tabulation of Official NVD Base vs. HelpUS Contextual Priorities ($n=30$)}\n")
    f.write("\\label{tab:benchmark_summary}\n")
    f.write("\\begin{tabular}{lcccccc}\n\\toprule\n")
    f.write("\\textbf{Official NVD Base} & \\multicolumn{5}{c}{\\textbf{HelpUS Environmental Priority}} & \\textbf{Total} \\\\\n")
    f.write("\\cmidrule(lr){2-6}\n")
    f.write(" & \\textbf{Critical} & \\textbf{High} & \\textbf{Medium} & \\textbf{Low} & \\textbf{Defer} & \\\\\n")
    f.write("\\midrule\n")
    for b in order_sev:
        row_vals = [crosstab.loc[b, e] for e in order_env]
        tot = sum(row_vals)
        f.write(f"\\textbf{{{b}}} & " + " & ".join(str(v) for v in row_vals) + f" & {tot} \\\\\n")
    f.write("\\midrule\n")
    col_totals = [crosstab[e].sum() for e in order_env]
    f.write(f"\\textbf{{Total}} & " + " & ".join(str(v) for v in col_totals) + f" & {len(df)} \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")

print("table_6_1_generated.tex gerada com sucesso!")

# 2. Gerar Appendix C LaTeX automaticamente com os 30 cenários completos
app_c_tex_path = os.path.join(chapters_dir, "appendix_c_historical_dataset.tex")
with open(app_c_tex_path, "w", encoding="utf-8") as f:
    f.write("\\chapter{Complete Experimental Datasets}\n\\label{app:historical_dataset}\n\n")
    f.write("This appendix documents the complete corpus of evaluated vulnerability scenarios, ensuring 100\\% computational reproducibility.\n\n")
    f.write("\\section{Historical 2017 Vulnerability Corpus (Santos et al.)}\n\\label{sec:app_historical_cves}\n")
    f.write("Table~\\ref{tab:app_historical_cves} documents the complete set of twelve Common Vulnerabilities and Exposures (CVEs) evaluated during the controlled trials across flat and segmented topologies~\cite{santos2017estimating}.\n\n")
    f.write("\\begin{table}[htbp]\n\\centering\\small\n")
    f.write("\\caption{Historical Vulnerability Dataset from the Santos et al.~\\cite{santos2017estimating} Empirical Trial}\n")
    f.write("\\label{tab:app_historical_cves}\n")
    f.write("\\begin{tabular}{lp{3.5cm}ccccp{2.6cm}}\n\\toprule\n")
    f.write("\\textbf{CVE ID} & \\textbf{Affected Software} & \\textbf{Target Host} & \\textbf{Type} & \\textbf{Base} & \\textbf{CVSS Vector} & \\textbf{Observed Human Error} \\\\\n\\midrule\n")
    f.write("CVE-2016-0126 & Microsoft Office 2016 & Customer Data PC & APP & 7.8 & AV:L/AC:L/PR:N/UI:R & 10.0\\% \\\\\n")
    f.write("CVE-2016-5167 & Google Chrome 53      & Mailing Kiosk    & APP & 8.8 & AV:N/AC:L/PR:N/UI:R & 21.0\\% \\\\\n")
    f.write("CVE-2016-0019 & Windows 10 Workstation& Customer PC      & SYS & 8.1 & AV:N/AC:H/PR:N/UI:N & 28.0\\% \\\\\n")
    f.write("CVE-2016-0067 & POS Terminal System   & Store POS IP     & SYS & 7.8 & AV:L/AC:L/PR:L/UI:N & 10.0\\% \\\\\n")
    f.write("CVE-2016-0036 & Windows Server 2012   & Corporate Server & SYS & 8.8 & AV:N/AC:L/PR:L/UI:N & 76.0\\% \\\\\n")
    f.write("CVE-2016-0469 & Oracle Retail MICROS  & Retail Store POS & SYS & 5.5 & AV:L/AC:L/PR:L/UI:N & 79.0\\% \\\\\n")
    f.write("CVE-2016-3234 & Microsoft Office 2010 & Store Admin PC   & APP & 5.5 & AV:L/AC:L/PR:N/UI:R & 45.0\\% \\\\\n")
    f.write("CVE-2016-6792 & Google Chrome 47      & Store Admin PC   & APP & 9.8 & AV:N/AC:L/PR:N/UI:N & 86.0\\% \\\\\n")
    f.write("CVE-2016-0012 & Microsoft Office 2010 & Legacy Wi-Fi PC  & APP & 4.3 & AV:N/AC:L/PR:N/UI:R & 34.0\\% \\\\\n")
    f.write("CVE-2016-1619 & Google Chrome 48      & Legacy Wi-Fi PC  & APP & 7.6 & AV:N/AC:L/PR:N/UI:R & 83.0\\% \\\\\n")
    f.write("CVE-2016-6441 & Cisco IOS XE (ASR 900)& Core VLAN Switch & SYS & 9.8 & AV:N/AC:L/PR:N/UI:N & 86.0\\% \\\\\n")
    f.write("CVE-2016-6428 & Cisco IOS XR          & Core VLAN Switch & SYS & 7.8 & AV:L/AC:L/PR:L/UI:N & 90.0\\% \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n\n")

    f.write("\\section{The Complete 30-Scenario Scientific Benchmark Suite}\n\\label{sec:app_modern_benchmark}\n")
    f.write("Table~\\ref{tab:app_modern_scenarios} documents the complete corpus of 30 enterprise validation scenarios evaluated in Chapter~\\ref{chap:empirical_evaluation}, contrasting the official NVD Base metrics against the HelpUS Evidence-Grounded Priority.\n\n")
    f.write("\\begin{table}[htbp]\n\\centering\\scriptsize\n")
    f.write("\\caption{The Complete 30-Scenario Scientific Benchmark Suite ($n=30$)}\n")
    f.write("\\label{tab:app_modern_scenarios}\n")
    f.write("\\begin{tabular}{lllccllc}\n\\toprule\n")
    f.write("\\textbf{Scenario ID} & \\textbf{CVE ID} & \\textbf{Asset Class} & \\textbf{Exposure} & \\textbf{Base} & \\textbf{Base Sev} & \\textbf{Env Priority} & \\textbf{$\\Delta$ Shift} \\\\\n\\midrule\n")
    for _, r in df.iterrows():
        sid = r['scenario_id']
        cid = r['cve_id']
        aclass = str(r['asset_class'])[:22].replace("_", " ").title()
        exp = str(r['internet_exposure']).replace("_", " ").title()
        bscore = r['cvss_b_score']
        bsev = r['base_sev']
        epri = r['env_sev']
        dshift = r['priority_delta']
        sign = "+" if dshift > 0 else ""
        f.write(f"{sid} & {cid} & {aclass} & {exp} & {bscore:.1f} & {bsev} & {epri} & {sign}{dshift} \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")

print("appendix_c_historical_dataset.tex gerado com todos os 30 cenarios!")

# 3. Gerar Figuras Científicas com consistência 100% garantida
plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

# FIGURA 1: Distribuição de Severidade
fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=300)
categories = ['Critical', 'High', 'Medium', 'Low', 'Defer']
nvd_counts = [df['base_sev'].value_counts().get(c, 0) for c in categories]
env_counts = [df['env_sev'].value_counts().get(c, 0) for c in categories]
x = np.arange(len(categories))
width = 0.35

rects1 = ax.bar(x - width/2, nvd_counts, width, label='Official NVD Base Severity', color='#d9534f', edgecolor='black', linewidth=0.8)
rects2 = ax.bar(x + width/2, env_counts, width, label='HelpUS Contextual Priority', color='#0284c7', edgecolor='black', linewidth=0.8)

ax.set_ylabel('Number of Scenarios (n=30)', fontweight='bold')
ax.set_title('Empirical Severity Redistribution (NVD Base vs. HelpUS Priority)', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    if h > 0: ax.annotate(f'{h}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8)
for rect in rects2:
    h = rect.get_height()
    if h > 0: ax.annotate(f'{h}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig1_severity_redistribution.pdf"))
plt.savefig(os.path.join(figures_dir, "fig1_severity_redistribution.png"))
plt.close()

# FIGURA 2: Matriz de Transição (Heatmap fiel à tabela gerada)
fig, ax = plt.subplots(figsize=(5.8, 4.4), dpi=300)
sns.heatmap(crosstab, annot=True, fmt='d', cmap='Blues', cbar=True, ax=ax, linewidths=0.5, linecolor='gray', annot_kws={"size": 11, "weight": "bold"})
ax.set_xlabel('HelpUS Environmental Priority', fontweight='bold')
ax.set_ylabel('NVD Official Base Severity', fontweight='bold')
ax.set_title('Empirical Priority Transition Matrix (n=30)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig2_transition_matrix.pdf"))
plt.savefig(os.path.join(figures_dir, "fig2_transition_matrix.png"))
plt.close()

# FIGURA 3: Distribuição de Deltas de Prioridade
fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=300)
delta_counts = df['priority_delta'].value_counts().sort_index()
deltas = delta_counts.index.tolist()
counts = delta_counts.values.tolist()
bar_colors = ['#5cb85c' if d < 0 else ('#777777' if d == 0 else '#d9534f') for d in deltas]
bars = ax.bar([str(d) for d in deltas], counts, color=bar_colors, edgecolor='black', linewidth=0.8, width=0.55)
ax.set_xlabel(r'Priority Level Shift ($\Delta$ Priority Levels: Environmental - Base)', fontweight='bold')
ax.set_ylabel('Number of Evaluated Assets', fontweight='bold')
ax.set_title(r'Distribution of Contextual Priority Deltas ($\Delta$)', fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.5)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#5cb85c', edgecolor='black', label=r'Mitigated / Downgraded ($\Delta < 0$)'),
    Patch(facecolor='#777777', edgecolor='black', label=r'Unchanged ($\Delta = 0$)'),
    Patch(facecolor='#d9534f', edgecolor='black', label=r'Escalated / Upgraded ($\Delta > 0$)')
]
ax.legend(handles=legend_elements, frameon=True, facecolor='white', framealpha=0.9)
for bar in bars:
    h = bar.get_height()
    ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig3_delta_distribution.pdf"))
plt.savefig(os.path.join(figures_dir, "fig3_delta_distribution.png"))
plt.close()

print("Figuras 1, 2 e 3 sincronizadas com a tabela e CSV com 100% de consistencia!")
