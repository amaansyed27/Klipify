"""
Klipify - AI-Powered Educational Video Platform
New modular UI with sidebar navigation and improved video handling.

Transform any YouTube video into a comprehensive learning experience with:
- Smart video clips with multiple download formats
- AI-generated summaries in a clean interface
- Interactive timestamped notes with YouTube links
- WhatsApp-style AI chat assistant
"""

import streamlit as st
import sys
import os

# Add src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import our modular components
from src.ui.ui_components import (
    load_modern_css, 
    create_landing_page, 
    create_sidebar_navigation,
    show_clips_page,
    show_summary_page, 
    show_notes_page,
    show_chat_page,
    show_my_videos_page
)
from src.ui.displays import display_error_state
from src.services.video_service import initialize_videodb_client
from src.services.ai_service import initialize_genai_client
from src.utils.helpers import (
    initialize_chat_session, 
    validate_youtube_url, 
    validate_api_keys,
    reset_session_state
)
from src.processing import VideoProcessingPipeline, validate_processing_requirements


def main():
    """Main Klipify application with new UI flow."""
    
    # Set page configuration
    favicon_path = os.path.join(os.path.dirname(__file__), "assets", "favicon.ico")
    
    st.set_page_config(
        page_title="Klipify - AI Educational Video Platform",
        page_icon="🎬" if not os.path.exists(favicon_path) else favicon_path,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load modern CSS
    load_modern_css()
    
    # Initialize chat session
    initialize_chat_session()
    
    # Check if we have processed video data
    video_processed = st.session_state.get('video_data') is not None
    
    if not video_processed:
        # Show landing page for new users
        show_landing_page()
    else:
        # Show dashboard with sidebar navigation
        show_dashboard_with_sidebar()


def show_landing_page():
    """Display the landing page for video input."""
    # Validate API keys first
    videodb_ok, genai_ok = validate_api_keys()
    
    if not videodb_ok or not genai_ok:
        display_error_state()
        return
    
    # Check if user clicked a quick action button
    if st.session_state.get('current_page') in ["My Videos", "Clips", "Summary", "Chat"]:
        # If user has video data, show the dashboard
        if st.session_state.get('video_data'):
            show_dashboard_with_sidebar()
            return
        else:
            # If no video data, show message and reset to landing
            st.warning("Please process a video first before accessing this feature.")
            st.session_state.current_page = None
    
    # Create the landing page
    youtube_url, process_button = create_landing_page()
    
    # Handle video processing
    if process_button and youtube_url:
        process_video(youtube_url)


def show_dashboard_with_sidebar():
    """Display the main dashboard with sidebar navigation."""
    # Create sidebar navigation
    current_page = create_sidebar_navigation()
    
    # Display the selected page
    video_data = st.session_state.video_data
    
    if current_page == "Clips":
        show_clips_page(video_data)
    elif current_page == "Summary":
        show_summary_page(video_data)
    elif current_page == "Notes":
        show_notes_page(video_data)
    elif current_page == "Chat":
        show_chat_page(video_data)
    elif current_page == "My Videos":
        show_my_videos_page()


def process_video(youtube_url):
    """Process the video using the pipeline."""
    # Validate YouTube URL
    is_valid_url, result = validate_youtube_url(youtube_url)
    
    if not is_valid_url:
        st.error(f"❌ {result}")
        return
    
    youtube_id = result
    
    # Initialize clients
    video_client = initialize_videodb_client()
    ai_client = initialize_genai_client()
    
    # Validate clients
    is_valid, error_msg = validate_processing_requirements(video_client, ai_client)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        return
    
    # Process the video
    with st.container():
        st.markdown("## 🔄 Processing Your Video")
        st.markdown("Please wait while we analyze and create clips from your video...")
        
        pipeline = VideoProcessingPipeline(video_client, ai_client)
        video_data = pipeline.process_video(youtube_url, youtube_id)
        
        if video_data:
            st.success("✅ Video processed successfully! Redirecting to dashboard...")
            st.balloons()
            st.rerun()  # Refresh to show dashboard


if __name__ == "__main__":
    main()
