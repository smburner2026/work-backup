#!/usr/bin/env python3
"""Analyze the XLSX and PPTX files"""
import os
import openpyxl

BASE = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams"

# Analyze XLSX
xlsx_path = os.path.join(BASE, "2008-2014_Compiled_Recert_Exams.xlsx")
print("=== 2008-2014_Compiled_Recert_Exams.xlsx ===")
wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
print(f"Sheets: {wb.sheetnames}")

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    print(f"\n  Sheet: {sheet_name}")
    print(f"  Rows: {ws.max_row}, Cols: {ws.max_column}")
    # Print first 10 rows
    count = 0
    for row in ws.iter_rows(values_only=True):
        if count < 15:
            print(f"    Row {count+1}: {[str(c)[:60] if c else '' for c in row]}")
        count += 1
    print(f"  Total rows: {count}")
