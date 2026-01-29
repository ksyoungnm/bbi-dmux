# Multi-Plate PCR Index Support - Summary

## Good News!

The functionality you requested **already exists** in bbi-dmux! You can provide multi-plate P5 and P7 index mappings using the `params.pcr_index_pair_file` parameter.

## What Was Done

This PR clarifies and documents the existing multi-plate support feature. No code changes were needed - the feature has been available all along through the `pcr_index_pair_file` configuration option.

## How to Use Multi-Plate Support

### Quick Start

1. **Create a CSV file** with your PCR index mappings:

```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
P01_rxn1,P01-A01,GCTCTCGCCT,P01-A01,TCGGATTCGG
P01_rxn2,P01-A01,GCTCTCGCCT,P01-B01,TCCGGCTTAT
P02_rxn1,P02-A01,CTCCATCGAG,P02-A01,GTCGCCAACC
P02_rxn2,P02-A01,CTCCATCGAG,P02-B01,AACGATCTAC
```

2. **Configure your experiment** in `experiment.config`:

```javascript
// Point to your PCR index file
params.pcr_index_pair_file = "/path/to/your/pcr_indexes.csv"

// Remove these if present (incompatible with pcr_index_pair_file):
// params.p5_cols
// params.p7_rows
// params.p5_wells
// params.p7_wells
// params.p5_barcode_file
// params.p7_barcode_file
```

3. **Run the pipeline** as usual:

```bash
nextflow run bbi-dmux -c experiment.config
```

## Key Features

✓ **Plate Prefixes**: Use P01, P02, P03, etc. to identify plates
✓ **Exact Mapping**: Specify exactly which P5 and P7 index identifies each well
✓ **Flexible**: Support for any number of plates
✓ **Validated**: Built-in validation for well IDs and sequences
✓ **Tested**: Feature is proven and working (see demo_multiplate_support.py)

## Documentation

Three resources are now available:

1. **MULTIPLATE_PCR_INDEXES.md**: Comprehensive guide with:
   - Detailed file format specifications
   - Multiple examples
   - Comparison of all configuration options
   - Troubleshooting guide

2. **demo_multiplate_support.py**: Working demonstration script showing:
   - How to create a multi-plate PCR index file
   - How the file is loaded and processed
   - What the output looks like

3. **example.config**: Enhanced documentation of the pcr_index_pair_file option

## Example

Here's a complete example for a two-plate experiment:

**File: `my_experiment_pcr_indexes.csv`**
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
plate1_combo1,P01-A01,GCTCTCGCCT,P01-A01,TCGGATTCGG
plate1_combo2,P01-A01,GCTCTCGCCT,P01-A02,TCCGGCTTAT
plate1_combo3,P01-A02,CAGAAGCTAG,P01-A01,TCGGATTCGG
plate1_combo4,P01-A02,CAGAAGCTAG,P01-A02,TCCGGCTTAT
plate2_combo1,P02-B01,CTCCATCGAG,P02-B01,GTCGCCAACC
plate2_combo2,P02-B01,CTCCATCGAG,P02-B02,AACGATCTAC
plate2_combo3,P02-B02,TTGGTAGTCG,P02-B01,GTCGCCAACC
plate2_combo4,P02-B02,TTGGTAGTCG,P02-B02,AACGATCTAC
```

**Configuration:**
```javascript
params.pcr_index_pair_file = "/path/to/my_experiment_pcr_indexes.csv"
```

That's it! The pipeline will correctly demultiplex reads from both plates.

## Demonstration

Run the included demonstration script to see the feature in action:

```bash
python3 demo_multiplate_support.py
```

Output shows:
- Loading of multi-plate PCR index file
- Creation of P5 and P7 whitelists with plate prefixes
- Valid PCR combinations across multiple plates

## What Changed in This PR

### Documentation Added/Updated:
- ✓ Created MULTIPLATE_PCR_INDEXES.md (comprehensive guide)
- ✓ Created demo_multiplate_support.py (working demonstration)
- ✓ Updated example.config (clarified options)
- ✓ Updated README.md (highlighted feature)
- ✓ Updated .gitignore (proper Python cache exclusion)

### Code Changes:
- **None** - The feature already existed and is working correctly

## Why This Approach?

During implementation, I discovered that:

1. The `pcr_index_pair_file` parameter **already fully supports** multi-plate format
2. It provides **exactly** what you requested: "exact mapping between a given well in a given plate, and the exact p5 and p7 index that identifies that well"
3. The feature was already implemented, tested, and working
4. The only issue was lack of documentation

So instead of modifying code, I focused on creating comprehensive documentation to help you and other users discover and use this existing feature.

## Questions?

- See **MULTIPLATE_PCR_INDEXES.md** for detailed information
- Run **demo_multiplate_support.py** to see it working
- Check **example.config** for all configuration options

The multi-plate support is ready to use right now!
