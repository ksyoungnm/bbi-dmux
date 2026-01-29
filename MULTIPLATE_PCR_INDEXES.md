# Multi-Plate PCR Index Support in bbi-dmux

## Overview

This document explains how to configure bbi-dmux for experiments with PCR indexes spanning multiple plates. The `params.pcr_index_pair_file` parameter provides the most flexible way to specify exact mappings between wells in multiple plates and their corresponding P5 and P7 indexes.

## Problem Statement

In single-cell experiments, PCR indexes (P5 and P7) are used to identify samples. Previously, users might have assumed that custom P5 and P7 barcode files only supported single-plate experiments. This document clarifies how to properly configure multi-plate experiments.

## Solution: Use pcr_index_pair_file

The `params.pcr_index_pair_file` parameter (Option 3 in the configuration) **already supports multi-plate scenarios** and provides the exact functionality needed for multi-plate experiments.

### File Format

The PCR index pair file is a CSV file with the following structure:

**Header (required):**
```
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
```

**Data rows:**
Each row specifies:
- `pcr_rxn_name`: A unique identifier for this PCR reaction
- `p5_well`: The P5 well ID (can include plate prefix)
- `p5_index`: The P5 index sequence
- `p7_well`: The P7 well ID (can include plate prefix)
- `p7_index`: The P7 index sequence

### Single-Plate Format

Without plate prefixes (original format):
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn_1,A05,GCTCTCGCCT,B06,TCGGATTCGG
rxn_2,A05,GCTCTCGCCT,B07,TCCGGCTTAT
rxn_3,A06,CAGAAGCTAG,B06,TCGGATTCGG
rxn_4,A06,CAGAAGCTAG,B07,TCCGGCTTAT
```

### Multi-Plate Format

With plate prefixes (for multi-plate experiments):
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn_1,P01-A05,GCTCTCGCCT,P01-B06,TCGGATTCGG
rxn_2,P01-A05,GCTCTCGCCT,P01-B07,TCCGGCTTAT
rxn_3,P01-A06,CAGAAGCTAG,P01-B06,TCGGATTCGG
rxn_4,P02-A05,CTCCATCGAG,P02-B06,GTCGCCAACC
rxn_5,P02-A05,CTCCATCGAG,P02-B07,AACGATCTAC
rxn_6,P03-A05,TTGGTAGTCG,P03-B06,AACCGACCTC
```

**Format specifications:**
- Plate ID format: `Pnn` where `nn` are decimal digits (e.g., P01, P02, P10, P99)
- Well format: `<row><column>` where:
  - `<row>` is a letter A-H
  - `<column>` is a number 01-12
- Complete well ID format: `Pnn-<row><column>` (e.g., P01-A05, P02-B06)
- All alphabetic characters are converted to upper case when the file is read
- `none` is permitted in either the p5_index or p7_index column but not both
- If `none` is in any row, it must be in all rows

## Usage Example

### 1. Create Your PCR Index Pair File

Create a file named `my_pcr_indexes.csv`:

```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
plate1_rxn1,P01-A01,GCTCTCGCCT,P01-A01,TCGGATTCGG
plate1_rxn2,P01-A01,GCTCTCGCCT,P01-B01,TCCGGCTTAT
plate1_rxn3,P01-B01,CAGAAGCTAG,P01-A01,TCGGATTCGG
plate1_rxn4,P01-B01,CAGAAGCTAG,P01-B01,TCCGGCTTAT
plate2_rxn1,P02-A01,CTCCATCGAG,P02-A01,GTCGCCAACC
plate2_rxn2,P02-A01,CTCCATCGAG,P02-B01,AACGATCTAC
plate2_rxn3,P02-B01,TTGGTAGTCG,P02-A01,GTCGCCAACC
plate2_rxn4,P02-B01,TTGGTAGTCG,P02-B01,AACGATCTAC
```

### 2. Configure Your Experiment

In your `experiment.config` file:

```javascript
// Specify the PCR index pair file
params.pcr_index_pair_file = "/path/to/my_pcr_indexes.csv"

// DO NOT use these parameters with pcr_index_pair_file:
// params.p5_cols
// params.p7_rows
// params.p5_wells
// params.p7_wells
// params.multi_exp
// params.p5_barcode_file
// params.p7_barcode_file
```

### 3. Run the Pipeline

```bash
nextflow run bbi-dmux -c experiment.config
```

