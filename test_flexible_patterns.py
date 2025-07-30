#!/usr/bin/env python3
"""
Test the flexible pattern detection without PowerShell string issues.
"""

from enhanced_text_processor import EnhancedTextProcessor

def test_flexible_patterns():
    processor = EnhancedTextProcessor()
    
    print("=" * 60)
    print("TESTING FLEXIBLE PATTERN DETECTION")
    print("=" * 60)
    
    # Test cases with various punctuation
    test_cases = [
        "date: 25/07/2025",
        "date.... 07/25/2025", 
        "date:,.,.m.m,, 2025/07/25",
        "invoice no: 12345",
        "invoice no### 67890",
        "ref no: ABC123-456",
        "ref no::: XYZ789-001",
        "etd: 15/08/2025",
        "etd.... 2025/08/15",
        "departure### 25/12/2024"
    ]
    
    print("Testing pattern detection:")
    for case in test_cases:
        match = processor._find_label_match(case)
        if match:
            result = f"MATCH -> {match['category']} -> {match['replacement']}"
        else:
            result = "NO MATCH"
        print(f"  '{case}' -> {result}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    test_flexible_patterns() 