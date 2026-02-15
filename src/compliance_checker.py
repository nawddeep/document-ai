"""
Compliance Checker - Core Validation Engine
Author: Nawddeep
Date: February 2026

Features:
- Rule-based compliance checking
- Keyword matching with multiple patterns
- Weighted scoring system
- Detailed explanations
- Evidence tracking
"""

import json
import re
from typing import Dict, List, Optional
from pathlib import Path


class ComplianceChecker:
    """
    Checks financial documents against regulatory requirements
    """
    
    def __init__(self, rules_path: str = None, verbose: bool = True):
        """
        Initialize Compliance Checker
        
        Args:
            rules_path: Path to rules JSON file
            verbose: Print progress messages
        """
        self.verbose = verbose
        
        # Default rules path
        if rules_path is None:
            rules_path = "data/regulations/rules_index.json"
        
        self.rules_path = rules_path
        self.rules = self._load_rules()
        
        if self.verbose:
            total_standards = len(self.rules)
            total_checks = sum(len(std['checks']) for std in self.rules.values())
            print(f"✅ Compliance Checker initialized")
            print(f"   📋 Loaded {total_standards} standards")
            print(f"   🔍 Total checks: {total_checks}")
    
    def _load_rules(self) -> Dict:
        """
        Load compliance rules from JSON file
        
        Returns:
            Rules dictionary
        """
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            
            if self.verbose:
                print(f"   📄 Rules loaded from: {self.rules_path}")
            
            return rules
        
        except FileNotFoundError:
            print(f"   ❌ Rules file not found: {self.rules_path}")
            print(f"   💡 Using minimal default rules")
            return self._get_default_rules()
        
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON in rules file: {e}")
            return self._get_default_rules()
    
    def _get_default_rules(self) -> Dict:
        """
        Minimal default rules if file not found
        """
        return {
            "IndAS-1": {
                "name": "Financial Statements",
                "checks": [
                    {
                        "id": "IndAS1-1",
                        "requirement": "Balance Sheet",
                        "keywords": ["balance sheet"],
                        "mandatory": True,
                        "weight": 10
                    }
                ]
            }
        }
    
    def check_compliance(
        self, 
        document_text: str,
        sections: Optional[Dict] = None
    ) -> Dict:
        """
        Main compliance checking function
        
        Args:
            document_text: Full document text
            sections: Optional pre-segmented document sections
        
        Returns:
            Compliance results dictionary
        """
        if self.verbose:
            print("\n" + "="*70)
            print("🔍 RUNNING COMPLIANCE CHECKS")
            print("="*70)
        
        # Prepare text for searching
        document_text_lower = document_text.lower()
        
        # Initialize results
        all_results = []
        summary = {
            'total_checks': 0,
            'compliant': 0,
            'non_compliant': 0,
            'missing': 0,
            'total_weight': 0,
            'achieved_weight': 0
        }
        
        # Check each standard
        for standard_id, standard_info in self.rules.items():
            if self.verbose:
                print(f"\n📌 {standard_id}: {standard_info['name']}")
                print("-"*70)
            
            standard_results = {
                'standard_id': standard_id,
                'standard_name': standard_info['name'],
                'category': standard_info.get('category', 'general'),
                'priority': standard_info.get('priority', 'MEDIUM'),
                'checks': [],
                'compliant_count': 0,
                'total_count': 0
            }
            
            # Check each requirement
            for check in standard_info['checks']:
                summary['total_checks'] += 1
                standard_results['total_count'] += 1
                
                weight = check.get('weight', 5)
                summary['total_weight'] += weight
                
                # Search for keywords
                found, evidence = self._search_keywords(
                    document_text_lower,
                    check['keywords']
                )
                
                # Determine status
                if found:
                    status = "COMPLIANT"
                    symbol = "✅"
                    summary['compliant'] += 1
                    summary['achieved_weight'] += weight
                    standard_results['compliant_count'] += 1
                else:
                    if check.get('mandatory', True):
                        status = "NON-COMPLIANT"
                        symbol = "❌"
                        summary['non_compliant'] += 1
                    else:
                        status = "MISSING"
                        symbol = "⚠️"
                        summary['missing'] += 1
                
                # Store check result
                check_result = {
                    'check_id': check['id'],
                    'requirement': check['requirement'],
                    'status': status,
                    'symbol': symbol,
                    'mandatory': check.get('mandatory', True),
                    'weight': weight,
                    'evidence': evidence,
                    'keywords_searched': check['keywords']
                }
                
                standard_results['checks'].append(check_result)
                
                # Print result
                if self.verbose:
                    print(f"   {symbol} {status:15} - {check['requirement']}")
                    if evidence:
                        # Truncate evidence for display
                        evidence_preview = evidence[:80] + "..." if len(evidence) > 80 else evidence
                        print(f"      💡 Evidence: '{evidence_preview}'")
            
            all_results.append(standard_results)
        
        # Calculate compliance score
        if summary['total_weight'] > 0:
            compliance_score = (summary['achieved_weight'] / summary['total_weight']) * 100
        else:
            compliance_score = 0
        
        summary['compliance_score'] = round(compliance_score, 2)
        
        # Print summary
        if self.verbose:
            self._print_summary(summary)
        
        return {
            'summary': summary,
            'detailed_results': all_results,
            'document_length': len(document_text),
            'timestamp': self._get_timestamp()
        }
    
    def _search_keywords(
        self, 
        text: str, 
        keywords: List[str]
    ) -> tuple:
        """
        Search for keywords in text
        
        Args:
            text: Document text (lowercase)
            keywords: List of keywords to search
        
        Returns:
            (found: bool, evidence: str or None)
        """
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            if keyword_lower in text:
                # Find context around the keyword
                evidence = self._extract_context(text, keyword_lower)
                return (True, evidence)
        
        return (False, None)
    
    def _extract_context(
        self, 
        text: str, 
        keyword: str,
        context_length: int = 100
    ) -> str:
        """
        Extract context around found keyword
        
        Args:
            text: Full text
            keyword: Found keyword
            context_length: Characters before/after
        
        Returns:
            Context string
        """
        index = text.find(keyword)
        
        if index == -1:
            return keyword
        
        start = max(0, index - context_length)
        end = min(len(text), index + len(keyword) + context_length)
        
        context = text[start:end].strip()
        
        # Clean up
        context = " ".join(context.split())
        
        return context
    
    def _print_summary(self, summary: Dict):
        """
        Print compliance summary
        
        Args:
            summary: Summary dictionary
        """
        print("\n" + "="*70)
        print("📊 COMPLIANCE SUMMARY")
        print("="*70)
        
        total = summary['total_checks']
        
        print(f"\n   📋 Total Checks:     {total}")
        print(f"   ✅ Compliant:        {summary['compliant']} ({summary['compliant']*100//total if total else 0}%)")
        print(f"   ❌ Non-Compliant:    {summary['non_compliant']} ({summary['non_compliant']*100//total if total else 0}%)")
        print(f"   ⚠️  Missing:          {summary['missing']} ({summary['missing']*100//total if total else 0}%)")
        
        print(f"\n   🎯 Compliance Score: {summary['compliance_score']:.1f}%")
        print(f"   📊 Weighted Score:   {summary['achieved_weight']}/{summary['total_weight']}")
        
        # Rating
        score = summary['compliance_score']
        if score >= 90:
            rating = "🌟 EXCELLENT"
        elif score >= 75:
            rating = "✅ GOOD"
        elif score >= 60:
            rating = "⚠️  FAIR"
        else:
            rating = "❌ POOR"
        
        print(f"   🏆 Rating:           {rating}")
        print("="*70)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_non_compliant_items(self, results: Dict) -> List[Dict]:
        """
        Extract all non-compliant items
        
        Args:
            results: Compliance check results
        
        Returns:
            List of non-compliant items
        """
        non_compliant = []
        
        for standard in results['detailed_results']:
            for check in standard['checks']:
                if check['status'] in ['NON-COMPLIANT', 'MISSING']:
                    non_compliant.append({
                        'standard': standard['standard_name'],
                        'requirement': check['requirement'],
                        'status': check['status'],
                        'priority': standard['priority']
                    })
        
        return non_compliant
    
    def generate_recommendations(self, results: Dict) -> List[str]:
        """
        Generate recommendations based on compliance gaps
        
        Args:
            results: Compliance check results
        
        Returns:
            List of recommendations
        """
        recommendations = []
        non_compliant = self.get_non_compliant_items(results)
        
        # High priority issues
        high_priority = [nc for nc in non_compliant if nc['priority'] == 'HIGH']
        
        if high_priority:
            recommendations.append(
                f"🔴 URGENT: Address {len(high_priority)} high-priority compliance gaps"
            )
        
        # Specific recommendations
        for item in non_compliant[:5]:  # Top 5
            recommendations.append(
                f"   - Add {item['requirement']} ({item['standard']})"
            )
        
        # Score-based recommendations
        score = results['summary']['compliance_score']
        
        if score < 60:
            recommendations.append(
                "💡 Consider comprehensive compliance review"
            )
        elif score < 80:
            recommendations.append(
                "💡 Focus on missing high-priority disclosures"
            )
        
        return recommendations


