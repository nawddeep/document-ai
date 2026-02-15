"""
Test Complete System - Automated Full Workflow Test
Author: Nawddeep
Date: February 2026
"""

import sys
import os
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.document_processor import DocumentProcessor
from src.table_extractor import TableExtractor
from src.segmentor import DocumentSegmenter
from src.compliance_checker import ComplianceChecker
from src.report_generator import ReportGenerator


def test_complete_system():
    """
    Test the complete system workflow
    """
    print("="*70)
    print("🎯 FINANCIAL COMPLIANCE AI - COMPLETE SYSTEM TEST")
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
    
    pdf_filename = os.path.basename(PDF_PATH)
    print(f"\n✅ Processing: {pdf_filename}")
    
    # ====================================================================
    # STEP 1: TEXT EXTRACTION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 1: DOCUMENT PROCESSING & TEXT EXTRACTION")
    print("="*70)
    
    processor = DocumentProcessor(verbose=True)
    extraction_result = processor.extract_text_from_pdf(
        PDF_PATH,
        max_pages=100  # Process first 100 pages for testing
    )
    
    if not extraction_result['text']:
        print("\n❌ Error: No text extracted from PDF")
        return
    
    stats = processor.get_statistics(extraction_result)
    print(f"\n✅ Text extraction successful!")
    
    # ====================================================================
    # STEP 2: TABLE EXTRACTION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 2: FINANCIAL TABLES EXTRACTION")
    print("="*70)
    
    extractor = TableExtractor(verbose=True)
    tables = extractor.extract_all_tables(PDF_PATH, max_pages=100)
    
    print(f"\n✅ Table extraction complete!")
    print(f"   📊 Found {len(tables)} tables")
    
    # Save tables to Excel
    if tables:
        excel_path = os.path.join(OUTPUT_DIR, f"tables_{pdf_filename.replace('.pdf', '.xlsx')}")
        extractor.save_tables_to_excel(tables, excel_path)
    
    # ====================================================================
    # STEP 3: DOCUMENT SEGMENTATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 3: DOCUMENT SEGMENTATION")
    print("="*70)
    
    segmenter = DocumentSegmenter(verbose=True)
    structure = segmenter.build_document_structure(extraction_result['page_texts'])
    
    print(f"\n✅ Segmentation complete!")
    print(f"   📋 Identified {structure['metadata']['sections_found']} major sections")
    
    # ====================================================================
    # STEP 4: COMPLIANCE VALIDATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 4: COMPLIANCE VALIDATION")
    print("="*70)
    
    checker = ComplianceChecker(
        rules_path=RULES_PATH,
        verbose=True
    )
    
    compliance_results = checker.check_compliance(
        extraction_result['text'],
        sections=structure['sections']
    )
    
    print(f"\n✅ Compliance check complete!")
    
    # ====================================================================
    # STEP 5: REPORT GENERATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 5: REPORT GENERATION")
    print("="*70)
    
    # HTML Report
    generator = ReportGenerator(verbose=True)
    html_report_path = os.path.join(
        OUTPUT_DIR, 
        f"compliance_report_{pdf_filename.replace('.pdf', '.html')}"
    )
    
    generator.generate_html_report(
        compliance_results=compliance_results,
        extraction_stats=stats,
        pdf_filename=pdf_filename,
        output_path=html_report_path
    )
    
    # JSON Report (for data analysis)
    json_report_path = os.path.join(
        OUTPUT_DIR,
        f"compliance_data_{pdf_filename.replace('.pdf', '.json')}"
    )
    
    report_data = {
        'pdf_file': pdf_filename,
        'extraction_stats': stats,
        'document_structure': {
            'total_pages': structure['total_pages'],
            'sections_found': structure['metadata']['sections_found']
        },
        'tables_found': len(tables),
        'compliance_results': compliance_results
    }
    
    with open(json_report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ JSON data saved: {json_report_path}")
    
    # ====================================================================
    # STEP 6: RECOMMENDATIONS
    # ====================================================================
    print("\n" + "="*70)
    print("💡 COMPLIANCE RECOMMENDATIONS")
    print("="*70)
    
    recommendations = checker.generate_recommendations(compliance_results)
    for rec in recommendations:
        print(rec)
    
    # ====================================================================
    # FINAL SUMMARY
    # ====================================================================
    print("\n" + "="*70)
    print("🎉 ANALYSIS COMPLETE")
    print("="*70)
    
    score = compliance_results['summary']['compliance_score']
    
    print(f"\n   📄 Document: {pdf_filename}")
    print(f"   🎯 Compliance Score: {score:.1f}%")
    print(f"   📊 Total Checks: {compliance_results['summary']['total_checks']}")
    print(f"   ✅ Passed: {compliance_results['summary']['compliant']}")
    print(f"   ❌ Failed: {compliance_results['summary']['non_compliant']}")
    print(f"   📊 Tables Extracted: {len(tables)}")
    print(f"   📋 Sections Found: {structure['metadata']['sections_found']}")
    
    print(f"\n   📁 Generated Files:")
    print(f"      • HTML Report: {html_report_path}")
    print(f"      • JSON Data: {json_report_path}")
    if tables:
        print(f"      • Excel Tables: {excel_path}")
    
    print(f"\n   🌐 Open HTML Report:")
    print(f"      file://{os.path.abspath(html_report_path)}")
    
    print("\n" + "="*70)
    print("✅ All Done! Review the HTML report in your browser.")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        test_complete_system()
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
