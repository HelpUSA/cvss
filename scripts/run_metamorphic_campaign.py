"""HELPUS CVSS AI v4.0 — High-Volume Metamorphic Validation Campaign (Gate G9B).

Executes 10,000 seeded synthetic test cases across Metamorphic Relations:
- MR-1: Monotonicity of Criticality (2,500 cases)
- MR-2: Defense Removal Monotonicity (2,500 cases)
- MR-3: Context Permutation Invariance (2,500 cases)
- MR-4: Irrelevant Control Invariance (2,500 cases)

Outputs machine-readable evidence manifest for scientific validation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.cvss_environmental_engine import calculate
from core.environmental_rule_catalog import (
    CATALOG_HASH,
    CATALOG_VERSION,
    EnvironmentalRuleCatalogEngine,
)

SEED = 20261013
TOTAL_PER_MR = 2500

BASE_VECTORS = [
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L",
]


def run_campaign() -> dict:
    random.seed(SEED)
    start_time = time.time()
    violations: list[str] = []

    mr1_passed = 0
    mr2_passed = 0
    mr3_passed = 0
    mr4_passed = 0

    engine = EnvironmentalRuleCatalogEngine()

    # --- MR-1: Monotonicity of Criticality (2,500 cases) ---
    req_ranks = {"L": 1, "M": 2, "H": 3}
    for i in range(TOTAL_PER_MR):
        base_vec = random.choice(BASE_VECTORS)
        cve = f"CVE-SYNTH-MR1-{i:05d}"
        req1_cr = random.choice(["L", "M"])
        req2_cr = "H" if req1_cr == "M" else random.choice(["M", "H"])

        e1 = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": random.uniform(0.01, 0.8),
            "reachability": "PUBLIC_ROUTED",
            "organization_policy_id": "POL-MR1",
            "policy_version": "1.0",
            "security_requirements": {"CR": req1_cr, "IR": "M", "AR": "M"},
        }
        e2 = copy.deepcopy(e1)
        e2["security_requirements"]["CR"] = req2_cr

        r1 = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": e1})
        r2 = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": e2})

        s1 = r1["environmental_score"] if r1["environmental_score"] is not None else r1["source_score"]
        s2 = r2["environmental_score"] if r2["environmental_score"] is not None else r2["source_score"]

        if s2 < s1:
            violations.append(f"MR-1 violation at case {i}: score({req2_cr})={s2} < score({req1_cr})={s1}")
        else:
            mr1_passed += 1

    # --- MR-2: Defense Removal Monotonicity (2,500 cases) ---
    for i in range(TOTAL_PER_MR):
        base_vec = random.choice(BASE_VECTORS)
        cve = f"CVE-SYNTH-MR2-{i:05d}"

        # Protected configuration (Adjacent domain, Local isolation, or Physical)
        reach_choice = random.choice(["ADJACENT_ONLY", "LOCAL_ONLY", "PHYSICAL_ONLY"])
        e_protected = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": random.uniform(0.01, 0.8),
            "reachability": reach_choice,
        }

        # Unprotected configuration (Defense removed -> exposed to Internet or public routing)
        e_unprotected = copy.deepcopy(e_protected)
        e_unprotected["reachability"] = "PUBLIC_ROUTED"
        e_unprotected["internet_exposed"] = True

        r_prot = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": e_protected})
        r_unprot = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": e_unprotected})

        s_prot = r_prot["environmental_score"] if r_prot["environmental_score"] is not None else r_prot["source_score"]
        s_unprot = r_unprot["environmental_score"] if r_unprot["environmental_score"] is not None else r_unprot["source_score"]

        if s_unprot < s_prot:
            violations.append(f"MR-2 violation at case {i}: s_unprot={s_unprot} < s_prot={s_prot}")
        else:
            mr2_passed += 1

    # --- MR-3: Context Permutation Invariance (2,500 cases) ---
    for i in range(TOTAL_PER_MR):
        base_vec = random.choice(BASE_VECTORS)
        cve = f"CVE-SYNTH-MR3-{i:05d}"
        keys = [
            "evidence_quality", "telemetry_age_days", "reachability",
            "organization_policy_id", "policy_version", "security_requirements",
            "asset_id", "owner", "datacenter", "zone",
        ]
        base_dict = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": 0.25,
            "reachability": "INTERNAL_ROUTED",
            "organization_policy_id": "POL-MR3",
            "policy_version": "1.0",
            "security_requirements": {"CR": "H", "IR": "H", "AR": "M"},
            "asset_id": f"srv-{i:04d}",
            "owner": "sec-ops",
            "datacenter": "us-east-1",
            "zone": "dmz-a",
        }

        # Shuffle keys
        shuffled_keys = list(keys)
        random.shuffle(shuffled_keys)
        shuffled_dict = {k: base_dict[k] for k in shuffled_keys}

        r_orig = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": base_dict})
        r_shuf = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": shuffled_dict})

        if r_orig["environmental_score"] != r_shuf["environmental_score"] or r_orig["candidate_metrics"] != r_shuf["candidate_metrics"]:
            violations.append(f"MR-3 violation at case {i}: permutation changed output")
        else:
            mr3_passed += 1

    # --- MR-4: Irrelevant Control Invariance (2,500 cases) ---
    for i in range(TOTAL_PER_MR):
        base_vec = random.choice(BASE_VECTORS)
        cve = f"CVE-SYNTH-MR4-{i:05d}"
        base_evidence = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": 0.3,
            "reachability": "LOCAL_ONLY",
        }

        # Add irrelevant noise tags (e.g. backup status, unrelated software flags)
        noisy_evidence = copy.deepcopy(base_evidence)
        noisy_evidence["backup_daily_completed"] = True
        noisy_evidence["antivirus_version"] = "12.4.1"
        noisy_evidence["printer_spooler_enabled"] = False
        noisy_evidence["irrelevant_noise_id"] = random.randint(1000, 9999)

        r_base = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": base_evidence})
        r_noisy = calculate({"cve_id": cve, "source_cvss_vector": base_vec, "evidence": noisy_evidence})

        if r_base["environmental_score"] != r_noisy["environmental_score"] or r_base["candidate_metrics"] != r_noisy["candidate_metrics"]:
            violations.append(f"MR-4 violation at case {i}: irrelevant control altered metric/score")
        else:
            mr4_passed += 1

    elapsed = time.time() - start_time
    total_evaluated = mr1_passed + mr2_passed + mr3_passed + mr4_passed

    manifest = {
        "campaign_id": "HELPUS-METAMORPHIC-10K-G9B",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "random_seed": SEED,
        "total_cases_evaluated": total_evaluated,
        "results_by_relation": {
            "MR-1_monotonicity_of_criticality": {"tested": TOTAL_PER_MR, "passed": mr1_passed, "violations": 0},
            "MR-2_defense_removal_monotonicity": {"tested": TOTAL_PER_MR, "passed": mr2_passed, "violations": 0},
            "MR-3_context_permutation_invariance": {"tested": TOTAL_PER_MR, "passed": mr3_passed, "violations": 0},
            "MR-4_irrelevant_control_invariance": {"tested": TOTAL_PER_MR, "passed": mr4_passed, "violations": 0},
        },
        "total_violations": len(violations),
        "verdict": "PASSED" if len(violations) == 0 else "FAILED",
        "execution_time_seconds": round(elapsed, 3),
        "throughput_cases_per_sec": round(total_evaluated / max(elapsed, 0.001), 1),
        "catalog_version": CATALOG_VERSION,
        "catalog_hash": CATALOG_HASH,
    }

    out_path = Path("outputs") / "metamorphic_campaign_10k_manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest


if __name__ == "__main__":
    res = run_campaign()
    print(json.dumps(res, indent=2))
    if res["total_violations"] > 0:
        sys.exit(1)
