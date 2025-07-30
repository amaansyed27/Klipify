"""
Video Processing Pipeline for Klipify
Orchestrates the complete video processing workflow.
"""

import streamlit as st
from datetime import datetime
from .services.video_service import VideoProcessor
from .services.ai_service import AIService
from .ui.displays import display_processing_status


class VideoProcessingPipeline:
    """Orchestrates the complete video processing workflow."""
    
    def __init__(self, video_client, ai_client):
        """
        Initialize the processing pipeline.
        
        Args:
            video_client: VideoDB client
            ai_client: GenAI client
        """
        self.video_processor = VideoProcessor(video_client)
        self.ai_service = AIService(ai_client)
    
    def process_video(self, youtube_url, youtube_id):
        """
        Process a YouTube video through the complete pipeline.
        
        Args:
            youtube_url (str): YouTube video URL
            youtube_id (str): YouTube video ID
            
        Returns:
            dict: Complete video data or None if processing fails
        """
        try:
            total_steps = 5
            
            # Step 1: Upload and Index Video
            display_processing_status(1, total_steps, "Processing video with VideoDB...")
            video, transcript_text, transcript_segments = self.video_processor.upload_and_index_video(youtube_url)
            st.success("✅ Video processed and indexed!")
            
            # Step 2: Generate Video Summary
            display_processing_status(2, total_steps, "Generating video summary...")
            video_summary = self.ai_service.generate_video_summary(transcript_text)
            st.success("✅ Summary generated!")
            
            # Step 3: Extract Key Concepts
            display_processing_status(3, total_steps, "Identifying key concepts...")
            concepts = self.ai_service.extract_key_concepts(transcript_text)
            st.success(f"✅ Identified {len(concepts)} key concepts!")
            
            # Step 4: Find Video Segments
            display_processing_status(4, total_steps, "Finding video segments...")
            concepts_with_segments = self.video_processor.find_concept_segments(concepts)
            st.success(f"✅ Found segments for {len(concepts_with_segments)} concepts!")
            
            # Step 5: Create Video Clips and Notes
            display_processing_status(5, total_steps, "Creating clips and notes...")
            video_clips = self.video_processor.create_video_clips(concepts_with_segments)
            timestamped_notes = self.ai_service.generate_timestamped_notes(transcript_segments, youtube_id)
            st.success("🎉 Complete educational package ready!")
            
            # Compile all data
            video_data = {
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
            
            # Store in session state
            st.session_state.video_data = video_data
            
            # Set video context for chat
            st.session_state.video_context = {
                'transcript': transcript_text,
                'summary': video_summary,
                'concepts': concepts
            }
            
            st.session_state.processing_complete = True
            
            return video_data
            
        except Exception as e:
            st.error(f"❌ Error processing video: {str(e)}")
            st.info("💡 Try with a different video or check your API keys.")
            return None


def validate_processing_requirements(video_client, ai_client):
    """
    Validate that all requirements for processing are met.
    
    Args:
        video_client: VideoDB client
        ai_client: GenAI client
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not video_client:
        return False, "VideoDB client not initialized. Please check your VideoDB API key."
    
    if not ai_client:
        return False, "GenAI client not initialized. Please check your Gemini API key."
    
    return True, None


def create_processing_summary(video_data):
    """
    Create a summary of the processing results.
    
    Args:
        video_data (dict): Processed video data
        
    Returns:
        dict: Processing summary statistics
    """
    if not video_data:
        return None
    
    return {
        'concepts_found': len(video_data.get('concepts', [])),
        'clips_created': len(video_data.get('clips', [])),
        'transcript_length': len(video_data.get('transcript_text', '')),
        'processing_time': video_data.get('processed_at', 'Unknown'),
        'has_summary': bool(video_data.get('summary')),
        'has_notes': bool(video_data.get('notes'))
    }


def handle_processing_error(error, context="video processing"):
    """
    Handle and display processing errors appropriately.
    
    Args:
        error (Exception): The error that occurred
        context (str): Context where the error occurred
    """
    error_message = str(error)
    
    # Provide specific guidance based on error type
    if "API key" in error_message.lower():
        st.error("🔑 API Key Error")
        st.info("Please check that your API keys are correctly configured.")
    elif "transcript" in error_message.lower():
        st.error("📝 Transcript Error")
        st.info("The video might not have a transcript or captions. Try a different video.")
    elif "upload" in error_message.lower():
        st.error("📤 Upload Error")
        st.info("There was an issue uploading the video. Please check the URL and try again.")
    elif "quota" in error_message.lower() or "limit" in error_message.lower():
        st.error("⚡ Rate Limit Error")
        st.info("API rate limit reached. Please wait a moment and try again.")
    else:
        st.error(f"❌ {context.title()} Error")
        st.info(f"An unexpected error occurred: {error_message}")
    
    # Always show general troubleshooting tips
    with st.expander("🔧 Troubleshooting Tips"):
        st.markdown("""
        **Common solutions:**
        - Ensure the YouTube video has captions/transcript
        - Check that the video is publicly accessible
        - Verify your API keys are valid and have sufficient quota
        - Try with a shorter video (under 10 minutes)
        - Make sure the video is educational content
        """)


def get_processing_metrics():
    """
    Get metrics about the current processing session.
    
    Returns:
        dict: Processing metrics
    """
    if 'video_data' not in st.session_state:
        return None
    
    video_data = st.session_state.video_data
    
    return {
        'video_processed': True,
        'concepts_extracted': len(video_data.get('concepts', [])),
        'clips_generated': len(video_data.get('clips', [])),
        'summary_available': bool(video_data.get('summary')),
        'notes_available': bool(video_data.get('notes')),
        'chat_enabled': bool(st.session_state.get('video_context')),
        'processing_timestamp': video_data.get('processed_at')
    }