# ============================================
# TEST CODE
# ============================================

def test_compliance_checker():
    """
    Test the compliance checker
    """
    print("\n" + "="*70)
    print("🧪 TESTING COMPLIANCE CHECKER")
    print("="*70)
    
    # Initialize
    checker = ComplianceChecker(
        rules_path="data/regulations/rules_index.json",
        verbose=True
    )
    
    # Sample document text (simulated)
    sample_text = """
    HDFC Bank Limited
    Annual Report 2024
    
    Balance Sheet as at March 31, 2024
    
    Assets:
    Non-current assets
    Property, plant and equipment
    Current assets
    
    Liabilities:
    Current liabilities
    Non-current liabilities
    
    Statement of Profit and Loss for the year ended March 31, 2024
    Revenue from operations
    Other income
    Total income
    
    Expenses:
    Employee benefits expense
    Depreciation and amortization
    
    Statement of Cash Flows for the year ended March 31, 2024
    Cash flows from operating activities
    Cash flows from investing activities
    Cash flows from financing activities
    
    Notes to Financial Statements
    
    1. Corporate Information
    2. Significant Accounting Policies
    3. Property, Plant and Equipment
       Gross block
       Accumulated depreciation
        
    24. Related Party Disclosures
        List of related parties
        Transactions with related parties
        Key management personnel compensation
        
    
    Independent Auditor's Report
    Opinion: Unqualified
    Key Audit Matters
    Basis for opinion
    """
    
    # Run compliance check
    results = checker.check_compliance(sample_text)
    
    # Get recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    recommendations = checker.generate_recommendations(results)
    for rec in recommendations:
        print(rec)
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    test_compliance_checker()
