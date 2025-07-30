# 🚀 Klipify Deployment Guide

Quick deployment options for Klipify.

## 📋 Prerequisites

- **VideoDB API Key**: [Get it here](https://console.videodb.io/)
- **Google Gemini API Key**: [Get it here](https://aistudio.google.com/app/apikey)

## 🏠 Local Deployment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets** in `.streamlit/secrets.toml`:
   ```toml
   VIDEODB_API_KEY = "your_videodb_key"
   GEMINI_API_KEY = "your_gemini_key"
   ```

3. **Run the app**:
   ```bash
   streamlit run klipify_main.py
   ```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in dashboard
4. Deploy with one click

### Heroku
1. Add `Procfile`:
   ```
   web: streamlit run klipify_main.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy via Heroku CLI or GitHub integration

### Railway
1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically

## 🔧 Environment Variables

Required for cloud deployment:
- `VIDEODB_API_KEY`
- `GEMINI_API_KEY`

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables in production
- Enable HTTPS for production deployments

## 📊 Performance Tips

- Use caching for repeated API calls
- Optimize video processing for large files
- Monitor API usage limits

---

For detailed configuration, see the inline code comments.
