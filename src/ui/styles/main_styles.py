"""
Main CSS styles for Klipify UI components.
"""

import streamlit as st

def load_modern_css():
    """Load professional CSS styling for the new UI."""
    st.markdown("""
    <style>
    /* Preserve Streamlit toolbar and core functionality */
    .stToolbar {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    
    .stDeployButton {
        display: block !important;
        visibility: visible !important;
    }
    
    header[data-testid="stHeader"] {
        display: block !important;
        visibility: visible !important;
        height: auto !important;
        background: transparent !important;
    }
    
    /* Global styling */
    .main > div {
        padding-top: 0.5rem;
    }
    
    /* Professional color palette */
    :root {
        --primary-blue: #2563eb;
        --secondary-blue: #1e40af;
        --dark-bg: #1f2937;
        --darker-bg: #111827;
        --surface-bg: #1f2937;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --border-color: #374151;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --error-red: #ef4444;
        --accent-blue: #3b82f6;
    }
    
    /* Landing page hero section - reduced padding */
    .hero-section {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        text-align: center;
        color: white;
        margin: 0.5rem 0 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        margin-bottom: 1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Quick action buttons */
    .quick-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .quick-action-btn {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.5rem 1rem;
        text-decoration: none;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .quick-action-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        color: white;
        text-decoration: none;
    }
    
    /* Sidebar navigation styling */
    .nav-sidebar {
        background: var(--dark-bg);
        border: 1px solid var(--border-color);
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .nav-item {
        background: var(--darker-bg);
        border: 1px solid var(--border-color);
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        color: var(--text-primary);
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
    }
    
    .nav-item:hover {
        background: var(--primary-blue);
        border-color: var(--primary-blue);
    }
    
    .nav-item.active {
        background: var(--primary-blue);
        border-color: var(--secondary-blue);
    }
    
    /* Professional clip cards */
    .clip-card {
        background: var(--dark-bg);
        border: 1px solid var(--border-color);
        padding: 1.25rem;
        margin: 1rem 0;
        transition: border-color 0.2s ease;
    }
    
    .clip-card:hover {
        border-color: var(--primary-blue);
    }
    
    .clip-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .clip-meta {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-bottom: 1rem;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 0.5rem;
        border-radius: 50%;
    }
    
    .status-success { background-color: var(--success-green); }
    .status-warning { background-color: var(--warning-orange); }
    .status-error { background-color: var(--error-red); }
    
    /* Metrics styling */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: var(--dark-bg);
        border: 1px solid var(--border-color);
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        display: block;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    /* Professional radio button styling */
    .stRadio > div {
        background: transparent;
    }
    
    .stRadio > div > label {
        color: var(--text-primary) !important;
        font-weight: 500;
        padding: 0.5rem 0;
        border-bottom: 1px solid transparent;
        transition: all 0.2s ease;
        display: block;
    }
    
    .stRadio > div > label:hover {
        color: var(--primary-blue) !important;
        border-bottom-color: var(--border-color);
    }
    
    .stRadio > div > label[data-checked="true"] {
        color: var(--primary-blue) !important;
        font-weight: 600;
        border-bottom-color: var(--primary-blue);
    }
    
    /* Professional buttons */
    .pro-button {
        background: var(--primary-blue);
        color: white;
        border: 1px solid var(--primary-blue);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        text-align: center;
    }
    
    .pro-button:hover {
        background: var(--secondary-blue);
        border-color: var(--secondary-blue);
    }
    
    .pro-button.secondary {
        background: transparent;
        color: var(--primary-blue);
        border-color: var(--primary-blue);
    }
    
    .pro-button.secondary:hover {
        background: var(--primary-blue);
        color: white;
    }
    
    /* Page styling */
    .page-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .page-header h2 {
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
        font-weight: 600;
        font-size: 1.75rem;
    }
    
    .page-subtitle {
        color: var(--text-secondary);
        margin: 0;
        font-size: 1rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        margin: 2rem 0;
    }
    
    .empty-state h3 {
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .empty-state p {
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .metrics-container { grid-template-columns: repeat(2, 1fr); }
        .quick-actions { 
            flex-direction: column; 
            align-items: center;
        }
        .quick-action-btn {
            width: 200px;
            text-align: center;
        }
    }
    
    /* Input and button styling */
    .stTextInput > div > div > input {
        border: 1px solid var(--border-color);
        background: var(--dark-bg);
        color: var(--text-primary);
        padding: 0.75rem;
        font-size: 0.875rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue);
        outline: none;
    }
    
    .stButton > button {
        border: 1px solid var(--border-color);
        background: var(--primary-blue);
        color: white;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--secondary-blue);
        border-color: var(--secondary-blue);
    }
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Professional sidebar */
    .css-1d391kg {
        background-color: var(--darker-bg);
        border-right: 1px solid var(--border-color);
    }
    
    /* Professional main area */
    .css-18e3th9 {
        background-color: var(--darker-bg);
    }
    
    </style>
    """, unsafe_allow_html=True)
