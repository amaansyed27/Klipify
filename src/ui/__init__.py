"""
UI Components Package
Contains all user interface elements and styling.
"""

# Import from the old components.py file directly (avoiding circular imports)
from .components import load_css, create_header, create_feature_showcase
from .displays import display_content_tabs, display_sidebar_input

# Also re-export the new modular components
from .ui_components import (
    load_modern_css, 
    create_landing_page, 
    create_sidebar_navigation,
    show_clips_page,
    show_summary_page, 
    show_notes_page,
    show_chat_page,
    show_my_videos_page
)

__all__ = [
    # Legacy components (for klipify_main.py)
    'load_css',
    'create_header', 
    'create_feature_showcase',
    'display_content_tabs',
    'display_sidebar_input',
    # New modular components (for klipify_new_ui.py)
    'load_modern_css',
    'create_landing_page',
    'create_sidebar_navigation',
    'show_clips_page',
    'show_summary_page',
    'show_notes_page',
    'show_chat_page',
    'show_my_videos_page'
]
