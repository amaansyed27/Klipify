"""
Main components module for Klipify UI.
Re-exports all components for easy importing.
"""

# Import styles
from ..styles.main_styles import load_modern_css

# Import components from the new modular structure
from .landing_page import create_landing_page, show_quick_start_guide
from .navigation import create_sidebar_navigation, show_sidebar_metrics
from .clips_page import show_clips_page
from .summary_page import show_summary_page
from .notes_page import show_notes_page
from .chat_page import show_chat_page, handle_chat_message, add_quick_question
from .video_management import show_my_videos_page

# Re-export everything for backward compatibility
__all__ = [
    'load_modern_css',
    'create_landing_page',
    'show_quick_start_guide', 
    'create_sidebar_navigation',
    'show_sidebar_metrics',
    'show_clips_page',
    'show_summary_page', 
    'show_notes_page',
    'show_chat_page',
    'handle_chat_message',
    'add_quick_question',
    'show_my_videos_page'
]
