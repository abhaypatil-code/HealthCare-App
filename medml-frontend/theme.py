"""
Theme configuration for the Healthcare System
Light theme with blue and white color palette for trust, calm, and peace
"""

import streamlit as st

# Color Palette - Healthcare Light & Calm Theme
THEME_COLORS = {
    # Primary Colors (Trust & Brand)
    'primary': '#0067A5',         # Deep Cerulean
    'primary_dark': '#004F80',    # Darker shade for hover/active
    'primary_light': '#E6F0F6',   # Very light tint for backgrounds
    
    # Secondary Colors (Calm & Support)
    'secondary': '#A0D2EB',       # Light Sky Blue
    
    # Base & Text Colors (Cleanliness & Readability)
    'background': '#FFFFFF',      # Pure White (main background)
    'surface': '#F4F7F9',        # Off-white (for content sections)
    'text_primary': '#253B4A',    # Dark Slate Blue (for headings)
    'text_secondary': '#5A6D7A',  # Medium Gray (for body text)
    'border': '#DDE4E9',          # Light Gray (for borders/dividers)
    
    # Accent & Status Colors (Action & Information)
    'accent': '#007BFF',          # Active Blue (for buttons/links)
    'success': '#28A745',         # Reassuring Green (for Success)
    'warning': '#FFC107',         # Soft Yellow (for Warning)
    'error': '#DC3545',           # Clear Red (for Error/Urgent)
    
    # Additional colors for compatibility
    'primary_light': '#E6F0F6',   # Alias for primary_light
    'secondary_light': '#A0D2EB', # Alias for secondary
    'secondary_dark': '#004F80',  # Alias for primary_dark
    'surface_light': '#F4F7F9',  # Alias for surface
    'text_light': '#5A6D7A',     # Alias for text_secondary
    'success_light': '#28A745',   # Alias for success
    'warning_light': '#FFC107',  # Alias for warning
    'error_light': '#DC3545',    # Alias for error
    'info': '#007BFF',           # Alias for accent
    'info_light': '#007BFF',     # Alias for accent
    'border_light': '#DDE4E9',    # Alias for border
    'accent_light': '#007BFF',   # Alias for accent
}

