#!/usr/bin/env python3
"""
Fix Pydantic Secret import issue
"""
import os
import sys

def fix_pydantic_import():
    """Fix the Secret import issue in pydantic_settings"""
    
    print("🔧 FIXING PYDANTIC IMPORT ISSUE")
    print("=" * 40)
    
    # Path to the problematic file
    utils_file = r"C:\Users\divya\miniconda3\Lib\site-packages\pydantic_settings\sources\utils.py"
    
    try:
        # Read the file
        with open(utils_file, 'r') as f:
            content = f.read()
        
        # Check if the problematic import exists
        if "from pydantic import BaseModel, Json, RootModel, Secret" in content:
            print("✅ Found problematic import")
            
            # Fix the import
            fixed_content = content.replace(
                "from pydantic import BaseModel, Json, RootModel, Secret",
                "from pydantic import BaseModel, Json, RootModel\ntry:\n    from pydantic import Secret\nexcept ImportError:\n    from pydantic.v1 import Secret"
            )
            
            # Write the fixed content back
            with open(utils_file, 'w') as f:
                f.write(fixed_content)
            
            print("✅ Fixed import issue")
            return True
        else:
            print("❌ Import issue not found or already fixed")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing import: {e}")
        return False

if __name__ == "__main__":
    if fix_pydantic_import():
        print("\n🎉 PYDANTIC IMPORT FIXED!")
        print("🔄 Please restart the backend server")
    else:
        print("\n❌ Could not fix the import issue")
        print("💡 Alternative: Install compatible pydantic version")
        print("   pip install pydantic==1.10.13 pydantic-settings==2.0.3")
