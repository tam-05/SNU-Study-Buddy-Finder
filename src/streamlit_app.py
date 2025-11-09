import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Study Buddy Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Black & White Theme CSS with Poppins Font
st.markdown("""
<style>
    /* CSS Version 2.0 - Dark Mode Fix */
    /* Import Google Fonts - Poppins */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    
    .stMarkdown, p, span, div {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Warm Neutral Color Palette - Eye-Friendly */
    /* Primary: #3E2723 (Dark Brown), #4E342E (Medium Brown), #5D4037 (Warm Brown) */
    /* Secondary: #FFF8E1 (Warm Cream), #FFECB3 (Light Beige), #FFE0B2 (Soft Peach) */
    /* Accent: #6D4C41 (Soft Brown), #8D6E63 (Medium Brown), #A1887F (Light Brown) */
    /* Text: #3E2723 (Dark Brown), #5D4037 (Medium Brown Text) */
    /* Backgrounds: #FFF9F0 (Soft Cream), #FFF5E6 (Warm White) */
    
    /* Hide Streamlit footer only */
    footer {visibility: hidden;}
    
    /* DARK THEME SUPPORT - Streamlit adds stApp class */
    /* When Streamlit is in dark mode, override all light colors */
    
    /* Main containers in dark mode */
    .stApp[data-theme="dark"] .main,
    .stApp[class*="dark"] .main,
    body[class*="dark"] .main {
        background: #0E1117 !important;
    }
    
    .stApp[data-theme="dark"] .block-container,
    .stApp[class*="dark"] .block-container,
    body[class*="dark"] .block-container {
        background: #0E1117 !important;
    }
    
    /* Section cards in dark mode */
    .stApp[data-theme="dark"] .section-card,
    .stApp[class*="dark"] .section-card,
    body[class*="dark"] .section-card {
        background: #262730 !important;
        border-color: #464852 !important;
        color: #FAFAFA !important;
    }
    
    /* Metric cards in dark mode */
    .stApp[data-theme="dark"] .metric-card,
    .stApp[class*="dark"] .metric-card,
    body[class*="dark"] .metric-card {
        background: #1E1E1E !important;
        border-color: #464852 !important;
    }
    
    .stApp[data-theme="dark"] .metric-label,
    .stApp[class*="dark"] .metric-label,
    body[class*="dark"] .metric-label {
        color: #B0B0B0 !important;
    }
    
    .stApp[data-theme="dark"] .metric-value,
    .stApp[class*="dark"] .metric-value,
    body[class*="dark"] .metric-value {
        color: #FAFAFA !important;
    }
    
    /* Buddy cards in dark mode */
    .stApp[data-theme="dark"] .buddy-card,
    .stApp[class*="dark"] .buddy-card,
    body[class*="dark"] .buddy-card {
        background: #262730 !important;
        border-color: #464852 !important;
    }
    
    /* Stat boxes in dark mode */
    .stApp[data-theme="dark"] .stat-box,
    .stApp[class*="dark"] .stat-box,
    body[class*="dark"] .stat-box {
        background: linear-gradient(135deg, #262730 0%, #2D2D3A 100%) !important;
        border-color: #464852 !important;
        color: #FAFAFA !important;
    }
    
    .stApp[data-theme="dark"] .stat-label,
    .stApp[class*="dark"] .stat-label,
    body[class*="dark"] .stat-label {
        color: #CCCCCC !important;
    }
    
    .stApp[data-theme="dark"] .stat-number,
    .stApp[class*="dark"] .stat-number,
    body[class*="dark"] .stat-number {
        color: #FAFAFA !important;
    }
    
    /* Section headers in dark mode */
    .stApp[data-theme="dark"] .section-header,
    .stApp[class*="dark"] .section-header,
    body[class*="dark"] .section-header {
        color: #FAFAFA !important;
        border-bottom-color: #8D6E63 !important;
    }
    
    /* Profile elements in dark mode */
    .stApp[data-theme="dark"] .profile-id,
    .stApp[class*="dark"] .profile-id,
    body[class*="dark"] .profile-id {
        color: #FAFAFA !important;
    }
    
    /* All h4 elements in dark mode */
    .stApp[data-theme="dark"] h4,
    .stApp[class*="dark"] h4,
    body[class*="dark"] h4 {
        color: #FAFAFA !important;
    }
    
    /* All paragraph text in section cards */
    .stApp[data-theme="dark"] .section-card p,
    .stApp[class*="dark"] .section-card p,
    body[class*="dark"] .section-card p {
        color: #FAFAFA !important;
    }
    
    /* Main container - Warm cream background */
    .main {
        background: #FFF9F0;
        padding: 0;
    }
    
    .block-container {
        background: #FFF9F0;
        padding: 3rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    /* Header Section - Warm Brown Gradient */
    .app-header {
        background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%);
        color: #FFF8E1;
        padding: 2.5rem 2rem;
        margin: -3rem -2rem 2.5rem -2rem;
        border-bottom: 4px solid #A1887F;
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.3);
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: white;
        text-align: center;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
        font-family: 'Poppins', sans-serif;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .sub-title {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.95);
        text-align: center;
        font-weight: 400;
        letter-spacing: 0.3px;
        font-family: 'Poppins', sans-serif;
        margin: 0.25rem 0;
    }
    
    /* Section Cards - Warm with Floating Effect */
    .section-card {
        background: #FFFBF5;
        border: 2px solid #FFE0B2;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(141, 110, 99, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .section-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(141, 110, 99, 0.2);
        border-color: #8D6E63;
    }
    
    /* Force all text in section cards to be black - CRITICAL FOR DARK MODE */
    .section-card, 
    .section-card *:not(.profile-header):not(.profile-header *),
    .section-card h1,
    .section-card h2, 
    .section-card h3,
    .section-card h4,
    .section-card h5,
    .section-card h6,
    .section-card p,
    .section-card span,
    .section-card div,
    .section-card li,
    .section-card ul {
        color: #000000 !important;
    }
    
    /* Except for elements that should stay white */
    .section-card .profile-header,
    .section-card .profile-header *,
    .stat-box,
    .stat-box * {
        color: #FFF8E1 !important;
    }
    
    /* Fix for buddy card content */
    .buddy-card,
    .buddy-card *:not(.badge-excellent):not(.badge-veryhigh):not(.badge-high):not(.badge-medium):not(.badge-mediumlow):not(.badge-low):not(.badge-verylow):not(.badge-minimal) {
        color: #000000 !important;
    }
    
    /* Fix for metric cards */
    .metric-card,
    .metric-card * {
        color: #000000 !important;
    }
    
    /* Override Streamlit's default text colors in main area */
    .main .stMarkdown,
    .main .stMarkdown *,
    .main p,
    .main span:not([class*="badge"]),
    .main div:not(.stat-box):not(.stat-box *) {
        color: #000000 !important;
    }
    
    /* Plotly chart text - force dark color */
    .js-plotly-plot .plotly text {
        fill: #000000 !important;
    }
    
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        fill: #000000 !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #000000 !important;
        margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #8D6E63;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Profile Section - Warm Brown */
    .profile-header {
        background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%);
        color: #FFF8E1;
        padding: 1rem;
        margin: -1.5rem -1.5rem 1.5rem -1.5rem;
        text-align: center;
        border-radius: 14px 14px 0 0;
    }
    
    .profile-id {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF !important;
    }
    
    /* Metric Cards - Warm with Floating Effect */
    .metric-card {
        background: #FFF5E6;
        border: 2px solid #FFE0B2;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-card:hover {
        border-color: #8D6E63;
        background: #FFFBF5;
        transform: translateY(-6px);
        box-shadow: 0 8px 16px rgba(141, 110, 99, 0.15);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #000000 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Recommendation Cards - Warm with Floating Effect */
    .buddy-card {
        background: #FFFBF5;
        border: 2px solid #FFE0B2;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(141, 110, 99, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .buddy-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(141, 110, 99, 0.2);
        border-color: #8D6E63;
    }
    
    /* Score Badges - Gradient from Darkest to Lightest */
    /* 90-100%: Darkest Brown */
    .badge-excellent {
        display: inline-block;
        background: linear-gradient(135deg, #2C1810 0%, #3E2723 100%);
        color: #FFF8E1;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 3px 10px rgba(44, 24, 16, 0.4);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #6D4C41;
    }
    
    /* 80-89%: Very Dark Brown */
    .badge-veryhigh {
        display: inline-block;
        background: linear-gradient(135deg, #3E2723 0%, #4E342E 100%);
        color: #FFF8E1;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 3px 10px rgba(62, 39, 35, 0.4);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #795548;
    }
    
    /* 70-79%: Dark Brown */
    .badge-high {
        display: inline-block;
        background: linear-gradient(135deg, #4E342E 0%, #5D4037 100%);
        color: #FFF8E1;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(78, 52, 46, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #8D6E63;
    }
    
    /* 60-69%: Medium Brown */
    .badge-medium {
        display: inline-block;
        background: linear-gradient(135deg, #5D4037 0%, #6D4C41 100%);
        color: #FFF8E1;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(93, 64, 55, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #A1887F;
    }
    
    /* 50-59%: Light Medium Brown */
    .badge-mediumlow {
        display: inline-block;
        background: linear-gradient(135deg, #6D4C41 0%, #795548 100%);
        color: #FFF8E1;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(109, 76, 65, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #BCAAA4;
    }
    
    /* 40-49%: Light Brown */
    .badge-low {
        display: inline-block;
        background: linear-gradient(135deg, #795548 0%, #8D6E63 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(121, 85, 72, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #D7CCC8;
    }
    
    /* 30-39%: Very Light Brown */
    .badge-verylow {
        display: inline-block;
        background: linear-gradient(135deg, #8D6E63 0%, #A1887F 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(141, 110, 99, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #EFEBE9;
    }
    
    /* 0-29%: Lightest Brown */
    .badge-minimal {
        display: inline-block;
        background: linear-gradient(135deg, #A1887F 0%, #BCAAA4 100%);
        color: #3E2723;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(161, 136, 127, 0.3);
        font-family: 'Poppins', sans-serif;
        border: 2px solid #FFF8E1;
    }
    
    /* Stat Boxes - Warm gradient with Floating Effect */
    .stat-box {
        background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%);
        color: #FFF8E1;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.8rem 0;
        border: 2px solid #A1887F;
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stat-box:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 20px rgba(62, 39, 35, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
        color: #FFFFFF !important;
    }
    
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        color: #FFFFFF !important;
    }
    
    /* Sidebar - Warm Brown Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3E2723 0%, #4E342E 100%) !important;
        border-right: 3px solid #8D6E63;
        z-index: 999 !important;
        padding: 1.5rem 1rem !important;
    }

    
    button[data-testid="baseButton-header"]:hover {
        background: #FFECB3 !important;
        border-color: #6D4C41 !important;
    }
    
    button[data-testid="baseButton-header"] svg {
        fill: #3E2723 !important;
        stroke: #3E2723 !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Make header toolbar visible with proper styling */
    [data-testid="stToolbar"] {
        background: transparent !important;
        z-index: 9999 !important;
    }
    
    /* Style ALL header buttons including deploy - Compact size */
    button[kind="header"],
    button[kind="headerNoPadding"],
    [data-testid="stToolbar"] button,
    [data-testid="stMainMenu"] button {
        background: #3E2723 !important;
        color: #FFF8E1 !important;
        border: 2px solid #8D6E63 !important;
        border-radius: 6px !important;
        z-index: 9999 !important;
        box-shadow: 0 2px 8px rgba(62, 39, 35, 0.4) !important;
        padding: 6px 12px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.85rem !important;
    }
    
    button[kind="header"]:hover,
    button[kind="headerNoPadding"]:hover,
    [data-testid="stToolbar"] button:hover,
    [data-testid="stHeader"] button:hover {
        background: #5D4037 !important;
        border-color: #A1887F !important;
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.5) !important;
    }
    
    button[kind="header"] svg,
    button[kind="headerNoPadding"] svg,
    [data-testid="stToolbar"] svg,
    [data-testid="stHeader"] svg {
        fill: #FFF8E1 !important;
        stroke: #FFF8E1 !important;
        width: 16px !important;
        height: 16px !important;
    }
    
    /* Make MainMenu visible but styled */
    #MainMenu {
        visibility: visible !important;
        z-index: 9999 !important;
    }
    
    #MainMenu button {
        background: #3E2723 !important;
        color: #FFF8E1 !important;
        border: 3px solid #8D6E63 !important;
    }
    
    #MainMenu button:hover {
        background: #5D4037 !important;
    }  
    
    header button:hover {
        background: #5D4037 !important;
        border-color: #A1887F !important;
    }
      
    /* Deploy button specific styling - Compact */
    button[data-testid="stAppDeployButton"],
    button[title*="Deploy"],
    button[aria-label*="Deploy"] {
        background: #3E2723 !important;
        color: #FFF8E1 !important;
        border: 2px solid #8D6E63 !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(62, 39, 35, 0.4) !important;
        font-weight: 700 !important;
        padding: 6px 12px !important;
        font-size: 0.85rem !important;
    }
    
    button[data-testid="stAppDeployButton"]:hover,
    button[title*="Deploy"]:hover,
    button[aria-label*="Deploy"]:hover {
        background: #5D4037 !important;
        border-color: #A1887F !important;
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.5) !important;
    }
    
    /* Sidebar navigation */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar section headers - Warm card style */
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFF8E1 !important;
        font-weight: 700;
        font-size: 1rem;
        background: rgba(255, 248, 225, 0.1);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #A1887F;
        backdrop-filter: blur(10px);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar selectbox styling - Warm */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #FFF8E1 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(62, 39, 35, 0.2) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"] {
        color: #3E2723 !important;
    }

  [data-testid="stSidebar"] [data-baseweb="select"] [role="button"] {
        background-color: #FFF8E1 !important;
        border: 2px solid #A1887F !important;
        border-radius: 10px !important;
        color: #3E2723 !important;
        font-weight: 600 !important;
        padding: 0.7rem 1rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #3E2723 !important;
        font-family: 'Poppins', sans-serif !important;
    }

div[data-baseweb="select"] {
    background-color: #FFF8E1 !important;
    border-radius: 10px !important;
    border: 2px solid #A1887F !important;
}

/* Selected value inside the box */
div[data-baseweb="select"] > div {
    background-color: #FFF8E1 !important;
    color: #3E2723 !important;
    font-weight: 600 !important;
}

/* Dropdown list panel */
ul[role="listbox"] {
    background-color: #FFF8E1 !important;
    border-radius: 10px;
    border: 2px solid #A1887F !important;
}

/* Dropdown options */
li[role="option"] {
    color: #3E2723 !important;
    font-weight: 500 !important;
}

li[role="option"][aria-selected="true"] {
    background-color: #8D6E63 !important;
    color: white !important;
}

    
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #3E2723 !important;
    }
    
    /* Selectbox dropdown menu */
    [data-testid="stSidebar"] [role="listbox"] {
        background-color: #FFF8E1 !important;
        border: 2px solid #8D6E63 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.2) !important;
    }
    
    [data-testid="stSidebar"] [role="option"] {
        background-color: #FFF8E1 !important;
        color: #3E2723 !important;
        padding: 0.7rem 1rem !important;
        transition: all 0.2s ease !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    [data-testid="stSidebar"] [role="option"]:hover {
        background-color: #FFECB3 !important;
        color: #3E2723 !important;
    }
    
    /* Selected option highlighting */
    [data-testid="stSidebar"] [role="option"][aria-selected="true"] {
        background-color: #8D6E63 !important;
        color: #FFF8E1 !important;
        font-weight: 700 !important;
    }
    
    /* Dropdown menu outside sidebar */
    [role="listbox"] {
        background-color: #FFF8E1 !important;
        border: 2px solid #8D6E63 !important;
    }
    
    [role="option"] {
        background-color: #FFF8E1 !important;
        color: #3E2723 !important;
    }
    
    [role="option"]:hover {
        background-color: #FFECB3 !important;
        color: #3E2723 !important;
    }
    
    [role="option"][aria-selected="true"] {
        background-color: #8D6E63 !important;
        color: #FFF8E1 !important;
    }
    
    /* Sidebar labels - Modern style */
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Input text color */
    [data-testid="stSidebar"] input {
        color: #5A7521 !important;
        background-color: white !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar slider styling - Black & White */
    [data-testid="stSidebar"] .stSlider {
        padding: 1rem 0;
        margin: 0.5rem 0;
    }
    
    [data-testid="stSidebar"] .stSlider > div > div > div {
        background-color: rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
        height: 6px !important;
    }
    
    [data-testid="stSidebar"] .stSlider > div > div > div > div {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] .stSlider [role="slider"] {
        background-color: white !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0 3px 10px rgba(255, 255, 255, 0.5) !important;
        width: 22px !important;
        height: 22px !important;
    }
    
    /* Slider value labels */
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] span {
        color: white !important;
        font-weight: 600 !important;
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 4px !important;
    }
    
    /* Sidebar checkbox styling - Modern card-style */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 0.7rem 0.8rem !important;
        border-radius: 8px !important;
        margin: 0.3rem 0 !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stCheckbox"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label span {
        color: white !important;
    }
    
    /* Checkbox itself - Brown theme */
    [data-testid="stSidebar"] input[type="checkbox"] {
        accent-color: #8D6E63 !important;
        width: 20px !important;
        height: 20px !important;
        cursor: pointer !important;
        border-radius: 4px !important;
    }
    
    /* Checkbox checked state */
    [data-testid="stSidebar"] input[type="checkbox"]:checked {
        background-color: #8D6E63 !important;
        border-color: #8D6E63 !important;
    }
    
    /* Sidebar metric styling - Black & White */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        margin: 0.6rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetric"]:hover {
        border-color: rgba(255, 255, 255, 0.7);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Sidebar info box - Black & White */
    [data-testid="stSidebar"] .stInfo {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
        padding: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stInfo p {
        color: white !important;
        font-size: 0.9rem !important;
    }
    
    /* Streamlit native components styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 800;
        color: #000000;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        font-weight: 600;
        color: #666;
        text-transform: uppercase;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #000000;
        margin: 2rem 0;
    }
    
    /* Info/Success/Warning boxes */
    .stSuccess {
        background: #f0f0f0 !important;
        border-left: 4px solid #000000 !important;
        color: #000000 !important;
    }
    
    .stWarning {
        background: #f8f9fa !important;
        border-left: 4px solid #666 !important;
        color: #000000 !important;
    }
    
    .stInfo {
        background: #ffffff !important;
        border: 2px solid #000000 !important;
        color: #000000 !important;
    }
    
    /* Spacing improvements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Column separation */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    [data-testid="column"]:first-child {
        padding-left: 0;
    }
    
    [data-testid="column"]:last-child {
        padding-right: 0;
    }
    
    /* Make sure all interactive elements are accessible */
    button, input, select, textarea {
        pointer-events: auto !important;
    }
    /* 1. Force the main header bar to ALWAYS be visible and NOT fade out */
header[data-testid="stHeader"] {
    visibility: visible !important;
    opacity: 1 !important;
    background: transparent !important;
    z-index: 9999 !important;
}

/* 2. Force the content inside the header (buttons) to be visible */
header [data-testid="stHeader"] > div,
header [data-testid="stToolbar"] > div {
    opacity: 1 !important;
    visibility: visible !important;
}

/* 3. Style for the EXPANDED sidebar 'X' button */
button[data-testid="baseButton-header"] {
    background: #FFF8E1 !important;
    border: 3px solid #8D6E63 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(62, 39, 35, 0.5) !important;
    opacity: 1 !important;
    visibility: visible !important;
}
/* 3a. Icon color for the 'X' button */
button[data-testid="baseButton-header"] svg {
    fill: #3E2723 !important;
    stroke: #3E2723 !important;
}
button[data-testid="baseButton-header"]:hover {
    background: #FFECB3 !important;
    border-color: #6D4C41 !important;
}

/* 4. Style for the COLLAPSED sidebar hamburger button */
[data-testid="stSidebarCollapsedControl"] {
    background: #FFF8E1 !important;
    border: 3px solid #8D6E63 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(62, 39, 35, 0.5) !important;
    opacity: 1 !important;
    visibility: visible !important;
    display: block !important; 
    z-index: 9999 !important;
    /* Position it slightly */
    left: 7px; 
    top: 7px;
}
/* 4a. Icon color for the hamburger button */
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #3E2723 !important;
    stroke: #3E2723 !important;
}
[data-testid="stSidebarCollapsedControl"]:hover {
    background: #FFECB3 !important;
    border-color: #6D4C41 !important;
}

    /* Ensure all arrows and chevrons are visible */
    svg[data-testid="stSidebarNavSeparator"],
    svg[data-testid="stSidebarNavLink"],
    [class*="chevron"],
    [class*="arrow"] {
        fill: #FFF8E1 !important;
        stroke: #FFF8E1 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    [data-testid="collapsedControl"] svg {
        fill: #3E2723 !important;
        stroke: #3E2723 !important;
    }
    
    /* Sidebar user content when collapsed */
    [data-testid="stSidebarUserContent"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* All sidebar control buttons */
    [class*="collapsedControl"],
    [class*="CollapsedControl"] {
        background: #FFF8E1 !important;
        border: 3px solid #8D6E63 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    [class*="collapsedControl"] svg,
    [class*="CollapsedControl"] svg {
        fill: #3E2723 !important;
        stroke: #3E2723 !important;
    }
    
    /* Ensure header buttons don't disappear */
    [data-testid="stHeader"] > div {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Settings and deploy button container */
    [data-testid="stToolbar"] > div {
        opacity: 1 !important;
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)

def train_model_if_needed():
    """Train model if it doesn't exist"""
    import os
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
    
    # Check both src directory and root directory
    model_paths = ['buddy_model.joblib', 'src/buddy_model.joblib']
    if any(os.path.exists(p) for p in model_paths):
        return
    
    with st.spinner('🔄 Training model for the first time... This will take a moment.'):
        # Load data - try both paths
        data_paths = ['data/students.csv', '../data/students.csv']
        df = None
        for path in data_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                break
        
        if df is None:
            st.error("❌ Data file not found!")
            st.stop()
            
        df_clean = df.copy()
        
        # First, one-hot encode categorical features BEFORE normalization
        categorical_cols = ['club_top1', 'club_top2', 'hobby_top1', 'hobby_top2']
        df_encoded = pd.get_dummies(df_clean, columns=categorical_cols, prefix=categorical_cols)
        
        # Normalize numerical features
        scaler = StandardScaler()
        numerical_cols = ['teamwork_preference', 'introversion_extraversion', 
                         'books_read_past_year', 'weekly_hobby_hours',
                         'risk_taking', 'conscientiousness', 'open_to_new_experiences']
        
        df_encoded[numerical_cols] = scaler.fit_transform(df_encoded[numerical_cols])
        
        # Clustering - exclude non-numeric columns
        exclude_cols = ['student_id', 'timestamp', 'age', 'height_cm', 'weight_kg', 
                       'cuisine_top1', 'cuisine_top2', 'cuisine_top3', 'spice_tolerance',
                       'dietary_pref', 'eating_out_per_week', 'food_budget_per_meal',
                       'sweet_tooth_level', 'tea_vs_coffee', 'movie_genre_top1', 
                       'movie_genre_top2', 'movie_genre_top3', 'series_genre_top1',
                       'series_genre_top2', 'series_genre_top3', 'content_lang_top1',
                       'content_lang_top2', 'content_lang_top3', 'ott_top1', 'ott_top2',
                       'ott_top3', 'binge_freq_per_week', 'screen_time_hours_per_week',
                       'gaming_days_per_week', 'gaming_hours_per_week', 'game_genre_top1',
                       'game_genre_top2', 'game_genre_top3', 'gaming_platform_top1',
                       'gaming_platform_top2', 'gaming_platform_top3', 'esports_viewing',
                       'social_platform_top1', 'social_platform_top2', 'social_platform_top3',
                       'daily_social_media_minutes', 'primary_content_type', 
                       'content_creation_freq', 'music_genre_top1', 'music_genre_top2',
                       'music_genre_top3', 'listening_hours_per_day', 'music_lang_top1',
                       'music_lang_top2', 'live_concerts_past_year', 'reads_books',
                       'book_genre_top1', 'book_genre_top2', 'book_genre_top3',
                       'fashion_spend_per_month', 'shopping_mode_pref', 
                       'ethical_shopping_importance', 'travel_freq_per_year',
                       'travel_type_top1', 'travel_type_top2', 'travel_type_top3',
                       'budget_per_trip', 'travel_planning_pref']
        
        feature_cols = [col for col in df_encoded.columns if col not in exclude_cols]
        X = df_encoded[feature_cols].values
        
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df_clean['Cluster'] = kmeans.fit_predict(X)
        
        # Calculate similarity matrix
        cosine_sim = cosine_similarity(X)
        euclidean_sim = 1 / (1 + euclidean_distances(X))
        similarity_matrix = 0.6 * cosine_sim + 0.4 * euclidean_sim
        
        # Save artifacts
        artifacts = {
            'df_clean': df_clean,
            'similarity_matrix': similarity_matrix,
            'kmeans_model': kmeans,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'model_version': 'improved',
            'n_features': len(feature_cols)
        }
        
        joblib.dump(artifacts, 'buddy_model.joblib')

@st.cache_resource
def load_model_artifacts():
    """Load pre-trained improved model and data"""
    import os
    
    train_model_if_needed()
    
    # Try to load from root directory first, then src directory
    model_paths = ['buddy_model.joblib', 'src/buddy_model.joblib']
    artifacts = None
    
    for path in model_paths:
        if os.path.exists(path):
            artifacts = joblib.load(path)
            break
    
    if artifacts is None:
        st.error("❌ Could not load model file!")
        st.stop()
    
    similarity_matrix = artifacts['similarity_matrix']
    model_version = artifacts.get('model_version', '2.0_improved')
    return artifacts, similarity_matrix

def get_compatibility_badge(score):
    """Return HTML badge based on compatibility score"""
    if score >= 60:
        return f'<span class="score-badge-high">🌟 {score:.1f}% Match</span>'
    elif score >= 40:
        return f'<span class="score-badge-medium">⭐ {score:.1f}% Match</span>'
    else:
        return f'<span class="score-badge-low">💫 {score:.1f}% Match</span>'

def get_confidence_level(score):
    """Get confidence level text"""
    if score >= 60:
        return '<span class="confidence-high">● HIGH CONFIDENCE</span>'
    elif score >= 40:
        return '<span class="confidence-medium">● MEDIUM CONFIDENCE</span>'
    else:
        return '<span class="confidence-low">● LOW CONFIDENCE</span>'

def get_personality_label(score):
    """Convert personality score to label"""
    if score >= 4:
        return "🙋 Extrovert"
    elif score <= 2:
        return "🤫 Introvert"
    else:
        return "😊 Ambivert"

def recommend_buddies(student_idx, similarity_matrix, df_clean, top_n=5, min_score=0.0):
    """Get top N study buddy recommendations with dynamic filtering"""
    similarities = pd.Series(similarity_matrix[student_idx], index=df_clean.index)
    similarities = similarities.drop(student_idx)

    # Filter by minimum score
    if min_score > 0:
        similarities = similarities[similarities >= min_score]

    # Get top N
    if len(similarities) < top_n:
        st.warning(f"⚠️ Only {len(similarities)} matches found. Try lowering the similarity threshold.")

    top_indices = similarities.nlargest(min(top_n, len(similarities))).index

    recommendations = pd.DataFrame({
        'Student_Index': top_indices,
        'Similarity_Raw': similarities[top_indices].values,
        'Compatibility_Score': similarities[top_indices].values * 100,
        'Teamwork': df_clean.loc[top_indices, 'teamwork_preference'].values,
        'Personality': df_clean.loc[top_indices, 'introversion_extraversion'].values,
        'Top_Club': df_clean.loc[top_indices, 'club_top1'].values,
        'Second_Club': df_clean.loc[top_indices, 'club_top2'].values,
        'Top_Hobby': df_clean.loc[top_indices, 'hobby_top1'].values,
        'Second_Hobby': df_clean.loc[top_indices, 'hobby_top2'].values,
        'Books_Read': df_clean.loc[top_indices, 'books_read_past_year'].values,
        'Hobby_Hours': df_clean.loc[top_indices, 'weekly_hobby_hours'].values,
        'Risk_Taking': df_clean.loc[top_indices, 'risk_taking'].values,
        'Conscientiousness': df_clean.loc[top_indices, 'conscientiousness'].values,
        'Openness': df_clean.loc[top_indices, 'open_to_new_experiences'].values,
        'Cluster': df_clean.loc[top_indices, 'Cluster'].values
    })

    return recommendations

def main():
    # Load model and data
    artifacts, similarity_matrix = load_model_artifacts()
    df_clean = artifacts['df_clean']
    kmeans_model = artifacts['kmeans_model']

    # Calculate dynamic statistics
    total_students = len(df_clean)
    total_clusters = df_clean['Cluster'].nunique()
    total_clubs = df_clean['club_top1'].nunique()
    total_hobbies = df_clean['hobby_top1'].nunique()
    avg_similarity = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)].mean()
    current_time = datetime.now().strftime("%B %d, %Y")
    model_version = artifacts.get('model_version', '2.0_improved')
    n_features = artifacts.get('n_features', 'N/A')

    # Header with model info
    st.markdown(f"""
    <div class="app-header">
        <h1 class="main-title">🎓 STUDY BUDDY FINDER</h1>
        <p class="sub-title">{total_students} Students • {total_clusters} Clusters • {n_features} Features</p>
        <p class="sub-title">AI-Powered Matching</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🔍 Find Your Study Buddy")
        st.markdown("---")

        # Student selection
        student_idx = st.selectbox(
            "👤 Select Your Student ID",
            options=list(df_clean.index),
            format_func=lambda x: f"Student #{x}",
            help="Choose your student ID to find compatible study partners"
        )

        st.markdown("---")

        # Number of recommendations
        top_n = st.slider(
            "📊 Number of Recommendations",
            min_value=3,
            max_value=20,
            value=5,
            step=1,
            help="How many study buddy recommendations do you want?"
        )
        
        # Minimum similarity threshold
        min_similarity = st.slider(
            "🎯 Minimum Match Score (%)",
            min_value=0,
            max_value=80,
            value=0,
            step=5,
            help="Filter out matches below this score"
        ) / 100.0

        st.markdown("---")

        # Filter options
        st.markdown("### 🎯 Advanced Filters")
        
        filter_by_cluster = st.checkbox("✓ Same Personality Cluster", value=False)
        filter_by_club = st.checkbox("✓ Same Primary Club", value=False)
        filter_by_hobby = st.checkbox("✓ Same Primary Hobby", value=False)
        
        # Teamwork preference filter
        filter_teamwork = st.checkbox("✓ Similar Teamwork Level", value=False)

        st.markdown("---")
        
        # Quick stats in sidebar
        st.markdown("### 📈 System Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Students", total_students)
            st.metric("Clubs", total_clubs)
        with col_b:
            st.metric("Clusters", total_clusters)
            st.metric("Hobbies", total_hobbies)
        st.metric("Avg Match Quality", f"{avg_similarity:.1%}", delta=None)
        
        st.markdown("---")
        
        # Model info
        st.markdown("### 🤖 Model Info")
        st.info(f""" 
**Features:** {n_features}  
**Algorithm:** Hybrid Similarity  
(Cosine + Euclidean)
        """)
        
        st.markdown("---")
        st.info("💡 **Tip:** Start with fewer filters for more matches!")

    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        profile = df_clean.loc[student_idx]
        personality_label = get_personality_label(profile['introversion_extraversion'])

        # Profile Card with Black Header
        st.markdown(f"""
        <div class="section-card">
            <div class="profile-header">
                <h2 class="profile-id">STUDENT #{student_idx}</h2>
            </div>
            <div class="metric-card">
                <div class="metric-label">⭐ TEAMWORK</div>
                <div class="metric-value">{profile['teamwork_preference']}/5</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">😊 PERSONALITY</div>
                <div class="metric-value">{personality_label}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">📚 BOOKS/YEAR</div>
                <div class="metric-value">{int(profile['books_read_past_year'])}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🏆 PRIMARY CLUB</div>
                <div class="metric-value" style="font-size: 1rem;">{profile['club_top1']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🎨 PRIMARY HOBBY</div>
                <div class="metric-value" style="font-size: 1rem;">{profile['hobby_top1']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">⏰ HOBBY HOURS/WEEK</div>
                <div class="metric-value">{int(profile['weekly_hobby_hours'])}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">👥 PERSONALITY GROUP</div>
                <div class="metric-value">CLUSTER {profile['Cluster']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Personality Traits Section
        st.markdown("")
        st.markdown(f"""
        <div class="section-card">
            <h3 class="section-header">🧠 Personality Traits</h3>
        </div>
        """, unsafe_allow_html=True)
        
        traits = {
            'Risk Taking': profile['risk_taking'],
            'Conscientiousness': profile['conscientiousness'],
            'Openness': profile['open_to_new_experiences']
        }

        fig_traits = go.Figure(go.Bar(
            x=list(traits.values()),
            y=list(traits.keys()),
            orientation='h',
            marker=dict(
                color='#5D4037',
                line=dict(color='#6D4C41', width=2)
            ),
            text=list(traits.values()),
            textposition='outside',
            textfont=dict(size=14, color='#000000', family='Poppins', weight=700)
        ))
        fig_traits.update_layout(
            xaxis=dict(title="Score", range=[0, 5.5], showgrid=True, gridcolor='#FFE0B2', tickfont=dict(color='#000000')),
            yaxis=dict(title="", tickfont=dict(color='#000000')),
            height=200,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='#FFF9F0',
            paper_bgcolor='#FFF9F0',
            font=dict(family='Poppins', size=12, color='#000000')
        )
        st.plotly_chart(fig_traits, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div class="section-card">
            <h3 class="section-header">🎯 Study Buddy Matches</h3>
        </div>
        """, unsafe_allow_html=True)

        # Get recommendations with minimum score
        recommendations = recommend_buddies(student_idx, similarity_matrix, df_clean, top_n=top_n, min_score=min_similarity)

        # Apply filters
        filtered_recs = recommendations.copy()

        if filter_by_cluster:
            student_cluster = profile['Cluster']
            filtered_recs = filtered_recs[filtered_recs['Cluster'] == student_cluster]

        if filter_by_club:
            student_club = profile['club_top1']
            filtered_recs = filtered_recs[filtered_recs['Top_Club'] == student_club]

        if filter_by_hobby:
            student_hobby = profile['hobby_top1']
            filtered_recs = filtered_recs[filtered_recs['Top_Hobby'] == student_hobby]

        if filter_teamwork:
            teamwork_range = (profile['teamwork_preference'] - 1, profile['teamwork_preference'] + 1)
            filtered_recs = filtered_recs[
                (filtered_recs['Teamwork'] >= teamwork_range[0]) &
                (filtered_recs['Teamwork'] <= teamwork_range[1])
            ]

        if len(filtered_recs) == 0:
            st.warning("⚠️ No matches found with current filters. Try adjusting your preferences!")
        else:
            st.success(f"✅ Found {len(filtered_recs)} compatible study buddies!")
            st.markdown("")

            # Display recommendations with clean cards
            for idx, row in filtered_recs.iterrows():
                buddy_personality = get_personality_label(row['Personality'])

                # Score badge class with gradient (darkest to lightest)
                score = row['Compatibility_Score']
                if score >= 90:
                    badge_html = f'<span class="badge-excellent">🌟 {score:.1f}% MATCH</span>'
                elif score >= 80:
                    badge_html = f'<span class="badge-veryhigh">🌟 {score:.1f}% MATCH</span>'
                elif score >= 70:
                    badge_html = f'<span class="badge-high">⭐ {score:.1f}% MATCH</span>'
                elif score >= 60:
                    badge_html = f'<span class="badge-medium">⭐ {score:.1f}% MATCH</span>'
                elif score >= 50:
                    badge_html = f'<span class="badge-mediumlow">⭐ {score:.1f}% MATCH</span>'
                elif score >= 40:
                    badge_html = f'<span class="badge-low">💫 {score:.1f}% MATCH</span>'
                elif score >= 30:
                    badge_html = f'<span class="badge-verylow">💫 {score:.1f}% MATCH</span>'
                else:
                    badge_html = f'<span class="badge-minimal">💫 {score:.1f}% MATCH</span>'

                st.markdown(f"""
                <div class="buddy-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="margin: 0; font-weight: 800;">STUDENT #{int(row['Student_Index'])}</h3>
                        {badge_html}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                        <div>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>⭐ Teamwork:</b> {row['Teamwork']}/5</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>😊 Personality:</b> {buddy_personality}</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>📚 Books:</b> {int(row['Books_Read'])}/year</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>💪 Conscient.:</b> {row['Conscientiousness']}/5</p>
                        </div>
                        <div>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>🏆 Club:</b> {row['Top_Club']}</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>🎯 2nd Club:</b> {row['Second_Club']}</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>🎨 Hobby:</b> {row['Top_Hobby']}</p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;"><b>⏰ Hours:</b> {int(row['Hobby_Hours'])}/week</p>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #f0f0f0;">
                        <p style="margin: 0; font-size: 0.8rem; color: #666;">
                            <b>🎲 Risk:</b> {row['Risk_Taking']}/5 • <b>🌟 Openness:</b> {row['Openness']}/5 • <b>👥 Cluster:</b> {row['Cluster']}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Compatibility chart
            st.markdown(f"""
            <div class="section-card">
                <h4 style="font-size: 1rem; font-weight: 700; margin: 0 0 1rem 0;">📊 COMPATIBILITY SCORES</h4>
            </div>
            """, unsafe_allow_html=True)

            # Create gradient colors based on scores (darkest for highest)
            def get_bar_color(score):
                if score >= 90:
                    return '#2C1810'  # Darkest
                elif score >= 80:
                    return '#3E2723'  # Very Dark
                elif score >= 70:
                    return '#4E342E'  # Dark
                elif score >= 60:
                    return '#5D4037'  # Medium Dark
                elif score >= 50:
                    return '#6D4C41'  # Medium
                elif score >= 40:
                    return '#795548'  # Light Medium
                elif score >= 30:
                    return '#8D6E63'  # Light
                else:
                    return '#A1887F'  # Lightest
            
            bar_colors = [get_bar_color(score) for score in filtered_recs['Compatibility_Score']]
            
            fig_compat = px.bar(
                filtered_recs,
                x='Student_Index',
                y='Compatibility_Score',
                text='Compatibility_Score'
            )
            fig_compat.update_traces(
                marker_color=bar_colors,
                marker_line_color='#6D4C41',
                marker_line_width=2,
                texttemplate='%{text:.1f}%',
                textposition='outside',
                textfont=dict(size=12, color='#000000', family='Poppins', weight=700)
            )
            fig_compat.update_layout(
                height=300,
                showlegend=False,
                xaxis_title="Student ID",
                yaxis_title="Match %",
                plot_bgcolor='#FFF9F0',
                paper_bgcolor='#FFF9F0',
                font=dict(family='Poppins', size=11, color='#000000'),
                xaxis=dict(showgrid=False, tickfont=dict(color='#000000')),
                yaxis=dict(showgrid=True, gridcolor='#FFE0B2', tickfont=dict(color='#000000'))
            )
            st.plotly_chart(fig_compat, use_container_width=True)

    with col3:
        st.markdown(f"""
        <div class="section-card">
            <h3 class="section-header">📈 Analytics</h3>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic system stats
        st.markdown(f"""
        <div class="stat-box" style="margin: 10px 0;">
            <div class="stat-number">{total_students}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-box" style="margin: 10px 0;">
            <div class="stat-number">{total_clusters}</div>
            <div class="stat-label">Personality Groups</div>
        </div>
        <div class="stat-box" style="margin: 10px 0;">
            <div class="stat-number">{total_clubs}</div>
            <div class="stat-label">Unique Clubs</div>
        </div>
        <div class="stat-box" style="margin: 10px 0;">
            <div class="stat-number">{total_hobbies}</div>
            <div class="stat-label">Unique Hobbies</div>
        </div>
        <div class="stat-box" style="margin: 10px 0;">
            <div class="stat-number">{avg_similarity:.1%}</div>
            <div class="stat-label">Avg Match Quality</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Dynamic cluster distribution
        st.markdown(f"""
        <div class="section-card">
            <h4 style="font-size: 1rem; font-weight: 700; margin: 0 0 1rem 0;">👥 CLUSTER DISTRIBUTION</h4>
        </div>
        """, unsafe_allow_html=True)

        cluster_counts = df_clean['Cluster'].value_counts().sort_index()
        cluster_percentages = (cluster_counts / len(df_clean) * 100).round(1)

        fig_cluster = px.pie(
            values=cluster_counts.values,
            names=[f"Group {i}" for i in cluster_counts.index],
            color_discrete_sequence=['#3E2723', '#4E342E', '#5D4037', '#6D4C41', '#795548', '#8D6E63', '#A1887F', '#BCAAA4', '#D7CCC8'],
            hole=0.5
        )
        fig_cluster.update_traces(
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=12, color='white', family='Poppins', weight=700)
        )
        fig_cluster.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_cluster, use_container_width=True)

        # Dynamic top clubs
        st.markdown(f"""
        <div class="section-card">
            <h4 style="font-size: 1rem; font-weight: 700; margin: 0 0 1rem 0;">🏆 TOP CLUBS</h4>
        </div>
        """, unsafe_allow_html=True)

        club_counts = df_clean['club_top1'].value_counts().head(5)
        fig_clubs = px.bar(
            x=club_counts.values,
            y=club_counts.index,
            orientation='h',
            text=club_counts.values
        )
        fig_clubs.update_traces(
            marker_color='#5D4037',
            marker_line_color='#6D4C41',
            marker_line_width=2,
            textposition='outside',
            textfont=dict(size=12, color='#000000', family='Poppins', weight=700)
        )
        fig_clubs.update_layout(
            height=230,
            showlegend=False,
            xaxis_title="",
            yaxis_title="",
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='#FFF9F0',
            paper_bgcolor='#FFF9F0',
            font=dict(family='Poppins', size=10, color='#000000'),
            xaxis=dict(showgrid=False, showticklabels=False, tickfont=dict(color='#000000')),
            yaxis=dict(showgrid=False, tickfont=dict(color='#000000'))
        )
        st.plotly_chart(fig_clubs, use_container_width=True)

    # Additional insights section
    st.markdown("---")
    st.markdown(f"""
    <div class="section-card">
        <h3 class="section-header">💡 Insights & Tips</h3>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class="section-card">
            <h4 style="font-weight: 700; margin-bottom: 0.5rem;">🤝 BEST MATCHING FACTORS</h4>
            <ul style="list-style: none; padding-left: 0; margin: 0;">
                <li style="margin: 0.3rem 0;">• Similar teamwork preferences</li>
                <li style="margin: 0.3rem 0;">• Compatible personality types</li>
                <li style="margin: 0.3rem 0;">• Shared club memberships</li>
                <li style="margin: 0.3rem 0;">• Common hobbies and interests</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="section-card">
            <h4 style="font-weight: 700; margin-bottom: 0.5rem;">📚 STUDY TIPS</h4>
            <ul style="list-style: none; padding-left: 0; margin: 0;">
                <li style="margin: 0.3rem 0;">• Meet in campus study spaces</li>
                <li style="margin: 0.3rem 0;">• Set regular study schedules</li>
                <li style="margin: 0.3rem 0;">• Share notes and resources</li>
                <li style="margin: 0.3rem 0;">• Attend club events together</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="section-card">
            <h4 style="font-weight: 700; margin-bottom: 0.5rem;">⚠️ REMEMBER</h4>
            <ul style="list-style: none; padding-left: 0; margin: 0;">
                <li style="margin: 0.3rem 0;">• Respect study boundaries</li>
                <li style="margin: 0.3rem 0;">• Communicate preferences clearly</li>
                <li style="margin: 0.3rem 0;">• Be punctual for study sessions</li>
                <li style="margin: 0.3rem 0;">• Give feedback to improve matching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%); color: #FFF8E1; text-align: center; padding: 2rem; margin: 2rem -2rem -2rem -2rem; border-top: 4px solid #A1887F; font-family: 'Poppins', sans-serif; box-shadow: 0 -4px 12px rgba(62, 39, 35, 0.2);">
        <p style="margin: 0; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px;">🎓 STUDY BUDDY FINDER</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.95;">{n_features} Features • Hybrid Similarity Algorithm</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

