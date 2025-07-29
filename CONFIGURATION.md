# 🔧 Configuration Guide

## API Keys Setup

This application requires two API keys:

### 1. VideoDB API Key
- **Where to get**: [VideoDB Console](https://console.videodb.io/)
- **Free tier**: 50 uploads, no credit card required
- **Environment variable**: `VIDEODB_API_KEY`

### 2. Gemini API Key
- **Where to get**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Free tier**: Available with rate limits
- **Environment variable**: `GEMINI_API_KEY` (Note: This changed from `GOOGLE_API_KEY`)

## Setup Methods

### Method 1: Environment Variables (Recommended for local development)

**Windows (PowerShell):**
```powershell
$env:VIDEODB_API_KEY="sk-dHWGyJA7BJ_3j2DHR7pzrtf3z6AnGllzciooMTS7URc"
$env:GEMINI_API_KEY="AIzaSyA0VHjInnHnOw7deFZqbx7XSir2wrCci0c"
```

**Windows (Command Prompt):**
```cmd
set VIDEODB_API_KEY=your_videodb_key_here
set GEMINI_API_KEY=your_gemini_key_here
```

**Linux/Mac:**
```bash
export VIDEODB_API_KEY="your_videodb_key_here"
export GEMINI_API_KEY="your_gemini_key_here"
```

### Method 2: Streamlit Secrets (Recommended for deployment)

1. Create `.streamlit` folder in your project directory
2. Create `.streamlit/secrets.toml` file:
```toml
VIDEODB_API_KEY = "your_videodb_key_here"
GEMINI_API_KEY = "your_gemini_key_here"
```

### Method 3: .env File (Alternative)

Create a `.env` file in your project root:
```
VIDEODB_API_KEY=your_videodb_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Verification

To test if your setup is working:

1. Run the application: `streamlit run ai_tutor_app.py`
2. Check for any API key warnings in the UI
3. Try processing a short YouTube video (2-5 minutes recommended for testing)

## Troubleshooting

### "API key not found" errors
- Double-check the environment variable names (especially `GEMINI_API_KEY`)
- Restart your terminal/IDE after setting environment variables
- Verify your API keys are valid and active

### "Invalid YouTube URL" errors
- Ensure the URL is a public YouTube video
- Try different URL formats (youtube.com/watch?v= or youtu.be/)

### "Video processing failed" errors
- Some videos may have restricted access or copyright protection
- Try with educational content or videos with clear spoken audio
- Shorter videos (under 10 minutes) work better for testing

### "No segments found" errors
- This can happen with videos that have unclear audio or non-educational content
- Try with videos that have clear, educational spoken content
- Ensure the video has been properly indexed (this can take time for longer videos)

## Best Practices

1. **Test with short videos first** (2-5 minutes)
2. **Use educational content** with clear speech
3. **Avoid copyrighted or restricted content**
4. **Be patient** - indexing longer videos can take several minutes

## API Limits

### VideoDB
- Free tier: 50 video uploads
- Processing time depends on video length

### Google Gemini
- Free tier available with rate limits
- Monitor usage in Google AI Studio console

## Security Notes

- Never commit API keys to version control
- Use environment variables or Streamlit secrets
- Regenerate keys if accidentally exposed
