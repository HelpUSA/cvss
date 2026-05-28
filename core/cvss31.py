import math

AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
AC = {"L": 0.77, "H": 0.44}
UI = {"N": 0.85, "R": 0.62}
CIA = {"H": 0.56, "L": 0.22, "N": 0.0}
PRU = {"N": 0.85, "L": 0.62, "H": 0.27}
PRC = {"N": 0.85, "L": 0.68, "H": 0.50}
REQ = ("AV", "AC", "PR", "UI", "S", "C", "I", "A")

def roundup(x):
    return math.ceil(float(x) * 10.0 - 1e-7) / 10.0

def severity(s):
    s = float(s)
    if s == 0:
        return "None"
    if s < 4:
        return "Low"
    if s < 7:
        return "Medium"
    if s < 9:
        return "High"
    return "Critical"

def parse_vector(v):
    p = str(v).strip().split("/")
    if not p or p[0] not in ("CVSS:3.1", "CVSS:3.0"):
        raise ValueError("only CVSS 3.x vectors are supported")
    m = {"version": p[0].split(":")[1]}
    for part in p[1:]:
        if ":" not in part:
            raise ValueError("invalid CVSS metric segment: " + part)
        k, val = part.split(":", 1)
        m[k] = val
    miss = [k for k in REQ if k not in m]
    if miss:
        raise ValueError("missing required base metrics: " + ",".join(miss))
    return m

def base_score(v):
    m = parse_vector(v)
    scope = m["S"]
    pr = (PRC if scope == "C" else PRU)[m["PR"]]
    exploitability = 8.22 * AV[m["AV"]] * AC[m["AC"]] * pr * UI[m["UI"]]
    isc = 1 - ((1 - CIA[m["C"]]) * (1 - CIA[m["I"]]) * (1 - CIA[m["A"]]))

    if scope == "U":
        impact = 6.42 * isc
    else:
        impact = 7.52 * (isc - 0.029) - 3.25 * ((isc - 0.02) ** 15)

    if impact <= 0:
        score = 0.0
    elif scope == "U":
        score = roundup(min(impact + exploitability, 10))
    else:
        score = roundup(min(1.08 * (impact + exploitability), 10))

    return {
        "version": m["version"],
        "vector": v,
        "base_score": score,
        "base_severity": severity(score),
        "scope": scope,
        "impact_subscore": round(impact, 3),
        "exploitability_subscore": round(exploitability, 3),
        "metrics": m,
    }

def official_cvss_output(v):
    r = base_score(v)
    return {
        "official_cvss": {
            "version": r["version"],
            "vector": r["vector"],
            "base_score": r["base_score"],
            "base_severity": r["base_severity"],
            "temporal_score": None,
            "environmental_score": None,
            "scope": r["scope"],
            "impact_subscore": r["impact_subscore"],
            "exploitability_subscore": r["exploitability_subscore"],
        }
    }
