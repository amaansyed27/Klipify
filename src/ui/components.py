"""
UI Components for Klipify
Contains all UI elements including CSS, headers, and layouts.
"""

import streamlit as st
import os
import base64


def load_css():
    """Load basic CSS for the application."""
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def get_logo_path():
    """Get the path to the logo image."""
    # Try to find logo in assets folder
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logo_path = os.path.join(current_dir, "assets", "logo.png")
    
    # If logo exists, return the path, otherwise return None
    if os.path.exists(logo_path):
        return logo_path
    return None


def get_base64_image(image_path):
    """Convert image to base64 for embedding."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_simple_header():
    """Create a simple header using Streamlit native components."""
    # Use Streamlit's native components instead of HTML
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Simple logo using emoji
        st.markdown(
            "<div style='text-align: center; font-size: 4rem; margin: 1rem 0;'>🎬</div>",
            unsafe_allow_html=True
        )
        
        # Title and subtitle using Streamlit
        st.markdown(
            "<h1 style='text-align: center; color: #667eea; font-size: 3rem; margin: 0;'>Klipify</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>Transform any YouTube video into a comprehensive learning experience</p>",
            unsafe_allow_html=True
        )


def create_header():
    """Create the main Klipify header using native Streamlit components."""
    # Use the simplified header approach
    create_simple_header()


def create_feature_showcase():
    """Create the feature showcase using native Streamlit components."""
    st.markdown("### ✨ Key Features")
    
    # Create feature cards using Streamlit columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎬 Smart Video Clips")
        st.write("AI-powered extraction of educational segments, automatically creating bite-sized learning clips focused on key concepts.")
        
        st.markdown("#### 📝 Timestamped Notes")
        st.write("Detailed study notes with precise timestamps, structured sections, and key takeaways for efficient learning.")
    
    with col2:
        st.markdown("#### 📋 Intelligent Summary")
        st.write("Comprehensive video analysis with learning objectives, main topics, target audience, and difficulty assessment.")
        
        st.markdown("#### 💬 AI Study Assistant")
        st.write("Interactive AI tutor grounded in video content for personalized learning support and Q&A sessions.")
    
    st.markdown("---")


def show_error_message(title, message, help_text=None):
    """Display a formatted error message."""
    st.error(f"🔑 **{title}**")
    if help_text:
        st.markdown(f"""
        <div class="feature-card">
            <h4>🛠️ {message}</h4>
            {help_text}
        </div>
        """, unsafe_allow_html=True)


def show_success_message(message):
    """Display a formatted success message."""
    st.success(f"✅ {message}")


def show_info_message(message):
    """Display a formatted info message."""
    st.info(f"ℹ️ {message}")


def show_warning_message(message):
    """Display a formatted warning message."""
    st.warning(f"⚠️ {message}")
