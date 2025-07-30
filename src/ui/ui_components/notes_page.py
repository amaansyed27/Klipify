"""
Notes page component for displaying interactive notes and transcript.
"""

import streamlit as st
from ...utils.helpers import create_youtube_link

def show_notes_page(video_data):
    """Display the notes page with professional design."""
    st.markdown("""
    <div class="page-header">
        <h2>📝 Study Notes</h2>
        <p class="page-subtitle">Interactive timestamped notes and transcript</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional metrics
    col1, col2, col3 = st.columns(3)
    transcript_segments = video_data.get('transcript_segments', [])
    
    with col1:
        word_count = sum(len(segment.get('text', '').split()) for segment in transcript_segments)
        st.metric("Word Count", f"{word_count:,}")
    
    with col2:
        st.metric("Segments", len(transcript_segments))
    
    with col3:
        duration = video_data.get('duration', 0)
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            st.metric("Duration", f"{minutes}:{seconds:02d}")
        else:
            st.metric("Duration", "Unknown")
    
    st.markdown("---")
    
    # Study notes section
    notes = video_data.get('notes', '')
    if notes and notes != 'No notes available.':
        st.markdown("""
        <div class="section-header">
            <h3>📚 Study Notes</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean and escape the notes content to prevent HTML rendering issues
        import html
        clean_notes = html.escape(notes) if notes else ""
        clean_notes = clean_notes.replace('\\n', '<br>')
        
        st.markdown(f"""
        <div class="notes-content">
            {clean_notes}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Interactive transcript section
    st.markdown("""
    <div class="section-header">
        <h3>🎬 Interactive Transcript</h3>
    </div>
    """, unsafe_allow_html=True)
    
    youtube_id = video_data.get('youtube_id', '')
    
    if transcript_segments:
        _show_transcript_section(transcript_segments, youtube_id)
    else:
        st.markdown("""
        <div class="empty-state">
            <h3>No transcript available</h3>
            <p>Transcript could not be generated for this video.</p>
        </div>
        """, unsafe_allow_html=True)


def _show_transcript_section(transcript_segments, youtube_id):
    """Display the interactive transcript with search functionality."""
    # Enhanced search functionality with better UX
    st.markdown("""
    <div class="section-header">
        <h4>🔍 Search & Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2.5, 1, 0.5])
    with col1:
        search_term = st.text_input(
            "🔍 Search transcript...", 
            placeholder="Find specific content in the video",
            help="Search through all transcript segments to find specific topics or keywords"
        )
    with col2:
        segments_per_page = st.selectbox(
            "Segments per page", 
            [10, 25, 50, 100], 
            index=1,
            help="Number of transcript segments to display per page"
        )
    with col3:
        if st.button("🗑️ Clear", help="Clear search and show all segments"):
            st.rerun()
    
    # Filter segments based on search
    if search_term:
        search_lower = search_term.lower()
        filtered_segments = [
            segment for segment in transcript_segments
            if search_lower in segment.get('text', '').lower()
        ]
        
        if filtered_segments:
            st.markdown(f"""
            <div class="search-results-info">
                Found {len(filtered_segments)} segments containing "{search_term}"
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="search-no-results">
                No segments found containing your search term.
            </div>
            """, unsafe_allow_html=True)
            return
    else:
        filtered_segments = transcript_segments
    
    # Pagination
    if 'transcript_page' not in st.session_state:
        st.session_state.transcript_page = 0
    
    total_pages = (len(filtered_segments) - 1) // segments_per_page + 1
    
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Previous Page", disabled=st.session_state.transcript_page == 0):
                st.session_state.transcript_page = max(0, st.session_state.transcript_page - 1)
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center; color: var(--text-secondary);'>Page {st.session_state.transcript_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next Page →", disabled=st.session_state.transcript_page >= total_pages - 1):
                st.session_state.transcript_page = min(total_pages - 1, st.session_state.transcript_page + 1)
                st.rerun()
    
    # Display segments
    start_idx = st.session_state.transcript_page * segments_per_page
    end_idx = start_idx + segments_per_page
    current_segments = filtered_segments[start_idx:end_idx]
    
    for i, segment in enumerate(current_segments):
        start_time = segment.get('start', 0)
        text = segment.get('text', '')
        
        # Clean and escape text content to prevent HTML issues
        import html
        clean_text = html.escape(text) if text else ""
        
        # Create YouTube link with timestamp
        youtube_url = create_youtube_link(youtube_id, start_time) if youtube_id else None
        
        st.markdown(f"""
        <div class="transcript-segment">
            <div class="segment-header">
                <span class="segment-time">{_format_timestamp(start_time)}</span>
                {f'<a href="{youtube_url}" target="_blank" class="time-link">🔗 Jump to time</a>' if youtube_url else ''}
            </div>
            <div class="segment-text">{clean_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show results summary
    if total_pages > 1 or search_term:
        st.markdown(f"""
        <div class="search-results-info">
            📊 Showing {len(current_segments)} of {len(filtered_segments)} segments
            {f' | 🔍 Filtered by: "{search_term}"' if search_term else ''}
            {f' | 📄 Page {st.session_state.transcript_page + 1} of {total_pages}' if total_pages > 1 else ''}
        </div>
        """, unsafe_allow_html=True)


def _format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    if not seconds:
        return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
