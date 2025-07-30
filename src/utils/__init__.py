"""
Utilities Package for Klipify v2.0
Contains helper functions, session management, and video format handling.
"""

from .helpers import (
    get_youtube_id,
    validate_youtube_url,
    initialize_chat_session,
    format_timestamp,
    validate_api_keys,
    reset_session_state,
    create_youtube_link,
    create_setup_instructions
)

from .video_utils import (
    VideoFormatHandler,
    check_video_compatibility,
    create_video_info_card
)

__all__ = [
    # Original helpers
    'get_youtube_id',
    'validate_youtube_url', 
    'initialize_chat_session',
    'format_timestamp',
    'validate_api_keys',
    'reset_session_state',
    'create_youtube_link',
    'create_setup_instructions',
    
    # Video utilities
    'VideoFormatHandler',
    'check_video_compatibility',
    'create_video_info_card'
]
