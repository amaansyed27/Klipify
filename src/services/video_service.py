"""
Video Processing Service for Klipify
Handles all VideoDB operations including upload, indexing, and clip generation.
"""

import streamlit as st
import videodb
from videodb import SearchType, IndexType
from datetime import datetime


class VideoProcessor:
    """Handles video processing operations using VideoDB."""
    
    def __init__(self, client):
        """Initialize with VideoDB client."""
        self.client = client
        self.video = None
    
    def upload_and_index_video(self, youtube_url):
        """
        Upload video to VideoDB and index for search.
        
        Args:
            youtube_url (str): YouTube video URL
            
        Returns:
            tuple: (video_object, transcript_text, transcript_segments)
        """
        try:
            # Upload video
            st.info("📤 Uploading video to VideoDB...")
            self.video = self.client.upload(url=youtube_url)
            
            # Index spoken words for semantic search
            st.info("🔍 Indexing video content for search...")
            self.video.index_spoken_words()
            
            # Get transcript
            transcript_text = self.video.get_transcript_text()
            transcript_segments = self.video.get_transcript()
            
            # Validate transcript
            if not transcript_text or len(transcript_text.strip()) < 50:
                raise ValueError("Could not extract meaningful transcript")
            
            return self.video, transcript_text, transcript_segments
            
        except Exception as e:
            raise Exception(f"Video processing failed: {str(e)}")
    
    def find_concept_segments(self, concepts):
        """
        Find video segments for each concept using semantic search.
        
        Args:
            concepts (list): List of concept strings
            
        Returns:
            list: List of concept data with timestamps
        """
        if not self.video:
            raise ValueError("No video loaded. Upload a video first.")
        
        concepts_with_segments = []
        
        for concept in concepts:
            try:
                search_results = self.video.search(
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
            except Exception as e:
                st.warning(f"Could not find segment for concept '{concept}': {str(e)}")
                continue
        
        return concepts_with_segments
    
    def create_video_clips(self, concepts_with_segments):
        """
        Create short video clips for each concept.
        
        Args:
            concepts_with_segments (list): Concepts with timestamp data
            
        Returns:
            list: List of clip data with stream URLs
        """
        if not self.video:
            raise ValueError("No video loaded. Upload a video first.")
        
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
                clip_stream = self.video.generate_stream(timeline=[(start_time, clip_end)])
                
                clips.append({
                    'concept': concept,
                    'start_time': start_time,
                    'end_time': clip_end,
                    'duration': clip_duration,
                    'stream_url': clip_stream,
                    'formatted_time': self._format_timestamp(start_time)
                })
                
            except Exception as e:
                st.warning(f"Could not create clip for {concept}: {str(e)}")
                continue
        
        return clips
    
    def get_video_metadata(self):
        """Get metadata about the processed video."""
        if not self.video:
            return None
        
        try:
            return {
                'video_id': getattr(self.video, 'id', 'unknown'),
                'duration': getattr(self.video, 'length', 0),
                'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception:
            return {
                'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    @staticmethod
    def _format_timestamp(seconds):
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"


def initialize_videodb_client():
    """
    Initialize VideoDB client from API keys.
    
    Returns:
        VideoDB client or None if initialization fails
    """
    try:
        videodb_api_key = st.secrets.get("VIDEODB_API_KEY") or st.secrets.get("videodb_api_key")
        
        if not videodb_api_key:
            import os
            videodb_api_key = os.getenv("VIDEODB_API_KEY")
        
        if not videodb_api_key:
            return None
        
        return videodb.connect(api_key=videodb_api_key)
        
    except Exception as e:
        st.error(f"Failed to initialize VideoDB client: {str(e)}")
        return None
