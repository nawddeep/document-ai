"""
Table Extractor - Financial Tables Extraction Module
Author: Nawddeep
Date: February 2026

Features:
- Extract tables using pdfplumber & camelot
- Identify table types (Balance Sheet, P&L, Cash Flow)
- Convert to pandas DataFrames
- Handle merged cells and complex layouts
"""

import pdfplumber
import pandas as pd
from typing import List, Dict, Optional
import re
import os


class TableExtractor:
    """
    Extracts and identifies financial tables from PDFs
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Table Extractor
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
        
        # Table type patterns
        self.table_patterns = {
            'balance_sheet': [
                r'balance\s+sheet',
                r'statement\s+of\s+financial\s+position',
                r'assets.*liabilities'
            ],
            'profit_loss': [
                r'profit.*loss',
                r'statement\s+of\s+profit',
                r'income\s+statement',
                r'revenue.*expenses'
            ],
            'cash_flow': [
                r'cash\s+flow',
                r'statement\s+of\s+cash\s+flows',
                r'operating.*investing.*financing'
            ],
            'equity': [
                r'changes\s+in\s+equity',
                r'statement\s+of\s+changes'
            ]
        }
        
        if self.verbose:
            print("📊 Table Extractor initialized")
    
    def extract_all_tables(
        self, 
        pdf_path: str, 
        max_pages: int = 200
    ) -> List[Dict]:
        """
        Extract all tables from PDF
        
        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum pages to process
        
        Returns:
            List of table dictionaries
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"📊 Extracting tables from PDF")
            print(f"{'='*70}")
        
        all_tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_check = min(max_pages, total_pages)
                
                if self.verbose:
                    print(f"   📄 Total pages: {total_pages}")
                    print(f"   🔢 Processing: {pages_to_check} pages")
                
                # Extract from each page
                for i in range(pages_to_check):
                    page = pdf.pages[i]
                    page_text = page.extract_text() or ""
                    
                    # Try to extract tables
                    tables = page.extract_tables()
                    
                    if tables:
                        if self.verbose and len(tables) > 0:
                            print(f"   📄 Page {i+1}: Found {len(tables)} table(s)")
                        
                        for table_idx, table in enumerate(tables):
                            if table and len(table) > 1:  # At least 2 rows
                                # Convert to DataFrame
                                try:
                                    df = self._table_to_dataframe(table)
                                    
                                    # Identify table type
                                    table_type = self._identify_table_type(
                                        df, 
                                        page_text
                                    )
                                    
                                    # Store table info
                                    table_info = {
                                        'page': i + 1,
                                        'table_index': table_idx,
                                        'type': table_type,
                                        'data': df,
                                        'rows': len(df),
                                        'columns': len(df.columns),
                                        'page_text_snippet': page_text[:200]
                                    }
                                    
                                    all_tables.append(table_info)
                                
                                except Exception as e:
                                    if self.verbose:
                                        print(f"      ⚠️  Error processing table: {e}")
                    
                    # Progress indicator
                    if self.verbose and (i + 1) % 50 == 0:
                        print(f"   ⏳ Progress: {i + 1}/{pages_to_check} pages")
                
                if self.verbose:
                    print(f"\n   ✅ Extraction complete")
                    print(f"   📊 Total tables found: {len(all_tables)}")
                    
                    # Summary by type
                    type_counts = {}
                    for table in all_tables:
                        t_type = table['type']
                        type_counts[t_type] = type_counts.get(t_type, 0) + 1
                    
                    print(f"\n   📋 Tables by type:")
                    for t_type, count in type_counts.items():
                        print(f"      {t_type}: {count}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        return all_tables
    
    def _table_to_dataframe(self, table: List[List]) -> pd.DataFrame:
        """
        Convert table array to DataFrame
        
        Args:
            table: 2D array from pdfplumber
        
        Returns:
            pandas DataFrame
        """
        if not table or len(table) < 2:
            return pd.DataFrame()
        
        # Use first row as headers
        headers = table[0]
        data_rows = table[1:]
        
        # Clean headers
        headers = [str(h).strip() if h else f"Column_{i}" 
                   for i, h in enumerate(headers)]
        
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Clean data
        df = df.applymap(lambda x: str(x).strip() if x else "")
        
        return df
    
    def _identify_table_type(
        self, 
        df: pd.DataFrame, 
        page_text: str
    ) -> str:
        """
        Identify type of financial table
        
        Args:
            df: Table DataFrame
            page_text: Text from the page
        
        Returns:
            Table type string
        """
        # Combine sources for checking
        text_to_check = (
            page_text.lower() + " " + 
            " ".join(df.columns).lower() + " " +
            " ".join(df.iloc[:, 0].astype(str)).lower()
        )
        
        # Check each pattern
        for table_type, patterns in self.table_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_to_check, re.IGNORECASE):
                    return table_type
        
        return 'other'
    
    def extract_financial_statements(
        self, 
        pdf_path: str
    ) -> Dict[str, List[pd.DataFrame]]:
        """
        Extract only financial statement tables
        
        Args:
            pdf_path: Path to PDF
        
        Returns:
            Dictionary of financial statements by type
        """
        all_tables = self.extract_all_tables(pdf_path)
        
        financial_statements = {
            'balance_sheet': [],
            'profit_loss': [],
            'cash_flow': [],
            'equity': [],
            'other': []
        }
        
        for table in all_tables:
            table_type = table['type']
            if table_type in financial_statements:
                financial_statements[table_type].append(table['data'])
        
        return financial_statements
    
    def save_tables_to_excel(
        self, 
        tables: List[Dict], 
        output_path: str
    ):
        """
        Save extracted tables to Excel file
        
        Args:
            tables: List of table dictionaries
            output_path: Output Excel file path
        """
        if self.verbose:
            print(f"\n💾 Saving tables to Excel: {output_path}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables[:20]):  # Max 20 tables
                sheet_name = f"{table['type'][:20]}_p{table['page']}"
                
                try:
                    table['data'].to_excel(
                        writer, 
                        sheet_name=sheet_name,
                        index=False
                    )
                except Exception as e:
                    if self.verbose:
                        print(f"   ⚠️  Error saving table {i}: {e}")
        
        if self.verbose:
            print(f"   ✅ Saved {min(len(tables), 20)} tables to Excel")


# ============================================
# TEST CODE
# ============================================

def test_table_extractor():
    """
    Test the table extractor
    """
    print("\n" + "="*70)
    print("🧪 TESTING TABLE EXTRACTOR")
    print("="*70)
    
    # Initialize
    extractor = TableExtractor(verbose=True)
    
    # Test PDF
    pdf_path = "data/sample_document/Dixon_2025.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  Test PDF not found: {pdf_path}")
        return
    
    # Extract tables
    tables = extractor.extract_all_tables(pdf_path, max_pages=100)
    
    # Show samples
    print(f"\n📊 SAMPLE TABLES:")
    print("="*70)
    
    for i, table in enumerate(tables[:3]):  # First 3 tables
        print(f"\nTable {i+1}:")
        print(f"   Type: {table['type']}")
        print(f"   Page: {table['page']}")
        print(f"   Size: {table['rows']} rows × {table['columns']} cols")
        print(f"   Preview:")
        print(table['data'].head(3))
        print("-"*70)
    
    # Save to Excel
    if tables:
        output_path = "data/outputs/extracted_tables.xlsx"
        extractor.save_tables_to_excel(tables, output_path)
    
    print(f"\n✅ Test complete!")


if __name__ == "__main__":
    test_table_extractor()
