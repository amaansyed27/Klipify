"""
Klipify - AI-Powered Educational Video Platform
Main application entry point with modular architecture.

Transform any YouTube video into a comprehensive learning experience with:
- Smart video clips and shorts
- AI-generated summaries  
- Timestamped notes
- Interactive AI chat assistant
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
from src.ui.components import load_css, create_header, create_feature_showcase
from src.ui.displays import display_content_tabs, display_sidebar_input, display_error_state
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
    """Main Klipify application function."""
    
    # Set page configuration with favicon
    favicon_path = os.path.join(os.path.dirname(__file__), "assets", "favicon.ico")
    
    st.set_page_config(
        page_title="Klipify - AI Educational Video Platform",
        page_icon="🎬" if not os.path.exists(favicon_path) else favicon_path,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS for modern UI
    load_css()
    
    # Initialize chat session
    initialize_chat_session()
    
    # Create main header (FIXED: Using native Streamlit components)
    create_header()
    
    # Feature showcase (FIXED: Using native Streamlit components)
    create_feature_showcase()
    
    # Validate API keys
    videodb_ok, genai_ok = validate_api_keys()
    
    if not videodb_ok or not genai_ok:
        display_error_state()
        return
    
    # Initialize clients
    video_client = initialize_videodb_client()
    ai_client = initialize_genai_client()
    
    # Validate clients are properly initialized
    is_valid, error_msg = validate_processing_requirements(video_client, ai_client)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        display_error_state()
        return
    
    # Sidebar for input and controls
    youtube_url, process_button = display_sidebar_input()
    
    # Handle video processing
    if process_button and youtube_url:
        # Validate YouTube URL
        is_valid_url, result = validate_youtube_url(youtube_url)
        
        if not is_valid_url:
            st.error(f"❌ {result}")
            return
        
        youtube_id = result
        
        # Process the video using our pipeline
        with st.container():
            st.markdown("## 🔄 Processing Your Video")
            
            pipeline = VideoProcessingPipeline(video_client, ai_client)
            video_data = pipeline.process_video(youtube_url, youtube_id)
            
            if video_data:
                st.rerun()  # Refresh to show processed content
    
    # Display processed content if available
    if st.session_state.get('video_data'):
        st.markdown("---")
        display_content_tabs(st.session_state.video_data)


if __name__ == "__main__":
    main()
