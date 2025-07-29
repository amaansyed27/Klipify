"""
AI Tutor - Instant Educational Shorts Generator
A Streamlit web application that processes YouTube videos using VideoDB
and Google's Gemini model to create educational knowledge nuggets.
"""

import streamlit as st
import videodb
from videodb import SearchType, IndexType
import os
import re
from google import genai


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
        page_title="AI Tutor - Educational Shorts Generator",
        page_icon="🧠",
        layout="wide"
    )
    
    # App title and description
    st.title("🧠 AI Tutor: Instant Educational Shorts Generator")
    st.markdown("""
    Transform any YouTube educational video into bite-sized knowledge nuggets! 
    Simply paste a YouTube URL and let AI identify key concepts with timestamped links.
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
    
    # User input
    st.subheader("📹 Enter YouTube Video URL")
    youtube_url = st.text_input(
        "YouTube URL:",
        placeholder="https://www.youtube.com/watch?v=example",
        help="Paste the URL of an educational YouTube video"
    )
    
    # Process button
    if st.button("🚀 Generate Knowledge Nuggets", type="primary"):
        if not youtube_url:
            st.warning("⚠️ Please enter a YouTube URL first.")
            return
        
        # Extract YouTube ID
        youtube_id = get_youtube_id(youtube_url)
        if not youtube_id:
            st.error("❌ Invalid YouTube URL. Please check the URL and try again.")
            return
        
        try:
            # Step 1: Process video with VideoDB
            with st.spinner('Step 1/4: Processing video with VideoDB...'):
                st.info("📤 Uploading video to VideoDB and indexing for search...")
                
                # Upload video to VideoDB
                video = video_db_client.upload(url=youtube_url)
                st.info("✅ Video uploaded successfully!")
                
                # Index the video for spoken words (required for search)
                st.info("🔍 Indexing video content for semantic search...")
                video.index_spoken_words()
                st.info("✅ Video indexed successfully!")
                
                # Get the transcript text directly
                transcript_text = video.get_transcript_text()
                
                if not transcript_text or len(transcript_text.strip()) < 50:
                    st.error("❌ Could not extract meaningful transcript from the video. Please try with a different video that has clear spoken content.")
                    return
                
                st.success("✅ Video processed and indexed for search!")
                
                # Show transcript preview
                with st.expander("📝 Preview Transcript (First 500 characters)"):
                    st.text(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
            
            # Step 2: Identify key concepts with Gemini
            with st.spinner('Step 2/4: Identifying key concepts with Gemini...'):
                st.info("🧠 Analyzing transcript to identify key educational concepts...")
                
                # Create prompt for Gemini
                prompt = f"""You are an expert instructional designer. Analyze the following video transcript and identify the 5-8 most important educational concepts or topics that a student should focus on. 

Each concept should be:
- A clear, specific topic or idea
- Something that can be explained in 30-60 seconds
- Educationally valuable
- Searchable within the video content

Return the concepts as a simple list separated by newlines, with each concept being concise (1-8 words max).

Here is the transcript: {transcript_text}"""
                
                # Call Gemini using the new client syntax with latest model
                response = genai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # Parse the response
                concepts = [concept.strip() for concept in response.text.strip().split('\n') if concept.strip()]
                
                st.success(f"✅ Identified {len(concepts)} key concepts!")
                
                # Display identified concepts
                with st.expander("🔍 Preview Identified Concepts"):
                    for i, concept in enumerate(concepts, 1):
                        st.write(f"{i}. {concept}")
            
            # Step 3: Find video segments for each concept
            with st.spinner('Step 3/4: Finding video segments for each concept...'):
                st.info("🎯 Searching for relevant video clips for each concept...")
                
                knowledge_nuggets = []
                progress_bar = st.progress(0)
                
                for i, concept in enumerate(concepts):
                    try:
                        # Update progress
                        progress = (i + 1) / len(concepts)
                        progress_bar.progress(progress)
                        st.info(f"🔍 Searching for: {concept}")
                        
                        # Search for the concept in the video using semantic search
                        search_results = video.search(
                            query=concept, 
                            search_type=SearchType.semantic,
                            index_type=IndexType.spoken_word
                        )
                        
                        if search_results and len(search_results.get_shots()) > 0:
                            # Get the first (best) result shot
                            shots = search_results.get_shots()
                            best_shot = shots[0]
                            knowledge_nuggets.append({
                                'concept': concept,
                                'start_time': best_shot.start,
                                'end_time': best_shot.end,
                                'search_score': getattr(best_shot, 'search_score', 0)
                            })
                            st.success(f"✅ Found segment for: {concept}")
                        else:
                            st.warning(f"⚠️ No clear segment found for: {concept}")
                    except Exception as e:
                        st.warning(f"⚠️ Search failed for concept: {concept} - {str(e)}")
                        continue
                
                progress_bar.empty()
                st.success(f"✅ Found video segments for {len(knowledge_nuggets)} out of {len(concepts)} concepts!")
            
            # Step 4: Generate study guide
            with st.spinner('Step 4/4: Generating your study guide...'):
                st.info("📚 Creating your personalized study guide...")
                
                # Small delay for effect
                import time
                time.sleep(1)
                
                st.success("🎉 Your AI-powered study guide is ready!")
            
            # Display Results
            st.markdown("---")
            st.subheader("📚 Your Knowledge Nuggets")
            st.markdown("Click on any concept to jump directly to that part of the video!")
            
            if knowledge_nuggets:
                for i, nugget in enumerate(knowledge_nuggets, 1):
                    concept = nugget['concept']
                    start_time = int(nugget['start_time'])
                    end_time = int(nugget['end_time'])
                    duration = end_time - start_time
                    
                    # Create a card-like display for each nugget
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. {concept}")
                            st.markdown(f"**Duration:** {duration} seconds")
                            
                            # Clickable timestamped link
                            youtube_link = f"https://www.youtube.com/watch?v={youtube_id}&t={start_time}s"
                            st.markdown(f"🎬 [**Watch Clip**]({youtube_link})")
                        
                        with col2:
                            st.metric("Start Time", f"{start_time}s")
                        
                        st.markdown("---")
            else:
                st.warning("⚠️ No video segments were found for the identified concepts. This might happen with very short videos or videos with unclear audio.")
        
        except Exception as e:
            st.error(f"❌ An error occurred while processing the video: {str(e)}")
            st.info("💡 Try with a different video or check your API keys.")


if __name__ == "__main__":
    main()
