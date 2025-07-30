"""
VideoDB Video Management Service
Handles listing, managing, and deleting videos from VideoDB
"""

import streamlit as st
from videodb import connect
import requests


class VideoDBManager:
    """Manages VideoDB videos for the user."""
    
    def __init__(self):
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Connect to VideoDB using stored credentials."""
        try:
            api_key = st.secrets.get("VIDEODB_API_KEY")
            if api_key:
                self.conn = connect(api_key=api_key)
                return True
        except Exception as e:
            st.error(f"Failed to connect to VideoDB: {e}")
        return False
    
    def list_videos(self):
        """List all videos in the user's VideoDB account."""
        if not self.conn:
            return []
        
        try:
            # Get collection (assuming default collection)
            collection = self.conn.get_collection()
            videos = collection.get_videos()
            
            video_list = []
            for video in videos:
                video_info = {
                    'id': video.id,
                    'name': video.name or 'Untitled',
                    'description': getattr(video, 'description', '') or '',
                    'length': getattr(video, 'length', 0),
                    'upload_date': getattr(video, 'created_at', 'Unknown'),
                    'status': getattr(video, 'status', 'Unknown'),
                    'thumbnail': getattr(video, 'thumbnail_url', ''),
                    'stream_url': getattr(video, 'stream_url', ''),
                }
                video_list.append(video_info)
            
            return video_list
        except Exception as e:
            st.error(f"Error listing videos: {e}")
            return []
    
    def delete_video(self, video_id):
        """Delete a video from VideoDB."""
        if not self.conn:
            return False
        
        try:
            collection = self.conn.get_collection()
            video = collection.get_video(video_id)
            video.delete()
            return True
        except Exception as e:
            st.error(f"Error deleting video: {e}")
            return False
    
    def get_video_details(self, video_id):
        """Get detailed information about a specific video."""
        if not self.conn:
            return None
        
        try:
            collection = self.conn.get_collection()
            video = collection.get_video(video_id)
            
            # Get video details including clips if any
            details = {
                'id': video.id,
                'name': video.name or 'Untitled',
                'description': getattr(video, 'description', '') or '',
                'length': getattr(video, 'length', 0),
                'upload_date': getattr(video, 'created_at', 'Unknown'),
                'status': getattr(video, 'status', 'Unknown'),
                'thumbnail': getattr(video, 'thumbnail_url', ''),
                'stream_url': getattr(video, 'stream_url', ''),
                'file_size': getattr(video, 'file_size', 0),
                'format': getattr(video, 'format', 'Unknown'),
            }
            
            return details
        except Exception as e:
            st.error(f"Error getting video details: {e}")
            return None
    
    def generate_clips_from_existing(self, video_id, concepts=None):
        """Generate clips from an existing VideoDB video."""
        if not self.conn:
            return None
        
        try:
            from ..services.video_service import VideoService
            
            # Get the video
            collection = self.conn.get_collection()
            video = collection.get_video(video_id)
            
            # Create VideoService instance and generate clips
            video_service = VideoService()
            
            # Generate clips using the same logic as new uploads
            clips_data = video_service.generate_clips_from_video(video, concepts)
            
            return clips_data
        except Exception as e:
            st.error(f"Error generating clips from existing video: {e}")
            return None
    
    def format_duration(self, seconds):
        """Format duration in seconds to human readable format."""
        if not seconds:
            return "Unknown"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def format_file_size(self, bytes_size):
        """Format file size in bytes to human readable format."""
        if not bytes_size:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"


# Global instance
video_db_manager = VideoDBManager()
