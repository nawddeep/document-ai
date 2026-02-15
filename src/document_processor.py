"""
Document Processor - PDF Text Extraction Module
Author: Nawddeep
Date: February 2026

Features:
- Digital PDF text extraction (pdfplumber)
- OCR for scanned PDFs (Tesseract)
- Automatic fallback mechanism
- Page-wise text tracking
- Metadata extraction
"""

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from typing import Dict, List, Optional


class DocumentProcessor:
    """
    Extracts text from PDF documents using multiple methods
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the Document Processor
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
        self.supported_formats = ['.pdf', '.PDF']
        
        if self.verbose:
            print("📄 Document Processor initialized")
    
    def extract_text_from_pdf(
        self, 
        pdf_path: str, 
        max_pages: Optional[int] = None,
        min_text_threshold: int = 1000
    ) -> Dict:
        """
        Main extraction method with automatic fallback
        
        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum pages to process (None = all)
            min_text_threshold: Minimum characters for digital extraction
        
        Returns:
            dict: {
                'text': str,           # Full extracted text
                'page_texts': list,    # Page-wise text data
                'metadata': dict       # Extraction metadata
            }
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"📥 Processing: {os.path.basename(pdf_path)}")
            print(f"{'='*70}")
        
        # Validate file
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        if not any(pdf_path.endswith(ext) for ext in self.supported_formats):
            raise ValueError(f"Unsupported format. Use: {self.supported_formats}")
        
        # Try digital extraction first
        result = self._extract_digital_text(pdf_path, max_pages)
        
        # Fallback to OCR if needed
        if len(result['text']) < min_text_threshold:
            if self.verbose:
                print(f"   ⚠️  Only {len(result['text'])} characters extracted")
                print(f"   ⚠️  Threshold: {min_text_threshold} characters")
                print(f"   🔄 Falling back to OCR...")
            
            result = self._extract_with_ocr(pdf_path, max_pages or 10)
        
        return result
    
    def _extract_digital_text(
        self, 
        pdf_path: str, 
        max_pages: Optional[int]
    ) -> Dict:
        """
        Extract text from digital PDF using pdfplumber
        
        Args:
            pdf_path: Path to PDF
            max_pages: Pages to process
        
        Returns:
            Extraction result dictionary
        """
        if self.verbose:
            print("   📖 Method: Digital extraction (pdfplumber)")
        
        full_text = ""
        page_texts = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_process = min(max_pages or total_pages, total_pages)
                
                if self.verbose:
                    print(f"   📄 Total pages: {total_pages}")
                    print(f"   🔢 Processing: {pages_to_process} pages")
                
                # Extract from each page
                for i in range(pages_to_process):
                    page = pdf.pages[i]
                    page_text = page.extract_text()
                    
                    if page_text:
                        full_text += page_text + "\n\n"
                        page_texts.append({
                            'page_num': i + 1,
                            'text': page_text,
                            'char_count': len(page_text),
                            'word_count': len(page_text.split())
                        })
                    else:
                        # Empty page
                        page_texts.append({
                            'page_num': i + 1,
                            'text': "",
                            'char_count': 0,
                            'word_count': 0,
                            'note': 'No text extracted (possible image-only page)'
                        })
                    
                    # Progress indicator
                    if self.verbose and (i + 1) % 20 == 0:
                        print(f"   ⏳ Progress: {i + 1}/{pages_to_process} pages")
                
                # Summary
                if self.verbose:
                    print(f"   ✅ Extraction complete")
                    print(f"   📊 Characters: {len(full_text):,}")
                    print(f"   📊 Words: {len(full_text.split()):,}")
                    print(f"   📊 Pages with text: {len([p for p in page_texts if p['char_count'] > 0])}")
                
                return {
                    'text': full_text,
                    'page_texts': page_texts,
                    'metadata': {
                        'total_pages': total_pages,
                        'processed_pages': pages_to_process,
                        'method': 'digital',
                        'pages_with_text': len([p for p in page_texts if p['char_count'] > 0]),
                        'total_characters': len(full_text),
                        'total_words': len(full_text.split())
                    }
                }
        
        except Exception as e:
            if self.verbose:
                print(f"   ❌ Digital extraction error: {str(e)}")
            
            return {
                'text': '',
                'page_texts': [],
                'metadata': {
                    'method': 'digital',
                    'error': str(e)
                }
            }
    
    def _extract_with_ocr(
        self, 
        pdf_path: str, 
        max_pages: int = 10
    ) -> Dict:
        """
        Extract text using Tesseract OCR
        
        Args:
            pdf_path: Path to PDF
            max_pages: Maximum pages for OCR (default: 10)
        
        Returns:
            Extraction result dictionary
        """
        if self.verbose:
            print("   🔍 Method: OCR (Tesseract)")
            print(f"   ⚠️  OCR limited to {max_pages} pages (performance)")
        
        full_text = ""
        page_texts = []
        
        try:
            # Convert PDF to images
            if self.verbose:
                print("   📸 Converting PDF to images...")
            
            images = convert_from_path(
                pdf_path, 
                first_page=1, 
                last_page=max_pages,
                dpi=300  # Higher DPI for better OCR
            )
            
            if self.verbose:
                print(f"   🖼️  Converted {len(images)} pages to images")
            
            # OCR each image
            for i, img in enumerate(images):
                if self.verbose:
                    print(f"   🔍 OCR page {i + 1}/{len(images)}...", end=" ")
                
                # Perform OCR
                page_text = pytesseract.image_to_string(img, lang='eng')
                
                full_text += page_text + "\n\n"
                page_texts.append({
                    'page_num': i + 1,
                    'text': page_text,
                    'char_count': len(page_text),
                    'word_count': len(page_text.split())
                })
                
                if self.verbose:
                    print(f"({len(page_text)} chars)")
            
            # Summary
            if self.verbose:
                print(f"   ✅ OCR complete")
                print(f"   📊 Characters: {len(full_text):,}")
                print(f"   📊 Words: {len(full_text.split()):,}")
            
            return {
                'text': full_text,
                'page_texts': page_texts,
                'metadata': {
                    'total_pages': len(images),
                    'processed_pages': len(images),
                    'method': 'ocr',
                    'total_characters': len(full_text),
                    'total_words': len(full_text.split())
                }
            }
        
        except Exception as e:
            if self.verbose:
                print(f"   ❌ OCR error: {str(e)}")
            
            return {
                'text': '',
                'page_texts': [],
                'metadata': {
                    'method': 'ocr',
                    'error': str(e)
                }
            }
    
    def get_statistics(self, extraction_result: Dict) -> Dict:
        """
        Get detailed statistics from extraction result
        
        Args:
            extraction_result: Result from extract_text_from_pdf
        
        Returns:
            Statistics dictionary
        """
        text = extraction_result['text']
        page_texts = extraction_result['page_texts']
        
        return {
            'total_characters': len(text),
            'total_words': len(text.split()),
            'total_lines': len(text.split('\n')),
            'total_pages': len(page_texts),
            'pages_with_content': len([p for p in page_texts if p['char_count'] > 0]),
            'avg_chars_per_page': sum(p['char_count'] for p in page_texts) / len(page_texts) if page_texts else 0,
            'method': extraction_result['metadata'].get('method', 'unknown')
        }


