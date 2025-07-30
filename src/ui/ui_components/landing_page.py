"""
Landing page component for Klipify.
"""

import streamlit as st

def create_landing_page():
    """Create the professional landing page for video input."""
    
    # Professional hero section with reduced padding
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎬 Klipify</h1>
        <p class="hero-subtitle">AI-powered video analysis and educational content extraction</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Smart clips • AI summaries • Timestamped notes • Interactive chat</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons using proper Streamlit columns
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        my_videos_btn = st.button("📁 My Videos", key="hero_my_videos", use_container_width=True)
    with col2:
        clips_btn = st.button("🎬 View Clips", key="hero_clips", use_container_width=True)
    with col3:
        summary_btn = st.button("📊 AI Summary", key="hero_summary", use_container_width=True)
    with col4:
        chat_btn = st.button("💬 Chat", key="hero_chat", use_container_width=True)
    
    # Handle quick action button clicks
    if my_videos_btn:
        st.session_state.current_page = "My Videos"
        st.rerun()
    elif clips_btn:
        st.session_state.current_page = "Clips" 
        st.rerun()
    elif summary_btn:
        st.session_state.current_page = "Summary"
        st.rerun()
    elif chat_btn:
        st.session_state.current_page = "Chat"
        st.rerun()
    
    # Professional feature overview
    st.markdown("### Key Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎬 Intelligent Video Segmentation**  
        AI-driven extraction of key educational segments with precise timestamp identification.
        
        **📋 Comprehensive Analysis**  
        Automated content summarization with learning objectives and difficulty assessment.
        """)
    
    with col2:
        st.markdown("""
        **📝 Interactive Documentation**  
        Timestamped study notes with searchable content and YouTube integration.
        
        **💬 AI-Powered Assistant**  
        Context-aware chat interface for in-depth content exploration and Q&A.
        """)
    
    st.markdown("---")
    
    # Professional input section
    st.markdown("### Video Processing")

    # --- CHANGE THIS LINE ---
    # Give both columns an equal width ratio to make the elements the same size.
    col1, col2 = st.columns(2) 

    with col1:
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="Enter YouTube URL (e.g., https://www.youtube.com/watch?v=example)",
            help="Paste any educational YouTube video URL for AI analysis",
            label_visibility="collapsed"
        )

    with col2:
        process_button = st.button(
            "▶ Process", 
            type="primary", 
            use_container_width=True  # This correctly makes the button fill its column
        )

    return youtube_url, process_button


def show_quick_start_guide():
    """Show a quick start guide for new users."""
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    1. **Upload a Video**: Enter a YouTube URL above or check your existing videos
    2. **AI Analysis**: Our AI will automatically extract key segments and insights
    3. **Explore Content**: Browse clips, summaries, and interactive transcripts
    4. **Ask Questions**: Use the AI chat to dive deeper into the content
    
    **Pro Tip**: Start with educational videos for best results!
    """)
