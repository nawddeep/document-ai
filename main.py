"""
Financial Compliance AI - Complete System
Author: Nawddeep
Date: February 2026

Complete end-to-end compliance checking system
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


def validate_pdf_input(pdf_path):
    """
    Validate PDF file input
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not pdf_path:
        return False, "No file path provided"
    
    if not os.path.exists(pdf_path):
        return False, f"File not found: {pdf_path}"
    
    if not os.path.isfile(pdf_path):
        return False, f"Path is not a file: {pdf_path}"
    
    if not pdf_path.lower().endswith('.pdf'):
        return False, f"File is not a PDF: {pdf_path}"
    
    # Check file size (warn if > 100MB)
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    if file_size_mb > 100:
        print(f"\n⚠️  Warning: Large file ({file_size_mb:.1f} MB) - processing may take time")
    
    return True, None


def main():
    """
    Main execution function - Complete workflow
    """
    print("="*70)
    print("🎯 FINANCIAL COMPLIANCE AI")
    print("   IndiaAI Challenge 2026")
    print("   Complete Compliance Analysis System")
    print("="*70)
    
    # Configuration
    RULES_PATH = "data/regulations/rules_index.json"
    OUTPUT_DIR = "data/outputs"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Validate rules file exists
    if not os.path.exists(RULES_PATH):
        print(f"\n❌ Error: Rules file not found: {RULES_PATH}")
        print("   Please ensure data/regulations/rules_index.json exists")
        return
    
    # Get PDF path
    print("\n📄 Enter PDF file path:")
    print("   (or press Enter for default test file)")
    
    pdf_path = input("   Path: ").strip()
    
    if not pdf_path:
        # Try to find any PDF in sample_documents
        pdf_path = "data/sample_document/Dixon_2025.pdf"
        if os.path.exists(pdf_path):
            print(f"   Using: {os.path.basename(pdf_path)}")
    
    # Validate PDF file
    is_valid, error_msg = validate_pdf_input(pdf_path)
    if not is_valid:
        print(f"\n❌ Error: {error_msg}")
        print("\n💡 Tips:")
        print("   • Use absolute path: /full/path/to/file.pdf")
        print("   • Or relative path: data/sample_document/Dixon_2025.pdf")
        print("   • Check file exists: ls -la path/to/file.pdf")
        return
    
    pdf_filename = os.path.basename(pdf_path)
    print(f"\n✅ Processing: {pdf_filename}")
    
    # ====================================================================
    # STEP 1: TEXT EXTRACTION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 1: DOCUMENT PROCESSING & TEXT EXTRACTION")
    print("="*70)
    
    try:
        processor = DocumentProcessor(verbose=True)
        extraction_result = processor.extract_text_from_pdf(
            pdf_path,
            max_pages=150  # Process first 150 pages
        )
        
        if not extraction_result['text']:
            print("\n❌ Error: No text extracted from PDF")
            print("   Possible reasons:")
            print("   • PDF is encrypted or password-protected")
            print("   • PDF contains only images (OCR failed)")
            print("   • PDF is corrupted")
            return
        
        stats = processor.get_statistics(extraction_result)
        print(f"\n✅ Text extraction successful!")
        
    except Exception as e:
        print(f"\n❌ Error during text extraction: {str(e)}")
        print("   Try with a different PDF or check file integrity")
        return
    
    # ====================================================================
    # STEP 2: TABLE EXTRACTION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 2: FINANCIAL TABLES EXTRACTION")
    print("="*70)
    
    try:
        extractor = TableExtractor(verbose=True)
        tables = extractor.extract_all_tables(pdf_path, max_pages=150)
        
        print(f"\n✅ Table extraction complete!")
        print(f"   📊 Found {len(tables)} tables")
        
        # Save tables to Excel
        if tables:
            excel_path = os.path.join(OUTPUT_DIR, f"tables_{pdf_filename.replace('.pdf', '.xlsx')}")
            extractor.save_tables_to_excel(tables, excel_path)
        else:
            print("   ⚠️  No tables found in document")
            excel_path = None
            
    except Exception as e:
        print(f"\n⚠️  Warning: Table extraction failed: {str(e)}")
        print("   Continuing without table data...")
        tables = []
        excel_path = None
    
    # ====================================================================
    # STEP 3: DOCUMENT SEGMENTATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 3: DOCUMENT SEGMENTATION")
    print("="*70)
    
    try:
        segmenter = DocumentSegmenter(verbose=True)
        structure = segmenter.build_document_structure(extraction_result['page_texts'])
        
        print(f"\n✅ Segmentation complete!")
        print(f"   📋 Identified {structure['metadata']['sections_found']} major sections")
        
    except Exception as e:
        print(f"\n⚠️  Warning: Segmentation failed: {str(e)}")
        print("   Continuing with basic structure...")
        structure = {
            'total_pages': len(extraction_result['page_texts']),
            'sections': [],
            'metadata': {'sections_found': 0}
        }
    
    # ====================================================================
    # STEP 4: COMPLIANCE VALIDATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 4: COMPLIANCE VALIDATION")
    print("="*70)
    
    try:
        checker = ComplianceChecker(
            rules_path=RULES_PATH,
            verbose=True
        )
        
        compliance_results = checker.check_compliance(
            extraction_result['text'],
            sections=structure['sections']
        )
        
        print(f"\n✅ Compliance check complete!")
        
    except Exception as e:
        print(f"\n❌ Error during compliance checking: {str(e)}")
        print("   Cannot continue without compliance results")
        return
    
    # ====================================================================
    # STEP 5: REPORT GENERATION
    # ====================================================================
    print("\n" + "="*70)
    print("STEP 5: REPORT GENERATION")
    print("="*70)
    
    try:
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
        
    except Exception as e:
        print(f"\n❌ Error during report generation: {str(e)}")
        print("   Compliance results available but reports not generated")
        return
    
    # ====================================================================
    # STEP 6: RECOMMENDATIONS
    # ====================================================================
    print("\n" + "="*70)
    print("💡 COMPLIANCE RECOMMENDATIONS")
    print("="*70)
    
    try:
        recommendations = checker.generate_recommendations(compliance_results)
        for rec in recommendations:
            print(rec)
    except Exception as e:
        print(f"   ⚠️  Could not generate recommendations: {str(e)}")
    
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
    
    print(f"\n   📁 Generated Files:")
    print(f"      • HTML Report: {html_report_path}")
    print(f"      • JSON Data: {json_report_path}")
    if excel_path:
        print(f"      • Excel Tables: {excel_path}")
    
    print(f"\n   🌐 Open HTML Report:")
    print(f"      file://{os.path.abspath(html_report_path)}")
    
    print("\n" + "="*70)
    print("✅ All Done! Review the HTML report in your browser.")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
