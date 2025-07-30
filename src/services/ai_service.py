"""
AI Service for Klipify
Handles all AI operations including summary generation, concept extraction, and chat.
"""

import streamlit as st
from google import genai


class AIService:
    """Handles AI operations using Google GenAI."""
    
    def __init__(self, client):
        """Initialize with GenAI client."""
        self.client = client
        self.model_name = "gemini-2.5-flash"
    
    def generate_video_summary(self, transcript_text):
        """
        Generate a comprehensive summary of the video.
        
        Args:
            transcript_text (str): Full video transcript
            
        Returns:
            str: Formatted video summary
        """
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
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def extract_key_concepts(self, transcript_text):
        """
        Extract key concepts from the video transcript.
        
        Args:
            transcript_text (str): Full video transcript
            
        Returns:
            list: List of key concepts (6-8 items)
        """
        prompt = f"""
        Analyze this educational video transcript and identify 6-8 key concepts that students should focus on.
        
        Each concept should be:
        - A clear, specific topic (2-6 words)
        - Educationally valuable
        - Searchable within the video
        
        Return as a simple list, one concept per line.
        
        Transcript: {transcript_text}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            concepts = [concept.strip() for concept in response.text.strip().split('\n') if concept.strip()]
            return concepts[:8]  # Limit to 8 concepts
            
        except Exception as e:
            raise Exception(f"Failed to extract concepts: {str(e)}")
    
    def generate_timestamped_notes(self, transcript_segments, youtube_id=None):
        """
        Generate detailed timestamped notes from transcript segments.
        
        Args:
            transcript_segments (list): List of transcript segments with timestamps
            youtube_id (str, optional): YouTube video ID for creating clickable links
            
        Returns:
            str: Formatted timestamped notes with clickable links
        """
        # Prepare transcript with timestamps for analysis
        timestamped_content = ""
        for segment in transcript_segments:
            start_time = self._format_timestamp(segment.get('start', 0))
            text = segment.get('text', '')
            timestamped_content += f"[{start_time}] {text}\n"
        
        prompt = f"""
        You are an expert note-taker. Analyze this timestamped video transcript and create comprehensive study notes.
        
        Create structured notes with:
        1. Major sections/topics (with time ranges)
        2. Key concepts and definitions
        3. Important examples or explanations
        4. Action items or takeaways
        
        Format as markdown with clear headings and bullet points. 
        For each major section, include the timestamp in format [MM:SS] at the beginning.
        Make the content educational and easy to study from.
        
        Timestamped transcript:
        {timestamped_content}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Post-process to add clickable YouTube links if video ID is provided
            notes = response.text
            if youtube_id:
                notes = self._add_youtube_links_to_notes(notes, youtube_id)
            
            return notes
            
        except Exception as e:
            raise Exception(f"Failed to generate notes: {str(e)}")
    
    def _add_youtube_links_to_notes(self, notes, youtube_id):
        """
        Add clickable YouTube links to timestamp references in notes.
        
        Args:
            notes (str): Original notes with timestamps
            youtube_id (str): YouTube video ID
            
        Returns:
            str: Notes with clickable timestamp links
        """
        import re
        
        # Pattern to match timestamps like [12:34] or [01:23]
        timestamp_pattern = r'\[(\d{1,2}:\d{2})\]'
        
        def replace_timestamp(match):
            timestamp_str = match.group(1)
            # Convert MM:SS to seconds
            parts = timestamp_str.split(':')
            seconds = int(parts[0]) * 60 + int(parts[1])
            
            # Create YouTube link with timestamp
            youtube_link = f"https://www.youtube.com/watch?v={youtube_id}&t={seconds}s"
            
            # Return markdown link
            return f"[🔗 {timestamp_str}]({youtube_link})"
        
        # Replace all timestamps with clickable links
        enhanced_notes = re.sub(timestamp_pattern, replace_timestamp, notes)
        
        # Add a note about the clickable timestamps
        header = "📝 **Study Notes with Clickable Timestamps**\n\n"
        header += "💡 *Click on any timestamp [🔗 MM:SS] to jump to that moment in the video*\n\n"
        
        return header + enhanced_notes
    
    def chat_with_assistant(self, user_message, video_context, chat_history):
        """
        Handle chat with the AI assistant using video context.
        
        Args:
            user_message (str): User's question
            video_context (dict): Video context including transcript and summary
            chat_history (list): Previous chat messages
            
        Returns:
            str: AI assistant response
        """
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
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=context_prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate chat response: {str(e)}")
    
    @staticmethod
    def _format_timestamp(seconds):
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"


def initialize_genai_client():
    """
    Initialize Google GenAI client from API keys using the new API.
    
    Returns:
        GenAI client or None if initialization fails
    """
    try:
        # Try to get API key from various sources
        api_key = None
        
        # Try Streamlit secrets first
        if hasattr(st, 'secrets'):
            api_key = (st.secrets.get("GEMINI_API_KEY") or 
                      st.secrets.get("GOOGLE_API_KEY") or 
                      st.secrets.get("gemini_api_key") or 
                      st.secrets.get("google_api_key"))
        
        # Try environment variables
        if not api_key:
            import os
            api_key = (os.getenv("GEMINI_API_KEY") or 
                      os.getenv("GOOGLE_API_KEY"))
        
        if not api_key:
            return None
        
        # Set the API key as environment variable for the new client
        import os
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # Initialize client using new API format - no configure needed
        return genai.Client()
        
    except Exception as e:
        st.error(f"Failed to initialize GenAI client: {str(e)}")
        return None
