# 🚀 Klipify - AI Educational Video Platform

**Transform any YouTube video into a comprehensive learning experience with AI-powered clips, summaries, notes, and chat.**

## 🎯 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed
- **VideoDB API Key**: [Get it here](https://console.videodb.io/)
- **Google Gemini API Key**: [Get it here](https://aistudio.google.com/app/apikey)

### ⚡ Fast Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd klipify
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Add your API keys:
   ```toml
   [secrets]
   VIDEODB_API_KEY = "your_videodb_api_key_here"
   GOOGLE_API_KEY = "your_google_gemini_api_key_here"
   ```

4. **Launch Application**
   ```bash
   # Option 1: Use the batch file (Windows)
   run_new_ui.bat
   
   # Option 2: Direct command
   streamlit run klipify_new_ui.py
   ```

5. **Open Browser**
   - Navigate to `http://localhost:8501`
   - Start processing YouTube videos!

## ✨ Features

- 🎬 **Smart Video Clips** - AI extracts key educational segments
- 📊 **AI Summaries** - Comprehensive content analysis  
- 📝 **Timestamped Notes** - Interactive study materials
- 💬 **AI Chat Assistant** - Ask questions about video content
- 📁 **Video Management** - Organize and revisit processed videos

# 🚀 Klipify - AI Educational Video Platform

**Transform any YouTube video into a comprehensive learning experience with AI-powered clips, summaries, notes, and chat.**

## � Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed
- **VideoDB API Key**: [Get it here](https://console.videodb.io/)
- **Google Gemini API Key**: [Get it here](https://aistudio.google.com/app/apikey)

### ⚡ Fast Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd klipify
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Add your API keys:
   ```toml
   [secrets]
   VIDEODB_API_KEY = "your_videodb_api_key_here"
   GOOGLE_API_KEY = "your_google_gemini_api_key_here"
   ```

4. **Launch Application**
   ```bash
   # Option 1: Use the batch file (Windows)
   run_new_ui.bat
   
   # Option 2: Direct command
   streamlit run klipify_new_ui.py
   ```

5. **Open Browser**
   - Navigate to `http://localhost:8501`
   - Start processing YouTube videos!

## ✨ Features

- 🎬 **Smart Video Clips** - AI extracts key educational segments
- 📊 **AI Summaries** - Comprehensive content analysis  
- 📝 **Timestamped Notes** - Interactive study materials
- 💬 **AI Chat Assistant** - Ask questions about video content
- 📁 **Video Management** - Organize and revisit processed videos

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)
1. **Push to GitHub**
2. **Connect to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Set App Details:**
   - Main file: `klipify_new_ui.py`
   - Python version: 3.8+
4. **Add Secrets in Dashboard:**
   ```toml
   VIDEODB_API_KEY = "your_key_here"
   GOOGLE_API_KEY = "your_key_here"
   ```
5. **Deploy with one click**

### Railway
1. **Connect GitHub repository**
2. **Add environment variables:**
   - `VIDEODB_API_KEY`
   - `GOOGLE_API_KEY`
3. **Deploy automatically**

### Heroku
1. **Add `Procfile`:**
   ```
   web: streamlit run klipify_new_ui.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. **Deploy via Heroku CLI or GitHub integration**

## 🔧 Environment Variables

Required for cloud deployment:
- `VIDEODB_API_KEY` - Your VideoDB API key
- `GOOGLE_API_KEY` - Your Google Gemini API key

## 🔒 Security Notes

- ✅ Never commit API keys to version control
- ✅ Use environment variables in production
- ✅ Enable HTTPS for production deployments
- ✅ API keys are stored in `.streamlit/secrets.toml` (not tracked by git)

## 📊 Performance Tips

- 🚀 App uses caching for repeated API calls
- 🎬 Optimized video processing for large files
- 📈 Monitor API usage limits via respective dashboards
- 💾 Session state management for better UX

## 🛠️ Troubleshooting

### Common Issues:
1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **API Key Errors**: Verify keys are correctly set in secrets file
3. **Port Issues**: Use different port with `--server.port 8502` if 8501 is busy

### Getting Help:
- Check the browser console for detailed error messages
- Verify API key permissions on respective platforms
- Ensure Python version compatibility (3.8+)

---

**Ready to transform your learning experience? Start with any educational YouTube video! 🎓**