# ============================================
# TEST & DEMO CODE
# ============================================

def test_document_processor():
    """
    Test the document processor
    """
    print("\n" + "="*70)
    print("🧪 TESTING DOCUMENT PROCESSOR")
    print("="*70)
    
    # Initialize
    processor = DocumentProcessor(verbose=True)
    
    # Test file (update path as needed)
    test_files = [
        "data/sample_document/Dixon_2025.pdf",
        "data/sample_documents/annual_reports/hdfc_2024.pdf"
    ]
    
    for pdf_path in test_files:
        if os.path.exists(pdf_path):
            print(f"\n{'='*70}")
            print(f"📄 Testing: {os.path.basename(pdf_path)}")
            print(f"{'='*70}")
            
            # Extract
            result = processor.extract_text_from_pdf(pdf_path, max_pages=50)
            
            # Statistics
            stats = processor.get_statistics(result)
            
            print(f"\n📊 STATISTICS:")
            print(f"   Method: {stats['method']}")
            print(f"   Total pages: {stats['total_pages']}")
            print(f"   Pages with content: {stats['pages_with_content']}")
            print(f"   Total characters: {stats['total_characters']:,}")
            print(f"   Total words: {stats['total_words']:,}")
            print(f"   Avg chars/page: {stats['avg_chars_per_page']:.0f}")
            
            # Sample text
            print(f"\n📝 SAMPLE TEXT (first 500 chars):")
            print("-"*70)
            print(result['text'][:500])
            print("-"*70)
            
            break  # Test only first file
        else:
            print(f"⚠️  File not found: {pdf_path}")


if __name__ == "__main__":
    test_document_processor()
