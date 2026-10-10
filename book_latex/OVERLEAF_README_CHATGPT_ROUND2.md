# HelpUS CVSS AI - ChatGPT Round 2 book revision

This package is a pre-freeze monograph revision based on the latest Antigravity execution package and subsequent independent review.

Key changes:
- historical 2017 study cited as Allodi et al. (FDSE 2017) and treated as a CVSS v3.0-era human-factors baseline;
- Dataset B explicitly treated as development/regression data, not confirmatory generalization;
- source assessment terminology separated from NVD/CNA/FIRST roles;
- no claim that the Red Hat `cvss` library is an official FIRST engine;
- exact historical Fisher/OR statistics use generated macros and identify the conditional exact CI method;
- legacy Dataset B labels are clearly distinguished from CVSS severity and mapped only to local P0-P4 workflow labels for traceability;
- confirmatory C1/C2 results remain pending and are not invented;
- algorithm and HITL language shortened/qualified to improve layout and avoid unsupported cryptographic/compliance claims.

The book remains PRE-FREEZE. Dataset B provenance, full FIRST reference-corpus validation, Web/core parity, ethics determination, and independent C1/C2 evaluation remain release gates.