def apply_light_theme():
    """Apply the enhanced light theme CSS to Streamlit with compact spacing and sticky header."""
    st.markdown(f"""
    <style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming - Healthcare Light & Calm */
    :root {{
        /* Primary Colors (Trust & Brand) */
        --color-primary: {THEME_COLORS['primary']};
        --color-primary-dark: {THEME_COLORS['primary_dark']};
        --color-primary-light: {THEME_COLORS['primary_light']};
        
        /* Secondary Colors (Calm & Support) */
        --color-secondary: {THEME_COLORS['secondary']};
        
        /* Base & Text Colors (Cleanliness & Readability) */
        --color-bg-white: {THEME_COLORS['background']};
        --color-bg-light-gray: {THEME_COLORS['surface']};
        --color-text-primary: {THEME_COLORS['text_primary']};
        --color-text-secondary: {THEME_COLORS['text_secondary']};
        --color-border: {THEME_COLORS['border']};
        
        /* Accent & Status Colors (Action & Information) */
        --color-accent-cta: {THEME_COLORS['accent']};
        --color-success: {THEME_COLORS['success']};
        --color-warning: {THEME_COLORS['warning']};
        --color-danger: {THEME_COLORS['error']};
        
        /* Legacy variable names for compatibility */
        --primary-color: {THEME_COLORS['primary']};
        --primary-light: {THEME_COLORS['primary_light']};
        --primary-dark: {THEME_COLORS['primary_dark']};
        --secondary-color: {THEME_COLORS['secondary']};
        --background-color: {THEME_COLORS['background']};
        --surface-color: {THEME_COLORS['surface']};
        --text-primary: {THEME_COLORS['text_primary']};
        --text-secondary: {THEME_COLORS['text_secondary']};
        --success-color: {THEME_COLORS['success']};
        --warning-color: {THEME_COLORS['warning']};
        --error-color: {THEME_COLORS['error']};
        --info-color: {THEME_COLORS['accent']};
        --border-color: {THEME_COLORS['border']};
    }}
    
    /* Global styles */
    .stApp {{
        background-color: var(--background-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary) !important;
    }}
    
    /* Ensure all text is visible */
    .stApp * {{
        color: inherit;
    }}
    
    /* COMPACT SPACING - Reduce excess padding and margins */
    .main .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1400px !important;
        color: var(--text-primary) !important;
    }}
    
    /* STICKY HEADER - Make Streamlit header sticky and compact */
    header[data-testid="stHeader"] {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999 !important;
        background-color: var(--background-color) !important;
        border-bottom: 1px solid var(--border-color) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        padding: 0.5rem 1rem !important;
        height: auto !important;
    }}
    
    /* Adjust main content to account for sticky header */
    .main .block-container {{
        padding-top: 4rem !important;
    }}
    
    /* Compact spacing for all Streamlit components */
    .stExpander, .stContainer, .stMarkdown, .stMetric, .stDataFrame, 
    .stButton, .stForm, .stColumns, .stTabs, .stAlert, .stSubheader, 
    .stTitle, .stInfo, .stWarning, .stSuccess, .stError, .stCaption {{
        margin-bottom: 0.5rem !important;
    }}
    
    .element-container {{
        margin-bottom: 0.75rem !important;
    }}
    
    /* Compact divider spacing */
    hr {{
        margin: 0.75rem 0 !important;
    }}
    
    /* Reduce spacing in metric cards */
    .metric-card {{
        margin-bottom: 0.75rem !important;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-weight: 600;
        margin-bottom: 0.75rem !important;
    }}
    
    /* Ensure all text elements are visible - consolidated rules */
    p, span, div, label, .stMarkdown, .stMarkdown p, .stText,
    .stSelectbox label, .stTextInput label, .stTextArea label,
    .stNumberInput label, .stDateInput label, .stTimeInput label,
    .stCheckbox label, .stRadio label, .stMultiselect label,
    .stWidget label, .element-container {{
        color: var(--text-primary) !important;
    }}
    
    .element-container * {{
        color: inherit !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }}
    
    /* Button styling - consolidated */
    .stButton > button {{
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        background-color: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }}
    
    .stButton > button[kind="secondary"] {{
        background-color: var(--surface-color);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }}
    
    /* Form elements - consolidated */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        border: 1px solid var(--border-color);
        border-radius: 8px;
        background-color: var(--background-color);
        color: var(--text-primary);
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }}
    
    /* Metric cards */
    .metric-card {{
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}
    
    /* Risk level indicators */
    .risk-high {{
        background-color: var(--error-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    .risk-medium {{
        background-color: var(--warning-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    .risk-low {{
        background-color: var(--success-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    /* Alert boxes - consolidated */
    .stAlert {{
        border-radius: 8px;
        border: none;
    }}
    
    .stAlert[data-testid="alert-success"] {{
        background-color: var(--success-color);
        color: white;
    }}
    
    .stAlert[data-testid="alert-warning"] {{
        background-color: var(--warning-color);
        color: white;
    }}
    
    .stAlert[data-testid="alert-error"] {{
        background-color: var(--error-color);
        color: white;
    }}
    
    .stAlert[data-testid="alert-info"] {{
        background-color: var(--info-color);
        color: white;
    }}
    
    /* Data tables */
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }}
    
    /* Navigation bar */
    .navbar {{
        background-color: var(--surface-color);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 0;
        margin-bottom: 2rem;
    }}
    
    .navbar-brand {{
        color: var(--primary-color);
        font-size: 1.5rem;
        font-weight: 700;
        text-decoration: none;
    }}
    
    .navbar-nav {{
        display: flex;
        gap: 2rem;
        align-items: center;
    }}
    
    .navbar-nav a {{
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    
    .navbar-nav a:hover {{
        color: var(--primary-color);
    }}
    
    /* Cards */
    .card {{
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--surface-color);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary-color);
    }}
    </style>
    """, unsafe_allow_html=True)

def create_navbar(user_name, user_role):
    """Create a top navigation bar for authenticated users."""
    st.markdown(f"""
    <div class="navbar">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div class="navbar-brand">
                🩺 HealthCare System
            </div>
            <div class="navbar-nav">
                <span style="color: var(--text-secondary); font-weight: 500;">{user_name}</span>
                <span style="color: var(--text-light); font-size: 0.875rem; background: var(--primary-color); color: white; padding: 0.25rem 0.75rem; border-radius: 12px;">{user_role.title()}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, help_text=None, color="primary"):
    """Create a styled metric card."""
    color_class = f"color: var(--{color}-color);" if color in ['primary', 'success', 'warning', 'error', 'info'] else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; color: var(--text-secondary); font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{label}</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0 0; {color_class}">{value}</p>
                {f'<p style="font-size: 0.875rem; color: var(--text-light); margin: 0.25rem 0 0 0;">{help_text}</p>' if help_text else ""}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_risk_badge(level):
    """Create a styled risk level badge."""
    level_lower = level.lower()
    if level_lower == "high":
        return f'<span class="risk-high">🚨 {level.upper()}</span>'
    elif level_lower == "medium":
        return f'<span class="risk-medium">⚠️ {level.upper()}</span>'
    elif level_lower == "low":
        return f'<span class="risk-low">✅ {level.upper()}</span>'
    else:
        return f'<span style="background-color: var(--secondary-color); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.875rem;">{level.upper()}</span>'
