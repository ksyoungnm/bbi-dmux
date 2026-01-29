# PCR Index Validation Fix - Complete Summary

## Issue Resolved

User reported getting many error messages but the pipeline continued and failed later:
```
Error: P5 index sequence "CAGAAGCTAG" matches more than one well id in file
```
Then: `Traceback (most recent call last)...`

## Root Cause

The PCR index file validation in `bin/pcrindexutils.py` had incomplete error handling. Four validation checks (lines 187-229) would print error messages to stderr but didn't set `errorFlag = 1`, causing the validation to return True (success) even though the file was invalid.

This led to:
1. ❌ Error messages printed (confusing the user)
2. ❌ Validation passed (invalid data continued)
3. ❌ Silent data corruption in `make_pcr_whitelist()` dictionary
4. ❌ Pipeline failed later with confusing traceback

## The Fix

Added `errorFlag = 1` to four validation checks in `bin/pcrindexutils.py`:
- Line 194: When P5 well ID maps to multiple sequences
- Line 206: When P5 sequence maps to multiple well IDs ← User's issue
- Line 216: When P7 well ID maps to multiple sequences  
- Line 228: When P7 sequence maps to multiple well IDs

Now the validation properly fails immediately with a clear error message.

## Why This Validation Matters

In the downstream code (`make_pcr_whitelist()` at line 381), a dictionary is built:
```python
whitelist[sequence] = well_id
```

If the same sequence appears with different well IDs, the dictionary silently overwrites earlier entries with later ones, causing data corruption. The validation prevents this by ensuring each sequence uniquely identifies a well.

## What's Valid vs Invalid

### ✓ Valid: Combinatorial Barcoding
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-A01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← Same P5 well+seq, different P7
rxn3,PA-A01,GCTCTCGCCT,PA-01C,TCGCCGCCGG  ← Same P5 well+seq, different P7
```
This is valid - one P5 well combined with multiple P7 wells.

### ✗ Invalid: Ambiguous Sequence Mapping
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-B01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← ERROR: Same P5 seq, different P5 well!
```
This is invalid - when you see sequence GCTCTCGCCT, you can't tell if it's from well PA-A01 or PA-B01.

## Validation Rules

Your PCR index file must satisfy ALL of these rules:

1. Each P5 well ID must map to exactly one P5 sequence
2. Each P5 sequence must map to exactly one P5 well ID
3. Each P7 well ID must map to exactly one P7 sequence
4. Each P7 sequence must map to exactly one P7 well ID
5. Each (P5 well, P7 well) pair must be unique

## How to Fix Your File

The user needs to ensure their PCR index file has unique sequence-to-well mappings.

**Option 1: If it's a typo - use the correct well ID**
```csv
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-A01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← Fixed: same P5 well
```

**Option 2: Use different sequences for different wells**
```csv
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-B01,CAGAAGCTAG,PA-01B,TCCGGCTTAT  ← Fixed: different P5 sequence
```

## How to Check Your File

Run these commands to find problematic entries:

```bash
# Check for P5 sequences mapped to multiple wells
awk -F',' 'NR>1 {print $3 "," $2}' your_file.csv | sort | uniq -c | awk '$1>1'

# Check for P7 sequences mapped to multiple wells
awk -F',' 'NR>1 {print $5 "," $4}' your_file.csv | sort | uniq -c | awk '$1>1'
```

Any output indicates duplicate mappings that need to be fixed.

## Files Modified

1. **bin/pcrindexutils.py** - Added errorFlag to 4 validation checks
2. **test_validation_rules.py** - Comprehensive test suite
3. **test_duplicate_seq.csv** - Example invalid file for testing
4. **VALIDATION_ERROR_GUIDE.md** - Detailed user guide
5. **test_user_format.csv** - Updated to be valid

## Testing

All tests pass:
- ✅ Valid files (test_pcrprimers.csv, test_user_format.csv, test_standard_format.csv) load successfully
- ✅ Invalid file (test_duplicate_seq.csv) fails validation immediately
- ✅ Comprehensive test suite (test_validation_rules.py) passes 4/4 tests
- ✅ Code review passed
- ✅ Security scan passed (0 alerts)

Run the test suite: `python3 test_validation_rules.py`

## Before vs After

**Before:**
```
Error: P5 index sequence "X" matches more than one well id  ← Error printed
✗ Validation returns True (success)                         ← Bug!
✗ Pipeline continues with invalid data
✗ Silent data corruption in dictionary
✗ Confusing failure later
```

**After:**
```
Error: P5 index sequence "X" matches more than one well id  ← Error printed
✓ Validation returns False (failure)                        ← Fixed!
✓ Pipeline stops immediately
✓ Clear error message
✓ User can fix file before running pipeline
```

## Documentation

See these files for more information:
- **VALIDATION_ERROR_GUIDE.md** - User-friendly guide with examples
- **test_validation_rules.py** - Runnable test demonstrating rules
- **bin/pcrindexutils.py** - Implementation details

## Summary

The fix ensures that PCR index file validation properly fails when sequences are ambiguous, preventing silent data corruption and confusing later failures. Users now get immediate, clear feedback to fix their files before running the pipeline.
