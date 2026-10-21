# R6-T6 Detailed Case Analysis: Historical NVD Operational Deviations
## Test Suite: `TEST-SUITE-R6-T6-NVD-REPRESENTABILITY` ($N = 4$)

* **Preregistration Freeze**: `5a6c8c67088a8ed26e2cbf91a5e3317ceffb2925`
* **Execution Timestamp**: `2026-10-21T20:11:44Z`

---

### Case T6.1: SCN-NVD-001 (CVE-2026-4251)
* **Asset Class**: `public_web_application`
* **Internet Exposure (Raw)**: `public` (In closed-world enum: `True`)
* **Equation 8 Nominal Priority**: `MEDIUM` (Nominal delta: `1`)
* **Practitioner Operational Priority**: `LOW`
* **Primary Classification**: **`REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION`**

#### Dimensional Evaluation:
1. **Direct Schema v2 Validation**: `valid=False`. Direct errors (1):
   - `root.environmental_evidence.compensating_controls: Field 'compensating_controls' expects type <class 'list'>, got str`
2. **Normative Structural Transformation**: `valid=True`.
   - Applied transformations:
     * Wrapped compensating_controls narrative string into CompensatingControlItem array preserving full narrative in description
     * Wrapped evidence_links string into EvidenceLinkItem array
     * Normalized confidentiality_requirement to enum token 'H'
     * Normalized integrity_requirement to enum token 'H'
     * Normalized availability_requirement to enum token 'M'
     * Normalized candidate_modified_metrics to dictionary container
     * Wrapped uncertainty_flags string into list
     * Initialized extensions dictionary
3. **Governance Override Encapsulation**:
   - Applicable: `True`
   - Reason Code: `CONTROL_COMPENSATION`
   - Override Applied: `True`
   - Final Authorized Priority: `LOW`
   - Diagnostics: `['GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY']`
4. **Equation 8 Invariance Verified**: `True`

#### Methodological Rationale:
Valid under Schema v2 after deterministic normative structural transformation (array-wrapping and container normalization) with zero information invention. Operational priority divergence is fully encapsulated by formal GovernanceOverrideRecord.

---

### Case T6.2: SCN-NVD-003 (CVE-2026-4270)
* **Asset Class**: `identity_provider`
* **Internet Exposure (Raw)**: `restricted` (In closed-world enum: `False`)
* **Equation 8 Nominal Priority**: `HIGH` (Nominal delta: `1`)
* **Practitioner Operational Priority**: `HIGH`
* **Primary Classification**: **`NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`**

#### Dimensional Evaluation:
1. **Direct Schema v2 Validation**: `valid=False`. Direct errors (1):
   - `root.environmental_evidence.compensating_controls: Field 'compensating_controls' expects type <class 'list'>, got str`
2. **Normative Structural Transformation**: `valid=False`.
   - Applied transformations:
     * Wrapped compensating_controls narrative string into CompensatingControlItem array preserving full narrative in description
     * Wrapped evidence_links string into EvidenceLinkItem array
     * Normalized confidentiality_requirement to enum token 'H'
     * Normalized integrity_requirement to enum token 'H'
     * Normalized availability_requirement to enum token 'H'
     * Normalized candidate_modified_metrics to dictionary container
     * Wrapped uncertainty_flags string into list
     * Initialized extensions dictionary
   - Residual validation errors (1):
     * `root.environmental_evidence.internet_exposure: Invalid internet_exposure: 'restricted'`
3. **Governance Override Encapsulation**:
   - Applicable: `False`
   - Reason Code: `None`
   - Override Applied: `None`
   - Final Authorized Priority: `HIGH`
   - Diagnostics: `[]`
4. **Equation 8 Invariance Verified**: `True`

#### Methodological Rationale:
Attribute internet_exposure='restricted' is outside Schema v2 closed-world enum ['dmz', 'internal', 'isolated', 'public']. Resolving this requires fabricating network topology assumptions not present in the historical trace.

---

### Case T6.3: SCN-NVD-007 (CVE-2026-29513)
* **Asset Class**: `ot_monitoring_gateway`
* **Internet Exposure (Raw)**: `internal` (In closed-world enum: `True`)
* **Equation 8 Nominal Priority**: `CRITICAL` (Nominal delta: `2`)
* **Practitioner Operational Priority**: `MEDIUM`
* **Primary Classification**: **`REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION`**

#### Dimensional Evaluation:
1. **Direct Schema v2 Validation**: `valid=False`. Direct errors (1):
   - `root.environmental_evidence.compensating_controls: Field 'compensating_controls' expects type <class 'list'>, got str`
2. **Normative Structural Transformation**: `valid=True`.
   - Applied transformations:
     * Wrapped compensating_controls narrative string into CompensatingControlItem array preserving full narrative in description
     * Wrapped evidence_links string into EvidenceLinkItem array
     * Normalized confidentiality_requirement to enum token 'M'
     * Normalized integrity_requirement to enum token 'H'
     * Normalized availability_requirement to enum token 'H'
     * Normalized candidate_modified_metrics to dictionary container
     * Wrapped uncertainty_flags string into list
     * Initialized extensions dictionary
3. **Governance Override Encapsulation**:
   - Applicable: `True`
   - Reason Code: `EXPOSURE_CONTEXT_EXCEPTION`
   - Override Applied: `True`
   - Final Authorized Priority: `MEDIUM`
   - Diagnostics: `['GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY']`
4. **Equation 8 Invariance Verified**: `True`

#### Methodological Rationale:
Valid under Schema v2 after deterministic normative structural transformation (array-wrapping and container normalization) with zero information invention. Operational priority divergence is fully encapsulated by formal GovernanceOverrideRecord.

---

### Case T6.4: SCN-NVD-011 (CVE-2026-4224)
* **Asset Class**: `identity_provider`
* **Internet Exposure (Raw)**: `restricted` (In closed-world enum: `False`)
* **Equation 8 Nominal Priority**: `HIGH` (Nominal delta: `1`)
* **Practitioner Operational Priority**: `HIGH`
* **Primary Classification**: **`NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`**

#### Dimensional Evaluation:
1. **Direct Schema v2 Validation**: `valid=False`. Direct errors (1):
   - `root.environmental_evidence.compensating_controls: Field 'compensating_controls' expects type <class 'list'>, got str`
2. **Normative Structural Transformation**: `valid=False`.
   - Applied transformations:
     * Wrapped compensating_controls narrative string into CompensatingControlItem array preserving full narrative in description
     * Wrapped evidence_links string into EvidenceLinkItem array
     * Normalized confidentiality_requirement to enum token 'H'
     * Normalized integrity_requirement to enum token 'H'
     * Normalized availability_requirement to enum token 'H'
     * Normalized candidate_modified_metrics to dictionary container
     * Wrapped uncertainty_flags string into list
     * Initialized extensions dictionary
   - Residual validation errors (1):
     * `root.environmental_evidence.internet_exposure: Invalid internet_exposure: 'restricted'`
3. **Governance Override Encapsulation**:
   - Applicable: `False`
   - Reason Code: `None`
   - Override Applied: `None`
   - Final Authorized Priority: `HIGH`
   - Diagnostics: `[]`
4. **Equation 8 Invariance Verified**: `True`

#### Methodological Rationale:
Attribute internet_exposure='restricted' is outside Schema v2 closed-world enum ['dmz', 'internal', 'isolated', 'public']. Resolving this requires fabricating network topology assumptions not present in the historical trace.

---
