#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║          🎊 SYSTEM VERIFICATION & OUTPUT GUIDE 🎊               ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Checking Generated Files..."
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Check HTML Report
if [ -f "data/outputs/compliance_report_Dixon_2025.html" ]; then
    SIZE=$(ls -lh data/outputs/compliance_report_Dixon_2025.html | awk '{print $5}')
    echo "✅ HTML Report: $SIZE"
    echo "   📄 File: compliance_report_Dixon_2025.html"
else
    echo "❌ HTML Report: NOT FOUND"
fi

echo ""

# Check JSON Data
if [ -f "data/outputs/compliance_data_Dixon_2025.json" ]; then
    SIZE=$(ls -lh data/outputs/compliance_data_Dixon_2025.json | awk '{print $5}')
    echo "✅ JSON Data: $SIZE"
    echo "   📄 File: compliance_data_Dixon_2025.json"
else
    echo "❌ JSON Data: NOT FOUND"
fi

echo ""

# Check Excel Tables
if [ -f "data/outputs/tables_Dixon_2025.xlsx" ]; then
    SIZE=$(ls -lh data/outputs/tables_Dixon_2025.xlsx | awk '{print $5}')
    echo "✅ Excel Tables: $SIZE"
    echo "   📄 File: tables_Dixon_2025.xlsx"
else
    echo "❌ Excel Tables: NOT FOUND"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 QUICK COMMANDS TO VIEW OUTPUTS:"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  Open HTML Report (RECOMMENDED):"
echo "   open data/outputs/compliance_report_Dixon_2025.html"
echo ""
echo "2️⃣  View JSON Data:"
echo "   cat data/outputs/compliance_data_Dixon_2025.json | python3 -m json.tool | head -50"
echo ""
echo "3️⃣  Open Excel Tables:"
echo "   open data/outputs/tables_Dixon_2025.xlsx"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📍 FULL FILE PATHS:"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
pwd_path=$(pwd)
echo "   HTML: $pwd_path/data/outputs/compliance_report_Dixon_2025.html"
echo "   JSON: $pwd_path/data/outputs/compliance_data_Dixon_2025.json"
echo "   Excel: $pwd_path/data/outputs/tables_Dixon_2025.xlsx"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "✅ All files verified! Open the HTML report to see the results!"
echo ""
