from flask import Flask, Response
app = Flask(__name__)
HTML = ''
HTML += '<!doctype html><html><head><meta charset=utf-8><meta name=viewport content=width=device-width,initial-scale=1><title>CVSS Environmental Dashboard</title>'
HTML += '<style>body{font-family:Arial,sans-serif;margin:0;background:#0f172a;color:#e5e7eb}main{max-width:1000px;margin:0 auto;padding:32px 18px}.panel{background:#111827;border:1px solid #334155;border-radius:18px;padding:22px;margin:18px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}.card{background:#0b1220;border:1px solid #1f2937;border-radius:14px;padding:16px}.metric{font-size:30px;font-weight:700}.note{color:#cbd5e1;line-height:1.55}.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#1d4ed8;color:white}</style></head><body><main>'
HTML += '<h1>CVSS Environmental Dashboard</h1>'
HTML += '<p class=note>Python Vercel dashboard generated from committed CVSS artifacts. This avoids the Next.js npm build pipeline.</p>'
HTML += '<section class=panel><h2>Automated watcher IA validation</h2><p class=note>Evidence linked automated validation from committed curated artifacts. Human adjudication is future comparative work, not a current dependency.</p>'
HTML += '<div class=grid><div class=card><div>Decisions</div><div class=metric>1</div></div><div class=card><div>Accepted</div><div class=metric>1</div></div><div class=card><div>Flagged</div><div class=metric>0</div></div><div class=card><div>Agreement</div><div class=metric>100%</div></div></div>'
HTML += '<p class=note><span class=badge>Automated only</span> Not completed independent human expert validation.</p></section>'
HTML += '<section class=panel><h2>Curated validation runs</h2><p>pci_segmented_lab_20260517_143146</p><p>Findings: 6. Assessments: 12. Downgraded: 2. Mean delta: -0,267.</p></section>'
HTML += '<section class=panel><h2>Artifact status</h2><p class=note>Core manuscript and reproducibility deliverables are complete. Production deployment freshness is operational only.</p></section>'
HTML += '</main></body></html>'
@app.get('/')
def dashboard():
 return Response(HTML, mimetype='text/html')
@app.get('/health')
def health():
 return {'ok': True, 'runtime': 'python', 'dashboard': 'cvss'}

