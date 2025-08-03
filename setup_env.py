#!/usr/bin/env python3
"""
Setup script for SQL Agent - Excel to SQL
Helps users create their .env file with API key configuration
"""

import os
import getpass
from pathlib import Path

def main():
    print("🔧 SQL Agent - Environment Setup")
    print("=" * 40)
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Get API key from user
    print("\n🔑 Google Gemini API Key Setup")
    print("You can get your API key from: https://makersuite.google.com/app/apikey")
    print()
    
    api_key = getpass.getpass("Enter your Google Gemini API key (input will be hidden): ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Create .env file
    env_content = f"""# Google Gemini API Configuration
# This file contains your API key - keep it secure!
GEMINI_API_KEY={api_key}

# Alternative: You can also use GOOGLE_API_KEY
# GOOGLE_API_KEY={api_key}

# Database Configuration (optional)
# DATABASE_PATH=./data/database.db

# Application Configuration (optional)
# DEBUG=True
# LOG_LEVEL=INFO
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print("🔒 Your API key is now securely stored in the .env file")
        print("📝 The .env file is already included in .gitignore for security")
        print("\n🚀 You can now run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

if __name__ == "__main__":
    main() 