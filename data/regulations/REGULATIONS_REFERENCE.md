# Regulations Reference Guide

**Date**: February 16, 2026  
**Author**: Nawddeep  
**Purpose**: Reference documentation for compliance rules

---

## 📚 Available Regulation Documents

### Source PDFs (Reference Only)

Located in: `data/regulations/source_pdfs/`

1. **Schedule_III.pdf** (924 KB)
   - Companies Act 2013 - Schedule III
   - Format for Balance Sheet and P&L Statement
   - Disclosure requirements for financial statements

2. **SEBI_LODR.pdf** (398 KB)
   - SEBI Listing Obligations and Disclosure Requirements
   - Corporate governance requirements
   - Quarterly/Annual reporting requirements

3. **schedulefile.pdf** (922 KB)
   - Additional Schedule III reference

---

## 🎯 How Rules Are Used

### Current System (Stage 1)

The system uses **rules_index.json** which contains:
- 13 accounting standards
- 38 compliance checks
- Keyword-based pattern matching

**Location**: `data/regulations/rules_index.json`

### Rule Structure

```json
{
  "IndAS-1": {
    "name": "Presentation of Financial Statements",
    "category": "Financial Statements",
    "priority": "HIGH",
    "checks": [
      {
        "check_id": "IndAS1-1",
        "requirement": "Balance Sheet",
        "keywords": ["balance sheet", "statement of financial position"],
        "mandatory": true
      }
    ]
  }
}
```

---

## 📖 Reading Regulation PDFs

### Quick View Command

```bash
# View Schedule III
open data/regulations/source_pdfs/Schedule_III.pdf

# View SEBI LODR
open data/regulations/source_pdfs/SEBI_LODR.pdf
```

### Extract Text from PDF

```bash
# Activate virtual environment
source .venv/bin/activate

# Extract text from regulation PDF
python3 -c "
from src.document_processor import DocumentProcessor
proc = DocumentProcessor(verbose=False)
result = proc.extract_text_from_pdf('data/regulations/source_pdfs/Schedule_III.pdf', max_pages=10)
print(result['text'][:2000])
"
```

---

## 🔧 Adding New Rules

### Step 1: Read Regulation PDF

Open the PDF and identify key requirements:
```bash
open data/regulations/source_pdfs/Schedule_III.pdf
```

### Step 2: Extract Key Requirements

Look for phrases like:
- "shall disclose"
- "must present"
- "requires disclosure of"
- "mandatory to include"

### Step 3: Add to rules_index.json

```json
{
  "Schedule-III": {
    "name": "Schedule III Format Requirements",
    "category": "Format",
    "priority": "HIGH",
    "checks": [
      {
        "check_id": "SCHED3-1",
        "requirement": "Share Capital Disclosure",
        "keywords": ["share capital", "equity shares", "preference shares"],
        "mandatory": true,
        "source": "Schedule III, Part I, Section A"
      }
    ]
  }
}
```

### Step 4: Test New Rules

```bash
python3 test_system.py
```

---

## 📊 Current Coverage

### Standards Covered (13)

1. IndAS-1: Presentation of Financial Statements (6 checks)
2. IndAS-7: Statement of Cash Flows (4 checks)
3. IndAS-8: Accounting Policies (2 checks)
4. IndAS-10: Events After Reporting Period (2 checks)
5. IndAS-12: Income Taxes (3 checks)
6. IndAS-16: Property, Plant & Equipment (3 checks)
7. IndAS-18: Revenue Recognition (2 checks)
8. IndAS-24: Related Party Disclosures (4 checks)
9. IndAS-36: Impairment of Assets (1 check)
10. IndAS-109: Financial Instruments (2 checks)
11. Schedule-III: Format Requirements (3 checks)
12. SEBI-LODR: Listing Requirements (3 checks)
13. Auditor-Report: Audit Requirements (3 checks)

**Total**: 38 compliance checks

---

## 🚀 Enhancement Ideas (Stage 2)

### 1. PDF-Based Rule Extraction

Create automated tool to extract rules from PDFs:
- Parse regulation PDFs
- Identify requirement patterns
- Auto-generate rule entries
- Add page references

### 2. Enhanced Rule Metadata

Add more context to each rule:
```json
{
  "check_id": "IndAS1-1",
  "requirement": "Balance Sheet",
  "keywords": ["balance sheet"],
  "source_pdf": "Schedule_III.pdf",
  "page_reference": "Page 5-8",
  "regulation_text": "Every balance sheet shall show...",
  "examples": ["Reliance 2023 - Page 45", "TCS 2023 - Page 32"]
}
```

### 3. Severity Levels

Add severity classification:
- CRITICAL: Must have (regulatory requirement)
- HIGH: Should have (best practice)
- MEDIUM: Good to have (recommended)
- LOW: Optional (nice to have)

### 4. Cross-References

Link related checks:
```json
{
  "check_id": "IndAS1-1",
  "related_checks": ["SCHED3-1", "SEBI1-1"],
  "conflicts_with": [],
  "depends_on": ["IndAS1-2"]
}
```

---

## 📝 Notes

### For Stage 1 Submission

✅ Current JSON-based rules are SUFFICIENT  
✅ 38 checks cover major requirements  
✅ System is working and tested  
✅ PDFs stored as reference only  

### For Stage 2 (If Shortlisted)

- Read PDFs in detail
- Extract more specific requirements
- Add 50+ additional checks
- Implement severity levels
- Add page references
- Create rule validation tool

---

## 🔍 Quick Reference Commands

```bash
# List all regulation files
ls -lh data/regulations/source_pdfs/

# View a regulation PDF
open data/regulations/source_pdfs/Schedule_III.pdf

# Check current rules
cat data/regulations/rules_index.json | python3 -m json.tool

# Count total checks
python3 -c "
import json
with open('data/regulations/rules_index.json') as f:
    rules = json.load(f)
total = sum(len(std['checks']) for std in rules.values())
print(f'Total checks: {total}')
"

# Test compliance system
python3 test_system.py
```

---

**Status**: Reference system ready  
**PDFs**: 3 regulation documents stored  
**Rules**: 38 checks implemented  
**System**: Production ready for Stage 1
