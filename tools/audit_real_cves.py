import csv

csv_path = r"D:\AntiG\cvss\data\article\cvss40_environmental_scenarios.csv"
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
for i, r in enumerate(rows):
    sc_id = r.get("scenario_id")
    cve = r.get("cve_id")
    src = r.get("scenario_source")
    cna = r.get("cvss_source")
    score = r.get("cvss_b_score")
    asset = r.get("asset_class")
    print(f"{i+1:02d}: {sc_id} | {cve} | CNA: {cna} | Score: {score} | Asset: {asset} | Type: {src}")
