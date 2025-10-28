#!/usr/bin/env python3
"""
dedupe_csv_shiftjis.py
Remove duplicate rows from a CSV file encoded in Shift_JIS (tries 'shift_jis' then 'cp932').

Usage:
    python3 dedupe_csv_shiftjis.py input.csv output.csv --out-encoding shift_jis
"""

import csv
import sys
import argparse

def open_with_shift_variants(path, mode='r'):
    """Try reading with shift_jis then cp932."""
    encodings = ['shift_jis', 'cp932']
    last_exc = None
    for enc in encodings:
        try:
            return open(path, mode, encoding=enc, newline='')
        except UnicodeDecodeError as e:
            last_exc = e
    # If all failed, raise last exception (or open with binary to get a clearer error)
    raise last_exc or OSError("Failed to open file with shift_jis/cp932 encodings")

def dedupe_csv(in_path, out_path, out_encoding='utf-8'):
    # Read input with shift_jis / cp932
    with open_with_shift_variants(in_path, 'r') as infile:
        reader = csv.reader(infile)
        seen = set()
        unique_rows = []
        for row in reader:
            key = tuple(row)  # treat whole row as the dedupe key
            if key in seen:
                continue
            seen.add(key)
            unique_rows.append(row)

    # Write output (UTF-8 by default)
    with open(out_path, 'w', encoding=out_encoding, newline='') as outfile:
        writer = csv.writer(outfile)
        for row in unique_rows:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate rows from a Shift-JIS encoded CSV (preserve order).")
    parser.add_argument('input', help='Input CSV path (Shift-JIS / cp932 encoded)')
    parser.add_argument('output', help='Output CSV path (default encoding UTF-8)')
    parser.add_argument('--out-encoding', default='utf-8', help='Output encoding (default: utf-8)')
    args = parser.parse_args()

    try:
        dedupe_csv(args.input, args.output, out_encoding=args.out_encoding)
        print(f"Done. Deduplicated file written to: {args.output}")
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

