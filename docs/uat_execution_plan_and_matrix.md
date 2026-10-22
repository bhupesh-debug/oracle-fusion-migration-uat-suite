# User Acceptance Testing (UAT) Execution Plan & Test Script Matrix

**Enterprise:** `CORP_GLOBAL_HOLDINGS`  
**Test Environment:** Fusion Financials Test Pod (UAT)  
**Coordinator:** Bhupesh Dimri, Oracle Fusion ERP Functional Consultant  

---

## 1. UAT Test Script Matrix (15 Business Scenarios)

| Script ID | Cycle / Module | Test Scenario Description | Expected Outcome | Status |
|---|---|---|---|---|
| `UAT-GL-01` | GL Core | Manual Journal Entry creation with approval routing | Journal approved by Finance Manager and posted. | **PASS** |
| `UAT-GL-02` | GL Controls | Cross-Validation Rule rejection on invalid account combinations | System blocks posting and displays error code. | **PASS** |
| `UAT-GL-03` | GL Multi-Currency | Foreign Currency EUR journal entry with corporate rate | Converted to USD functional currency accurately. | **PASS** |
| `UAT-GL-04` | GL Close | Foreign Currency Revaluation execution | Unrealized Gain/Loss journals generated to Account 781000. | **PASS** |
| `UAT-GL-05` | GL Intercompany | Cross-entity balancing between Company 101 and 102 | Intercompany receivables/payables lines auto-injected. | **PASS** |
| `UAT-AP-01` | AP Invoicing | Standard 2-way matched invoice against IT services PO | Clean validation, routed to Cost Center Mgr for sign-off. | **PASS** |
| `UAT-AP-02` | AP Invoicing | Standard 3-way matched invoice against warehouse PO & Receipt | Validated without holds; eligible for payment batch. | **PASS** |
| `UAT-AP-03` | AP Controls | 3-way match invoice with unit price exceeding tolerance by 5% | Placed on `PRICE HOLD`; prevented from payment selection. | **PASS** |
| `UAT-AP-04` | AP Controls | 3-way match invoice billed before Goods Receipt logged | Placed on `QTY REC HOLD` until warehouse receipt recorded. | **PASS** |
| `UAT-AP-05` | AP BPM | High-value invoice ($150k) approval workflow routing | Routed sequentially to Manager $\rightarrow$ VP $\rightarrow$ CFO. | **PASS** |
| `UAT-AP-06` | AP Prepayments | Apply prepayment deposit against final supplier billing | Invoices netted; open liability reduced accurately. | **PASS** |
| `UAT-PY-01` | AP Payments | Electronic ACH payment process request (PPR) execution | Bank payment file generated in standard NACHA format. | **PASS** |
| `UAT-PY-02` | AP Payments | Urgent manual check issuance out of standard payment cycle | Check printed locally; status updated to Paid in AP. | **PASS** |
| `UAT-MIG-01` | Migration | FBDI Open AP Invoice import with 3-point reconciliation tie-out | Rows tie, hash balances tie, and GL matches subledger. | **PASS** |
| `UAT-REP-01` | Reporting | OTBI Real-Time AP Aging Report vs. General Ledger Trial Balance | Subledger balances match GL Account 211000 to the penny. | **PASS** |

---

## 2. Detailed Test Script Execution Walkthrough (`UAT-AP-03`)
- **Business Purpose:** Verify that Oracle Payables blocks payment when a vendor charges a unit price higher than the agreed Purchase Order contract price.
- **Prerequisites:** Active supplier `SUP0012`, approved PO `PO-88201` for 10 units @ $100.00 each.
- **Action Taken:**
  1. Navigate to *Payables* $\rightarrow$ *Invoices* $\rightarrow$ *Create Invoice*.
  2. Enter Supplier `SUP0012`, Invoice Number `INV-TEST-PRICE-01`, Amount `$1,050.00` ($105.00/unit).
  3. Click *Match Lines* and select PO `PO-88201`.
  4. Click *Invoice Actions* $\rightarrow$ *Validate*.
- **Expected Result:** Validation status displays `Needs Revalidation`; Holds tab shows `PRICE HOLD` with reason: *"Unit price billed $105.00 exceeds PO price $100.00 by 5.0% (Tolerance: 2.0%)"*.
- **Actual Result:** Invoice placed on hold as expected. Cannot be added to Payment Process Request. Test **PASSED**.