## Key Points

1. **Exact Mapping**: The PCR index pair file provides an exact, explicit mapping between each well (in each plate) and its corresponding P5 and P7 indexes.

2. **Flexible**: You can specify any combination of P5 and P7 wells across multiple plates. Each row in the file represents one PCR reaction.

3. **No Plate Assumptions**: Unlike the row/column approach, there are no assumptions about plate layout or which wells were used.

4. **Exclusive Parameters**: The `pcr_index_pair_file` parameter cannot be used in combination with:
   - `p5_cols` / `p7_rows`
   - `p5_wells` / `p7_wells`
   - `multi_exp`
   - `p5_barcode_file` / `p7_barcode_file`

## Comparison of Configuration Options

### Option 1: Rows and Columns (Single Plate)
```javascript
params.p7_rows = 'D E'
params.p5_cols = '4 5'
```
- **Use case**: Simple experiments with one plate using specific rows and columns
- **Limitation**: Single plate only

### Option 2: Well IDs (Single Plate)
```javascript
params.p7_wells = 'D3 E3'
params.p5_wells = 'B2 B7'
```
- **Use case**: Few wells from one plate
- **Limitation**: Single plate only

### Option 3: PCR Index Pair File (Multi-Plate)
```javascript
params.pcr_index_pair_file = "/path/to/file.csv"
```
- **Use case**: Multi-plate experiments, complex layouts, exact control
- **Advantage**: Supports multiple plates with explicit plate IDs
- **Advantage**: Provides exact mapping of each PCR reaction

### Option 4: Multi-Exp (Multiple Experiments, Single Plate Per Experiment)
```javascript
params.multi_exp = "{'Exp1':('D E', '4 5'), 'Exp2':('F', '3')}"
```
- **Use case**: Multiple experiments, each with their own plate/wells
- **Limitation**: Each experiment still limited to one plate

## Example: Two-Plate Experiment

Suppose you have:
- Plate 1 (P01): Uses wells A01-A12 for P5, wells A01-H01 for P7
- Plate 2 (P02): Uses wells B01-B12 for P5, wells A02-H02 for P7

Your PCR index pair file would explicitly list all combinations:

```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
P01_combo1,P01-A01,GCTCTCGCCT,P01-A01,TCGGATTCGG
P01_combo2,P01-A01,GCTCTCGCCT,P01-B01,TCCGGCTTAT
...
P02_combo1,P02-B01,CTCCATCGAG,P02-A02,GTCGCCAACC
P02_combo2,P02-B01,CTCCATCGAG,P02-B02,AACGATCTAC
...
```

## Validation

The pipeline performs several validation checks on the PCR index pair file:

1. **Header validation**: The file must have the correct header
2. **Well ID format**: Well IDs must match the expected format
3. **Index sequences**: Must contain only valid DNA bases (A, T, G, C)
4. **Uniqueness**: P5/P7 sequence pairs must be unique
5. **Consistency**: If plate prefixes are used, they should be consistent

## Troubleshooting

### Issue: "Missing header in file"
**Solution**: Ensure the first line of your CSV file is exactly:
```
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
```

### Issue: "bad P5 well name" or "bad P7 well name"
**Solution**: Check that well IDs follow the correct format:
- Without plate prefix: A01, B05, H12
- With plate prefix: P01-A01, P02-B05, P10-H12

### Issue: "P5 and P7 index sequence pair occurs more than once"
**Solution**: Each combination of P5 and P7 sequences must be unique in your file. Check for duplicate rows.

### Issue: Conflicts with other parameters
**Solution**: Remove any `p5_cols`, `p7_rows`, `p5_wells`, `p7_wells`, `multi_exp`, `p5_barcode_file`, or `p7_barcode_file` parameters from your config when using `pcr_index_pair_file`.

## Additional Resources

- See `test_pcrprimers.csv` in the repository for an example file
- See `bin/pcrindexutils.py` for the implementation details
- See `example.config` for all configuration options

## Summary

For multi-plate PCR index experiments:
- ✓ Use `params.pcr_index_pair_file` for complete control
- ✓ Support for explicit plate IDs (P01, P02, etc.)
- ✓ Exact mapping of each PCR reaction
- ✓ No assumptions about plate layout
- ✓ Validated file format with helpful error messages
- ✓ Already implemented and tested in bbi-dmux
