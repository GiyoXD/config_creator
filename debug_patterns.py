#!/usr/bin/env python3
"""
Debug specific pattern issues.
"""

from enhanced_text_processor import EnhancedTextProcessor

def debug_patterns():
    processor = EnhancedTextProcessor()
    
    print("DEBUGGING INDIVIDUAL PATTERNS")
    print("=" * 50)
    
    # Test cases that might be problematic
    problematic_cases = [
        "date.... 07/25/2025",
        "invoice no: 12345", 
        "invoice no### 67890",
        "ref no: ABC123-456",
        "ref no::: XYZ789-001"
    ]
    
    for case in problematic_cases:
        match = processor._find_label_match(case)
        if match:
            print(f"✅ '{case}' -> {match['category']} -> {match['replacement']}")
        else:
            print(f"❌ '{case}' -> NO MATCH")
    
    print("\nDEBUGGING REGEX PATTERNS")
    print("=" * 50)
    
    # Test the regex patterns directly
    import re
    
    test_text = "invoice no: 12345"
    patterns = processor.get_replacement_patterns()
    
    print(f"Testing text: '{test_text}'")
    for category, config in patterns.items():
        for pattern in config['patterns']:
            match = re.search(pattern, test_text, re.IGNORECASE)
            if match:
                print(f"  ✅ Category '{category}' pattern '{pattern}' MATCHED")
            else:
                print(f"  ❌ Category '{category}' pattern '{pattern}' NO MATCH")

if __name__ == "__main__":
    try:
        debug_patterns()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

