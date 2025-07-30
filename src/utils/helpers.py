"""
Utility functions for Klipify
Contains helper functions for URL parsing, session management, and common operations.
"""

import re
import streamlit as st


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


def validate_youtube_url(url):
    """
    Validate if the provided URL is a valid YouTube URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple: (is_valid, youtube_id_or_error_message)
    """
    if not url or not url.strip():
        return False, "Please provide a YouTube URL"
    
    youtube_id = get_youtube_id(url.strip())
    if not youtube_id:
        return False, "Invalid YouTube URL format. Please check the URL and try again."
    
    return True, youtube_id


def initialize_chat_session():
    """Initialize the chat session state."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'video_context' not in st.session_state:
        st.session_state.video_context = None


def reset_session_state():
    """Reset all session state variables."""
    keys_to_reset = [
        'chat_history', 
        'video_context', 
        'video_data', 
        'processing_complete'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]


def format_timestamp(seconds):
    """
    Convert seconds to MM:SS format.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted timestamp (MM:SS)
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def format_duration(seconds):
    """
    Convert seconds to human-readable duration.
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def validate_api_keys():
    """
    Check if required API keys are configured.
    
    Returns:
        tuple: (videodb_key_exists, genai_key_exists)
    """
    import os
    
    # Check VideoDB API key
    videodb_key = (
        st.secrets.get("VIDEODB_API_KEY") or 
        st.secrets.get("videodb_api_key") or 
        os.getenv("VIDEODB_API_KEY")
    )
    
    # Check GenAI API key
    genai_key = (
        st.secrets.get("GEMINI_API_KEY") or 
        st.secrets.get("GOOGLE_API_KEY") or 
        st.secrets.get("gemini_api_key") or 
        st.secrets.get("google_api_key") or 
        os.getenv("GEMINI_API_KEY") or 
        os.getenv("GOOGLE_API_KEY")
    )
    
    return bool(videodb_key), bool(genai_key)


def create_setup_instructions():
    """
    Create HTML for API setup instructions.
    
    Returns:
        str: HTML content for setup instructions
    """
    return """
    <ol>
        <li><strong>VideoDB API Key</strong>: Get your free key from <a href="https://console.videodb.io/" target="_blank">VideoDB Console</a></li>
        <li><strong>Gemini API Key</strong>: Get your key from <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a></li>
        <li><strong>Configuration Options:</strong>
            <ul>
                <li>Add keys to <code>.streamlit/secrets.toml</code> file</li>
                <li>Set as environment variables (VIDEODB_API_KEY, GEMINI_API_KEY)</li>
                <li>Use Streamlit Cloud secrets (for deployment)</li>
            </ul>
        </li>
    </ol>
    """


def get_app_info():
    """
    Get application information and metadata.
    
    Returns:
        dict: Application metadata
    """
    return {
        'name': 'Klipify',
        'version': '2.0.0',
        'description': 'AI-Powered Educational Video Platform',
        'author': 'Klipify Team',
        'features': [
            'Smart Video Clips',
            'AI-Generated Summaries',
            'Timestamped Notes',
            'Interactive AI Assistant'
        ]
    }


def sanitize_filename(filename):
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename.strip()


def create_youtube_link(video_id, timestamp=None):
    """
    Create a YouTube link with optional timestamp.
    
    Args:
        video_id (str): YouTube video ID
        timestamp (float, optional): Start time in seconds
        
    Returns:
        str: YouTube URL
    """
    base_url = f"https://www.youtube.com/watch?v={video_id}"
    
    if timestamp:
        base_url += f"&t={int(timestamp)}s"
    
    return base_url


def truncate_text(text, max_length=100, suffix="..."):
    """
    Truncate text to specified length.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add when truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
