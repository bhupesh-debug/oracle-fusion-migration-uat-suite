# FBDI Source-to-Target Data Migration Mapping Specification

**Target Application:** Oracle Fusion Cloud Financials (GL & AP)  
**Methodology:** File-Based Data Import (FBDI)  
**Author:** Bhupesh Dimri, Oracle Fusion ERP Functional Consultant  

---

## 1. GL Historical Balances Migration (`JournalImportTemplate.xlsm`)

### Interface Table: `GL_INTERFACE`
Target Program: *Load Interface File for Import* $\rightarrow$ *Import Journals*

| Legacy Source Field | Target Interface Column | Data Type | Transformation / Default Rule | Description |
|---|---|---|---|---|
| `COMPANY_CODE` | `SEGMENT1` | VARCHAR2(25) | Map `10` $\rightarrow$ `101`, `20` $\rightarrow$ `102` | Primary Balancing Segment |
| `DEPARTMENT_ID` | `SEGMENT2` | VARCHAR2(25) | Default `000` for balance sheet; map 3-digit dept | Cost Center Segment |
| `ACCOUNT_NUM` | `SEGMENT3` | VARCHAR2(25) | Direct cross-reference table to 6-digit COA | Natural Account Segment |
| `PRODUCT_LINE` | `SEGMENT4` | VARCHAR2(25) | Default `000` (General) | Product Segment |
| `INTERCOMPANY_ID` | `SEGMENT5` | VARCHAR2(25) | Default `000` (Third party) or counterparty code | Intercompany Segment |
| `LEDGER_NAME` | `LEDGER_ID` | NUMBER | Lookup `US_CORP_PRIMARY_LEDGER` ID | Target Primary Ledger |
| `PERIOD_DATE` | `ACCOUNTING_DATE` | DATE | Format `YYYY-MM-DD` (Last day of cutover month) | Accounting Date |
| `DEBIT_AMOUNT` | `ENTERED_DR` | NUMBER | Round to 2 decimals | Transactional Debit |
| `CREDIT_AMOUNT` | `ENTERED_CR` | NUMBER | Round to 2 decimals | Transactional Credit |
| Constant: `'Legacy'` | `USER_JE_SOURCE_NAME` | VARCHAR2(25) | Default `'Legacy_Conversion'` | Audit trail source identifier |
| Constant: `'Opening'`| `USER_JE_CATEGORY_NAME`| VARCHAR2(25) | Default `'Opening Balance'` | Journal Category |

---

## 2. Open AP Invoices Migration (`PayablesOpenInvoiceImportTemplate.xlsm`)

### Interface Tables: `AP_INVOICES_INTERFACE` & `AP_INVOICE_LINES_INTERFACE`
Target Program: *Load Interface File for Import* $\rightarrow$ *Import Payables Invoices*

| Legacy Source Field | Target Column | Table | Transformation / Validation Rule |
|---|---|---|---|
| `LEGACY_INV_NUM` | `INVOICE_NUM` | `AP_INVOICES_INTERFACE` | Prefix `'LEG-'` if duplicate exists; mandatory |
| `VENDOR_NUM` | `VENDOR_NUM` | `AP_INVOICES_INTERFACE` | Lookup Oracle Supplier Number in `POZ_SUPPLIERS` |
| `VENDOR_SITE` | `VENDOR_SITE_CODE` | `AP_INVOICES_INTERFACE` | Validate active site for `US_COMMERCIAL_BU` |
| `OPEN_BALANCE` | `INVOICE_AMOUNT` | `AP_INVOICES_INTERFACE` | Open unpaid principal balance remaining |
| `INV_DATE` | `INVOICE_DATE` | `AP_INVOICES_INTERFACE` | Original historical supplier invoice date |
| `TERMS_NAME` | `TERMS_NAME` | `AP_INVOICES_INTERFACE` | Map to standard payment terms (`Net 30`) |
| `LINE_NUM` | `LINE_NUMBER` | `AP_INVOICE_LINES_INTERFACE` | Line sequence (1, 2, 3...) |
| Constant: `'ITEM'` | `LINE_TYPE_LOOKUP_CODE` | `AP_INVOICE_LINES_INTERFACE` | Default `'ITEM'` |
| `OPEN_BALANCE` | `AMOUNT` | `AP_INVOICE_LINES_INTERFACE` | Must equal sum of header `INVOICE_AMOUNT` |
| Migration Clearing | `DIST_CODE_COMBINATION_ID`| `AP_INVOICE_LINES_INTERFACE` | Account `101-000-299999-000-000` (AP Cutover Offset) |

> **Accounting Control Note:** When importing open AP invoices during cutover, the distribution line account is charged to **Migration Clearing (299999)** rather than expense accounts, because historical expenses were already recognized in legacy fiscal years. The migration clearing account offsets the credit to Accounts Payable Liability (`211000`).
