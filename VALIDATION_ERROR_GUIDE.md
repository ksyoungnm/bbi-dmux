# PCR Index File Validation Error - User Guide

## Problem

You're seeing many error messages like:
```
Error: P5 index sequence "CAGAAGCTAG" matches more than one well id in file
```

And then the pipeline exits with a traceback.

## What This Means

Your PCR index file has the same P5 index sequence appearing with **different P5 well IDs**. This creates ambiguity - when the pipeline sees that sequence, it can't determine which well it came from.

## Example of the Problem

**Invalid file (causes the error you're seeing):**
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-B01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← ERROR: Same P5 sequence, different P5 well!
```

In this example, the P5 sequence "GCTCTCGCCT" is used for both PA-A01 and PA-B01. When a read has this sequence, we can't tell if it came from well PA-A01 or PA-B01.

## How to Fix It

Each P5 sequence must map to exactly ONE P5 well ID, and each P7 sequence must map to exactly ONE P7 well ID.

**Option 1: Correct well IDs (if you made a typo)**
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-A01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← Fixed: Same P5 well ID
```

**Option 2: Use different sequences**
```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG
rxn2,PA-B01,CAGAAGCTAG,PA-01B,TCCGGCTTAT  ← Fixed: Different P5 sequence
```

## Valid Combinatorial Barcoding Pattern

It IS valid to use the same P5 well + sequence with multiple P7 wells:

```csv
pcr_rxn_name,p5_well,p5_index,p7_well,p7_index
rxn1,PA-A01,GCTCTCGCCT,PA-01A,TCGGATTCGG  ← Same P5 well
rxn2,PA-A01,GCTCTCGCCT,PA-01B,TCCGGCTTAT  ← Same P5 well, different P7
rxn3,PA-A01,GCTCTCGCCT,PA-01C,TCGCCGCCGG  ← Same P5 well, different P7
rxn4,PA-B01,CAGAAGCTAG,PA-01A,GTCGCCAACC  ← Different P5 well (and sequence)
```

This is the standard combinatorial indexing approach - one P5 well combined with multiple P7 wells.

## Validation Rules

Your file must satisfy ALL of these rules:

1. ✓ Each P5 well ID must map to exactly one P5 sequence
2. ✓ Each P5 sequence must map to exactly one P5 well ID
3. ✓ Each P7 well ID must map to exactly one P7 sequence
4. ✓ Each P7 sequence must map to exactly one P7 well ID
5. ✓ Each (P5 well, P7 well) pair must be unique.

## How to Check Your File

Run this command to check which sequences are problematic:

```bash
# Check P5 sequences
awk -F',' 'NR>1 {print $3 "," $2}' your_file.csv | sort | uniq -c | awk '$1>1'

# Check P7 sequences
awk -F',' 'NR>1 {print $5 "," $4}' your_file.csv | sort | uniq -c | awk '$1>1'
```

Any output means you have duplicate mappings that need to be fixed.

## What Changed

Previously, the pipeline would print these error messages but continue running, then fail later with a confusing traceback. Now it fails immediately with a clear error message so you can fix the file before wasting time on a failed run.

## Need Help?

1. Check your PCR index file for duplicate sequence-to-well mappings
2. Ensure each P5 sequence is used with only one P5 well ID
3. Ensure each P7 sequence is used with only one P7 well ID
4. Run the validation test to confirm: `python3 test_validation_rules.py`
