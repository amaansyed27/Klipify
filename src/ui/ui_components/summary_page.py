"""
Summary page component for displaying video summary and concepts.
"""

import streamlit as st

def show_summary_page(video_data):
    """Display the summary page with professional design."""
    st.markdown("""
    <div class="page-header">
        <h2>📊 Video Summary</h2>
        <p class="page-subtitle">AI-generated insights and key educational concepts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional metadata cards
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = video_data.get('duration', 0)
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            st.metric("Duration", f"{minutes}:{seconds:02d}")
        else:
            st.metric("Duration", "Unknown")
    
    with col2:
        clips_count = len(video_data.get('clips', []))
        st.metric("Clips Generated", clips_count)
    
    with col3:
        concepts_count = len(video_data.get('concepts', []))
        st.metric("Key Concepts", concepts_count)
    
    # Quick access
    if video_data.get('youtube_url'):
        st.link_button("🔗 Watch Original Video", video_data['youtube_url'])
    
    st.markdown("---")
    
    # Executive summary section
    st.markdown("""
    <div class="section-header">
        <h3>📝 Executive Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    summary = video_data.get('summary', 'No summary available.')
    st.markdown(f"""
    <div class="summary-content">
        {summary}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key concepts section with search
    st.markdown("""
    <div class="section-header">
        <h3>🎯 Key Concepts</h3>
    </div>
    """, unsafe_allow_html=True)
    
    concepts = video_data.get('concepts', [])
    
    if concepts:
        _show_concepts_section(concepts)
    else:
        st.markdown("""
        <div class="empty-state">
            <h3>No concepts extracted</h3>
            <p>The AI couldn't identify key concepts from this video.</p>
        </div>
        """, unsafe_allow_html=True)


def _show_concepts_section(concepts):
    """Display concepts with pagination for performance."""
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_concepts = st.text_input("🔍 Search concepts...", placeholder="Filter concepts by keyword")
    with col2:
        show_all = st.checkbox("Show all concepts", value=False)
    
    # Filter concepts based on search
    if search_concepts:
        search_lower = search_concepts.lower()
        filtered_concepts = [
            concept for concept in concepts
            if search_lower in concept.lower()
        ]
    else:
        filtered_concepts = concepts
    
    if not filtered_concepts:
        st.info("No concepts found matching your search.")
        return
    
    # Pagination for performance - only show limited concepts by default
    concepts_to_show = filtered_concepts
    default_limit = 8
    pagination_limit = 24
    
    if not show_all and len(filtered_concepts) > default_limit:
        # Show pagination info
        st.markdown(f"""
        <div class="concept-info">
            Showing {default_limit} of {len(filtered_concepts)} concepts. 
            Check "Show all concepts" to see more.
        </div>
        """, unsafe_allow_html=True)
        
        # Use session state for pagination
        if 'concept_page' not in st.session_state:
            st.session_state.concept_page = 0
        
        max_page = (len(filtered_concepts) - 1) // pagination_limit
        
        if len(filtered_concepts) > pagination_limit:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("← Previous", disabled=st.session_state.concept_page == 0):
                    st.session_state.concept_page = max(0, st.session_state.concept_page - 1)
                    st.rerun()
            
            with col2:
                st.markdown(f"<div style='text-align: center; color: var(--text-secondary);'>Page {st.session_state.concept_page + 1} of {max_page + 1}</div>", unsafe_allow_html=True)
            
            with col3:
                if st.button("Next →", disabled=st.session_state.concept_page >= max_page):
                    st.session_state.concept_page = min(max_page, st.session_state.concept_page + 1)
                    st.rerun()
        
        start_idx = st.session_state.concept_page * pagination_limit
        end_idx = start_idx + pagination_limit
        concepts_to_show = filtered_concepts[start_idx:end_idx]
    else:
        concepts_to_show = filtered_concepts[:default_limit] if not show_all else filtered_concepts
    
    # Display concepts
    for i, concept in enumerate(concepts_to_show):
        st.markdown(f"""
        <div class="concept-card">
            <span class="concept-icon">💡</span>
            <span class="concept-text">{concept}</span>
        </div>
        """, unsafe_allow_html=True)
