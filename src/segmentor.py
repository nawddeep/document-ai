"""
Document Segmenter - Section Identification Module
Author: Nawddeep
Date: February 2026

Features:
- Identify major sections (Balance Sheet, P&L, Notes, etc.)
- Page-wise section mapping
- Hierarchical document structure
- Regex-based pattern matching
"""

import re
from typing import Dict, List, Optional
import os


class DocumentSegmenter:
    """
    Segments PDF documents into logical sections
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Document Segmenter
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
        
        # Section identification patterns
        self.section_patterns = {
            'balance_sheet': {
                'patterns': [
                    r'balance\s+sheet',
                    r'statement\s+of\s+financial\s+position'
                ],
                'priority': 10
            },
            'profit_loss': {
                'patterns': [
                    r'profit\s+and\s+loss',
                    r'statement\s+of\s+profit\s+and\s+loss',
                    r'income\s+statement'
                ],
                'priority': 10
            },
            'cash_flow': {
                'patterns': [
                    r'cash\s+flow\s+statement',
                    r'statement\s+of\s+cash\s+flows'
                ],
                'priority': 10
            },
            'equity_changes': {
                'patterns': [
                    r'changes\s+in\s+equity',
                    r'statement\s+of\s+changes\s+in\s+equity'
                ],
                'priority': 9
            },
            'notes_to_accounts': {
                'patterns': [
                    r'notes\s+to\s+accounts',
                    r'notes\s+forming\s+part',
                    r'notes\s+to\s+(the\s+)?financial\s+statements'
                ],
                'priority': 10
            },
            'auditor_report': {
                'patterns': [
                    r'independent\s+auditor',
                    r'auditor\'?s\s+report',
                    r'report\s+of\s+the\s+statutory\s+auditors'
                ],
                'priority': 10
            },
            'directors_report': {
                'patterns': [
                    r'director\'?s\s+report',
                    r'board\'?s\s+report'
                ],
                'priority': 8
            },
            'corporate_governance': {
                'patterns': [
                    r'corporate\s+governance\s+report',
                    r'report\s+on\s+corporate\s+governance'
                ],
                'priority': 8
            },
            'management_discussion': {
                'patterns': [
                    r'management\s+discussion',
                    r'md\s*&\s*a',
                    r'management\'?s\s+discussion\s+and\s+analysis'
                ],
                'priority': 7
            }
        }
        
        if self.verbose:
            print("🔍 Document Segmenter initialized")
            print(f"   📋 Tracking {len(self.section_patterns)} section types")
    
    def segment_document(
        self, 
        page_texts: List[Dict]
    ) -> Dict:
        """
        Segment document into sections
        
        Args:
            page_texts: List of page dictionaries from DocumentProcessor
        
        Returns:
            Sections dictionary
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"🔍 Segmenting document into sections")
            print(f"{'='*70}")
            print(f"   📄 Total pages: {len(page_texts)}")
        
        sections = {}
        
        # Find each section
        for section_name, section_info in self.section_patterns.items():
            section_result = self._find_section(
                page_texts,
                section_info['patterns'],
                section_name
            )
            
            sections[section_name] = section_result
        
        # Summary
        if self.verbose:
            found_sections = [name for name, data in sections.items() 
                             if data['found']]
            print(f"\n   ✅ Segmentation complete")
            print(f"   📋 Found {len(found_sections)} sections:")
            for section in found_sections:
                pages = sections[section]['pages']
                if pages:
                    page_range = f"{min(pages)}-{max(pages)}" if len(pages) > 1 else str(pages[0])
                    print(f"      • {section}: pages {page_range}")
        
        return sections
    
    def _find_section(
        self, 
        page_texts: List[Dict],
        patterns: List[str],
        section_name: str
    ) -> Dict:
        """
        Find specific section in document
        
        Args:
            page_texts: Page dictionaries
            patterns: Regex patterns to search
            section_name: Name of section
        
        Returns:
            Section info dictionary
        """
        result = {
            'found': False,
            'pages': [],
            'text': '',
            'start_page': None,
            'end_page': None,
            'total_chars': 0
        }
        
        for page_data in page_texts:
            page_num = page_data['page_num']
            text = page_data.get('text', '')
            text_lower = text.lower()
            
            # Check if any pattern matches
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    # Found the section
                    if not result['found']:
                        result['found'] = True
                        result['start_page'] = page_num
                        
                        if self.verbose:
                            print(f"   ✅ Found {section_name} on page {page_num}")
                    
                    result['pages'].append(page_num)
                    result['text'] += text + "\n"
                    result['total_chars'] += len(text)
                    result['end_page'] = page_num
                    break
        
        return result
    
    def build_document_structure(
        self, 
        page_texts: List[Dict]
    ) -> Dict:
        """
        Build complete document structure
        
        Args:
            page_texts: Page dictionaries from DocumentProcessor
        
        Returns:
            Document structure dictionary
        """
        sections = self.segment_document(page_texts)
        
        structure = {
            'total_pages': len(page_texts),
            'sections': sections,
            'metadata': {
                'segmentation_method': 'regex_pattern_matching',
                'sections_found': len([s for s in sections.values() if s['found']]),
                'total_sections_tracked': len(self.section_patterns)
            }
        }
        
        return structure
    
    def get_section_summary(self, sections: Dict) -> List[Dict]:
        """
        Get summary of all found sections
        
        Args:
            sections: Sections dictionary
        
        Returns:
            List of section summaries
        """
        summary = []
        
        for section_name, section_data in sections.items():
            if section_data['found']:
                summary.append({
                    'name': section_name,
                    'start_page': section_data['start_page'],
                    'end_page': section_data['end_page'],
                    'page_count': len(section_data['pages']),
                    'char_count': section_data['total_chars']
                })
        
        return sorted(summary, key=lambda x: x['start_page'])


# ============================================
# TEST CODE
# ============================================

def test_segmenter():
    """
    Test the document segmenter
    """
    print("\n" + "="*70)
    print("🧪 TESTING DOCUMENT SEGMENTER")
    print("="*70)
    
    # Import DocumentProcessor
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from document_processor import DocumentProcessor
    
    # Process a PDF
    pdf_path = "data/sample_document/Dixon_2025.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  Test PDF not found: {pdf_path}")
        return
    
    # Extract text
    processor = DocumentProcessor(verbose=False)
    result = processor.extract_text_from_pdf(pdf_path, max_pages=150)
    
    # Segment
    segmenter = DocumentSegmenter(verbose=True)
    structure = segmenter.build_document_structure(result['page_texts'])
    
    # Print summary
    print(f"\n📊 DOCUMENT STRUCTURE:")
    print("="*70)
    
    summary = segmenter.get_section_summary(structure['sections'])
    
    for section in summary:
        print(f"\n📄 {section['name'].upper().replace('_', ' ')}")
        print(f"   Pages: {section['start_page']}-{section['end_page']} ({section['page_count']} pages)")
        print(f"   Characters: {section['char_count']:,}")
    
    print(f"\n✅ Test complete!")


if __name__ == "__main__":
    test_segmenter()
