@echo off
echo 🧠 AI Tutor - Instant Educational Shorts Generator
echo ================================================

echo.
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found!

echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed!

echo.
echo 🔧 Setting up configuration...
echo Make sure to set your GEMINI_API_KEY environment variable!
python setup.py

echo.
echo 🚀 Starting AI Tutor application...
echo.
echo 🌐 Your app will open in your default browser
echo 🛑 Press Ctrl+C to stop the application
echo.

streamlit run ai_tutor_app.py

pause
