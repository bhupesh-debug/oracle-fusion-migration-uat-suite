# Defect Triage Governance & Formal UAT Exit Sign-Off Criteria

**Enterprise:** `CORP_GLOBAL_HOLDINGS`  
**Phase:** User Acceptance Testing (UAT) / Cutover Gate Review  

---

## 1. Defect Severity Rubric & SLAs

| Severity Level | Definition | Business Impact | SLA Resolution Target |
|---|---|---|---|
| **Severity 1 (Blocker)** | Critical system crash or complete process failure (e.g., cannot post journals, cannot generate payment file). No workaround. | Halts all testing in that functional area; immediate go-live blocker. | **< 4 Hours** |
| **Severity 2 (High)** | Major functional error affecting accounting balances or approval routing, but a viable manual operational workaround exists. | Requires VP / Steering Committee sign-off to proceed to cutover. | **< 24 Hours** |
| **Severity 3 (Medium)** | Minor functional discrepancy, reporting formatting error, or cosmetic UI defect that does not impact transactional integrity. | Does not block cutover; remediated in next scheduled sprint. | **< 5 Business Days** |
| **Severity 4 (Low)** | User preference, cosmetic label suggestion, or enhancement request. | Logged for post-stabilization backlog. | Post-Go-Live |

---

## 2. Daily Defect Triage Workflow

```
Defect Ticket Logged by User
           │
           ▼
[Lead Functional Consultant Review]
           │
           ├─► User / Training Issue (60%) ──► Quick 1-on-1 coaching; update job aid; close ticket
           │
           ├─► Data Migration Issue (25%) ──► Correct FBDI extraction transformation; reload dataset
           │
           └─► Configuration / Bug (15%)  ──► FSM configuration fix in Test Pod; retest & sign off
```

---

## 3. Formal Go-Live Exit Sign-Off Criteria
To secure approval for Production Cutover, all of the following exit conditions must be satisfied:
1. **100% of Priority 1 (Core) UAT Scripts Executed:** All 15 business scenarios completed.
2. **Zero Open Severity 1 (Blocker) Defects:** No blocking tickets remain unresolved.
3. **Zero Open Severity 2 (High) Defects:** All high-severity defects remediated or formally accepted with documented manual workarounds approved by the Financial Controller.
4. **FBDI Reconciliation Balance Tie-Out:** Source-to-target row count and monetary hash totals must tie to `$0.00` variance.
5. **Stakeholder Sign-Off Form:** Signed by Chief Financial Officer, Corporate Controller, AP Manager, and Lead Functional Consultant.
