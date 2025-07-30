"""
Clips page component for displaying video clips.
"""

import streamlit as st
from ...utils.helpers import create_youtube_link

def show_clips_page(video_data):
    """Display the clips page with professional design."""
    st.markdown("""
    <div class="page-header">
        <h2>🎬 Video Clips</h2>
        <p class="page-subtitle">AI-generated educational video segments</p>
    </div>
    """, unsafe_allow_html=True)
    
    clips = video_data.get('clips', [])
    youtube_id = video_data.get('youtube_id', '')
    
    if not clips:
        st.markdown("""
        <div class="empty-state">
            <h3>No clips available</h3>
            <p>No clips were generated. Try with a video that has clearer educational content.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Professional metrics overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clips", len(clips))
    with col2:
        total_duration = sum(clip.get('duration', 0) for clip in clips)
        st.metric("Duration", f"{total_duration:.0f}s")
    with col3:
        playable_clips = sum(1 for clip in clips if clip.get('playable', False))
        st.metric("Playable", f"{playable_clips}/{len(clips)}")
    with col4:
        concepts = len(set(clip.get('concept', '') for clip in clips))
        st.metric("Concepts", concepts)
    
    # Technology status - simplified
    timeline_clips = sum(1 for clip in clips if clip.get('timeline_url'))
    if timeline_clips > 0:
        st.success(f"✅ {len(clips)} clips ready to view")
    
    st.markdown("---")
    
    # Filter and search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search clips...", placeholder="Filter by concept or content")
    with col2:
        show_only_playable = st.checkbox("Show only playable", value=False)
    
    # Filter clips
    filtered_clips = clips
    if search_term:
        search_lower = search_term.lower()
        filtered_clips = [
            clip for clip in clips
            if search_lower in clip.get('concept', '').lower()
        ]
    
    if show_only_playable:
        filtered_clips = [clip for clip in filtered_clips if clip.get('playable', False)]
    
    if not filtered_clips:
        st.info(f"No clips found matching your filters.")
        return
    
    # Display clips professionally
    for i, clip in enumerate(filtered_clips):
        # Skip clips with errors
        if clip.get('error'):
            continue
        
        # Professional clip card
        playable_status = "status-success" if clip.get('playable', False) else "status-warning"
        technology = "Timeline" if clip.get('timeline_url') else "Legacy"
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="clip-card">
                    <div class="clip-title">
                        <span class="status-indicator {playable_status}"></span>
                        {clip.get('concept', f'Clip {i+1}')}
                    </div>
                    <div class="clip-meta">
                        Duration: {clip.get('duration', 0):.1f}s • 
                        Start: {_format_timestamp(clip.get('start_time', 0))} • 
                        Technology: {technology}
                    </div>
                """, unsafe_allow_html=True)
                
                # Show clip content if available
                if clip.get('explanation'):
                    st.markdown(f"**Explanation:** {clip['explanation']}")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                # Action buttons
                if clip.get('playable', False):
                    if clip.get('timeline_url'):
                        st.link_button("▶ Play Clip", clip['timeline_url'])
                    
                    # YouTube link with timestamp
                    if youtube_id and clip.get('start_time'):
                        youtube_url = create_youtube_link(youtube_id, clip['start_time'])
                        st.link_button("🔗 YouTube", youtube_url)
                else:
                    st.button("⏸ Not Playable", disabled=True)
    
    # Results summary
    st.markdown(f"""
    <div class="results-summary">
        Showing {len(filtered_clips)} of {len(clips)} clips
        {f' • Filtered by: "{search_term}"' if search_term else ''}
        {' • Playable only' if show_only_playable else ''}
    </div>
    """, unsafe_allow_html=True)


def _format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    if not seconds:
        return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
