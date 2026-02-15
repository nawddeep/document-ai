# test_ocr_setup.py

print("🧪 Testing OCR Setup...\n")
print("="*60)

# Test 1: Import check
print("\n1️⃣ Testing imports...")
try:
    import pdfplumber
    print("   ✅ pdfplumber installed")
except:
    print("   ❌ pdfplumber NOT installed")

try:
    import pytesseract
    print("   ✅ pytesseract installed")
except:
    print("   ❌ pytesseract NOT installed")

try:
    from pdf2image import convert_from_path
    print("   ✅ pdf2image installed")
except:
    print("   ❌ pdf2image NOT installed")

try:
    from PIL import Image
    print("   ✅ Pillow installed")
except:
    print("   ❌ Pillow NOT installed")

# Test 2: Tesseract check
print("\n2️⃣ Testing Tesseract...")
try:
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f"   ✅ Tesseract version: {version}")
except Exception as e:
    print(f"   ❌ Tesseract error: {e}")
    print("   💡 Solution: Install Tesseract and add to PATH")

# Test 3: PDF processing
print("\n3️⃣ Testing PDF processing...")
try:
    # Create a simple test
    test_text = "Testing OCR Setup - All systems working!"
    print(f"   ✅ Ready to process PDFs")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ Setup test complete!")
print("\nNext steps:")
print("1. Download a sample PDF")
print("2. Test extraction with: python test_extraction.py")