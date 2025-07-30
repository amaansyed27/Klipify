# 🎬 Klipify - AI Educational Video Platform

Transform any YouTube educational video into a comprehensive learning experience using AI-powered video processing and analysis.

## ✨ Features

- **🎬 Smart Video Clips** - AI-curated educational shorts focusing on key concepts
- **📋 Intelligent Summaries** - Comprehensive overviews with learning objectives
- **📝 Timestamped Notes** - Detailed study notes with precise video navigation
- **💬 AI Study Assistant** - Interactive tutor for personalized learning support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys:
  - [VideoDB API Key](https://console.videodb.io/) (free tier available)
  - [Google Gemini API Key](https://aistudio.google.com/app/apikey) (free tier available)

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd klipify
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   Create `.streamlit/secrets.toml`:
   ```toml
   VIDEODB_API_KEY = "your_videodb_api_key"
   GEMINI_API_KEY = "your_gemini_api_key"
   ```

3. **Run the application**:
   ```bash
   streamlit run klipify_main.py
   # Or use the batch file: run_app.bat
   ```

## 🏗️ Architecture

```
klipify/
├── klipify_main.py              # Main application entry point
├── src/                         # Modular source code
│   ├── ui/                      # User interface components
│   │   ├── components.py        # UI elements and styling
│   │   └── displays.py          # Tab content and layouts
│   ├── services/                # Business logic services
│   │   ├── video_service.py     # VideoDB operations
│   │   └── ai_service.py        # Google GenAI operations
│   ├── utils/                   # Utility functions
│   │   └── helpers.py           # Common helper functions
│   └── processing.py            # Video processing pipeline
├── assets/                      # Static assets (logos, icons)
├── requirements.txt             # Python dependencies
└── run_app.bat                 # Windows launcher script
```

## 🔧 Usage

1. **Enter YouTube URL** - Paste any educational YouTube video URL
2. **Process Video** - Click "Process Video" to start AI analysis
3. **Explore Content**:
   - **Video Clips** - Watch AI-generated educational shorts
   - **Summary** - Read comprehensive video analysis
   - **Notes** - Review timestamped study notes
   - **Chat** - Ask questions about the video content

## 🛠️ Technical Details

### Dependencies
- **Streamlit** - Web application framework
- **VideoDB** - Video processing and indexing
- **Google GenAI** - AI content generation
- **Python-dotenv** - Environment configuration

### AI Processing Pipeline
1. **Video Upload** - Upload to VideoDB for processing
2. **Content Indexing** - Extract and index spoken words
3. **AI Analysis** - Generate summaries and extract key concepts
4. **Segment Detection** - Find relevant video segments
5. **Clip Generation** - Create focused educational clips

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in Streamlit Cloud dashboard
4. Deploy with one click

### Local Production
```bash
streamlit run klipify_main.py --server.port 8501
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Documentation**: Check inline code comments
- **API Docs**: [VideoDB](https://docs.videodb.io/) | [Google GenAI](https://ai.google.dev/gemini-api/docs)

---

**Made with ❤️ for educational content creators and learners**
