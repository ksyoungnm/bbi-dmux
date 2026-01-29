#!/usr/bin/env python3
"""
Test script to verify the parse_fastq_barcodes bug fixes.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

import barcodeutils_bbi as bu

def test_validation_fix():
    """Test that validation correctly checks bc_property type."""
    print("="*70)
    print("Test 1: Validation type check fix")
    print("="*70)
    
    # This should fail if 'read' property is not a string
    bad_spec = {
        'test_barcode': {
            'start': 1,
            'end': 10,
            'read': 123,  # Invalid: should be string
            'whitelist': {'ATCGATCGAT'}
        }
    }
    
    valid, error = bu.validate_barcode_spec(bad_spec)
    if not valid and 'must be a string' in error:
        print("✓ Validation correctly rejects non-string 'read' property")
        print(f"  Error message: {error}")
        return True
    else:
        print("✗ Validation should have rejected non-string 'read' property")
        return False

def test_file_handle_fix():
    """Test that r2 file handle is created correctly."""
    print("\n" + "="*70)
    print("Test 2: R2 file handle creation fix")
    print("="*70)
    
    # Create temporary FASTQ files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fastq', delete=False) as r1_file:
        r1_file.write("@read1\n")
        r1_file.write("ATCGATCGAT\n")
        r1_file.write("+\n")
        r1_file.write("IIIIIIIIII\n")
        r1_path = r1_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fastq', delete=False) as r2_file:
        r2_file.write("@read1\n")
        r2_file.write("GCTAGCTAGC\n")
        r2_file.write("+\n")
        r2_file.write("IIIIIIIIII\n")
        r2_path = r2_file.name
    
    try:
        # Create a simple barcode spec
        spec = {
            'test_bc': {
                'start': 1,
                'end': 5,
                'read': 'r1',
                'whitelist': {'ATCGA'}
            }
        }
        
        # Try to parse - this should work now with the fix
        print("Attempting to parse FASTQ files with both r1 and r2...")
        try:
            # Parse just one read to test file handle creation
            parser = bu.parse_fastq_barcodes(r1_path, r2_path, spec=spec, edit_distance=1)
            entry = next(parser)
            print("✓ Successfully created file handles and parsed read")
            print(f"  Parsed entry keys: {list(entry.keys())}")
            return True
        except Exception as e:
            print(f"✗ Error parsing FASTQ files: {e}")
            import traceback
            traceback.print_exc()
            return False
    finally:
        # Clean up temp files
        os.unlink(r1_path)
        os.unlink(r2_path)

def main():
    print("Testing barcodeutils_bbi.py bug fixes")
    print("="*70)
    
    results = []
    results.append(test_validation_fix())
    results.append(test_file_handle_fix())
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓✓✓ All bug fixes verified!")
        return 0
    else:
        print("\n✗✗✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
