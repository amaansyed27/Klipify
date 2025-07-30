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
        Create short video clips for each concept using VideoDB Timeline approach.
        
        Args:
            concepts_with_segments (list): Concepts with timestamp data
            
        Returns:
            list: List of clip data with stream URLs and download options
        """
        if not self.video:
            raise ValueError("No video loaded. Upload a video first.")

        clips = []
        
        # Import Timeline and VideoAsset for proper clip creation
        try:
            from videodb.timeline import Timeline
            from videodb.asset import VideoAsset
        except ImportError:
            st.error("❌ VideoDB Timeline feature not available. Please update VideoDB SDK.")
            return clips

        for concept_data in concepts_with_segments:
            try:
                concept = concept_data['concept']
                start_time = concept_data['start_time']
                end_time = concept_data['end_time']
                
                # Create a short clip (limit to 60 seconds max for shorts)
                clip_duration = min(end_time - start_time, 60)
                clip_end = start_time + clip_duration
                
                # Initialize clip data
                clip_data = {
                    'concept': concept,
                    'start_time': start_time,
                    'end_time': clip_end,
                    'duration': clip_duration,
                    'formatted_time': self._format_timestamp(start_time),
                    'stream_url': None,
                    'download_url': None,
                    'timeline_url': None,
                    'playable': False
                }

                # Method 1: Use VideoDB Timeline for creating downloadable clips
                try:
                    # Create Timeline object
                    timeline = Timeline(self.client)
                    
                    # Create VideoAsset with the specific segment
                    video_asset = VideoAsset(
                        asset_id=self.video.id,
                        start=start_time,
                        end=clip_end
                    )
                    
                    # Add asset to timeline
                    timeline.add_inline(video_asset)
                    
                    # Generate stream from timeline (this creates a proper playable URL)
                    timeline_stream_url = timeline.generate_stream()
                    
                    clip_data['timeline_url'] = timeline_stream_url
                    clip_data['stream_url'] = timeline_stream_url  # Use timeline URL as primary
                    clip_data['playable'] = True
                    clip_data['format'] = 'Timeline-based stream'
                    
                    st.success(f"✅ Timeline clip created for: {concept}")
                    
                except Exception as timeline_e:
                    st.warning(f"Timeline generation failed for {concept}: {timeline_e}")
                    
                    # Fallback to legacy generate_stream method
                    try:
                        legacy_stream = self.video.generate_stream(timeline=[(start_time, clip_end)])
                        clip_data['stream_url'] = legacy_stream
                        clip_data['format'] = 'Legacy HLS stream'
                        st.info(f"⚠️ Using legacy stream for: {concept}")
                    except Exception as legacy_e:
                        st.error(f"Both timeline and legacy stream failed for {concept}: {legacy_e}")

                # Method 2: Try to create direct download URL if possible
                try:
                    if hasattr(timeline, 'export'):
                        # Some versions support direct export
                        download_url = timeline.export(format='mp4')
                        clip_data['download_url'] = download_url
                        clip_data['download_format'] = 'MP4'
                        st.success(f"✅ MP4 download available for: {concept}")
                except Exception:
                    # Provide conversion instructions
                    clip_data['conversion_info'] = {
                        'method': 'timeline_based',
                        'status': 'Stream available - convert using tools below',
                        'tools': ['VLC Media Player', 'FFmpeg', 'Online converters']
                    }

                # Method 3: Add quality options
                try:
                    # Try different resolutions with Timeline
                    for resolution in ['720p', '480p', '360p']:
                        try:
                            quality_timeline = Timeline(self.client)
                            quality_asset = VideoAsset(
                                asset_id=self.video.id,
                                start=start_time,
                                end=clip_end
                            )
                            quality_timeline.add_inline(quality_asset)
                            quality_url = quality_timeline.generate_stream(resolution=resolution)
                            clip_data[f'stream_{resolution}'] = quality_url
                            clip_data['available_qualities'] = clip_data.get('available_qualities', []) + [resolution]
                        except:
                            continue
                except Exception:
                    pass

                # Add metadata for better handling
                clip_data['videodb_info'] = {
                    'type': 'Timeline-based clip',
                    'compatibility': 'Optimized for streaming and conversion',
                    'recommended_players': ['Browser (if supported)', 'VLC Media Player', 'Online HLS players'],
                    'download_options': ['Convert from stream', 'Use Timeline export (if available)']
                }
                
                clips.append(clip_data)
                
            except Exception as e:
                st.error(f"❌ Could not create clip for {concept}: {str(e)}")
                # Still add a basic entry with error info
                clips.append({
                    'concept': concept,
                    'start_time': start_time,
                    'end_time': clip_end,
                    'duration': clip_end - start_time,
                    'formatted_time': self._format_timestamp(start_time),
                    'error': str(e),
                    'playable': False
                })
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
