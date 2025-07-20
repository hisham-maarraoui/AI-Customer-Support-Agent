#!/usr/bin/env python3
"""
Test script for Google Gemini integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_import():
    """Test if Google Gemini can be imported"""
    try:
        import google.generativeai as genai
        print("✅ Google Gemini import successful")
        return True
    except ImportError as e:
        print(f"❌ Google Gemini import failed: {e}")
        return False

def test_gemini_configuration():
    """Test if Google Gemini can be configured"""
    try:
        import google.generativeai as genai
        
        # Check if API key is set
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_google_api_key_here':
            print("⚠️  Google API key not configured (using placeholder)")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        print("✅ Google Gemini configuration successful")
        return True
    except Exception as e:
        print(f"❌ Google Gemini configuration failed: {e}")
        return False

def test_gemini_model():
    """Test if Gemini model can be created"""
    try:
        import google.generativeai as genai
        
        # Configure Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and api_key != 'your_google_api_key_here':
            genai.configure(api_key=api_key)
            
            # Create model
            model = genai.GenerativeModel('gemini-1.5-pro')
            print("✅ Gemini model creation successful")
            return True
        else:
            print("⚠️  Skipping model test - API key not configured")
            return False
    except Exception as e:
        print(f"❌ Gemini model creation failed: {e}")
        return False

def test_ai_agent_import():
    """Test if AI agent can be imported"""
    try:
        from app.services.ai_agent import AIAgentService
        print("✅ AI Agent import successful")
        return True
    except Exception as e:
        print(f"❌ AI Agent import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Google Gemini Integration")
    print("=" * 40)
    
    tests = [
        ("Gemini Import", test_gemini_import),
        ("Gemini Configuration", test_gemini_configuration),
        ("Gemini Model", test_gemini_model),
        ("AI Agent Import", test_ai_agent_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Google Gemini integration is working.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 