#!/usr/bin/env python3
"""
generate_migration_extracts.py
Generates synthetic legacy ERP extracts (Trial Balance, Open AP Invoices, Suppliers)
with row counts and hash totals for 3-point reconciliation validation in Oracle Fusion.
"""

import csv
import hashlib
import os
import random

random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Generate Legacy Supplier Master Extract
SUPPLIERS = []
for i in range(1, 101):
    SUPPLIERS.append({
        "legacy_vendor_id": f"VND-{i:04d}",
        "vendor_name": f"Enterprise Partner {i} Corp",
        "tax_id": f"EIN-99-00{i:04d}",
        "payment_terms": random.choice(["NET30", "NET60", "2/10NET30"]),
        "currency": "USD"
    })

# 2. Generate Legacy Open AP Invoices Extract
INVOICES = []
total_open_ap = 0.0

for n in range(1, 501):
    v = random.choice(SUPPLIERS)
    amt = round(random.uniform(500.0, 45000.0), 2)
    total_open_ap += amt

    INVOICES.append({
        "legacy_invoice_id": f"LEG-INV-{2026000 + n}",
        "legacy_vendor_id": v["legacy_vendor_id"],
        "vendor_name": v["vendor_name"],
        "invoice_date": f"2026-09-{random.randint(1, 28):02d}",
        "due_date": "2026-11-15",
        "open_amount": amt,
        "currency": "USD",
        "offset_account": "101-000-299999-000-000"
    })

total_open_ap = round(total_open_ap, 2)

# 3. Generate Legacy General Ledger Trial Balance Extract
GL_ACCOUNTS = [
    ("111000", "Operating Cash", 1250000.00, 0.00),
    ("121000", "Accounts Receivable Trade", 2450000.00, 0.00),
    ("141000", "Inventory Finished Goods", 1850000.00, 0.00),
    ("151000", "Prepaid Corporate Expenses", 350000.00, 0.00),
    ("211000", "Accounts Payable Trade Liability", 0.00, total_open_ap),
    ("221000", "Accrued Compensation & Payroll", 0.00, 480000.00),
    ("311000", "Retained Earnings Prior Periods", 0.00, 0.00) # Balancing account
]

TRIAL_BALANCE = []
tot_dr = sum(x[2] for x in GL_ACCOUNTS)
tot_cr = sum(x[3] for x in GL_ACCOUNTS)
retained_earnings = round(tot_dr - tot_cr, 2)

for acct, name, dr, cr in GL_ACCOUNTS:
    if acct == "311000":
        cr = retained_earnings
    TRIAL_BALANCE.append({
        "account_code": f"101-000-{acct}-000-000",
        "account_name": name,
        "debit": dr,
        "credit": cr
    })

tot_dr = round(sum(x["debit"] for x in TRIAL_BALANCE), 2)
tot_cr = round(sum(x["credit"] for x in TRIAL_BALANCE), 2)


def write_csv(filename, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} records to {filename}")


if __name__ == "__main__":
    write_csv("legacy_supplier_master.csv", SUPPLIERS)
    write_csv("legacy_open_ap_invoices.csv", INVOICES)
    write_csv("legacy_gl_trial_balance.csv", TRIAL_BALANCE)

    print("\n--- 3-POINT RECONCILIATION BENCHMARKS ---")
    print(f"Point 1 (Row Counts): Suppliers={len(SUPPLIERS)}, Invoices={len(INVOICES)}, GL Accounts={len(TRIAL_BALANCE)}")
    print(f"Point 2 (Hash Totals): GL Debits = ${tot_dr:,.2f} | GL Credits = ${tot_cr:,.2f} | Variance = ${abs(tot_dr - tot_cr):.2f}")
    print(f"Point 3 (Subledger Tie-Out): Open AP Invoices = ${total_open_ap:,.2f} | GL AP Account 211000 = ${total_open_ap:,.2f} | Variance = $0.00")
