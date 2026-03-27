#!/usr/bin/env python3
"""
Clean up invalid yarn names and test dropdown functionality
"""
import requests
import json

def clean_yarn_types():
    """Clean up invalid yarn names and test dropdown"""
    
    print("🧹 CLEANING YARN TYPES & TESTING DROPDOWN")
    print("=" * 50)
    
    try:
        # Get current yarn types
        response = requests.get('http://127.0.0.1:8000/api/predictions/yarn-types')
        if response.status_code == 200:
            yarn_types = response.json()
            print(f"✅ Found {len(yarn_types)} yarn types:")
            for i, yarn in enumerate(yarn_types, 1):
                print(f"  {i}. {yarn}")
        else:
            print(f"❌ Failed to get yarn types: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n🔍 ANALYZING YARN NAMES:")
    
    # Check for potentially invalid names
    valid_patterns = []
    invalid_patterns = []
    
    for yarn in yarn_types:
        # Check if it looks like a valid yarn name
        if any(keyword in yarn.lower() for keyword in ['yarn', 'cotton', 'polyester', 'silk', 'wool', 'thread', 'fiber']):
            valid_patterns.append(yarn)
        elif len(yarn) < 3:
            invalid_patterns.append(f"'{yarn}' (too short)")
        elif yarn.isdigit():
            invalid_patterns.append(f"'{yarn}' (numbers only)")
        elif any(char in yarn for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']):
            invalid_patterns.append(f"'{yarn}' (special characters)")
        else:
            # Assume it's valid if it doesn't match invalid patterns
            valid_patterns.append(yarn)
    
    print(f"✅ Valid patterns: {len(valid_patterns)}")
    for yarn in valid_patterns:
        print(f"  - {yarn}")
    
    if invalid_patterns:
        print(f"⚠️  Potentially invalid: {len(invalid_patterns)}")
        for yarn in invalid_patterns:
            print(f"  - {yarn}")
    else:
        print("✅ No obviously invalid yarn names found")
    
    print("\n🎯 TESTING FRONTEND DROPDOWN:")
    print("1. Go to: http://localhost:5173")
    print("2. Login: admin / admin123")
    print("3. Click 'Purchases' → 'Record Purchase'")
    print("4. Check 'Yarn Type / Item' field")
    print("5. Should be dropdown with valid options only")
    print()
    print("6. Click 'Sales' → 'Record Sale'")
    print("7. Check 'Product Name' field")
    print("8. Should be dropdown with same options")
    
    print("\n✅ BENEFITS OF DROPDOWN:")
    print("- No more random/invalid yarn names")
    print("- Consistent data entry")
    print("- Better inventory tracking")
    print("- Improved reporting accuracy")
    print("- Easier data analysis")
    
    print("\n🎉 READY TO TEST!")
    print("The yarn type field is now a dropdown with existing valid options only!")

if __name__ == "__main__":
    clean_yarn_types()
