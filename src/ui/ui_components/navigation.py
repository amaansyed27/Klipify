"""
Navigation sidebar component for Klipify.
"""

import streamlit as st

def create_sidebar_navigation():
    """Create the modern sidebar navigation and return current page."""
    
    with st.sidebar:
        # Modern navigation header
        st.markdown("""
        <div class="nav-sidebar">
            <h3 class="nav-title">🎬 Klipify</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation options with modern styling
        pages = {
            "🎬 Clips": "Clips",
            "📊 Summary": "Summary", 
            "📝 Notes": "Notes",
            "💬 Chat": "Chat",
            "📁 My Videos": "My Videos"
        }
        
        # Use radio for navigation with custom styling
        selected_page = st.radio(
            "Navigate to:",
            options=list(pages.keys()),
            label_visibility="collapsed",
            key="nav_radio"
        )
        
        # Video info section with modern styling
        video_data = st.session_state.get('video_data', {})
        if video_data:
            st.markdown("""
            <div class="sidebar-section">
                <h3>📺 Video Info</h3>
            </div>
            """, unsafe_allow_html=True)
            
            title = video_data.get('title', 'No title')
            if len(title) > 35:
                title = title[:35] + "..."
            st.markdown(f"**Title:** {title}")
            
            duration = video_data.get('duration', 0)
            if duration:
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                st.markdown(f"**Duration:** {minutes}:{seconds:02d}")
            
            clips_count = len(video_data.get('clips', []))
            if clips_count:
                st.markdown(f"**Clips:** {clips_count}")
        
        # Status section with modern styling
        st.markdown("""
        <div class="sidebar-section">
            <h3>⚡ Status</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if video_data:
            st.success("✅ Video processed")
            
            # Modern quick actions
            if st.button("🔄 Process New Video", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.rerun()
                
        else:
            st.info("📺 No video loaded")
            st.markdown("Upload a video to get started!")
        
    return pages[selected_page]
        
    return pages[selected_page]


def show_sidebar_metrics(video_data):
    """Display video metrics in the sidebar."""
    if not video_data:
        return
        
    with st.sidebar:
        st.markdown("### Metrics")
        
        col1, col2 = st.columns(2)
        with col1:
            clips_count = len(video_data.get('clips', []))
            st.metric("Clips", clips_count)
            
        with col2:
            concepts_count = len(video_data.get('concepts', []))
            st.metric("Concepts", concepts_count)
