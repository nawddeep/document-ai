# Financial Compliance AI - IndiaAI Challenge 2026

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated compliance checking system for Indian financial reports. Validates annual reports against IndAS standards, SEBI regulations, and Schedule III requirements.

## 🎯 Overview

This system automatically analyzes financial reports (annual reports, quarterly reports, audit reports) and validates them against Indian accounting standards and regulatory requirements. It extracts text, identifies financial tables, segments the document into logical sections, and generates comprehensive compliance reports.

## ✨ Features

- **Text Extraction**: Digital PDF processing with OCR fallback for scanned documents
- **Table Extraction**: Automatically identifies and extracts 40+ financial tables with type classification
- **Document Segmentation**: Auto-identifies 9 major section types (Balance Sheet, P&L, Cash Flow, etc.)
- **Compliance Checking**: Validates against 38 checks across 13 standards
- **Professional Reports**: Beautiful HTML reports with visualizations + JSON data + Excel exports

## 🚀 Quick Start

### Prerequisites

**macOS:**
```bash
brew install tesseract poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**Windows:**
- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Install [Poppler](http://blog.alivate.com.au/poppler-windows/)

### Installation

```bash
# Clone the repository
git clone https://github.com/nawddeep/document-ai.git
cd document-ai

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirment.txt

# Verify setup
python verify_setup.py
```

### Run Analysis

```bash
# Run with default sample PDF
python main.py
# Press ENTER when prompted

# Or specify your own PDF
python main.py
# Enter: path/to/your/annual_report.pdf
```

### View Results

```bash
# Open HTML report in browser
open data/outputs/compliance_report_Dixon_2025.html

# View JSON data
cat data/outputs/compliance_data_Dixon_2025.json | python -m json.tool

# Open Excel tables
open data/outputs/tables_Dixon_2025.xlsx
```

## 📊 Test Results

**Document**: Dixon 2025 Annual Report (395 pages)  
**Processed**: 100 pages in ~2 minutes  
**Tables Extracted**: 43 financial tables  
**Sections Found**: 5/9 major sections  
**Compliance Score**: 51.4%

### Sample Output

```
🎯 FINANCIAL COMPLIANCE AI
   IndiaAI Challenge 2026

✅ Processing: Dixon_2025.pdf

STEP 1: TEXT EXTRACTION
   📊 Characters: 336,186
   📊 Words: 49,759
   ✅ Extraction complete

STEP 2: TABLE EXTRACTION
   📊 Found 43 tables
   💾 Saved to Excel

STEP 3: DOCUMENT SEGMENTATION
   📋 Identified 5 sections

STEP 4: COMPLIANCE VALIDATION
   🎯 Compliance Score: 51.4%
   ✅ Compliant: 18/38 (47%)
   ❌ Non-Compliant: 16/38 (42%)

STEP 5: REPORT GENERATION
   ✅ HTML Report: compliance_report_Dixon_2025.html
   ✅ JSON Data: compliance_data_Dixon_2025.json
   ✅ Excel Tables: tables_Dixon_2025.xlsx
```

## 📁 Project Structure

```
document_ai/
├── main.py                      # Main entry point
├── test_complete_system.py      # Automated test script
├── verify_setup.py              # Setup verification
├── src/
│   ├── document_processor.py    # PDF text extraction
│   ├── table_extractor.py       # Table extraction
│   ├── segmentor.py             # Section identification
│   ├── compliance_checker.py    # Compliance validation
│   └── report_generator.py      # HTML report generation
├── data/
│   ├── regulations/
│   │   └── rules_index.json     # 13 standards, 38 checks
│   ├── sample_document/         # Sample PDFs
│   └── outputs/                 # Generated reports
└── tests/
    └── test_complete_system.py  # Test suite
```

## 🔧 Usage Examples

### Process Different PDF

```bash
python main.py
# Enter: data/sample_document/HDFC_2025.pdf
```

### Run Automated Test

```bash
# Quick test (50 pages)
python test_system.py

# Complete test (100 pages)
python test_complete_system.py
```

### Verify System Setup

```bash
python verify_setup.py
```

## 📈 Compliance Standards Covered

1. **IndAS-1**: Presentation of Financial Statements (6 checks)
2. **IndAS-7**: Statement of Cash Flows (4 checks)
3. **IndAS-8**: Accounting Policies (2 checks)
4. **IndAS-10**: Events After Reporting Period (2 checks)
5. **IndAS-12**: Income Taxes (3 checks)
6. **IndAS-16**: Property, Plant & Equipment (3 checks)
7. **IndAS-18**: Revenue Recognition (2 checks)
8. **IndAS-24**: Related Party Disclosures (4 checks)
9. **IndAS-36**: Impairment of Assets (1 check)
10. **IndAS-109**: Financial Instruments (2 checks)
11. **Schedule-III**: Format Requirements (3 checks)
12. **SEBI-LODR**: Listing Requirements (3 checks)
13. **Auditor-Report**: Audit Requirements (3 checks)

## 🎨 Output Files

### HTML Report
Professional compliance report with:
- Executive summary with compliance score
- Interactive progress bars
- Color-coded status indicators (✅ ❌ ⚠️)
- Evidence snippets for each check
- Detailed findings by standard
- Modern gradient design

### JSON Data
Structured data including:
- Extraction statistics
- Document structure
- Tables count
- Complete compliance results
- Detailed findings with evidence

### Excel Tables
All extracted financial tables organized by:
- Table type (balance_sheet, profit_loss, cash_flow, etc.)
- Page number
- Multiple sheets for easy navigation

## 🛠️ Technical Details

### Extraction Methods
- **Digital PDF**: pdfplumber for text extraction
- **Scanned PDF**: Tesseract OCR with automatic fallback
- **Tables**: pdfplumber table detection
- **Sections**: Regex-based pattern matching

### Performance
- **Speed**: ~3.4 pages/second for text extraction
- **Accuracy**: 100% text extraction success rate
- **Tables**: 43 tables from 100 pages
- **Sections**: 5/9 sections identified

### Supported Document Types
- Annual Reports ✅
- Financial Statements ✅
- Quarterly Reports ✅
- Audit Reports ✅
- Corporate Governance Reports ✅

## 📚 Documentation

- **QUICK_START_GUIDE.md** - Detailed getting started guide
- **FINAL_STATUS.md** - Complete system status and results
- **DAY1_SUMMARY.md** - Day 1 development summary
- **DAY2_SUMMARY.md** - Day 2 development summary

## 🧪 Testing

```bash
# Verify system setup
python verify_setup.py

# Run quick test (50 pages)
python test_system.py

# Run complete test (100 pages)
python test_complete_system.py

# Verify outputs
./verify_outputs.sh
```

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
source .venv/bin/activate
pip install -r requirment.txt
```

### "Tesseract not found"
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

### "PDF not found"
```bash
# Check available PDFs
ls -la data/sample_document/*.pdf

# Use absolute path
python main.py
# Enter: /full/path/to/your/file.pdf
```

## 🤝 Contributing

This is a submission for the IndiaAI Financial Reporting Compliance Challenge 2026. Contributions and suggestions are welcome!

## 👨‍💻 Author

**Nawddeep**  
IndiaAI Financial Reporting Compliance Challenge 2026

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- IndiaAI for organizing the challenge
- Anthropic Claude for development assistance
- Open source community for the amazing libraries

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact through the IndiaAI platform.

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: February 16, 2026
