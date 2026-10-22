-- ============================================================================
-- ORACLE FUSION DATA MIGRATION: 3-POINT RECONCILIATION TIE-OUT QUERY SUITE
-- Target Enterprise: CORP_GLOBAL_HOLDINGS
-- Purpose: Verify completeness, monetary hash totals, and subledger tie-outs
--          for FBDI trial balances and open AP invoice cutovers.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- POINT 1: ROW COUNT PARITY CHECK (LEGACY EXTRACT VS. INTERFACE VS. CORE)
-- ----------------------------------------------------------------------------
SELECT 
    'Open AP Invoices' AS migration_object,
    (SELECT COUNT(*) FROM legacy_open_invoices_extract) AS legacy_extracted_rows,
    (SELECT COUNT(*) FROM ap_invoices_interface WHERE source = 'Legacy_Conversion') AS interface_staged_rows,
    (SELECT COUNT(*) FROM ap_invoices_all WHERE description LIKE '%Legacy%') AS core_loaded_rows,
    ((SELECT COUNT(*) FROM legacy_open_invoices_extract) - 
     (SELECT COUNT(*) FROM ap_invoices_all WHERE description LIKE '%Legacy%')) AS row_count_variance;

-- ----------------------------------------------------------------------------
-- POINT 2: MONETARY HASH TOTAL TIE-OUT (GL TRIAL BALANCE)
-- Compares sum of debits and credits between legacy extract and loaded GL journals.
WITH legacy_hash AS (
    SELECT 
        SUM(debit) AS legacy_total_debits,
        SUM(credit) AS legacy_total_credits,
        ROUND(SUM(debit) - SUM(credit), 2) AS legacy_net_difference
    FROM legacy_gl_trial_balance
),
fusion_hash AS (
    SELECT 
        SUM(gjl.accounted_dr) AS fusion_total_debits,
        SUM(gjl.accounted_cr) AS fusion_total_credits,
        ROUND(SUM(gjl.accounted_dr) - SUM(gjl.accounted_cr), 2) AS fusion_net_difference
    FROM gl_je_headers gjh
    JOIN gl_je_lines gjl ON gjh.je_header_id = gjl.je_header_id
    WHERE gjh.je_source = 'Legacy_Conversion'
      AND gjh.period_name = 'OCT-26'
)
SELECT 
    l.legacy_total_debits,
    f.fusion_total_debits,
    ROUND(l.legacy_total_debits - f.fusion_total_debits, 2) AS debit_variance,
    l.legacy_total_credits,
    f.fusion_total_credits,
    ROUND(l.legacy_total_credits - f.fusion_total_credits, 2) AS credit_variance
FROM legacy_hash l
CROSS JOIN fusion_hash f;

-- ----------------------------------------------------------------------------
-- POINT 3: SUBLEDGER TO GENERAL LEDGER LIABILITY TIE-OUT
-- Proves that total open invoices in AP equal the balance on GL Account 211000.
WITH ap_open_liability AS (
    SELECT 
        SUM(invoice_amount - COALESCE(amount_paid, 0)) AS total_subledger_unpaid
    FROM ap_invoices_all
    WHERE payment_status_flag <> 'Y'
      AND description LIKE '%Legacy%'
),
gl_trade_liability AS (
    SELECT 
        SUM(gjl.accounted_cr - gjl.accounted_dr) AS total_gl_ap_balance
    FROM gl_je_lines gjl
    JOIN gl_code_combinations gcc ON gjl.code_combination_id = gcc.code_combination_id
    JOIN gl_je_headers gjh ON gjl.je_header_id = gjh.je_header_id
    WHERE gcc.segment3 = '211000' -- AP Trade Liability
      AND gjh.je_source = 'Legacy_Conversion'
)
SELECT 
    ap.total_subledger_unpaid,
    gl.total_gl_ap_balance,
    ROUND(ap.total_subledger_unpaid - gl.total_gl_ap_balance, 2) AS subledger_gl_variance
FROM ap_open_liability ap
CROSS JOIN gl_trade_liability gl;
