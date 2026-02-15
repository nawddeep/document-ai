"""
Test the complete system automatically
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.document_processor import DocumentProcessor
from src.compliance_checker import ComplianceChecker


def test_system():
    """
    Test the complete system
    """
    print("="*70)
    print("🎯 FINANCIAL COMPLIANCE CHECKER - TEST")
    print("   IndiaAI Challenge 2026")
    print("="*70)
    
    # Configuration
    RULES_PATH = "data/regulations/rules_index.json"
    OUTPUT_DIR = "data/outputs"
    PDF_PATH = "data/sample_document/Dixon_2025.pdf"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Validate file
    if not os.path.exists(PDF_PATH):
        print(f"\n❌ Error: File not found: {PDF_PATH}")
        return
    
    print(f"\n✅ Processing: {os.path.basename(PDF_PATH)}")
    
    # STEP 1: Extract text
    print("\n" + "="*70)
    print("STEP 1: TEXT EXTRACTION")
    print("="*70)
    
    processor = DocumentProcessor(verbose=True)
    extraction_result = processor.extract_text_from_pdf(
        PDF_PATH,
        max_pages=50  # Process first 50 pages for testing
    )
    
    if not extraction_result['text']:
        print("\n❌ Error: No text extracted from PDF")
        return
    
    # Statistics
    stats = processor.get_statistics(extraction_result)
    print(f"\n✅ Extraction successful!")
    print(f"   📊 Method: {stats['method']}")
    print(f"   📊 Pages: {stats['total_pages']}")
    print(f"   📊 Characters: {stats['total_characters']:,}")
    
    # STEP 2: Compliance Check
    print("\n" + "="*70)
    print("STEP 2: COMPLIANCE VALIDATION")
    print("="*70)
    
    checker = ComplianceChecker(
        rules_path=RULES_PATH,
        verbose=True
    )
    
    compliance_results = checker.check_compliance(
        extraction_result['text']
    )
    
    # STEP 3: Generate Report
    print("\n" + "="*70)
    print("STEP 3: GENERATING REPORT")
    print("="*70)
    
    # Save results to JSON
    import json
    output_file = os.path.join(OUTPUT_DIR, "compliance_report.json")
    
    report_data = {
        'pdf_file': os.path.basename(PDF_PATH),
        'extraction_stats': stats,
        'compliance_results': compliance_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Report saved: {output_file}")
    
    # STEP 4: Recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    recommendations = checker.generate_recommendations(compliance_results)
    for rec in recommendations:
        print(rec)
    
    # Final Summary
    print("\n" + "="*70)
    print("🎉 PROCESSING COMPLETE")
    print("="*70)
    
    score = compliance_results['summary']['compliance_score']
    print(f"\n   🎯 Overall Compliance Score: {score:.1f}%")
    print(f"   📄 Report saved to: {output_file}")
    print(f"\n   Next steps:")
    print(f"   1. Review the report")
    print(f"   2. Address non-compliant items")
    print(f"   3. Re-run the check")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        test_system()
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
