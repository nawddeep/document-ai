#!/usr/bin/env python3
"""
Quick Demo Script - Financial Compliance AI
Author: Nawddeep
Date: February 2026

Runs a quick demo with the default sample PDF.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.document_processor import DocumentProcessor
from src.compliance_checker import ComplianceChecker

def main():
    """Quick demo - processes first 20 pages only"""
    
    print("="*70)
    print("🚀 FINANCIAL COMPLIANCE AI - QUICK DEMO")
    print("   Processing first 20 pages only")
    print("="*70)
    
    # Configuration
    pdf_path = "data/sample_document/Dixon_2025.pdf"
    rules_path = "data/regulations/rules_index.json"
    
    # Check files exist
    if not os.path.exists(pdf_path):
        print(f"\n❌ Error: Sample PDF not found: {pdf_path}")
        return
    
    if not os.path.exists(rules_path):
        print(f"\n❌ Error: Rules file not found: {rules_path}")
        return
    
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    print("   (First 20 pages for quick demo)")
    
    # Step 1: Extract text
    print("\n" + "-"*70)
    print("STEP 1: Text Extraction")
    print("-"*70)
    
    try:
        processor = DocumentProcessor(verbose=False)
        result = processor.extract_text_from_pdf(pdf_path, max_pages=20)
        
        stats = processor.get_statistics(result)
        print(f"✅ Extracted {stats['total_words']:,} words from {stats['total_pages']} pages")
        print(f"   Method: {stats['extraction_method'].upper()}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Step 2: Compliance check
    print("\n" + "-"*70)
    print("STEP 2: Compliance Validation")
    print("-"*70)
    
    try:
        checker = ComplianceChecker(rules_path=rules_path, verbose=False)
        compliance = checker.check_compliance(result['text'])
        
        summary = compliance['summary']
        score = summary['compliance_score']
        
        print(f"✅ Compliance Score: {score:.1f}%")
        print(f"   Total Checks: {summary['total_checks']}")
        print(f"   ✅ Passed: {summary['compliant']}")
        print(f"   ❌ Failed: {summary['non_compliant']}")
        print(f"   ⚠️  Missing: {summary['missing']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Summary
    print("\n" + "="*70)
    print("🎉 DEMO COMPLETE")
    print("="*70)
    
    print("\n💡 For full analysis with reports:")
    print("   python main.py")
    
    print("\n📚 For detailed guide:")
    print("   cat QUICK_START_GUIDE.md")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
