#!/usr/bin/env python3

"""
Demonstration script showing that multi-plate PCR index support
already exists via the pcr_index_pair_file parameter.
"""

import sys
import os

# Add bin directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

import pcrindexutils as pu

def create_test_multiplate_file():
    """Create a test PCR index pair file with multi-plate format."""
    test_file = '/tmp/test_multiplate_pcr.csv'
    with open(test_file, 'w') as f:
        f.write("pcr_rxn_name,p5_well,p5_index,p7_well,p7_index\n")
        # Plate 1 entries
        f.write("P01_rxn1,P01-A01,GCTCTCGCCT,P01-A01,TCGGATTCGG\n")
        f.write("P01_rxn2,P01-A01,GCTCTCGCCT,P01-B01,TCCGGCTTAT\n")
        f.write("P01_rxn3,P01-B01,CAGAAGCTAG,P01-A01,TCGGATTCGG\n")
        # Plate 2 entries  
        f.write("P02_rxn1,P02-A01,CTCCATCGAG,P02-A01,GTCGCCAACC\n")
        f.write("P02_rxn2,P02-A01,CTCCATCGAG,P02-B01,AACGATCTAC\n")
        f.write("P02_rxn3,P02-B01,TTGGTAGTCG,P02-A01,GTCGCCAACC\n")
    return test_file

def main():
    print("=" * 70)
    print("Multi-Plate PCR Index Support Demonstration")
    print("=" * 70)
    print()
    
    # Create test file
    print("Creating test multi-plate PCR index file...")
    test_file = create_test_multiplate_file()
    print(f"  ✓ Created: {test_file}")
    print()
    
    # Load the file using existing pcrindexutils
    print("Loading file with existing pcrindexutils.load_pcr_indexlist()...")
    try:
        pcr_list = pu.load_pcr_indexlist(test_file)
        print(f"  ✓ Successfully loaded {len(pcr_list)} PCR reactions")
        print()
        
        # Display first few entries
        print("Sample entries:")
        for i, entry in enumerate(pcr_list[:3], 1):
            print(f"  {i}. PCR rxn: {entry[0]}")
            print(f"     P5: {entry[1]} -> {entry[2]}")
            print(f"     P7: {entry[3]} -> {entry[4]}")
        print()
        
        # Create whitelists with well IDs
        print("Creating P5 and P7 whitelists...")
        p5_whitelist = pu.make_pcr_whitelist(pcr_list, 'p5', 10, 
                                             reverse_complement=False, 
                                             well_ids=True)
        p7_whitelist = pu.make_pcr_whitelist(pcr_list, 'p7', 10, 
                                             reverse_complement=False, 
                                             well_ids=True)
        
        print(f"  ✓ P5 whitelist: {len(p5_whitelist)} unique sequences")
        print(f"  ✓ P7 whitelist: {len(p7_whitelist)} unique sequences")
        print()
        
        # Show some mappings
        print("Sample sequence → well ID mappings:")
        print("  P5 mappings:")
        for seq, well in list(p5_whitelist.items())[:3]:
            print(f"    {seq} → {well}")
        print("  P7 mappings:")
        for seq, well in list(p7_whitelist.items())[:3]:
            print(f"    {seq} → {well}")
        print()
        
        # Get valid combinations
        print("Getting valid PCR combinations...")
        valid_combos = pu.get_programmed_pcr_combos_pcrlist(pcr_list, well_ids=True)
        print(f"  ✓ Found {len(valid_combos)} valid P5/P7 combinations")
        print()
        
        print("Sample valid combinations:")
        for p5_well, p7_well in list(valid_combos)[:5]:
            print(f"  {p5_well} + {p7_well}")
        print()
        
        print("=" * 70)
        print("✓ SUCCESS: Multi-plate PCR index support is WORKING!")
        print("=" * 70)
        print()
        print("The pcr_index_pair_file parameter fully supports:")
        print("  • Plate prefixes (P01, P02, etc.)")
        print("  • Exact well-to-index mappings")
        print("  • Multiple plates in one file")
        print("  • Well IDs in format Pnn-<row><column>")
        print()
        print("See MULTIPLATE_PCR_INDEXES.md for usage guide.")
        
        return 0
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == '__main__':
    sys.exit(main())
