#!/usr/bin/env python3
"""
Test script to understand current well ID format requirements and test new regex.
"""

import re
import sys

# Current regex from pcrindexutils.py line 88/97
current_regex = r'^([pP][0-9]+[-])?[a-hA-H]([0][1-9]|[1][0-2])$'

# Test cases from actual usage
test_cases = [
    # Format: (well_id, should_pass_current, description)
    ("A01", True, "Standard well without plate"),
    ("H12", True, "Corner well without plate"),
    ("P01-A01", True, "Standard format with plate"),
    ("P1-A01", True, "Single digit plate number"),
    ("PA-A01", False, "Alphanumeric plate ID with row-column"),
    ("PA-01A", False, "Alphanumeric plate ID with column-row"),
    ("PA_A01", False, "Underscore separator with row-column"),
    ("P01_A01", False, "Numeric plate with underscore"),
    ("01A", False, "Column-row without plate"),
    ("PB-B05", False, "Multi-letter plate ID"),
]

print("Testing current regex:", current_regex)
print("=" * 70)

for well_id, expected, description in test_cases:
    match = re.match(current_regex, well_id)
    passes = match is not None
    status = "✓" if passes == expected else "✗"
    print(f"{status} {well_id:15} - {description:40} {'PASS' if passes else 'FAIL'}")

print("\n" + "=" * 70)

# Proposed new regex - more flexible
# Allow: alphanumeric plate IDs, hyphen or underscore separator, row-column or column-row
proposed_regex = r'^([a-zA-Z][a-zA-Z0-9]*[-_])?([a-hA-H]([0][1-9]|[1][0-2])|([0][1-9]|[1][0-2])[a-hA-H])$'

print("\nTesting proposed regex:", proposed_regex)
print("=" * 70)

# All test cases should pass with the new regex
for well_id, _, description in test_cases:
    match = re.match(proposed_regex, well_id)
    passes = match is not None
    status = "✓" if passes else "✗"
    print(f"{status} {well_id:15} - {description:40} {'PASS' if passes else 'FAIL'}")

print("\n" + "=" * 70)
print("Summary:")
print(f"Current regex passes: {sum(1 for w, e, _ in test_cases if (re.match(current_regex, w) is not None) == e)}/{len(test_cases)}")
print(f"Proposed regex passes: {sum(1 for w, _, _ in test_cases if re.match(proposed_regex, w) is not None)}/{len(test_cases)}")
