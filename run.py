#!/usr/bin/env python3
"""
SQL Agent - Excel to SQL Query Generator
Startup script for the application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'openpyxl',
        'sqlalchemy',
        'langchain',
        'langchain_google_genai',
        'google_generativeai',
        'plotly',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🤖 SQL Agent - Excel to SQL Query Generator")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies are installed")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        sys.exit(1)
    
    print("🚀 Starting the application...")
    print("📱 Open your browser and go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 