@echo off
echo Starting Klipify with New UI...
echo.
echo Make sure you have:
echo - VideoDB API key in secrets.toml
echo - Google GenAI API key in secrets.toml
echo.
echo Opening in your default browser...
echo.

streamlit run klipify_new_ui.py --server.port 8504

pause
