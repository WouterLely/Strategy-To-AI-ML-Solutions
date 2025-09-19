#!/usr/bin/env python3
"""
TechAdvance Solutions - Automated Startup Script
Automatically creates database and starts the Streamlit application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_env_file():
    """Check if .env file exists, create template if it doesn't"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("🔧 .env file not found. Creating template...")
        try:
            env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Instructions:
# 1. Get your API key from: https://platform.openai.com/api-keys
# 2. Replace 'your_openai_api_key_here' with your actual API key
# 3. Save this file and restart the application"""
            
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            
            print("✅ .env template created!")
            print("📝 Please edit .env file and add your OpenAI API key")
            print("🔗 Get your API key from: https://platform.openai.com/api-keys")
            return False
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def check_database():
    """Check if database exists, create if it doesn't"""
    db_path = Path("data/database/company.db")
    
    if not db_path.exists():
        print("🔧 Database not found. Creating database...")
        try:
            # Ensure the database directory exists
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Run the database creation script
            result = subprocess.run([sys.executable, "scripts/create_database.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Database created successfully!")
            else:
                print(f"❌ Database creation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    else:
        print("✅ Database already exists")
    
    return True

def start_streamlit():
    """Start the Streamlit application"""
    print("🚀 Starting TechAdvance Solutions platform...")
    
    try:
        # Start Streamlit with the enterprise app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/enterprise_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main startup function"""
    print("🌟 TechAdvance Solutions - Automated Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app/enterprise_app.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check and create .env file if needed
    if not check_env_file():
        print("❌ Failed to setup .env file. Exiting...")
        sys.exit(1)
    
    # Check and create database if needed
    if not check_database():
        print("❌ Failed to setup database. Exiting...")
        sys.exit(1)
    
    # Start the application
    start_streamlit()

if __name__ == "__main__":
    main()
