# Advanced Security Requirements (CR / IR / AR)

Date: 2026-10-15

## Normative basis

FIRST CVSS v4.0 defines Confidentiality Requirement (CR), Integrity Requirement (IR), and Availability Requirement (AR) as Environmental Security Requirement metrics that describe the importance of the vulnerable system in the consumer's environment.

Threat, Environmental, and Supplemental metrics are optional in the vector. Omitted values are treated as Not Defined (X).

## UX model

CR/IR/AR are intentionally hidden behind progressive disclosure in the guided Step 4 flow.

Defaults:
- CR = X
- IR = X
- AR = X

The basic user can ignore the section completely.

## Governance

The existing environmental-analysis service already refuses to apply Security Requirements unless evidence includes:
- organizationPolicyId
- policyVersion

This increment exposes only ACTIVE tenant policy versions and requires one to be selected before any CR/IR/AR value differs from X.

This prevents an operator from entering ungoverned Security Requirements ad hoc.

## Semantic boundary

CR/IR/AR describe the importance/criticality of the vulnerable system in that environment.

They do not:
- alter Base metrics;
- represent the vulnerability's intrinsic characteristics;
- act as generic compensating-control fields;
- replace Modified Base Metrics.

## Values

Each advanced field exposes:
- X — Not Defined
- H — High
- M — Medium
- L — Low

When all values remain X, no Security Requirements object is sent.

## No scorer changes

The canonical CVSS calculation, rule catalog, FIRST reference gates, ABSTAIN policy, TTL and sealed C1/C2 material remain untouched.
