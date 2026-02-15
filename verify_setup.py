#!/usr/bin/env python3
"""
System Setup Verification Script
Author: Nawddeep
Date: February 2026

Verifies that all dependencies and files are properly configured.
"""

import sys
import os

print("🔍 Verifying System Setup...\n")
print("="*70)

errors = []
warnings = []

# Check Python version
print("\n📍 Python Environment:")
print("-"*70)
if sys.version_info < (3, 8):
    errors.append("Python 3.8+ required")
    print(f"❌ Python: {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
else:
    print(f"✅ Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Check dependencies
print("\n📍 Required Dependencies:")
print("-"*70)

dependencies = {
    'pdfplumber': 'PDF processing',
    'pytesseract': 'OCR support',
    'pdf2image': 'PDF to image conversion',
    'pandas': 'Data processing',
    'openpyxl': 'Excel export'
}

for module, purpose in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {module:20} - {purpose}")
    except ImportError:
        errors.append(f"Missing: {module}")
        print(f"❌ {module:20} - NOT INSTALLED")

# Check Tesseract
print("\n📍 OCR Engine:")
print("-"*70)
try:
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract: v{version}")
except Exception as e:
    warnings.append("Tesseract not configured (OCR won't work for scanned PDFs)")
    print(f"⚠️  Tesseract: Not configured")
    print(f"   Install: brew install tesseract (macOS)")
    print(f"   Install: sudo apt-get install tesseract-ocr (Ubuntu)")

# Check directories
print("\n📍 Project Structure:")
print("-"*70)

dirs = [
    'data/regulations',
    'data/sample_document',
    'data/outputs',
    'src',
    'tests'
]

for d in dirs:
    if os.path.exists(d):
        print(f"✅ {d}")
    else:
        errors.append(f"Missing directory: {d}")
        print(f"❌ {d}")

# Check rules file
print("\n📍 Configuration Files:")
print("-"*70)

if os.path.exists('data/regulations/rules_index.json'):
    try:
        import json
        with open('data/regulations/rules_index.json') as f:
            rules = json.load(f)
        total_checks = sum(len(std['checks']) for std in rules.values())
        print(f"✅ rules_index.json: {len(rules)} standards, {total_checks} checks")
    except Exception as e:
        errors.append(f"Invalid rules_index.json: {e}")
        print(f"❌ rules_index.json: Invalid JSON")
else:
    errors.append("Missing rules_index.json")
    print(f"❌ rules_index.json: NOT FOUND")

# Check sample PDFs
print("\n📍 Sample Documents:")
print("-"*70)

pdf_dir = 'data/sample_document'
if os.path.exists(pdf_dir):
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    if pdfs:
        print(f"✅ Found {len(pdfs)} sample PDF(s):")
        for pdf in pdfs[:5]:  # Show first 5
            size_mb = os.path.getsize(os.path.join(pdf_dir, pdf)) / (1024*1024)
            print(f"   • {pdf} ({size_mb:.1f} MB)")
        if len(pdfs) > 5:
            print(f"   ... and {len(pdfs)-5} more")
    else:
        warnings.append("No sample PDFs found")
        print(f"⚠️  No PDF files found in {pdf_dir}")
else:
    errors.append(f"Missing directory: {pdf_dir}")
    print(f"❌ {pdf_dir}: NOT FOUND")

# Check main scripts
print("\n📍 Main Scripts:")
print("-"*70)

scripts = ['main.py', 'test_system.py', 'test_complete_system.py']
for script in scripts:
    if os.path.exists(script):
        print(f"✅ {script}")
    else:
        warnings.append(f"Missing script: {script}")
        print(f"⚠️  {script}: NOT FOUND")

# Summary
print("\n" + "="*70)

if errors:
    print("\n❌ SETUP INCOMPLETE\n")
    print("Critical issues found:")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
    print("\n💡 Fix these issues before running the system:")
    print("   pip install -r requirment.txt")
    print("   brew install tesseract poppler  # macOS")
    print("   sudo apt-get install tesseract-ocr poppler-utils  # Ubuntu")
    print("\n" + "="*70)
    sys.exit(1)
elif warnings:
    print("\n⚠️  SETUP COMPLETE WITH WARNINGS\n")
    print("Non-critical issues:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")
    print("\n✅ System is functional but some features may not work")
    print("\n🚀 You can proceed with: python main.py")
else:
    print("\n✅ ALL CHECKS PASSED!")
    print("\n🎉 System is fully configured and ready to use!")
    print("\n🚀 Next steps:")
    print("   1. Run analysis: python main.py")
    print("   2. Run quick test: python test_system.py")
    print("   3. Read guide: QUICK_START_GUIDE.md")

print("="*70 + "\n")
