# Multi-Plate P5/P7 Index Support

## Overview

This document describes the multi-plate index support feature for P5 and P7 barcode files in bbi-dmux. Previously, the pipeline only supported single-plate (96-well) barcode files. Now you can specify multiple plates worth of indexes in a single file.

## Background

In single-cell experiments, PCR indexes (P5 and P7) are used to identify samples. Previously, when providing custom P5 and P7 barcode files, the system assumed you were working with a single 96-well plate (wells A01-H12). This limitation prevented users from working with experiments spanning multiple plates.

## New Feature: Multi-Plate Support

The barcode file format now supports plate prefixes, allowing you to specify indexes from multiple plates in a single file. This enables experiments with hundreds or thousands of wells across multiple plates.

## File Formats

### Single-Plate Format (Backward Compatible)

The original format continues to work as before:

```
A01	TCCTACCAGT
A02	GCGTTGGAGC
A03	GATCTTACGC
B01	AGTCGATTCA
B02	GCATTAGCCT
...
```

This format assumes all wells are from a single plate and can contain up to 96 wells (A01-H12).

### Multi-Plate Format (New)

The new format includes plate identifiers:

```
P01-A01	TCCTACCAGT
P01-A02	GCGTTGGAGC
P01-A03	GATCTTACGC
P02-A01	AGTCGATTCA
P02-A02	GCATTAGCCT
P02-A03	TTACGCGATT
P03-A01	GCATTGCATG
...
```

**Format specifications:**
- Plate ID format: `Pnn` where `nn` are decimal digits (e.g., P01, P02, P10, P99)
- Well format: `<row><column>` where:
  - `<row>` is a letter A-H
  - `<column>` is a number 01-12
- Complete well ID format: `Pnn-<row><column>` (e.g., P01-A01, P02-B05)
- File format: Tab-separated, one well per line: `<well_id><TAB><sequence>`

## Usage

### In Configuration Files

Specify your custom barcode files in your experiment configuration:

```javascript
// For P5 barcodes
params.p5_barcode_file = "/path/to/your/p5_multiplate_barcodes.txt"

// For P7 barcodes
params.p7_barcode_file = "/path/to/your/p7_multiplate_barcodes.txt"
```

### Creating Your Barcode Files

1. **Decide on your plate numbering scheme**: Use sequential plate numbers (P01, P02, P03, etc.)

2. **Create a tab-separated file**: Each line should contain a well ID and its corresponding index sequence

3. **Example P7 multi-plate file** (`my_p7_barcodes.txt`):
```
P01-A01	TCGGATTCGG
P01-B01	TCCGGCTTAT
P01-C01	TCGCCGCCGG
P01-D01	TTGGCAAGCC
P02-A01	GTCGCCAACC
P02-B01	AACGATCTAC
P02-C01	AACCGACCTC
P02-D01	AGGAGCGCGT
```

4. **Example P5 multi-plate file** (`my_p5_barcodes.txt`):
```
P01-A01	GCTCTCGCCT
P01-B01	CAGAAGCTAG
P01-C01	TACAACGCGT
P01-D01	GTCGTTAAGC
P02-A01	CTCCATCGAG
P02-B01	TTGGTAGTCG
P02-C01	AGGTCAATTA
P02-D01	CCTAGACGAG
```

## Examples

### Example 1: Two-Plate Experiment

If you have two plates of samples:
- Plate 1 (P01): Uses wells A01-H12 with one set of indexes
- Plate 2 (P02): Uses wells A01-H12 with different indexes

Your P7 barcode file would contain 192 entries (96 from P01 + 96 from P02), each with the format `Pnn-<well>`.

### Example 2: Partial Plates

You don't need to specify all 96 wells. If you only used specific wells:

```
P01-A01	TCGGATTCGG
P01-A02	TCCGGCTTAT
P01-B01	TCGCCGCCGG
P02-A01	GTCGCCAACC
P02-A02	AACGATCTAC
```

This is valid and will only demultiplex reads matching these specific well combinations.

### Example 3: Many Plates

For experiments with many plates, continue the numbering:

```
P01-A01	SEQUENCE1
P02-A01	SEQUENCE2
P03-A01	SEQUENCE3
...
P10-A01	SEQUENCE10
P11-A01	SEQUENCE11
...
```

## Validation and Error Checking

The pipeline performs several validation checks:
1. **Sequence validation**: All sequences must contain only valid DNA bases (A, T, G, C, N)
2. **Well ID format**: Well IDs must follow the correct format (Pnn-<row><column> or <row><column>)
3. **Uniqueness**: Each sequence must be unique within the file
4. **Consistency**: If using multi-plate format, all entries should use the same format

## Backward Compatibility

All existing single-plate barcode files will continue to work without modification. The system automatically detects whether you're using single-plate or multi-plate format based on the well ID format.

## Testing

Test files demonstrating the multi-plate format are included:
- `test_p5_multiplate.csv`: Example P5 multi-plate barcode file
- `test_p7_multiplate.csv`: Example P7 multi-plate barcode file
- `test_multiplate_support.py`: Test script validating the functionality

To run the tests:
```bash
python3 test_multiplate_support.py
```

## Relationship to pcr_index_pair_file

Note that the `params.pcr_index_pair_file` option (Option 3 in example.config) already supported plate prefixes in a different format. The new multi-plate barcode file support provides an alternative way to specify indexes when you're using the p5_barcode_file/p7_barcode_file approach (which pairs with p7_rows/p5_cols or p7_wells/p5_wells).

## Common Issues and Troubleshooting

### Issue: "Whitelist entry X is not a DNA sequence"
**Solution**: Check that all sequences contain only A, T, G, C, or N characters. Remove any special characters or ensure proper encoding.

### Issue: Mixing single-plate and multi-plate formats
**Solution**: Choose one format and use it consistently throughout your file. Don't mix entries like `A01` and `P01-A01` in the same file.

### Issue: Plate numbering doesn't match sample sheet
**Solution**: Ensure your plate numbering in the barcode file matches your experimental design and sample sheet.

## Questions and Support

For questions or issues:
1. Check the example files in the repository
2. Review the test script for usage examples
3. Open an issue on the GitHub repository with detailed information about your experiment setup

## Summary

Multi-plate support enables:
- ✓ Experiments spanning multiple plates
- ✓ Better organization of large-scale experiments
- ✓ Explicit plate identification in well names
- ✓ Backward compatibility with existing files
- ✓ Flexible well selection (partial plates supported)
