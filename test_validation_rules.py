#!/usr/bin/env python3
"""
Test and demonstrate PCR index file validation rules.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

import pcrindexutils as pu

def test_file(filename, expected_pass, description):
    """Test loading a PCR index file."""
    print(f"\n{'='*70}")
    print(f"Test: {description}")
    print(f"File: {filename}")
    print(f"Expected: {'PASS' if expected_pass else 'FAIL'}")
    print('='*70)
    
    try:
        pcr_list = pu.load_pcr_indexlist(filename)
        actual_pass = True
        print(f"Result: LOADED {len(pcr_list)} reactions")
    except SystemExit as e:
        actual_pass = False
        print(f"Result: VALIDATION FAILED (exit code {e.code})")
    except Exception as e:
        actual_pass = False
        print(f"Result: ERROR - {e}")
    
    if actual_pass == expected_pass:
        print("✓ Test passed as expected")
        return True
    else:
        print("✗ Test failed - unexpected result")
        return False

def main():
    print("="*70)
    print("PCR Index File Validation Test Suite")
    print("="*70)
    
    tests = [
        ('test_pcrprimers.csv', True, 
         'Original test file - same P5 seq with same P5 well, multiple P7 wells'),
        
        ('test_user_format.csv', True,
         'User format (PA-01A) - same P5 seq with same P5 well, multiple P7 wells'),
        
        ('test_standard_format.csv', True,
         'Standard format (P01-A01) - unique sequences per well'),
        
        ('test_duplicate_seq.csv', False,
         'Invalid: Same P5 sequence used with different P5 well IDs'),
    ]
    
    results = []
    for filename, expected, desc in tests:
        results.append(test_file(filename, expected, desc))
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All validation tests passed!")
        print("\nValidation Rules:")
        print("  1. Each P5 well ID must map to exactly one P5 sequence")
        print("  2. Each P5 sequence must map to exactly one P5 well ID")
        print("  3. Each P7 well ID must map to exactly one P7 sequence")
        print("  4. Each P7 sequence must map to exactly one P7 well ID")
        print("  5. Each (P5 well, P7 well) pair must be unique.")
        print("\nValid pattern (combinatorial barcoding):")
        print("  - Same P5 well + sequence paired with multiple P7 wells")
        print("  - Example: PA-A01 (seq1) + PA-01A (seq2), PA-01B (seq3), ...")
        print("\nInvalid pattern:")
        print("  - Same P5 sequence used with different P5 well IDs")
        print("  - Example: PA-A01 (seq1), PA-B01 (seq1) - ambiguous!")
        return 0
    else:
        print("\n✗ Some validation tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
