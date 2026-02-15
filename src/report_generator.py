"""
Report Generator - HTML Report Creation Module
Author: Nawddeep
Date: February 2026

Features:
- Professional HTML reports
- Interactive charts (no external libs needed)
- Compliance summary
- Detailed findings
- Recommendations section
"""

from datetime import datetime
from typing import Dict, List
import os


class ReportGenerator:
    """
    Generates professional HTML compliance reports
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Report Generator
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
        
        if self.verbose:
            print("📝 Report Generator initialized")
    
    def generate_html_report(
        self,
        compliance_results: Dict,
        extraction_stats: Dict = None,
        pdf_filename: str = "Unknown",
        output_path: str = None
    ) -> str:
        """
        Generate complete HTML report
        
        Args:
            compliance_results: Results from ComplianceChecker
            extraction_stats: Stats from DocumentProcessor
            pdf_filename: Name of processed PDF
            output_path: Where to save report
        
        Returns:
            Path to generated report
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print("📝 Generating HTML Report")
            print(f"{'='*70}")
        
        # Default output path
        if output_path is None:
            output_path = "data/outputs/compliance_report.html"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate HTML
        html = self._build_html(
            compliance_results,
            extraction_stats,
            pdf_filename
        )
        
        # Save file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        if self.verbose:
            print(f"   ✅ Report generated: {output_path}")
            print(f"   📄 File size: {len(html):,} bytes")
        
        return output_path
    
    def _build_html(
        self,
        results: Dict,
        stats: Dict,
        pdf_filename: str
    ) -> str:
        """
        Build complete HTML content
        """
        summary = results['summary']
        detailed = results['detailed_results']
        
        # Calculate percentages
        total = summary['total_checks']
        compliant_pct = (summary['compliant'] / total * 100) if total else 0
        non_compliant_pct = (summary['non_compliant'] / total * 100) if total else 0
        missing_pct = (summary['missing'] / total * 100) if total else 0
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Compliance Report - {pdf_filename}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 16px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #1a202c;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #f7fafc;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        
        .metric-card.compliant {{
            border-left-color: #48bb78;
        }}
        
        .metric-card.non-compliant {{
            border-left-color: #f56565;
        }}
        
        .metric-card.missing {{
            border-left-color: #ed8936;
        }}
        
        .metric-value {{
            font-size: 42px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .metric-card.compliant .metric-value {{
            color: #48bb78;
        }}
        
        .metric-card.non-compliant .metric-value {{
            color: #f56565;
        }}
        
        .metric-card.missing .metric-value {{
            color: #ed8936;
        }}
        
        .metric-label {{
            color: #718096;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .score-value {{
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .score-label {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .rating {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.2);
            margin-top: 10px;
            font-weight: 600;
        }}
        
        .check-item {{
            background: white;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #cbd5e0;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            transition: all 0.2s;
        }}
        
        .check-item:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }}
        
        .check-item.compliant {{
            border-left-color: #48bb78;
            background: #f0fff4;
        }}
        
        .check-item.non_compliant {{
            border-left-color: #f56565;
            background: #fff5f5;
        }}
        
        .check-item.missing {{
            border-left-color: #ed8936;
            background: #fffaf0;
        }}
        
        .check-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .check-status {{
            font-size: 24px;
            margin-right: 12px;
        }}
        
        .check-title {{
            font-weight: 600;
            font-size: 16px;
            color: #2d3748;
        }}
        
        .check-details {{
            margin-left: 36px;
            color: #718096;
            font-size: 14px;
        }}
        
        .evidence {{
            background: #edf2f7;
            padding: 10px;
            border-radius: 5px;
            margin-top: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #4a5568;
        }}
        
        .standard-group {{
            margin-bottom: 30px;
        }}
        
        .standard-header {{
            background: #edf2f7;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .standard-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .standard-subtitle {{
            color: #718096;
            font-size: 14px;
            margin-top: 4px;
        }}
        
        .footer {{
            background: #f7fafc;
            padding: 30px;
            text-align: center;
            color: #718096;
            font-size: 14px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e2e8f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
            transition: width 1s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Financial Compliance Report</h1>
            <p>IndiaAI Challenge 2026 • Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- File Info -->
            <div class="section">
                <h2>📄 Document Information</h2>
                <p><strong>File:</strong> {pdf_filename}</p>
                <p><strong>Analysis Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                {self._generate_extraction_stats_html(stats)}
            </div>
            
            <!-- Executive Summary -->
            <div class="section">
                <h2>📈 Executive Summary</h2>
                
                <!-- Score Card -->
                <div class="score-card">
                    <div class="score-value">{summary['compliance_score']:.1f}%</div>
                    <div class="score-label">Overall Compliance Score</div>
                    <div class="rating">{self._get_rating_label(summary['compliance_score'])}</div>
                </div>
                
                <!-- Progress Bar -->
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {summary['compliance_score']:.1f}%">
                        {summary['compliant']}/{total} checks passed
                    </div>
                </div>
                
                <!-- Metrics Grid -->
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">{total}</div>
                        <div class="metric-label">Total Checks</div>
                    </div>
                    <div class="metric-card compliant">
                        <div class="metric-value">{summary['compliant']}</div>
                        <div class="metric-label">Compliant ({compliant_pct:.0f}%)</div>
                    </div>
                    <div class="metric-card non-compliant">
                        <div class="metric-value">{summary['non_compliant']}</div>
                        <div class="metric-label">Non-Compliant ({non_compliant_pct:.0f}%)</div>
                    </div>
                    <div class="metric-card missing">
                        <div class="metric-value">{summary['missing']}</div>
                        <div class="metric-label">Missing ({missing_pct:.0f}%)</div>
                    </div>
                </div>
            </div>
            
            <!-- Detailed Results -->
            <div class="section">
                <h2>🔍 Detailed Compliance Results</h2>
                {self._generate_detailed_results_html(detailed)}
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated by <strong>Financial Compliance AI</strong></p>
            <p>IndiaAI Financial Reporting Compliance Challenge 2026</p>
            <p style="margin-top: 10px; font-size: 12px;">
                This report was automatically generated. Please review findings with a compliance expert.
            </p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_extraction_stats_html(self, stats: Dict) -> str:
        """Generate extraction statistics HTML"""
        if not stats:
            return ""
        
        return f"""
                <p><strong>Extraction Method:</strong> {stats.get('method', 'N/A').upper()}</p>
                <p><strong>Pages Analyzed:</strong> {stats.get('total_pages', 'N/A')}</p>
                <p><strong>Characters Extracted:</strong> {stats.get('total_characters', 0):,}</p>
                <p><strong>Words Extracted:</strong> {stats.get('total_words', 0):,}</p>
        """
    
    def _generate_detailed_results_html(self, detailed: List[Dict]) -> str:
        """Generate detailed results HTML"""
        html_parts = []
        
        for standard in detailed:
            standard_html = f"""
                <div class="standard-group">
                    <div class="standard-header">
                        <div class="standard-title">{standard['standard_id']}: {standard['standard_name']}</div>
                        <div class="standard-subtitle">
                            Category: {standard.get('category', 'N/A').replace('_', ' ').title()} • 
                            Priority: {standard.get('priority', 'MEDIUM')} • 
                            Passed: {standard.get('compliant_count', 0)}/{standard.get('total_count', 0)} checks
                        </div>
                    </div>
            """
            
            # Add checks
            for check in standard['checks']:
                status_class = check['status'].lower().replace(' ', '_').replace('-', '_')
                
                check_html = f"""
                    <div class="check-item {status_class}">
                        <div class="check-header">
                            <span class="check-status">{check['symbol']}</span>
                            <span class="check-title">{check['requirement']}</span>
                        </div>
                        <div class="check-details">
                            <div><strong>Status:</strong> {check['status']}</div>
                            <div><strong>Check ID:</strong> {check['check_id']}</div>
                            <div><strong>Mandatory:</strong> {'Yes' if check.get('mandatory', True) else 'No'}</div>
                """
                
                if check.get('evidence'):
                    check_html += f"""
                            <div class="evidence">
                                💡 Evidence: "{check['evidence'][:150]}{'...' if len(check['evidence']) > 150 else ''}"
                            </div>
                    """
                
                check_html += """
                        </div>
                    </div>
                """
                
                standard_html += check_html
            
            standard_html += "</div>"
            html_parts.append(standard_html)
        
        return "\n".join(html_parts)
    
    def _get_rating_label(self, score: float) -> str:
        """Get rating label based on score"""
        if score >= 90:
            return "🌟 EXCELLENT"
        elif score >= 75:
            return "✅ GOOD"
        elif score >= 60:
            return "⚠️  FAIR"
        else:
            return "❌ NEEDS IMPROVEMENT"


# ============================================
# TEST CODE
# ============================================

def test_report_generator():
    """
    Test the report generator
    """
    print("\n" + "="*70)
    print("🧪 TESTING REPORT GENERATOR")
    print("="*70)
    
    # Mock compliance results
    mock_results = {
        'summary': {
            'total_checks': 20,
            'compliant': 15,
            'non_compliant': 3,
            'missing': 2,
            'compliance_score': 75.0,
            'total_weight': 100,
            'achieved_weight': 75
        },
        'detailed_results': [
            {
                'standard_id': 'IndAS-1',
                'standard_name': 'Presentation of Financial Statements',
                'category': 'financial_statements',
                'priority': 'HIGH',
                'compliant_count': 4,
                'total_count': 5,
                'checks': [
                    {
                        'check_id': 'IndAS1-1',
                        'requirement': 'Balance Sheet',
                        'status': 'COMPLIANT',
                        'symbol': '✅',
                        'mandatory': True,
                        'weight': 10,
                        'evidence': 'Found: "balance sheet as at March 31, 2024"'
                    },
                    {
                        'check_id': 'IndAS1-2',
                        'requirement': 'Profit & Loss Statement',
                        'status': 'COMPLIANT',
                        'symbol': '✅',
                        'mandatory': True,
                        'weight': 10,
                        'evidence': 'Found: "statement of profit and loss"'
                    },
                    {
                        'check_id': 'IndAS1-5',
                        'requirement': 'Notes to Accounts',
                        'status': 'NON-COMPLIANT',
                        'symbol': '❌',
                        'mandatory': True,
                        'weight': 10,
                        'evidence': None
                    }
                ]
            }
        ],
        'document_length': 250000,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    mock_stats = {
        'method': 'digital',
        'total_pages': 250,
        'total_characters': 250000,
        'total_words': 45000
    }
    
    # Generate report
    generator = ReportGenerator(verbose=True)
    output_path = generator.generate_html_report(
        compliance_results=mock_results,
        extraction_stats=mock_stats,
        pdf_filename="test_annual_report.pdf",
        output_path="data/outputs/test_report.html"
    )
    
    print(f"\n✅ Test report generated!")
    print(f"   📄 Open in browser: file://{os.path.abspath(output_path)}")


if __name__ == "__main__":
    test_report_generator()
