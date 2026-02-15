#!/usr/bin/env python3
"""
Regulation Viewer Tool
Author: Nawddeep
Date: February 2026

View and analyze regulation PDFs
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.document_processor import DocumentProcessor
import json


def list_regulations():
    """List all available regulation PDFs"""
    print("="*70)
    print("📚 AVAILABLE REGULATION DOCUMENTS")
    print("="*70)
    
    pdf_dir = "data/regulations/source_pdfs"
    
    if not os.path.exists(pdf_dir):
        print("\n❌ No regulation PDFs found")
        print(f"   Create folder: mkdir -p {pdf_dir}")
        return
    
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    if not pdfs:
        print("\n⚠️  No PDF files in source_pdfs/")
        return
    
    print(f"\n📁 Location: {pdf_dir}/")
    print(f"📊 Total PDFs: {len(pdfs)}\n")
    
    for i, pdf in enumerate(sorted(pdfs), 1):
        path = os.path.join(pdf_dir, pdf)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"   {i}. {pdf:30} ({size_mb:.1f} MB)")
    
    print("\n" + "="*70)


def view_pdf_summary(pdf_name, max_pages=5):
    """View summary of a regulation PDF"""
    print("="*70)
    print(f"📄 REGULATION PDF SUMMARY: {pdf_name}")
    print("="*70)
    
    pdf_path = f"data/regulations/source_pdfs/{pdf_name}"
    
    if not os.path.exists(pdf_path):
        print(f"\n❌ Error: File not found: {pdf_path}")
        return
    
    print(f"\n📍 Processing first {max_pages} pages...")
    
    try:
        processor = DocumentProcessor(verbose=False)
        result = processor.extract_text_from_pdf(pdf_path, max_pages=max_pages)
        
        stats = processor.get_statistics(result)
        
        print(f"\n✅ Extraction successful!")
        print(f"   📊 Pages: {stats['total_pages']}")
        print(f"   📊 Words: {stats['total_words']:,}")
        print(f"   📊 Characters: {stats['total_characters']:,}")
        print(f"   📊 Method: {stats['extraction_method'].upper()}")
        
        # Show first 1000 characters
        print(f"\n📖 Content Preview (first 1000 chars):")
        print("-"*70)
        print(result['text'][:1000])
        print("-"*70)
        
        # Look for key phrases
        print(f"\n🔍 Key Phrases Found:")
        key_phrases = [
            'shall disclose',
            'must present',
            'requires',
            'mandatory',
            'financial statements',
            'balance sheet',
            'profit and loss'
        ]
        
        text_lower = result['text'].lower()
        found = []
        for phrase in key_phrases:
            count = text_lower.count(phrase)
            if count > 0:
                found.append(f"   • '{phrase}': {count} times")
        
        if found:
            for item in found[:10]:
                print(item)
        else:
            print("   No key phrases found in preview")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "="*70)


def show_current_rules():
    """Show current rules from rules_index.json"""
    print("="*70)
    print("📋 CURRENT COMPLIANCE RULES")
    print("="*70)
    
    rules_path = "data/regulations/rules_index.json"
    
    if not os.path.exists(rules_path):
        print(f"\n❌ Error: Rules file not found: {rules_path}")
        return
    
    try:
        with open(rules_path, 'r') as f:
            rules = json.load(f)
        
        total_checks = sum(len(std['checks']) for std in rules.values())
        
        print(f"\n📊 Total Standards: {len(rules)}")
        print(f"📊 Total Checks: {total_checks}\n")
        
        for std_id, std_data in rules.items():
            print(f"   {std_id}: {std_data['name']}")
            print(f"      Category: {std_data['category']}")
            print(f"      Priority: {std_data['priority']}")
            print(f"      Checks: {len(std_data['checks'])}")
            print()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("="*70)


def main():
    """Main menu"""
    if len(sys.argv) < 2:
        print("="*70)
        print("📚 REGULATION VIEWER TOOL")
        print("="*70)
        print("\nUsage:")
        print("   python3 tools/view_regulations.py list")
        print("   python3 tools/view_regulations.py view <pdf_name>")
        print("   python3 tools/view_regulations.py rules")
        print("\nExamples:")
        print("   python3 tools/view_regulations.py list")
        print("   python3 tools/view_regulations.py view Schedule_III.pdf")
        print("   python3 tools/view_regulations.py rules")
        print("="*70)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_regulations()
    
    elif command == 'view':
        if len(sys.argv) < 3:
            print("❌ Error: Please specify PDF name")
            print("   Example: python3 tools/view_regulations.py view Schedule_III.pdf")
            return
        pdf_name = sys.argv[2]
        view_pdf_summary(pdf_name)
    
    elif command == 'rules':
        show_current_rules()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Valid commands: list, view, rules")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
