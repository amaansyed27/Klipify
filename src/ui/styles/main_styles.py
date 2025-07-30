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
    
    /* Global styling - minimal padding */
    .main > div {
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    
    /* Reduce space between elements */
    .element-container {
        margin-bottom: 0.25rem !important;
    }
    
    /* Remove default Streamlit container padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
    
    /* Professional color palette */
    :root {
        --primary-blue: #2563eb;
        --primary-blue-light: #dbeafe;
        --primary-blue-dark: #1d4ed8;
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
    
    /* Landing page hero section - ultra minimal padding */
    .hero-section {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 1rem 1rem 0.75rem 1rem;
        text-align: center;
        color: white;
        margin: 0 0 0.5rem 0;
        border: 1px solid var(--border-color);
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        margin-bottom: 0.5rem;
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
    
    /* Modern Sidebar Navigation Styling */
    
    /* Reduce overall sidebar padding */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: var(--darker-bg) !important;
        border-right: 1px solid var(--border-color) !important;
        padding-top: 1rem !important;
    }
    
    /* Reduce sidebar content padding */
    .css-1d391kg .css-1cypcdb, [data-testid="stSidebar"] .css-1cypcdb {
        padding: 0.5rem 1rem !important;
    }
    
    /* Modern navigation container */
    .nav-sidebar {
        background: linear-gradient(145deg, var(--dark-bg), var(--darker-bg));
        border: 1px solid var(--border-color);
        padding: 0.75rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
    }
    
    /* Modern navigation title */
    .nav-title {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        text-align: center;
        background: linear-gradient(90deg, var(--primary-blue), var(--accent-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Modern navigation items */
    .nav-item {
        background: linear-gradient(145deg, var(--surface-bg), var(--darker-bg));
        border: 1px solid var(--border-color);
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
        color: var(--text-primary);
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        text-align: left;
        border-radius: 12px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    /* Add subtle gradient overlay on hover */
    .nav-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-blue));
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }
    
    .nav-item:hover::before {
        opacity: 0.1;
    }
    
    .nav-item:hover {
        background: var(--primary-blue);
        border-color: var(--accent-blue);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        color: white;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-blue));
        border-color: var(--accent-blue);
        font-weight: 600;
        color: white;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    }
    
    .nav-item.active::before {
        opacity: 0;
    }
    
    .nav-item:last-child {
        margin-bottom: 0;
    }
    
    /* Modern sidebar sections */
    .sidebar-section {
        background: linear-gradient(145deg, var(--surface-bg), var(--darker-bg));
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-section h3 {
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.3rem;
    }
    
    /* Style radio buttons to match the nav design */
    .stRadio > div {
        gap: 0.3rem !important;
    }
    
    .stRadio > div > label {
        background: linear-gradient(145deg, var(--surface-bg), var(--darker-bg)) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        margin-bottom: 0.3rem !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .stRadio > div > label:hover {
        background: var(--primary-blue) !important;
        border-color: var(--accent-blue) !important;
        color: white !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-blue)) !important;
        border-color: var(--accent-blue) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Hide default radio button circles */
    .stRadio > div > label > div:first-child {
        display: none !important;
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
        width: 100%;
        box-sizing: border-box; /* Ensures padding and border are included in the width */
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
        width: 100%;
        box-sizing: border-box; /* Ensures padding and border are included in the width */
        border: 1px solid var(--border-color);
        background: var(--primary-blue);
        color: white;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    /* Modern quick action buttons */
    .stButton > button {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, var(--primary-blue), var(--accent-blue)) !important;
        border-color: var(--accent-blue) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* Remove default Streamlit styling - but preserve toolbar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} - Commented out to preserve toolbar */
    /* .stDeployButton {display: none;} - Commented out to preserve deploy button */
    
    /* Professional sidebar with reduced padding */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: var(--darker-bg) !important;
        border-right: 1px solid var(--border-color) !important;
        padding-top: 0.5rem !important;
        min-width: 280px !important;
        max-width: 320px !important;
    }
    
    /* Professional main area with reduced padding */
    .css-18e3th9, [data-testid="stAppViewContainer"] .main {
        background-color: var(--darker-bg) !important;
        padding: 0.5rem !important;
    }
    
    /* Modern scrollbar for sidebar */
    .css-1d391kg::-webkit-scrollbar {
        width: 6px;
    }
    
    .css-1d391kg::-webkit-scrollbar-track {
        background: var(--darker-bg);
    }
    
    .css-1d391kg::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 3px;
    }
    
    .css-1d391kg::-webkit-scrollbar-thumb:hover {
        background: var(--primary-blue);
    }
    
    /* Notes page specific styling */
    .section-header {
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-blue);
    }
    
    .section-header h3 {
        color: var(--text-primary);
        margin: 0;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .notes-content {
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    .search-results-info {
        background: var(--primary-blue-light);
        border: 1px solid var(--primary-blue);
        border-radius: 6px;
        padding: 0.75rem;
        margin: 1rem 0;
        color: var(--primary-blue);
        font-weight: 500;
    }
    
    .search-no-results {
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--text-secondary);
        text-align: center;
    }
    
    .transcript-segment {
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin: 1rem 0;
        padding: 1rem;
        transition: all 0.2s ease;
    }
    
    .transcript-segment:hover {
        border-color: var(--primary-blue);
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
    }
    
    .segment-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .segment-time {
        font-family: 'Courier New', monospace;
        font-weight: 600;
        color: var(--primary-blue);
        background: var(--primary-blue-light);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
    }
    
    .time-link {
        color: var(--primary-blue) !important;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.875rem;
        transition: color 0.2s ease;
    }
    
    .time-link:hover {
        color: var(--primary-blue-dark) !important;
        text-decoration: underline;
    }
    
    .segment-text {
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    </style>
    """, unsafe_allow_html=True)
