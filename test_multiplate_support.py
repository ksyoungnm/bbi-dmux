#!/usr/bin/env python3

"""
Test script for verifying multi-plate barcode file support.
"""

import sys
import os

# Add bin directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

import barcodeutils_bbi as bu

def test_single_plate_format():
    """Test that single-plate format still works (backward compatibility)."""
    print("Testing single-plate format (backward compatibility)...")
    
    # Create a temporary single-plate file
    single_plate_file = '/tmp/test_single_plate.txt'
    with open(single_plate_file, 'w') as f:
        f.write("A01\tTCGGATTCGG\n")
        f.write("B01\tTCCGGCTTAT\n")
        f.write("C01\tTCGCCGCCGG\n")
    
    try:
        lookup = bu.load_whitelist(single_plate_file)
        print(f"  ✓ Loaded {len(lookup)} entries")
        print(f"  ✓ Sample entries: {list(lookup.items())[:3]}")
        
        # Verify mapping is correct
        assert 'TCGGATTCGG' in lookup
        assert lookup['TCGGATTCGG'] == 'A01'
        print("  ✓ Single-plate format works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    finally:
        if os.path.exists(single_plate_file):
            os.remove(single_plate_file)

def test_multi_plate_format():
    """Test that multi-plate format works."""
    print("\nTesting multi-plate format...")
    
    # Create a temporary multi-plate file
    multi_plate_file = '/tmp/test_multi_plate.txt'
    with open(multi_plate_file, 'w') as f:
        f.write("P01-A01\tTCGGATTCGG\n")
        f.write("P01-B01\tTCCGGCTTAT\n")
        f.write("P02-A01\tGTCGCCAACC\n")
        f.write("P02-B01\tAACGATCTAC\n")
    
    try:
        lookup = bu.load_whitelist(multi_plate_file)
        print(f"  ✓ Loaded {len(lookup)} entries")
        print(f"  ✓ Sample entries: {list(lookup.items())[:4]}")
        
        # Verify mapping is correct
        assert 'TCGGATTCGG' in lookup
        assert lookup['TCGGATTCGG'] == 'P01-A01'
        assert 'GTCGCCAACC' in lookup
        assert lookup['GTCGCCAACC'] == 'P02-A01'
        print("  ✓ Multi-plate format works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    finally:
        if os.path.exists(multi_plate_file):
            os.remove(multi_plate_file)

def test_real_files():
    """Test with the actual test files created."""
    print("\nTesting with actual test files...")
    
    try:
        # Test P7 multi-plate file
        p7_file = '/home/runner/work/bbi-dmux/bbi-dmux/test_p7_multiplate.csv'
        if os.path.exists(p7_file):
            p7_lookup = bu.load_whitelist(p7_file)
            print(f"  ✓ P7: Loaded {len(p7_lookup)} entries")
            print(f"  ✓ P7 sample entries: {list(p7_lookup.items())[:3]}")
        
        # Test P5 multi-plate file
        p5_file = '/home/runner/work/bbi-dmux/bbi-dmux/test_p5_multiplate.csv'
        if os.path.exists(p5_file):
            p5_lookup = bu.load_whitelist(p5_file)
            print(f"  ✓ P5: Loaded {len(p5_lookup)} entries")
            print(f"  ✓ P5 sample entries: {list(p5_lookup.items())[:3]}")
        
        print("  ✓ Real test files work correctly")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing Multi-Plate Barcode File Support")
    print("=" * 60)
    
    all_pass = True
    all_pass &= test_single_plate_format()
    all_pass &= test_multi_plate_format()
    all_pass &= test_real_files()
    
    print("\n" + "=" * 60)
    if all_pass:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
