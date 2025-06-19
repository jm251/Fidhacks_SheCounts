#!/usr/bin/env python3
"""
Setup script for SheCounts Financial Literacy Chatbot
This script helps you set up the chatbot frontend and backend.
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def setup_api_keys():
    """Guide user through API key setup"""
    print("\n" + "="*50)
    print("API KEY SETUP")
    print("="*50)
    
    print("\nYou need to configure the following API keys:")
    print("1. Google Gemini API Key")
    print("   - Visit: https://makersuite.google.com/app/apikey")
    print("   - Create a new API key")
    
    print("\n2. Pinecone API Key")
    print("   - Visit: https://app.pinecone.io/")
    print("   - Create an account and get your API key")
    
    print("\n3. Update the API keys in chatbot_backend.py:")
    print("   - Replace 'YOUR_API_KEY_HERE' with your Gemini API key")
    print("   - Replace 'YOUR_PINECONE_API_KEY_HERE' with your Pinecone API key")
    
    input("\nPress Enter when you have updated the API keys...")

def create_templates_folder():
    """Create Flask templates folder and move HTML file"""
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"✓ Created {templates_dir} directory")
    
    # Check if HTML file exists in parent directory
    html_file = "../chatbot_frontend.html"
    target_file = os.path.join(templates_dir, "chatbot_frontend.html")
    
    if os.path.exists(html_file) and not os.path.exists(target_file):
        try:
            import shutil
            shutil.copy2(html_file, target_file)
            print(f"✓ Copied HTML file to {target_file}")
        except Exception as e:
            print(f"✗ Error copying HTML file: {e}")
            print(f"  Please manually copy {html_file} to {target_file}")

def run_setup():
    """Run the complete setup process"""
    print("SheCounts Financial Literacy Chatbot Setup")
    print("="*45)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("✗ Error: requirements.txt not found!")
        print("  Please run this script from the 'chatbots code' directory")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create templates folder
    create_templates_folder()
    
    # Setup API keys
    setup_api_keys()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("\nTo start the chatbot:")
    print("1. Make sure your API keys are configured in chatbot_backend.py")
    print("2. Run: python chatbot_backend.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nFor development, you can also run the original Streamlit version:")
    print("   streamlit run chatbot_code_template.py")
    
    return True

if __name__ == "__main__":
    success = run_setup()
    if not success:
        sys.exit(1)
