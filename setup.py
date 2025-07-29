"""
Configuration and setup utilities for the AI Tutor application.
"""

import os
import streamlit as st
from pathlib import Path


def setup_streamlit_secrets():
    """
    Create the .streamlit directory and secrets.toml file if they don't exist.
    """
    streamlit_dir = Path(".streamlit")
    secrets_file = streamlit_dir / "secrets.toml"
    
    if not streamlit_dir.exists():
        streamlit_dir.mkdir(exist_ok=True)
        print(f"✅ Created {streamlit_dir} directory")
    
    if not secrets_file.exists():
        secrets_content = """# Streamlit secrets configuration
# Add your actual API keys here

VIDEODB_API_KEY = "your_videodb_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
"""
        with open(secrets_file, "w") as f:
            f.write(secrets_content)
        print(f"✅ Created {secrets_file}")
        print("📝 Please edit .streamlit/secrets.toml and add your actual API keys")
    else:
        print(f"ℹ️  {secrets_file} already exists")


def check_api_keys():
    """
    Check if API keys are properly configured.
    
    Returns:
        tuple: (videodb_key_found, google_key_found)
    """
    # Check VideoDB API key
    videodb_key = st.secrets.get("VIDEODB_API_KEY") or os.getenv("VIDEODB_API_KEY")
    videodb_configured = videodb_key and videodb_key != "your_videodb_api_key_here"
    
    # Check Google API key
    google_key = os.getenv("GEMINI_API_KEY")
    google_configured = google_key and google_key != "your_gemini_api_key_here"
    
    return videodb_configured, google_configured


if __name__ == "__main__":
    print("🔧 Setting up AI Tutor application...")
    setup_streamlit_secrets()
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .streamlit/secrets.toml with your actual API keys")
    print("2. Run: streamlit run ai_tutor_app.py")
