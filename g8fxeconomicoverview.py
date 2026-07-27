import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="G8 Currency Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DARK LUXURY CSS ====================
st.markdown("""
    <style>
    /* Dark Theme with Gold Accents */
    .stApp {
        background: #0a0a0a;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.8rem;
        color: #d4af37;
        text-align: center;
        font-weight: 300;
        letter-spacing: 8px;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.1);
        font-family: 'Georgia', serif;
    }
    
    .sub-header {
        text-align: center;
        color: #8a7a4a;
        font-size: 0.9rem;
        letter-spacing: 6px;
        margin-bottom: 2rem;
        font-weight: 300;
        font-family: 'Georgia', serif;
    }
    
    .gold-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #d4af37, transparent);
        margin: 1.5rem 0;
        opacity: 0.3;
    }
    
    /* Economy Cards - Luxury Style */
    .economy-card {
        background: linear-gradient(145deg, #141414, #0a0a0a);
        border: 1px solid #2a2a1a;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8), inset 0 1px 0 rgba(212, 175, 55, 0.05);
        transition: all 0.3s ease;
    }
    
    .economy-card:hover {
        border-color: #d4af37;
        box-shadow: 0 8px 40px rgba(212, 175, 55, 0.05), inset 0 1px 0 rgba(212, 175, 55, 0.1);
        transform: translateY(-2px);
    }
    
    .economy-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1a1a0a;
    }
    
    .economy-name {
        font-size: 2rem;
        font-weight: 700;
        color: #d4af37;
        font-family: 'Georgia', serif;
        letter-spacing: 2px;
    }
    
    .economy-currency {
        font-size: 0.85rem;
        color: #8a7a4a;
        margin-left: 10px;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    .category-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #d4af37;
        margin-bottom: 0.8rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #1a1a0a;
        font-family: 'Georgia', serif;
    }
    
    .indicator-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 12px;
        background: rgba(20, 20, 20, 0.5);
        border-radius: 6px;
        border: 1px solid #1a1a0a;
        margin-bottom: 4px;
        transition: all 0.2s ease;
    }
    
    .indicator-item:hover {
        border-color: #2a2a1a;
        background: rgba(30, 30, 20, 0.5);
    }
    
    .indicator-name {
        color: #b0a080;
        font-size: 0.82rem;
        font-weight: 400;
        flex: 1;
    }
    
    .indicator-biases {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .indicator-bias-group {
        display: flex;
        align-items: center;
        gap: 3px;
    }
    
    .indicator-bias-label {
        font-size: 0.5rem;
        color: #5a4a2a;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    /* ==================== SVG ARROWS - PROPERLY SIZED ==================== */
    .arrow-svg {
        display: inline-block;
        width: 16px;
        height: 18px;
        vertical-align: middle;
    }
    
    .arrow-svg-medium {
        display: inline-block;
        width: 22px;
        height: 24px;
        vertical-align: middle;
    }
    
    .arrow-svg-big {
        display: inline-block;
        width: 32px;
        height: 36px;
        vertical-align: middle;
    }
    
    /* Summary Grid */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 2rem;
    }
    
    .summary-card {
        background: linear-gradient(145deg, #141414, #0a0a0a);
        border: 1px solid #2a2a1a;
        border-radius: 12px;
        padding: 1rem 0.8rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .summary-card:hover {
        border-color: #d4af37;
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.05);
    }
    
    .summary-economy {
        font-size: 1.1rem;
        font-weight: 700;
        color: #d4af37;
        font-family: 'Georgia', serif;
    }
    
    .summary-currency-code {
        font-size: 0.7rem;
        color: #8a7a4a;
    }
    
    .bias-tag {
        font-size: 0.65rem;
        font-weight: 600;
        padding: 2px 12px;
        border-radius: 20px;
        letter-spacing: 0.5px;
        border: 1px solid transparent;
    }
    
    .bias-tag.bullish { 
        background: rgba(46, 204, 113, 0.15); 
        color: #2ecc71; 
        border-color: rgba(46, 204, 113, 0.3);
    }
    .bias-tag.rather-bullish { 
        background: rgba(46, 204, 113, 0.08); 
        color: #82e0aa; 
        border-color: rgba(46, 204, 113, 0.2);
    }
    .bias-tag.neutral { 
        background: rgba(212, 175, 55, 0.15); 
        color: #d4af37; 
        border-color: rgba(212, 175, 55, 0.3);
    }
    .bias-tag.rather-bearish { 
        background: rgba(231, 76, 60, 0.08); 
        color: #f5b7b1; 
        border-color: rgba(231, 76, 60, 0.2);
    }
    .bias-tag.bearish { 
        background: rgba(231, 76, 60, 0.15); 
        color: #e74c3c; 
        border-color: rgba(231, 76, 60, 0.3);
    }
    
    /* Management */
    .management-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 1.2rem;
        margin: 1.5rem 0;
    }
    
    .management-card {
        background: linear-gradient(145deg, #141414, #0a0a0a);
        border: 1px solid #2a2a1a;
        border-radius: 12px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .management-card:hover {
        border-color: #d4af37;
    }
    
    .management-economy {
        font-weight: 700;
        font-size: 1.2rem;
        color: #d4af37;
        margin-bottom: 0.8rem;
        font-family: 'Georgia', serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a, #141414);
        border-right: 1px solid #1a1a0a;
    }
    
    section[data-testid="stSidebar"] .sidebar-content {
        background: transparent;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #1a1a0a;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-header h1 {
        color: #d4af37;
        font-size: 2rem;
        font-weight: 300;
        letter-spacing: 4px;
        font-family: 'Georgia', serif;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #d4af37, #b8941f) !important;
        color: #0a0a0a !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        font-family: 'Georgia', serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
        background: linear-gradient(145deg, #e0c050, #d4af37) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #0a0a0a;
        border-bottom: 1px solid #1a1a0a;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #8a7a4a !important;
        font-weight: 400 !important;
        letter-spacing: 2px !important;
        padding: 0.6rem 1.5rem !important;
        font-family: 'Georgia', serif !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom: 2px solid #d4af37 !important;
    }
    
    /* Gold scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    ::-webkit-scrollbar-thumb {
        background: #d4af37;
        border-radius: 3px;
    }
    
    @media (max-width: 768px) {
        .summary-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .management-grid {
            grid-template-columns: 1fr;
        }
        .main-header {
            font-size: 2rem;
            letter-spacing: 4px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SVG ARROW GENERATORS ====================
def get_svg_arrow(bias, size='small'):
    """Generate SVG arrows with proper sizing"""
    
    # Colors
    colors = {
        'Bullish': {'main': '#2ecc71', 'gradient': 'url(#bullishGrad)'},
        'Rather Bullish': {'main': '#82e0aa', 'gradient': 'url(#ratherBullishGrad)'},
        'Neutral': {'main': '#d4af37', 'gradient': 'url(#neutralGrad)'},
        'Rather Bearish': {'main': '#f5b7b1', 'gradient': 'url(#ratherBearishGrad)'},
        'Bearish': {'main': '#e74c3c', 'gradient': 'url(#bearishGrad)'}
    }
    
    # Size mapping
    sizes = {
        'small': {'w': 16, 'h': 18, 'viewBox': '0 0 16 18', 'class': 'arrow-svg'},
        'medium': {'w': 22, 'h': 24, 'viewBox': '0 0 22 24', 'class': 'arrow-svg-medium'},
        'big': {'w': 32, 'h': 36, 'viewBox': '0 0 32 36', 'class': 'arrow-svg-big'}
    }
    
    size_config = sizes.get(size, sizes['small'])
    w, h = size_config['w'], size_config['h']
    viewBox = size_config['viewBox']
    css_class = size_config['class']
    
    # Arrow paths (scaled for 16x18 base)
    arrow_paths = {
        'Bullish': 'M8 1 L1 8 L4 8 L4 10 L12 10 L12 8 L15 8 Z',  # Up arrow
        'Rather Bullish': 'M8 1 L1 8 L5 8 L5 10 L11 10 L11 8 L15 8 Z M1 8 L5 10 L5 8 Z',  # Up-right
        'Neutral': 'M1 5 L15 5 L15 7 L1 7 Z M7 2 L8 1 L9 2 Z M7 14 L8 15 L9 14 Z',  # Right arrow
        'Rather Bearish': 'M8 15 L15 8 L11 8 L11 6 L5 6 L5 8 L1 8 Z M15 8 L11 6 L11 8 Z',  # Down-right
        'Bearish': 'M8 15 L1 8 L4 8 L4 6 L12 6 L12 8 L15 8 Z'  # Down arrow
    }
    
    color = colors.get(bias, colors['Neutral'])
    
    arrow_svg = f'''
    <svg class="{css_class}" viewBox="{viewBox}">
        <defs>
            <linearGradient id="{bias.replace(' ', '')}Grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color['main']};stop-opacity:0.7" />
                <stop offset="100%" style="stop-color:{color['main']};stop-opacity:1" />
            </linearGradient>
            <filter id="glow{bias.replace(' ', '')}">
                <feGaussianBlur stdDeviation="0.5" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <path d="{arrow_paths.get(bias, arrow_paths['Neutral'])}" 
              fill="{color['gradient']}" 
              filter="url(#glow{bias.replace(' ', '')})"
              stroke="{color['main']}" 
              stroke-width="0.3"/>
    </svg>
    '''
    
    return arrow_svg

def get_bias_class(bias):
    classes = {
        'Bullish': 'bullish',
        'Rather Bullish': 'rather-bullish',
        'Neutral': 'neutral',
        'Rather Bearish': 'rather-bearish',
        'Bearish': 'bearish'
    }
    return classes.get(bias, 'neutral')

# ==================== DATA STORAGE ====================
DATA_FILE = "g8_economy_data.json"

ECONOMIES = [
    {'name': 'United States', 'code': 'USD'},
    {'name': 'Eurozone', 'code': 'EUR'},
    {'name': 'United Kingdom', 'code': 'GBP'},
    {'name': 'Japan', 'code': 'JPY'},
    {'name': 'Canada', 'code': 'CAD'},
    {'name': 'Australia', 'code': 'AUD'},
    {'name': 'Switzerland', 'code': 'CHF'},
    {'name': 'New Zealand', 'code': 'NZD'}
]

ECONOMY_NAMES = {e['code']: e['name'] for e in ECONOMIES}
ECONOMY_CODES = [e['code'] for e in ECONOMIES]

BIAS_OPTIONS = ['Bullish', 'Rather Bullish', 'Neutral', 'Rather Bearish', 'Bearish']

CATEGORIES = [
    'Labor Market',
    'Inflation',
    'Housing Market',
    'Sentiment',
    'Markets',
    'Growth Activities'
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def initialize_data():
    data = load_data()
    if not data:
        data = {'indicators': {}}
        for economy in ECONOMY_CODES:
            data['indicators'][economy] = {}
            for category in CATEGORIES:
                data['indicators'][economy][category] = []
        save_data(data)
    return data

# ==================== MAIN APP ====================
def main():
    data = initialize_data()
    indicators_data = data['indicators']
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h1>💎 G8</h1>
            <p style="color: #8a7a4a; font-size: 0.8rem; letter-spacing: 3px; margin-top: -5px;">ECONOMIC DASHBOARD</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 LEGEND")
        st.markdown(f"""
        <div style="background: #141414; padding: 12px; border-radius: 8px; border: 1px solid #1a1a0a;">
            <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
                {get_svg_arrow('Bullish', 'small')} <span style="color: #b0a080; font-size: 0.8rem;">Bullish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
                {get_svg_arrow('Rather Bullish', 'small')} <span style="color: #b0a080; font-size: 0.8rem;">Rather Bullish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
                {get_svg_arrow('Neutral', 'small')} <span style="color: #b0a080; font-size: 0.8rem;">Neutral</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
                {get_svg_arrow('Rather Bearish', 'small')} <span style="color: #b0a080; font-size: 0.8rem;">Rather Bearish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
                {get_svg_arrow('Bearish', 'small')} <span style="color: #b0a080; font-size: 0.8rem;">Bearish</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Stats
        total = 0
        bullish = 0
        bearish = 0
        for economy in ECONOMY_CODES:
            for category in CATEGORIES:
                for indicator in indicators_data[economy].get(category, []):
                    total += 1
                    bias_5y = indicator.get('5Y', 'Neutral')
                    if 'Bullish' in bias_5y:
                        bullish += 1
                    elif 'Bearish' in bias_5y:
                        bearish += 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<p style="color: #2ecc71; text-align: center; font-size: 1.3rem; font-weight: 700; margin: 0;">{bullish}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.6rem; margin: 0;">BULLISH</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p style="color: #d4af37; text-align: center; font-size: 1.3rem; font-weight: 700; margin: 0;">{total - bullish - bearish}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.6rem; margin: 0;">NEUTRAL</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<p style="color: #e74c3c; text-align: center; font-size: 1.3rem; font-weight: 700; margin: 0;">{bearish}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.6rem; margin: 0;">BEARISH</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption(f"💾 {DATA_FILE}")
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Tabs
    tab1, tab2 = st.tabs(["📊 DASHBOARD", "⚙️ MANAGEMENT"])
    
    # ==================== TAB 1: DASHBOARD ====================
    with tab1:
        st.markdown('<h1 class="main-header">G8 ECONOMIC DASHBOARD</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">FUNDAMENTAL BIAS OVERVIEW • {datetime.now().strftime("%B %Y")}</p>', unsafe_allow_html=True)
        
        # Summary Grid
        st.markdown("### QUICK OVERVIEW")
        cols = st.columns(4)
        for idx, economy in enumerate(ECONOMIES):
            with cols[idx % 4]:
                code = economy['code']
                name = economy['name']
                eco_bullish = 0
                eco_bearish = 0
                for category in CATEGORIES:
                    for indicator in indicators_data[code].get(category, []):
                        bias_5y = indicator.get('5Y', 'Neutral')
                        if 'Bullish' in bias_5y:
                            eco_bullish += 1
                        elif 'Bearish' in bias_5y:
                            eco_bearish += 1
                
                if eco_bullish > eco_bearish:
                    overall = 'Bullish'
                elif eco_bearish > eco_bullish:
                    overall = 'Bearish'
                else:
                    overall = 'Neutral'
                
                arrow_svg = get_svg_arrow(overall, 'big')
                st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-economy">{code}</div>
                    <div class="summary-currency-code">{name}</div>
                    <div style="margin: 2px 0;">{arrow_svg}</div>
                    <div><span class="bias-tag {get_bias_class(overall)}">{overall}</span></div>
                    <div style="font-size: 0.6rem; color: #5a4a2a; margin-top: 2px;">
                        <span style="color: #2ecc71;">▲{eco_bullish}</span> 
                        <span style="color: #e74c3c;">▼{eco_bearish}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        
        # Detailed View
        st.markdown("### DETAILED ECONOMY VIEW")
        
        selected_economy = st.selectbox(
            "Select Economy", 
            ECONOMY_CODES,
            format_func=lambda x: f"{x} - {ECONOMY_NAMES.get(x, '')}",
            key="economy_select"
        )
        
        if selected_economy:
            economy_code = selected_economy
            economy_name = ECONOMY_NAMES.get(economy_code, '')
            
            st.markdown(f"""
            <div class="economy-card">
                <div class="economy-header">
                    <div>
                        <span class="economy-name">{economy_name}</span>
                        <span class="economy-currency">({economy_code})</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### ECONOMIC INDICATORS")
            
            economy_indicators = indicators_data.get(economy_code, {})
            total_indicators = sum(len(economy_indicators.get(cat, [])) for cat in CATEGORIES)
            
            if total_indicators == 0:
                st.markdown('<p style="color: #5a4a2a; font-style: italic; text-align: center; padding: 2rem;">No indicators added yet. Go to Management tab to add indicators.</p>', unsafe_allow_html=True)
            else:
                for category in CATEGORIES:
                    indicators = economy_indicators.get(category, [])
                    if indicators:
                        st.markdown(f'<div class="category-title">{category.upper()} <span style="color: #5a4a2a; font-size: 0.65rem;">({len(indicators)})</span></div>', unsafe_allow_html=True)
                        
                        for indicator in indicators:
                            name = indicator.get('name', '')
                            bias_5y = indicator.get('5Y', 'Neutral')
                            bias_3m = indicator.get('3M', 'Neutral')
                            
                            arrow_5y = get_svg_arrow(bias_5y, 'small')
                            arrow_3m = get_svg_arrow(bias_3m, 'small')
                            
                            st.markdown(f"""
                            <div class="indicator-item">
                                <span class="indicator-name">{name}</span>
                                <div class="indicator-biases">
                                    <div class="indicator-bias-group">
                                        <span class="indicator-bias-label">5Y</span>
                                        {arrow_5y}
                                    </div>
                                    <div class="indicator-bias-group">
                                        <span class="indicator-bias-label">3M</span>
                                        {arrow_3m}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
    
    # ==================== TAB 2: MANAGEMENT ====================
    with tab2:
        st.markdown('<h1 class="main-header">⚙️ MANAGEMENT</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">CONFIGURE ECONOMIC INDICATORS</p>', unsafe_allow_html=True)
        
        st.markdown("### MANAGE ECONOMIC INDICATORS")
        
        mgmt_economy = st.selectbox(
            "Select Economy", 
            ECONOMY_CODES,
            format_func=lambda x: f"{x} - {ECONOMY_NAMES.get(x, '')}",
            key="mgmt_economy"
        )
        
        if mgmt_economy:
            st.markdown(f'<h3 style="color: #d4af37; font-family: Georgia, serif; font-size: 1.2rem;">{ECONOMY_NAMES.get(mgmt_economy, "")} ({mgmt_economy})</h3>', unsafe_allow_html=True)
            
            selected_category = st.selectbox("Select Category", CATEGORIES, key="category_select")
            current_indicators = indicators_data[mgmt_economy].get(selected_category, [])
            
            st.markdown(f'<p style="color: #8a7a4a; font-size: 0.8rem;">Indicators in <span style="color: #d4af37;">{selected_category}</span>: {len(current_indicators)}</p>', unsafe_allow_html=True)
            
            if current_indicators:
                for idx, indicator in enumerate(current_indicators):
                    col1, col2, col3, col4 = st.columns([2.5, 1.5, 1.5, 1])
                    with col1:
                        st.text(f"📌 {indicator.get('name', '')}")
                    with col2:
                        bias_5y = indicator.get('5Y', 'Neutral')
                        arrow_5y = get_svg_arrow(bias_5y, 'small')
                        st.markdown(f"5Y {arrow_5y}", unsafe_allow_html=True)
                    with col3:
                        bias_3m = indicator.get('3M', 'Neutral')
                        arrow_3m = get_svg_arrow(bias_3m, 'small')
                        st.markdown(f"3M {arrow_3m}", unsafe_allow_html=True)
                    with col4:
                        if st.button("🗑️", key=f"remove_{mgmt_economy}_{selected_category}_{idx}"):
                            current_indicators.pop(idx)
                            indicators_data[mgmt_economy][selected_category] = current_indicators
                            data['indicators'] = indicators_data
                            save_data(data)
                            st.rerun()
            else:
                st.markdown('<p style="color: #5a4a2a; font-style: italic; font-size: 0.85rem;">No indicators in this category yet</p>', unsafe_allow_html=True)
            
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            
            # Add new indicator
            st.markdown("#### ➕ ADD NEW INDICATOR")
            
            with st.form("add_indicator_form"):
                indicator_name = st.text_input("Indicator Name", placeholder="e.g., Retail Sales MoM", key="indicator_name")
                
                col1, col2 = st.columns(2)
                with col1:
                    bias_5y = st.selectbox("5Y Trend", BIAS_OPTIONS, key="indicator_bias_5y")
                with col2:
                    bias_3m = st.selectbox("3M Trend", BIAS_OPTIONS, key="indicator_bias_3m")
                
                submitted_indicator = st.form_submit_button("➕ ADD INDICATOR")
                
                if submitted_indicator and indicator_name:
                    new_indicator = {
                        'name': indicator_name,
                        '5Y': bias_5y,
                        '3M': bias_3m,
                        'added': datetime.now().isoformat()
                    }
                    current_indicators.append(new_indicator)
                    indicators_data[mgmt_economy][selected_category] = current_indicators
                    data['indicators'] = indicators_data
                    save_data(data)
                    st.success(f"✅ Added '{indicator_name}'!")
                    st.rerun()
                elif submitted_indicator:
                    st.warning("Please enter an indicator name")
            
            # Quick add template
            with st.expander("📋 Quick Add Template"):
                template_indicators = {
                    'Labor Market': ['Unemployment Rate', 'Non-Farm Payrolls', 'Avg Hourly Earnings', 'Jobless Claims'],
                    'Inflation': ['CPI YoY', 'Core CPI YoY', 'PPI YoY', 'PCE Price Index'],
                    'Housing Market': ['Housing Starts', 'Building Permits', 'Existing Home Sales', 'Case-Shiller Index'],
                    'Sentiment': ['Consumer Confidence', 'Business Confidence', 'PMI', 'IFO Business Climate'],
                    'Markets': ['S&P 500', '10Y Treasury', 'Dollar Index', 'Commodity Index'],
                    'Growth Activities': ['GDP Growth', 'Industrial Production', 'Retail Sales MoM', 'Retail Sales YoY']
                }
                
                for cat, indicators in template_indicators.items():
                    if cat == selected_category:
                        st.markdown(f'<p style="color: #d4af37; font-size: 0.8rem; margin: 0.5rem 0 0.3rem 0;">{cat}:</p>', unsafe_allow_html=True)
                        cols = st.columns(4)
                        for idx, ind in enumerate(indicators):
                            with cols[idx % 4]:
                                if st.button(f"+ {ind}", key=f"template_{cat}_{ind}"):
                                    new_ind = {
                                        'name': ind,
                                        '5Y': 'Neutral',
                                        '3M': 'Neutral',
                                        'added': datetime.now().isoformat()
                                    }
                                    current_indicators.append(new_ind)
                                    indicators_data[mgmt_economy][selected_category] = current_indicators
                                    data['indicators'] = indicators_data
                                    save_data(data)
                                    st.success(f"Added '{ind}'!")
                                    st.rerun()

if __name__ == "__main__":
    main()