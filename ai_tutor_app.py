"""
AI Tutor - Comprehensive Educational Video Platform
A Streamlit web application that processes YouTube videos using VideoDB
and Google's Gemini model to create:
- Video clips and shorts
- AI-generated summaries
- Timestamped notes
- Interactive AI chat assistant
"""

import streamlit as st
import videodb
from videodb import SearchType, IndexType
import os
import re
from google import genai
import json
from datetime import datetime
import time


def format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def generate_video_summary(genai_client, transcript_text):
    """Generate a comprehensive summary of the video."""
    prompt = f"""
    You are an expert educational content analyst. Create a comprehensive summary of this video transcript.
    
    Provide:
    1. A brief overview (2-3 sentences)
    2. Key learning objectives (3-5 bullet points)
    3. Main topics covered (with brief descriptions)
    4. Target audience
    5. Difficulty level (Beginner/Intermediate/Advanced)
    
    Format your response as a well-structured summary that helps students understand what they'll learn.
    
    Transcript: {transcript_text}
    """
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def generate_timestamped_notes(genai_client, transcript_segments):
    """Generate detailed timestamped notes from transcript segments."""
    # Prepare transcript with timestamps for analysis
    timestamped_content = ""
    for segment in transcript_segments:
        start_time = format_timestamp(segment.get('start', 0))
        text = segment.get('text', '')
        timestamped_content += f"[{start_time}] {text}\n"
    
    prompt = f"""
    You are an expert note-taker. Analyze this timestamped video transcript and create comprehensive study notes.
    
    Create structured notes with:
    1. Major sections/topics (with time ranges)
    2. Key concepts and definitions
    3. Important examples or explanations
    4. Action items or takeaways
    
    Format as markdown with clear headings and bullet points. Include timestamps for easy navigation.
    
    Timestamped transcript:
    {timestamped_content}
    """
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def create_video_clips(video, concepts_with_segments):
    """Create short video clips for each concept using VideoDB."""
    clips = []
    
    for concept_data in concepts_with_segments:
        try:
            concept = concept_data['concept']
            start_time = concept_data['start_time']
            end_time = concept_data['end_time']
            
            # Create a short clip (limit to 60 seconds max for shorts)
            clip_duration = min(end_time - start_time, 60)
            clip_end = start_time + clip_duration
            
            # Generate clip stream URL
            clip_stream = video.generate_stream(timeline=[(start_time, clip_end)])
            
            clips.append({
                'concept': concept,
                'start_time': start_time,
                'end_time': clip_end,
                'duration': clip_duration,
                'stream_url': clip_stream,
                'formatted_time': format_timestamp(start_time)
            })
            
        except Exception as e:
            st.warning(f"Could not create clip for {concept}: {str(e)}")
            continue
    
    return clips


def get_youtube_id(url):
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: YouTube video ID or None if not found
    """
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def initialize_chat_session():
    """Initialize the chat session state."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'video_context' not in st.session_state:
        st.session_state.video_context = None


