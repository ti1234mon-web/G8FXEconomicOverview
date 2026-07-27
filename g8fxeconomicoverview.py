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
    
    /* Main container */
    .main-container {
        background: #0a0a0a;
        padding: 1rem;
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
    
    /* Currency Cards - Luxury Style */
    .currency-card {
        background: linear-gradient(145deg, #141414, #0a0a0a);
        border: 1px solid #2a2a1a;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8), inset 0 1px 0 rgba(212, 175, 55, 0.05);
        transition: all 0.3s ease;
    }
    
    .currency-card:hover {
        border-color: #d4af37;
        box-shadow: 0 8px 40px rgba(212, 175, 55, 0.05), inset 0 1px 0 rgba(212, 175, 55, 0.1);
        transform: translateY(-2px);
    }
    
    .currency-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1a1a0a;
    }
    
    .currency-name {
        font-size: 2rem;
        font-weight: 700;
        color: #d4af37;
        font-family: 'Georgia', serif;
        letter-spacing: 2px;
    }
    
    .currency-full {
        font-size: 0.85rem;
        color: #8a7a4a;
        margin-left: 10px;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    .bias-indicator {
        display: flex;
        align-items: center;
        gap: 25px;
    }
    
    .bias-item {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .bias-label {
        font-size: 0.75rem;
        color: #8a7a4a;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .bias-arrow {
        font-size: 2.2rem;
        line-height: 1;
    }
    
    .bias-tag {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 3px 14px;
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
    
    /* Category Sections */
    .category-section {
        margin-top: 1.2rem;
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
    
    .indicator-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 6px 20px;
        margin-bottom: 1rem;
    }
    
    .indicator-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 3px 0;
    }
    
    .indicator-name {
        color: #b0a080;
        font-size: 0.85rem;
        font-weight: 400;
    }
    
    .indicator-arrow {
        font-size: 1.1rem;
        line-height: 1;
    }
    
    /* Summary Grid - Gold Accent */
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
        padding: 1.2rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .summary-card:hover {
        border-color: #d4af37;
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.05);
    }
    
    .summary-currency {
        font-size: 1.2rem;
        font-weight: 700;
        color: #d4af37;
        font-family: 'Georgia', serif;
    }
    
    .summary-arrow {
        font-size: 2rem;
        margin: 6px 0;
    }
    
    /* Management Cards */
    .management-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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
    
    .management-currency {
        font-weight: 700;
        font-size: 1.2rem;
        color: #d4af37;
        margin-bottom: 0.8rem;
        font-family: 'Georgia', serif;
    }
    
    /* Sidebar - Dark Luxury */
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
    
    /* Form elements - Dark Theme */
    .stSelectbox, .stTextInput, .stTextArea {
        background: #0a0a0a !important;
        color: #d4af37 !important;
    }
    
    div[data-baseweb="select"] {
        background: #0a0a0a !important;
        border-color: #2a2a1a !important;
    }
    
    div[data-baseweb="select"] > div {
        background: #0a0a0a !important;
        color: #d4af37 !important;
    }
    
    /* Buttons - Gold Theme */
    .stButton > button {
        background: linear-gradient(145deg, #d4af37, #b8941f) !important;
        color: #0a0a0a !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        font-family: 'Georgia', serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
        background: linear-gradient(145deg, #e0c050, #d4af37) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Dataframes */
    .stDataFrame {
        background: #0a0a0a !important;
        border-color: #2a2a1a !important;
    }
    
    .stDataFrame thead tr th {
        background: #141414 !important;
        color: #d4af37 !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
    }
    
    .stDataFrame tbody tr td {
        background: #0a0a0a !important;
        color: #b0a080 !important;
        border-color: #1a1a0a !important;
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
        padding: 0.8rem 2rem !important;
        font-family: 'Georgia', serif !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom: 2px solid #d4af37 !important;
    }
    
    /* Gold scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    ::-webkit-scrollbar-thumb {
        background: #d4af37;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #b8941f;
    }
    
    /* Status indicators */
    .updated-text {
        color: #5a4a2a;
        font-size: 0.7rem;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    .gold-text {
        color: #d4af37;
    }
    
    .dim-gold {
        color: #8a7a4a;
    }
    
    @media (max-width: 768px) {
        .summary-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .indicator-grid {
            grid-template-columns: 1fr;
        }
        .main-header {
            font-size: 2rem;
            letter-spacing: 4px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==================== DATA STORAGE ====================
DATA_FILE = "g8_currency_data.json"

CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'NZD']
CURRENCY_NAMES = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'JPY': 'Japanese Yen',
    'CAD': 'Canadian Dollar',
    'AUD': 'Australian Dollar',
    'CHF': 'Swiss Franc',
    'NZD': 'New Zealand Dollar'
}

BIAS_OPTIONS = ['Bullish', 'Rather Bullish', 'Neutral', 'Rather Bearish', 'Bearish']

# ==================== CATEGORIES ====================
CATEGORIES = [
    'Consumer',
    'Labor Market',
    'Inflation',
    'Housing Market',
    'Sentiment',
    'Markets',
    'Growth Activities'
]

def get_arrow(bias):
    arrows = {
        'Bullish': '⬆️',
        'Rather Bullish': '↗️',
        'Neutral': '➡️',
        'Rather Bearish': '↘️',
        'Bearish': '⬇️'
    }
    return arrows.get(bias, '➡️')

def get_bias_class(bias):
    classes = {
        'Bullish': 'bullish',
        'Rather Bullish': 'rather-bullish',
        'Neutral': 'neutral',
        'Rather Bearish': 'rather-bearish',
        'Bearish': 'bearish'
    }
    return classes.get(bias, 'neutral')

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
        data = {
            'biases': {},
            'indicators': {}
        }
        for currency in CURRENCIES:
            # Initialize biases
            data['biases'][currency] = {
                '5Y': {'bias': 'Neutral', 'last_updated': datetime.now().isoformat()},
                '3M': {'bias': 'Neutral', 'last_updated': datetime.now().isoformat()}
            }
            # Initialize indicators with empty categories
            data['indicators'][currency] = {}
            for category in CATEGORIES:
                data['indicators'][currency][category] = []
        save_data(data)
    return data

# ==================== MAIN APP ====================
def main():
    # Load data
    data = initialize_data()
    bias_data = data['biases']
    indicators_data = data['indicators']
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h1>💎 G8</h1>
            <p style="color: #8a7a4a; font-size: 0.8rem; letter-spacing: 3px; margin-top: -5px;">CURRENCY DASHBOARD</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 LEGEND")
        st.markdown("""
        <div style="background: #141414; padding: 15px; border-radius: 10px; border: 1px solid #1a1a0a;">
            <div style="display: flex; align-items: center; gap: 10px; padding: 3px 0;">
                <span style="font-size: 1.3rem;">⬆️</span> <span style="color: #b0a080;">Bullish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 3px 0;">
                <span style="font-size: 1.3rem;">↗️</span> <span style="color: #b0a080;">Rather Bullish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 3px 0;">
                <span style="font-size: 1.3rem;">➡️</span> <span style="color: #b0a080;">Neutral</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 3px 0;">
                <span style="font-size: 1.3rem;">↘️</span> <span style="color: #b0a080;">Rather Bearish</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 3px 0;">
                <span style="font-size: 1.3rem;">⬇️</span> <span style="color: #b0a080;">Bearish</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        bullish = sum(1 for c in CURRENCIES if 'Bullish' in bias_data[c]['5Y']['bias'])
        bearish = sum(1 for c in CURRENCIES if 'Bearish' in bias_data[c]['5Y']['bias'])
        neutral = len(CURRENCIES) - bullish - bearish
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<p style="color: #2ecc71; text-align: center; font-size: 1.5rem; font-weight: 700; margin: 0;">{bullish}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.7rem; margin: 0;">BULLISH</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p style="color: #d4af37; text-align: center; font-size: 1.5rem; font-weight: 700; margin: 0;">{neutral}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.7rem; margin: 0;">NEUTRAL</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<p style="color: #e74c3c; text-align: center; font-size: 1.5rem; font-weight: 700; margin: 0;">{bearish}</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8a7a4a; text-align: center; font-size: 0.7rem; margin: 0;">BEARISH</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption(f"💾 Data saved to: {DATA_FILE}")
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Tabs
    tab1, tab2 = st.tabs(["📊 DASHBOARD", "⚙️ MANAGEMENT"])
    
    # ==================== TAB 1: DASHBOARD ====================
    with tab1:
        st.markdown('<h1 class="main-header">G8 CURRENCY DASHBOARD</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">FUNDAMENTAL BIAS OVERVIEW • {datetime.now().strftime("%B %Y")}</p>', unsafe_allow_html=True)
        
        # Summary Grid
        st.markdown("### QUICK OVERVIEW")
        cols = st.columns(4)
        for idx, currency in enumerate(CURRENCIES):
            with cols[idx % 4]:
                bias = bias_data[currency]['5Y']['bias']
                arrow = get_arrow(bias)
                st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-currency">{currency}</div>
                    <div class="summary-arrow">{arrow}</div>
                    <div><span class="bias-tag {get_bias_class(bias)}">{bias}</span></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        
        # Detailed Currency View with Indicators
        st.markdown("### DETAILED CURRENCY VIEW")
        
        selected_currency = st.selectbox("Select Currency", CURRENCIES, key="currency_select")
        
        if selected_currency:
            currency = selected_currency
            bias_5y = bias_data[currency]['5Y']['bias']
            bias_3m = bias_data[currency]['3M']['bias']
            arrow_5y = get_arrow(bias_5y)
            arrow_3m = get_arrow(bias_3m)
            
            # Currency Card
            st.markdown(f"""
            <div class="currency-card">
                <div class="currency-header">
                    <div>
                        <span class="currency-name">{currency}</span>
                        <span class="currency-full">{CURRENCY_NAMES.get(currency, '')}</span>
                    </div>
                    <div class="bias-indicator">
                        <div class="bias-item">
                            <span class="bias-label">5Y</span>
                            <span class="bias-arrow">{arrow_5y}</span>
                            <span class="bias-tag {get_bias_class(bias_5y)}">{bias_5y}</span>
                        </div>
                        <div class="bias-item">
                            <span class="bias-label">3M</span>
                            <span class="bias-arrow">{arrow_3m}</span>
                            <span class="bias-tag {get_bias_class(bias_3m)}">{bias_3m}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display Indicators by Category
            st.markdown("### ECONOMIC INDICATORS")
            
            currency_indicators = indicators_data.get(currency, {})
            
            for category in CATEGORIES:
                indicators = currency_indicators.get(category, [])
                
                # Calculate category bias based on individual indicator biases
                if indicators:
                    # Show category title with count
                    st.markdown(f'<div class="category-title">{category.upper()} <span style="color: #5a4a2a; font-size: 0.7rem;">({len(indicators)} indicators)</span></div>', unsafe_allow_html=True)
                    
                    # Display indicators in grid
                    cols = st.columns(3)
                    for idx, indicator in enumerate(indicators):
                        # Each indicator has a bias assigned
                        ind_bias = indicator.get('bias', 'Neutral')
                        arrow = get_arrow(ind_bias)
                        name = indicator.get('name', '')
                        
                        with cols[idx % 3]:
                            st.markdown(f"""
                            <div class="indicator-item">
                                <span class="indicator-name">{name}</span>
                                <span class="indicator-arrow">{arrow}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
    
    # ==================== TAB 2: MANAGEMENT ====================
    with tab2:
        st.markdown('<h1 class="main-header">⚙️ MANAGEMENT</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">CONFIGURE BIASES & ECONOMIC INDICATORS</p>', unsafe_allow_html=True)
        
        # Management tabs
        mgmt_tab1, mgmt_tab2 = st.tabs(["📈 Bias Settings", "📋 Indicator Management"])
        
        # ==================== BIAS SETTINGS ====================
        with mgmt_tab1:
            st.markdown("### SET CURRENCY BIASES")
            st.markdown('<p style="color: #8a7a4a; font-size: 0.85rem;">Configure 5-Year and 3-Month trends for each currency</p>', unsafe_allow_html=True)
            
            with st.form("bias_form"):
                updated_biases = {}
                
                cols = st.columns(2)
                for idx, currency in enumerate(CURRENCIES):
                    col = cols[idx % 2]
                    with col:
                        st.markdown(f"""
                        <div class="management-card">
                            <div class="management-currency">{currency}</div>
                        """, unsafe_allow_html=True)
                        
                        current_5y = bias_data[currency]['5Y']['bias']
                        current_3m = bias_data[currency]['3M']['bias']
                        
                        bias_5y = st.selectbox(
                            "5Y Trend",
                            BIAS_OPTIONS,
                            index=BIAS_OPTIONS.index(current_5y),
                            key=f"{currency}_5y_mgmt"
                        )
                        
                        bias_3m = st.selectbox(
                            "3M Trend",
                            BIAS_OPTIONS,
                            index=BIAS_OPTIONS.index(current_3m),
                            key=f"{currency}_3m_mgmt"
                        )
                        
                        updated_biases[currency] = {
                            '5Y': {'bias': bias_5y, 'last_updated': datetime.now().isoformat()},
                            '3M': {'bias': bias_3m, 'last_updated': datetime.now().isoformat()}
                        }
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                submitted_biases = st.form_submit_button("💾 SAVE ALL BIASES", use_container_width=True)
                
                if submitted_biases:
                    for currency in updated_biases:
                        bias_data[currency]['5Y'] = updated_biases[currency]['5Y']
                        bias_data[currency]['3M'] = updated_biases[currency]['3M']
                    
                    data['biases'] = bias_data
                    save_data(data)
                    st.success("✅ All biases saved successfully!")
                    st.balloons()
        
        # ==================== INDICATOR MANAGEMENT ====================
        with mgmt_tab2:
            st.markdown("### MANAGE ECONOMIC INDICATORS")
            st.markdown('<p style="color: #8a7a4a; font-size: 0.85rem;">Add or remove economic indicators for each currency</p>', unsafe_allow_html=True)
            
            # Currency selector for indicator management
            mgmt_currency = st.selectbox("Select Currency", CURRENCIES, key="mgmt_currency")
            
            if mgmt_currency:
                st.markdown(f'<h3 style="color: #d4af37; font-family: Georgia, serif;">{mgmt_currency} - {CURRENCY_NAMES.get(mgmt_currency, "")}</h3>', unsafe_allow_html=True)
                
                # Category selector
                selected_category = st.selectbox("Select Category", CATEGORIES, key="category_select")
                
                # Display current indicators in category
                current_indicators = indicators_data[mgmt_currency].get(selected_category, [])
                
                st.markdown(f'<p style="color: #8a7a4a; font-size: 0.85rem;">Current indicators in <span style="color: #d4af37;">{selected_category}</span>: {len(current_indicators)}</p>', unsafe_allow_html=True)
                
                # Show existing indicators with remove option
                if current_indicators:
                    for idx, indicator in enumerate(current_indicators):
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.text(f"📌 {indicator.get('name', '')}")
                        with col2:
                            bias = indicator.get('bias', 'Neutral')
                            arrow = get_arrow(bias)
                            st.text(f"{arrow} {bias}")
                        with col3:
                            if st.button("🗑️", key=f"remove_{mgmt_currency}_{selected_category}_{idx}"):
                                current_indicators.pop(idx)
                                indicators_data[mgmt_currency][selected_category] = current_indicators
                                data['indicators'] = indicators_data
                                save_data(data)
                                st.rerun()
                else:
                    st.markdown('<p style="color: #5a4a2a; font-style: italic;">No indicators in this category yet</p>', unsafe_allow_html=True)
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                
                # Add new indicator
                st.markdown("#### ➕ ADD NEW INDICATOR")
                
                with st.form("add_indicator_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        indicator_name = st.text_input("Indicator Name", placeholder="e.g., Retail Sales MoM", key="indicator_name")
                    with col2:
                        indicator_bias = st.selectbox(
                            "Bias",
                            BIAS_OPTIONS,
                            key="indicator_bias"
                        )
                    
                    submitted_indicator = st.form_submit_button("➕ ADD INDICATOR")
                    
                    if submitted_indicator and indicator_name:
                        # Add to current category
                        new_indicator = {
                            'name': indicator_name,
                            'bias': indicator_bias,
                            'added': datetime.now().isoformat()
                        }
                        
                        current_indicators.append(new_indicator)
                        indicators_data[mgmt_currency][selected_category] = current_indicators
                        data['indicators'] = indicators_data
                        save_data(data)
                        st.success(f"✅ Added '{indicator_name}' to {selected_category}!")
                        st.rerun()
                    elif submitted_indicator:
                        st.warning("Please enter an indicator name")
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                
                # Quick add template
                with st.expander("📋 Quick Add Template Indicators"):
                    st.markdown("""
                    <div style="background: #141414; padding: 1rem; border-radius: 8px; border: 1px solid #1a1a0a;">
                        <p style="color: #8a7a4a; font-size: 0.85rem;">Common indicators by category:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    template_indicators = {
                        'Consumer': ['Retail Sales MoM', 'Retail Sales YoY', 'Consumer Confidence', 'Personal Spending'],
                        'Labor Market': ['Unemployment Rate', 'Non-Farm Payrolls', 'Average Hourly Earnings', 'Jobless Claims'],
                        'Inflation': ['CPI YoY', 'Core CPI YoY', 'PPI YoY', 'PCE Price Index'],
                        'Housing Market': ['Housing Starts', 'Building Permits', 'Existing Home Sales', 'Case-Shiller Index'],
                        'Sentiment': ['Consumer Confidence', 'Business Confidence', 'PMI', 'IFO Business Climate'],
                        'Markets': ['S&P 500', '10Y Treasury', 'Dollar Index', 'Commodity Index'],
                        'Growth Activities': ['GDP Growth', 'Industrial Production', 'Capacity Utilization', 'Trade Balance']
                    }
                    
                    for cat, indicators in template_indicators.items():
                        st.markdown(f'<p style="color: #d4af37; font-size: 0.8rem; margin-top: 0.5rem;">{cat}:</p>', unsafe_allow_html=True)
                        cols = st.columns(4)
                        for idx, ind in enumerate(indicators):
                            with cols[idx % 4]:
                                if st.button(f"+ {ind}", key=f"template_{cat}_{ind}"):
                                    # Add to current category if matches
                                    if cat == selected_category:
                                        new_ind = {
                                            'name': ind,
                                            'bias': 'Neutral',
                                            'added': datetime.now().isoformat()
                                        }
                                        current_indicators.append(new_ind)
                                        indicators_data[mgmt_currency][selected_category] = current_indicators
                                        data['indicators'] = indicators_data
                                        save_data(data)
                                        st.success(f"Added '{ind}' to {selected_category}!")
                                        st.rerun()
                                    else:
                                        st.info(f"Switch to '{cat}' category to add this indicator")

if __name__ == "__main__":
    main()