"""
New Modern UI Components for Klipify
Includes sidebar navigation, landing page, and improved page layouts.
"""

import streamlit as st
import base64
import os
from ..utils.helpers import create_youtube_link, reset_session_state


def load_modern_css():
    """Load modern CSS styling for the new UI."""
    st.markdown("""
    <style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Landing page hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Sidebar navigation styling */
    .nav-sidebar {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .nav-item {
        background: rgba(255,255,255,0.1);
        border: none;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        text-align: left;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: rgba(255,255,255,0.3);
        border-left: 4px solid #fff;
    }
    
    /* Chat interface styling (WhatsApp style) */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: #f0f0f0;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 8px 0 8px 20%;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .ai-message {
        background: white;
        color: #333;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        margin: 8px 20% 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .message-time {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 4px;
    }
    
    /* Clip cards styling */
    .clip-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #007bff;
        transition: transform 0.3s ease;
    }
    
    .clip-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .clip-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .clip-meta {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Download buttons */
    .download-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .download-btn {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }
    
    .download-btn.youtube { background: linear-gradient(135deg, #ff4757, #c44569); }
    .download-btn.stream { background: linear-gradient(135deg, #26de81, #20bf6b); }
    .download-btn.mp4 { background: linear-gradient(135deg, #fd79a8, #e84393); }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #007bff, #0056b3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)


def create_landing_page():
    """Create the landing page for video input."""
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎬 Klipify</h1>
        <p class="hero-subtitle">Transform any YouTube video into a comprehensive learning experience</p>
        <p>✨ Smart clips • 📝 AI summaries • 🔍 Timestamped notes • 💬 Chat assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 🎬 Smart Clips
        AI extracts key educational segments into bite-sized clips with multiple download formats
        """)
    
    with col2:
        st.markdown("""
        ### 📋 AI Summary
        Get comprehensive summaries with key concepts and insights automatically identified
        """)
    
    with col3:
        st.markdown("""
        ### 📝 Time Notes
        Interactive timestamped notes with clickable YouTube links for easy navigation
        """)
    
    with col4:
        st.markdown("""
        ### 💬 AI Chat
        WhatsApp-style chat assistant to answer questions about the video content
        """)
    
    st.markdown("---")
    
    # Input section
    st.markdown("## 🚀 Get Started")
    st.markdown("Enter a YouTube URL to begin processing:")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        youtube_url = st.text_input(
            "",
            placeholder="https://www.youtube.com/watch?v=example",
            help="Paste the URL of an educational YouTube video",
            label_visibility="collapsed"
        )
    
    with col2:
        process_button = st.button(
            "🚀 Process Video", 
            type="primary", 
            use_container_width=True
        )
    
    # Instructions
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Paste** a YouTube URL of an educational video
        2. **Click** "Process Video" to start AI analysis
        3. **Wait** 30-60 seconds for processing
        4. **Explore** clips, summary, notes, and chat features
        
        **Best results with:** Educational content, tutorials, lectures, explainer videos
        """)
    
    return youtube_url, process_button


def create_sidebar_navigation():
    """Create the sidebar navigation and return current page."""
    
    with st.sidebar:
        st.markdown("""
        <div class="nav-sidebar">
            <h2 style="color: white; text-align: center; margin-bottom: 1rem;">📱 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation options
        pages = {
            "🎬 Clips": "Clips",
            "📋 Summary": "Summary", 
            "📝 Notes": "Notes",
            "💬 Chat": "Chat"
        }
        
        # Use radio for navigation
        selected_page = st.radio(
            "Choose a section:",
            options=list(pages.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Video info
        video_data = st.session_state.get('video_data', {})
        if video_data:
            st.markdown("### 📹 Current Video")
            st.markdown(f"**Clips:** {len(video_data.get('clips', []))}")
            st.markdown(f"**Concepts:** {len(video_data.get('concepts', []))}")
            
            # Quick actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔗 Original", use_container_width=True):
                    st.link_button("YouTube", video_data.get('youtube_url', '#'))
            
            with col2:
                if st.button("🔄 New Video", use_container_width=True):
                    reset_session_state()
                    st.rerun()
        
        st.markdown("---")
        
        # Status
        st.markdown("### ✅ Status")
        st.markdown('<div class="status-success">🟢 Video Processed</div>', unsafe_allow_html=True)
        
    return pages[selected_page]


def show_clips_page(video_data):
    """Display the clips page with enhanced video handling."""
    st.markdown("# 🎬 Video Clips")
    st.markdown("### Smart educational clips with enhanced VideoDB Timeline technology")
    
    clips = video_data.get('clips', [])
    youtube_id = video_data.get('youtube_id', '')
    
    if not clips:
        st.warning("⚠️ No clips were generated. Try with a video that has clearer educational content.")
        return
    
    # Clips overview with enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clips", len(clips))
    with col2:
        total_duration = sum(clip.get('duration', 0) for clip in clips)
        st.metric("Total Duration", f"{total_duration:.0f}s")
    with col3:
        playable_clips = sum(1 for clip in clips if clip.get('playable', False))
        st.metric("Playable Clips", f"{playable_clips}/{len(clips)}")
    with col4:
        concepts = len(set(clip.get('concept', '') for clip in clips))
        st.metric("Concepts", concepts)
    
    # Technology info
    timeline_clips = sum(1 for clip in clips if clip.get('timeline_url'))
    if timeline_clips > 0:
        st.success(f"✨ {timeline_clips} clips created using VideoDB Timeline technology for enhanced compatibility!")
    
    st.markdown("---")
    
    # Display clips with enhanced information
    for i, clip in enumerate(clips):
        # Check if clip has errors
        if clip.get('error'):
            st.error(f"❌ Error creating clip for '{clip.get('concept', f'Clip {i+1}')}': {clip['error']}")
            continue
        
        # Enhanced clip card with status indicators
        playable_icon = "✅" if clip.get('playable', False) else "⚠️"
        technology = "Timeline" if clip.get('timeline_url') else "Legacy"
        
        st.markdown(f"""
        <div class="clip-card">
            <div class="clip-title">{playable_icon} 📖 {clip.get('concept', f'Clip {i+1}')}</div>
            <div class="clip-meta">
                ⏱️ Duration: {clip.get('duration', 0):.0f}s | 
                🕐 Starts at: {clip.get('formatted_time', 'N/A')} | 
                📍 Timestamp: {clip.get('start_time', 0):.0f}s |
                🔧 Technology: {technology}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced download options using video utils
        from ..utils.video_utils import VideoFormatHandler
        
        # Show format information
        if clip.get('format'):
            st.info(f"📱 Format: {clip['format']}")
        
        # Create download buttons with enhanced options
        col1, col2, col3, col4 = st.columns(4)
        
        youtube_link = create_youtube_link(youtube_id, clip.get('start_time', 0))
        
        with col1:
            st.link_button("▶️ YouTube", youtube_link, use_container_width=True)
        
        with col2:
            if clip.get('playable', False):
                if st.button(f"🎥 Play Clip", key=f"play_{i}", use_container_width=True):
                    # Use timeline URL if available, otherwise fallback to stream URL
                    video_url = clip.get('timeline_url') or clip.get('stream_url')
                    VideoFormatHandler.display_video_player(
                        video_url, 
                        clip.get('concept', f'Clip {i+1}'),
                        i
                    )
            else:
                st.button("🎥 Not Available", disabled=True, use_container_width=True)
        
        with col3:
            if clip.get('download_url'):
                st.link_button("📥 Download", clip['download_url'], use_container_width=True)
            else:
                if st.button(f"🔄 Convert", key=f"convert_{i}", use_container_width=True):
                    st.info("💡 **Conversion Options:**")
                    st.markdown("- Use VLC Media Player to convert stream to MP4")
                    st.markdown("- Try online HLS to MP4 converters")
                    st.markdown("- Use FFmpeg command line tool")
                    if clip.get('stream_url') or clip.get('timeline_url'):
                        url_to_convert = clip.get('timeline_url') or clip.get('stream_url')
                        st.code(url_to_convert, language=None)
        
        with col4:
            if st.button(f"📋 Copy URL", key=f"copy_{i}", use_container_width=True):
                # Prefer timeline URL over stream URL
                url_to_copy = clip.get('timeline_url') or clip.get('stream_url') or youtube_link
                st.code(url_to_copy, language=None)
                st.success("URL ready to copy!")
        
        # Show available quality options if any
        if clip.get('available_qualities'):
            with st.expander(f"🎛️ Quality Options for {clip.get('concept')}"):
                for quality in clip['available_qualities']:
                    quality_url = clip.get(f'stream_{quality}')
                    if quality_url:
                        col_q1, col_q2 = st.columns([3, 1])
                        with col_q1:
                            st.markdown(f"**{quality}** - {quality_url[:50]}...")
                        with col_q2:
                            st.link_button(f"▶️ {quality}", quality_url, use_container_width=True)
        
        # Show technical details if available
        if clip.get('videodb_info'):
            with st.expander(f"ℹ️ Technical Details - {clip.get('concept')}"):
                info = clip['videodb_info']
                st.markdown(f"**Type:** {info.get('type', 'Unknown')}")
                st.markdown(f"**Compatibility:** {info.get('compatibility', 'Standard')}")
                
                if info.get('recommended_players'):
                    st.markdown("**Recommended Players:**")
                    for player in info['recommended_players']:
                        st.markdown(f"- {player}")
                
                if info.get('download_options'):
                    st.markdown("**Download Options:**")
                    for option in info['download_options']:
                        st.markdown(f"- {option}")
        
        st.markdown("---")



def show_summary_page(video_data):
    """Display the summary page with clean layout."""
    st.markdown("# 📋 Video Summary")
    st.markdown("### AI-generated insights and key concepts")
    
    # Video metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**📅 Processed:** {video_data.get('processed_at', 'N/A')}")
    with col2:
        st.markdown(f"**🔍 Concepts:** {len(video_data.get('concepts', []))}")
    with col3:
        st.link_button("🔗 Original Video", video_data.get('youtube_url', '#'), use_container_width=True)
    
    st.markdown("---")
    
    # Main summary
    st.markdown("## 📝 Executive Summary")
    summary = video_data.get('summary', 'No summary available.')
    st.markdown(summary)
    
    st.markdown("---")
    
    # Key concepts
    st.markdown("## 🎯 Key Concepts")
    concepts = video_data.get('concepts', [])
    
    if concepts:
        # Display concepts in a grid
        cols = st.columns(3)
        for i, concept in enumerate(concepts):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
                           padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                           border-left: 4px solid #2196f3;">
                    <strong>📌 {concept}</strong>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No key concepts extracted from this video.")


def show_notes_page(video_data):
    """Display the notes page with interactive timestamps."""
    st.markdown("# 📝 Timestamped Study Notes")
    st.markdown("### Interactive notes with YouTube links")
    
    # Notes overview
    notes = video_data.get('notes', 'No notes available.')
    st.markdown("## 📖 Study Notes")
    st.markdown(notes)
    
    st.markdown("---")
    
    # Interactive transcript
    st.markdown("## 🎬 Interactive Transcript")
    st.markdown("Click any timestamp to jump to that point in the YouTube video")
    
    transcript_segments = video_data.get('transcript_segments', [])
    youtube_id = video_data.get('youtube_id', '')
    
    if transcript_segments:
        # Search functionality
        search_term = st.text_input("🔍 Search in transcript:", placeholder="Enter keyword to search...")
        
        # Filter segments based on search
        filtered_segments = transcript_segments
        if search_term:
            filtered_segments = [
                seg for seg in transcript_segments 
                if search_term.lower() in seg.get('text', '').lower()
            ]
        
        if not filtered_segments and search_term:
            st.warning(f"No results found for '{search_term}'")
        else:
            # Display segments
            for segment in filtered_segments:
                start_time = segment.get('start', 0)
                text = segment.get('text', '')
                formatted_time = _format_timestamp(start_time)
                
                # Create clickable timestamp
                youtube_link = create_youtube_link(youtube_id, start_time)
                
                col1, col2 = st.columns([1, 6])
                with col1:
                    st.link_button(f"⏰ {formatted_time}", youtube_link, use_container_width=True)
                with col2:
                    # Highlight search term if searching
                    if search_term and search_term.lower() in text.lower():
                        highlighted_text = text.replace(
                            search_term, 
                            f"**{search_term}**"
                        )
                        st.markdown(highlighted_text)
                    else:
                        st.markdown(text)
                
                st.markdown("---")
    else:
        st.info("No transcript segments available.")


def show_chat_page(video_data):
    """Display the WhatsApp-style chat page."""
    st.markdown("# 💬 AI Study Assistant")
    st.markdown("### Ask questions about the video content")
    
    # Initialize chat if needed
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Set video context for AI
    if not st.session_state.get('video_context'):
        st.session_state.video_context = {
            'summary': video_data.get('summary', ''),
            'concepts': video_data.get('concepts', []),
            'notes': video_data.get('notes', ''),
            'youtube_url': video_data.get('youtube_url', '')
        }
    
    # Quick action buttons
    st.markdown("## 🚀 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Explain key concepts", use_container_width=True):
            add_quick_question("What are the main concepts explained in this video?")
    
    with col2:
        if st.button("📝 Create study notes", use_container_width=True):
            add_quick_question("Can you create detailed study notes from this video?")
    
    with col3:
        if st.button("❓ Generate quiz", use_container_width=True):
            add_quick_question("Create a quiz based on this video content.")
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("## 💬 Chat")
    
    # Display chat history with WhatsApp styling
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                # User message (right side, blue)
                st.markdown(f"""
                <div class="user-message">
                    {message['user']}
                    <div class="message-time">You</div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI message (left side, gray)
                st.markdown(f"""
                <div class="ai-message">
                    {message['assistant']}
                    <div class="message-time">AI Assistant</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ai-message">
                👋 Hi! I'm your AI study assistant. I've analyzed the video and I'm ready to help you understand the content better. Ask me anything!
                <div class="message-time">AI Assistant</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        handle_chat_message(user_input)


def add_quick_question(question):
    """Add a quick question to chat."""
    handle_chat_message(question)


def handle_chat_message(user_input):
    """Handle chat message and get AI response."""
    # Add user message to history
    with st.spinner("AI is thinking..."):
        try:
            # Get AI response
            from ..services.ai_service import initialize_genai_client, AIService
            
            genai_client = initialize_genai_client()
            if genai_client:
                ai_service = AIService(genai_client)
                
                ai_response = ai_service.chat_with_assistant(
                    user_input, 
                    st.session_state.video_context,
                    st.session_state.chat_history
                )
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": user_input,
                    "assistant": ai_response
                })
                
            else:
                ai_response = "Sorry, AI service is currently unavailable. Please check your API configuration."
                st.session_state.chat_history.append({
                    "user": user_input,
                    "assistant": ai_response
                })
                
        except Exception as e:
            ai_response = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": ai_response
            })
    
    st.rerun()


def _format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