def chat_with_assistant(genai_client, user_message, video_context, chat_history):
    """Handle chat with the AI assistant using video context."""
    # Prepare context for the AI
    context_prompt = f"""
    You are an educational AI assistant helping students understand a video. 
    
    Video Context:
    {video_context}
    
    Chat History:
    {chr(10).join([f"User: {msg['user']}" + chr(10) + f"Assistant: {msg['assistant']}" for msg in chat_history[-5:]])}
    
    Current Question: {user_message}
    
    Instructions:
    - Answer based on the video content when relevant
    - Provide educational explanations and examples
    - If the question is outside the video scope, use your general knowledge but mention this
    - Be helpful, clear, and encouraging
    - Ask follow-up questions to deepen understanding
    """
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context_prompt
    )
    
    return response.text
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: YouTube video ID or None if not found
    """
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def initialize_clients():
    """
    Initialize VideoDB and Google GenAI clients.
    
    Returns:
        tuple: (videodb_client, genai_client)
    """
    try:
        # Initialize VideoDB client
        videodb_api_key = st.secrets.get("VIDEODB_API_KEY") or os.getenv("VIDEODB_API_KEY")
        if not videodb_api_key:
            st.error("❌ VideoDB API key not found. Please set VIDEODB_API_KEY in secrets or environment variables.")
            return None, None
        
        video_db_client = videodb.connect(api_key=videodb_api_key)
        
        # Initialize Google GenAI client 
        # The new client automatically finds GEMINI_API_KEY from environment
        # Note: Changed from GOOGLE_API_KEY to GEMINI_API_KEY as per official docs
        genai_client = genai.Client()
        
        return video_db_client, genai_client
    
    except Exception as e:
        st.error(f"❌ Error initializing clients: {str(e)}")
        return None, None


def main():
    """Main application function."""
    
    # Set page configuration
    st.set_page_config(
        page_title="AI Tutor - Comprehensive Educational Platform",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize chat session
    initialize_chat_session()
    
    # App title and description
    st.title("🧠 AI Tutor: Comprehensive Educational Platform")
    st.markdown("""
    Transform any YouTube educational video into a complete learning experience with:
    - 🎬 **Smart Video Clips** - Bite-sized educational shorts
    - 📋 **AI Summary** - Quick overview and learning objectives  
    - 📝 **Timestamped Notes** - Detailed study notes with navigation
    - 💬 **AI Chat Assistant** - Interactive Q&A grounded in video content
    """)
    
    # Initialize clients
    video_db_client, genai_client = initialize_clients()
    
    if not video_db_client or not genai_client:
        st.warning("⚠️ Please ensure both VIDEODB_API_KEY and GEMINI_API_KEY are properly configured.")
        st.info("""
        **Setup Instructions:**
        1. Get your VideoDB API key from https://console.videodb.io/
        2. Get your Google API key from https://aistudio.google.com/app/apikey
        3. Set GEMINI_API_KEY environment variable (the new client uses this name)
        4. Add VIDEODB_API_KEY to your Streamlit secrets or environment variables
        """)
        return
    
    # Sidebar for input and controls
    with st.sidebar:
        st.header("📹 Video Input")
        youtube_url = st.text_input(
            "YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=example",
            help="Paste the URL of an educational YouTube video"
        )
        
        process_button = st.button("🚀 Process Video", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Display processing status
        if 'processing_complete' in st.session_state and st.session_state.processing_complete:
            st.success("✅ Video processed successfully!")
            st.info("Navigate between tabs to explore different features")
    
    # Main content area with tabs
    if process_button and youtube_url:
        # Extract YouTube ID
        youtube_id = get_youtube_id(youtube_url)
        if not youtube_id:
            st.error("❌ Invalid YouTube URL. Please check the URL and try again.")
            return
        
        # Process the video
        process_video(video_db_client, genai_client, youtube_url, youtube_id)
    
    # Display processed content if available
    if 'video_data' in st.session_state:
        display_processed_content()


def process_video(video_db_client, genai_client, youtube_url, youtube_id):
    """Process the video and extract all educational content."""
    
    try:
        # Step 1: Upload and Index Video
        with st.spinner('Step 1/5: Processing video with VideoDB...'):
            st.info("📤 Uploading video to VideoDB...")
            video = video_db_client.upload(url=youtube_url)
            
            st.info("🔍 Indexing video content for search...")
            video.index_spoken_words()
            
            # Get transcript
            transcript_text = video.get_transcript_text()
            transcript_segments = video.get_transcript()
            
            if not transcript_text or len(transcript_text.strip()) < 50:
                st.error("❌ Could not extract meaningful transcript. Please try a different video.")
                return
            
            st.success("✅ Video processed and indexed!")
        
        # Step 2: Generate Video Summary
        with st.spinner('Step 2/5: Generating video summary...'):
            st.info("📋 Creating comprehensive video summary...")
            video_summary = generate_video_summary(genai_client, transcript_text)
            st.success("✅ Summary generated!")
        
        # Step 3: Extract Key Concepts
        with st.spinner('Step 3/5: Identifying key concepts...'):
            st.info("🧠 Analyzing content for key educational concepts...")
            concepts = extract_key_concepts(genai_client, transcript_text)
            st.success(f"✅ Identified {len(concepts)} key concepts!")
        
        # Step 4: Find Video Segments
        with st.spinner('Step 4/5: Finding video segments...'):
            st.info("🎯 Searching for relevant clips...")
            concepts_with_segments = find_concept_segments(video, concepts)
            st.success(f"✅ Found segments for {len(concepts_with_segments)} concepts!")
        
        # Step 5: Create Video Clips and Notes
        with st.spinner('Step 5/5: Creating clips and notes...'):
            st.info("🎬 Generating video clips...")
            video_clips = create_video_clips(video, concepts_with_segments)
            
            st.info("📝 Creating timestamped notes...")
            timestamped_notes = generate_timestamped_notes(genai_client, transcript_segments)
            
            st.success("🎉 Complete educational package ready!")
        
        # Store all data in session state
        st.session_state.video_data = {
            'youtube_id': youtube_id,
            'youtube_url': youtube_url,
            'video_object': video,
            'transcript_text': transcript_text,
            'transcript_segments': transcript_segments,
            'summary': video_summary,
            'concepts': concepts,
            'clips': video_clips,
            'notes': timestamped_notes,
            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Set video context for chat
        st.session_state.video_context = {
            'transcript': transcript_text,
            'summary': video_summary,
            'concepts': concepts
        }
        
        st.session_state.processing_complete = True
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        st.info("💡 Try with a different video or check your API keys.")


def extract_key_concepts(genai_client, transcript_text):
    """Extract key concepts using Gemini."""
    prompt = f"""
    Analyze this educational video transcript and identify 6-8 key concepts that students should focus on.
    
    Each concept should be:
    - A clear, specific topic (2-6 words)
    - Educationally valuable
    - Searchable within the video
    
    Return as a simple list, one concept per line.
    
    Transcript: {transcript_text}
    """
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    concepts = [concept.strip() for concept in response.text.strip().split('\n') if concept.strip()]
    return concepts[:8]  # Limit to 8 concepts


def find_concept_segments(video, concepts):
    """Find video segments for each concept."""
    concepts_with_segments = []
    
    for concept in concepts:
        try:
            search_results = video.search(
                query=concept,
                search_type=SearchType.semantic,
                index_type=IndexType.spoken_word
            )
            
            if search_results and len(search_results.get_shots()) > 0:
                best_shot = search_results.get_shots()[0]
                concepts_with_segments.append({
                    'concept': concept,
                    'start_time': best_shot.start,
                    'end_time': best_shot.end,
                })
        except Exception:
            continue
    
    return concepts_with_segments


def display_processed_content():
    """Display the processed video content in tabs."""
    
    video_data = st.session_state.video_data
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Video Clips", "📋 Summary", "📝 Notes", "💬 AI Assistant"])
    
    with tab1:
        display_video_clips_tab(video_data)
    
    with tab2:
        display_summary_tab(video_data)
    
    with tab3:
        display_notes_tab(video_data)
    
    with tab4:
        display_chat_tab()


def display_video_clips_tab(video_data):
    """Display the video clips tab."""
    st.header("🎬 Educational Video Clips")
    st.markdown("Watch bite-sized clips focusing on key concepts:")
    
    clips = video_data['clips']
    youtube_id = video_data['youtube_id']
    
    if not clips:
        st.warning("⚠️ No video clips were generated. Try with a video that has clearer educational content.")
        return
    
    # Display clips in a grid
    cols = st.columns(2)
    
    for i, clip in enumerate(clips):
        with cols[i % 2]:
            with st.container():
                st.subheader(f"📖 {clip['concept']}")
                st.write(f"**Duration:** {clip['duration']:.0f} seconds")
                st.write(f"**Starts at:** {clip['formatted_time']}")
                
                # Embedded video player with timestamp
                youtube_link = f"https://www.youtube.com/watch?v={youtube_id}&t={int(clip['start_time'])}s"
                
                # Create columns for buttons
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.link_button("▶️ Watch on YouTube", youtube_link, use_container_width=True)
                
                with btn_col2:
                    if st.button(f"🎥 Play Clip", key=f"clip_{i}", use_container_width=True):
                        st.video(clip['stream_url'])
                
                st.markdown("---")


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
    
    st.markdown("---")
    
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
    
    st.markdown("---")
    
    # Raw transcript with timestamps (collapsible)
    with st.expander("📄 Full Transcript with Timestamps"):
        transcript_segments = video_data['transcript_segments']
        
        for segment in transcript_segments:
            start_time = format_timestamp(segment.get('start', 0))
            text = segment.get('text', '')
            st.write(f"**[{start_time}]** {text}")


def display_chat_tab():
    """Display the AI chat assistant tab."""
    st.header("💬 AI Study Assistant")
    st.markdown("Ask questions about the video content or get help with related topics!")
    
    # Chat interface
    if not st.session_state.video_context:
        st.warning("⚠️ Please process a video first to enable the AI assistant.")
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
                # Get clients for chat
                _, genai_client = initialize_clients()
                
                ai_response = chat_with_assistant(
                    genai_client, 
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
        
        st.rerun()


if __name__ == "__main__":
    main()
