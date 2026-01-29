# PCR Well ID Validation Fix - Summary

## Problem Solved

You reported an error when trying to use a PCR index file with well IDs in the format `PA-01A`:

```
Error: bad P5 well name in row 2 of PCR reaction file
```

This error occurred because the validation regex was too restrictive and only accepted well IDs in the format `P01-A01` (P followed by digits, hyphen, row letter, column number).

## Solution

The validation has been updated to accept flexible well ID formats that are commonly used:

### Now Supported Formats

**With plate prefix:**
- `PA-01A`, `PB-12H` - Alphanumeric plate ID with column-row format (YOUR FORMAT ✓)
- `PA-A01`, `PB-B05` - Alphanumeric plate ID with row-column format
- `PA_A01`, `PB_B05` - Underscore separator instead of hyphen
- `P01-A01`, `P1-B05` - Original numeric plate format (backward compatible)

**Without plate prefix:**
- `A01`, `H12` - Standard row-column format
- `01A`, `12H` - Column-row format

## What Changed

**File:** `bin/pcrindexutils.py`

**Old regex (lines 88, 97):**
```python
^([pP][0-9]+[-])?[a-hA-H]([0][1-9]|[1][0-2])$
```
This only accepted:
- Plate IDs: P followed by digits (P1, P01, P10)
- Separator: Hyphen only
- Well format: Row-column only (A01)

**New regex:**
```python
^([a-zA-Z][a-zA-Z0-9]*[-_])?([a-hA-H]([0][1-9]|[1][0-2])|([0][1-9]|[1][0-2])[a-hA-H])$
```
This now accepts:
- Plate IDs: Any alphanumeric starting with a letter (PA, PB, P01, P1A)
- Separator: Hyphen (-) or underscore (_)
- Well format: Row-column (A01) or column-row (01A)

## Testing

Your exact format now works:

```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
test_1,PA-01A,GCTCTCGCCT,PA-01A,TCGGATTCGG
test_2,PA-01B,GCTCTCGCCT,PA-01B,TCCGGCTTAT
test_3,PA-01C,GCTCTCGCCT,PA-01C,TCGCCGCCGG
```

✓ Loads successfully without errors
✓ All validation checks pass
✓ Backward compatible with existing formats

## How to Use

Your PCR index file format `PA-01A` will now work directly with the pipeline command:

```bash
pypy3 /path/to/make_sample_fastqs.py \
  --pcr_index_pair_file /path/to/your/pcr_index_file.csv \
  ...other parameters...
```

No changes needed to your file - the validation now accepts your format.

## Files Modified

- `bin/pcrindexutils.py` - Updated validation regex and documentation
- Test files created to validate all formats

## Backward Compatibility

✅ All previously valid well ID formats continue to work
✅ No breaking changes
✅ Only expands what formats are accepted

## Testing Performed

1. ✓ User format (PA-01A) - Successfully loads
2. ✓ Existing test file (192 entries with PA_A01, PA-01A) - Successfully loads
3. ✓ Standard format (P01-A01, A01) - Backward compatible
4. ✓ Code review passed
5. ✓ Security scan passed (0 alerts)

Your PCR index file should now work without any errors!
