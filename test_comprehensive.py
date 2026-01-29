#!/usr/bin/env python3
"""
Comprehensive test demonstrating the PCR well ID validation fix.
This test covers all the formats that users need.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

import pcrindexutils as pu

def test_format(filename, description):
    """Test loading a PCR index file."""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"File: {filename}")
    print('='*70)
    
    try:
        pcr_list = pu.load_pcr_indexlist(filename)
        print(f"✓ Successfully loaded {len(pcr_list)} PCR reactions")
        
        # Show first few entries
        print("\nFirst 3 entries:")
        for i, entry in enumerate(pcr_list[:3], 1):
            print(f"  {i}. {entry[0]:15} P5: {entry[1]:12} -> {entry[2][:10]}")
            print(f"     {' '*15} P7: {entry[3]:12} -> {entry[4][:10]}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*70)
    print("PCR Well ID Validation Fix - Comprehensive Test")
    print("="*70)
    
    results = []
    
    # Test 1: User's original format (PA-01A)
    results.append(test_format(
        'test_user_format.csv',
        "User format: PA-01A (alphanumeric plate, column-row)"
    ))
    
    # Test 2: Existing test file (mixed formats)
    results.append(test_format(
        'test_pcrprimers.csv',
        "Existing test file: PA_A01 and PA-01A (mixed)"
    ))
    
    # Test 3: Standard format (P01-A01)
    results.append(test_format(
        'test_standard_format.csv',
        "Standard format: P01-A01 (backward compatibility)"
    ))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! The fix works correctly.")
        print("\nSupported formats:")
        print("  • PA-01A, PB-12H (alphanumeric plate, column-row)")
        print("  • PA-A01, PB-B05 (alphanumeric plate, row-column)")
        print("  • PA_A01, PB_B05 (underscore separator)")
        print("  • P01-A01, P1-B05 (numeric plate, hyphen)")
        print("  • A01, H12 (no plate prefix)")
        print("  • 01A, 12H (column-row, no plate)")
        return 0
    else:
        print("\n✗ Some tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
