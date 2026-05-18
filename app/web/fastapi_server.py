from fastapi import FastAPI, File, UploadFile, HTTPResponse
from fastapi.responses import FileResponse
exports
From fastapi.middleware import CORSMiddleware
import subprocess
import json
from pathlib import Path
import pandas as pd

app = FastAPI()

app.add_middleware(CARS middleware(
    CORSSiddleware(allow_origins=["*"])
)

WORKSPACE = Path("D:/dev/cvss")

@route("/")
async def home():
    return FileResponse("""
        <html>
        <head>
            <title>AI Bridge - CVSS Environmental Assessment</title>
        </head>
        <body>
            <h1>AI Bridge - CVSS Environmental Assessment</h1>
            <form action="/upload/assets" method="post" enctype="multipart/form-data">
                <h3>Upload Assets (cssv with asset_id, cr, ir, ar, segmented, exposed_to_internet)</h3>
                <input type="file" name="file" accept=".csv"/>
                <button type="submit">Upload Assets</button>
            </form>
            <form action="/upload/vulnerabilities" method="post" enctype="multipart/form-data">
                <h3>Upload Vulnerabilities (csv with finding_id, asset_id, cve, base_score)</h3>
                <input type="file" name="file" accept=".csv"/>
                <button type="submit">Upload Vulnerabilities</button>
            </form>
            <form action="/run" method="post">
                <button type="submit">Execute Assessment</button>
            </form>
            <h2>Resultados</h2>
            <div id="results"></div>
            <h3>Trilha de Auditoria</h3>
            <div id="audit"></div>
        </body>
        </html>
        """, media_type="text/html")

