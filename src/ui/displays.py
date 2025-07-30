"""
Display and Tab Components for Klipify
Contains all tab content and display logic for the main application.
"""

import streamlit as st
from .components import show_warning_message
from ..services.ai_service import initialize_genai_client
from ..utils.helpers import create_youtube_link


def display_content_tabs(video_data):
    """
    Display the main content tabs with processed video data.
    
    Args:
        video_data (dict): Processed video data from session state
    """
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Video Clips", "📋 Summary", "📝 Notes", "💬 AI Assistant"])
    
    with tab1:
        display_video_clips_tab(video_data)
    
    with tab2:
        display_summary_tab(video_data)
    
    with tab3:
        display_notes_tab(video_data)
    
    with tab4:
        display_chat_tab(video_data)


def display_video_clips_tab(video_data):
    """Display the video clips tab."""
    st.header("🎬 Educational Video Clips")
    st.markdown("Watch bite-sized clips focusing on key concepts:")
    
    clips = video_data['clips']
    youtube_id = video_data['youtube_id']
    
    if not clips:
        show_warning_message("No video clips were generated. Try with a video that has clearer educational content.")
        return
    
    # Display clips in a grid
    for i, clip in enumerate(clips):
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"📖 {clip['concept']}")
                st.write(f"**Duration:** {clip['duration']:.0f} seconds")
                st.write(f"**Starts at:** {clip['formatted_time']}")
            
            with col2:
                # Create buttons for interaction
                youtube_link = create_youtube_link(youtube_id, clip['start_time'])
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.link_button("▶️ YouTube", youtube_link, use_container_width=True)
                
                with btn_col2:
                    if st.button(f"🎥 Play", key=f"clip_{i}", use_container_width=True):
                        st.video(clip['stream_url'])
            
            st.divider()


def display_summary_tab(video_data):
    """Display the video summary tab."""
    st.header("📋 Video Summary")
    
    # Video metadata
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Processed:** {video_data['processed_at']}")
        st.write(f"**Concepts Identified:** {len(video_data['concepts'])}")
    
    with col2:
        st.link_button("🔗 Original Video", video_data['youtube_url'], use_container_width=True)
    
    st.divider()
    
    # AI-generated summary
    st.markdown(video_data['summary'])
    
    # Quick concept overview
    st.subheader("🔍 Key Concepts Covered")
    concept_cols = st.columns(3)
    
    for i, concept in enumerate(video_data['concepts']):
        with concept_cols[i % 3]:
            st.info(f"📌 {concept}")


def display_notes_tab(video_data):
    """Display the timestamped notes tab."""
    st.header("📝 Timestamped Study Notes")
    
    # Display AI-generated notes
    st.markdown(video_data['notes'])
    
    st.divider()
    
    # Raw transcript with timestamps (collapsible)
    with st.expander("📄 Full Transcript with Timestamps"):
        transcript_segments = video_data['transcript_segments']
        
        for segment in transcript_segments:
            start_time = _format_timestamp(segment.get('start', 0))
            text = segment.get('text', '')
            st.write(f"**[{start_time}]** {text}")


def display_chat_tab(video_data):
    """Display the AI chat assistant tab."""
    st.header("💬 AI Study Assistant")
    st.markdown("Ask questions about the video content or get help with related topics!")
    
    # Chat interface
    if not st.session_state.get('video_context'):
        show_warning_message("Please process a video first to enable the AI assistant.")
        return
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(message["user"])
        with st.chat_message("assistant"):
            st.write(message["assistant"])
    
    # Chat input
    if user_input := st.chat_input("Ask me anything about the video..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get client for chat
                genai_client = initialize_genai_client()
                
                if genai_client:
                    from ..services.ai_service import AIService
                    ai_service = AIService(genai_client)
                    
                    try:
                        ai_response = ai_service.chat_with_assistant(
                            user_input, 
                            st.session_state.video_context,
                            st.session_state.chat_history
                        )
                        st.write(ai_response)
                        
                        # Save to chat history
                        st.session_state.chat_history.append({
                            "user": user_input,
                            "assistant": ai_response
                        })
                        
                    except Exception as e:
                        st.error(f"Chat error: {str(e)}")
                        ai_response = "I'm sorry, I encountered an error. Please try again."
                else:
                    st.error("AI service not available. Please check your API configuration.")
                    ai_response = "AI service is currently unavailable."
        
        st.rerun()


def display_processing_status(step, total_steps, message):
    """
    Display processing status with progress.
    
    Args:
        step (int): Current step number
        total_steps (int): Total number of steps
        message (str): Status message
    """
    progress = step / total_steps
    st.progress(progress)
    st.info(f"**Step {step}/{total_steps}:** {message}")


def display_sidebar_input():
    """Display the sidebar input section."""
    with st.sidebar:
        st.markdown("### 📹 **Video Input**")
        
        youtube_url = st.text_input(
            "YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=example",
            help="Paste the URL of an educational YouTube video"
        )
        
        process_button = st.button(
            "🚀 Process Video", 
            type="primary", 
            use_container_width=True
        )
        
        st.divider()
        
        # Display processing status
        if st.session_state.get('processing_complete'):
            st.success("✅ Video processed successfully!")
            st.info("Navigate between tabs to explore different features")
            
            # Add reset button
            if st.button("🔄 Process New Video", use_container_width=True):
                from ..utils.helpers import reset_session_state
                reset_session_state()
                st.rerun()
        
        return youtube_url, process_button


def display_error_state():
    """Display error state with setup instructions."""
    from ..ui.components import show_error_message
    from ..utils.helpers import create_setup_instructions
    
    show_error_message(
        "API Configuration Required",
        "Setup Instructions",
        create_setup_instructions()
    )


def _format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
