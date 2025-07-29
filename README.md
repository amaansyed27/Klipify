# 🧠 AI Tutor: Instant Educational Shorts Generator

Transform any YouTube educational video into bite-sized knowledge nuggets! This Streamlit application uses VideoDB for video processing and Google's Gemini model to identify key concepts with timestamped links.

## 🚀 Features

- **YouTube Video Processing**: Upload and transcribe any YouTube video
- **AI-Powered Concept Extraction**: Uses Google Gemini to identify key educational concepts
- **Smart Video Segmentation**: Finds exact video clips for each concept using semantic search
- **Timestamped Links**: Generate clickable YouTube links that jump to specific moments
- **Interactive Study Guide**: Beautiful, user-friendly interface for learning

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit**: Web application framework
- **VideoDB SDK**: Video processing and semantic search
- **Google GenAI**: Google's new Gemini client library (`google-genai`)

## 📋 Prerequisites

1. **VideoDB API Key**: Get your free API key from [VideoDB Console](https://console.videodb.io/)
2. **Google API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 🔧 Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (choose one method):

   **Method A: Streamlit Secrets (Recommended)**
   - Create a `.streamlit` folder in the project directory
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Add your actual API keys:
     ```toml
     VIDEODB_API_KEY = "your_actual_videodb_api_key"
     GEMINI_API_KEY = "your_actual_gemini_api_key"
     ```

   **Method B: Environment Variables**
   ```bash
   set VIDEODB_API_KEY=your_actual_videodb_api_key
   set GEMINI_API_KEY=your_actual_gemini_api_key
   ```

## 🏃‍♂️ Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run ai_tutor_app.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Enter a YouTube URL** and click "Generate Knowledge Nuggets"

## 📱 How to Use

1. **Enter YouTube URL**: Paste any educational YouTube video URL
2. **Process Video**: The app will:
   - Upload the video to VideoDB
   - Generate a transcript
   - Identify key concepts using Gemini AI
   - Find relevant video segments
3. **Get Results**: Receive a list of "Knowledge Nuggets" with clickable timestamps

## 🎯 Example Videos to Try

- Educational lectures
- Tutorial videos
- Documentary content
- How-to guides
- Academic presentations

## 🔍 How It Works

1. **Video Processing**: VideoDB extracts and transcribes the audio
2. **Concept Identification**: Gemini AI analyzes the transcript to find key educational concepts
3. **Semantic Search**: VideoDB finds the exact video segments for each concept
4. **Result Generation**: Creates timestamped YouTube links for easy navigation

## 🚨 Troubleshooting

**API Key Issues**:
- Ensure your API keys are valid and active
- Check that environment variables or secrets are properly set

**Video Processing Errors**:
- Make sure the YouTube URL is valid and publicly accessible
- Some videos may have restricted access or copyright protection

**Long Processing Times**:
- Longer videos take more time to process
- The transcript generation step can take several minutes for long content

## 📄 File Structure

```
AI Demos July/
├── ai_tutor_app.py           # Main Streamlit application
├── requirements.txt          # Python dependencies
├── secrets_template.toml     # Template for API keys
└── README.md                # This file
```

## 🤝 Contributing

Feel free to contribute improvements, bug fixes, or new features!

## 📝 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ using Streamlit, VideoDB, and Google GenAI**
