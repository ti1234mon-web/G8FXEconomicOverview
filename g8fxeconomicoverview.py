import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="G8 Currency Dashboard",
    page_icon="💹",
    layout="wide"
)

# Custom CSS for clean dashboard
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1a1a2e;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    .currency-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e8e8e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .currency-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .currency-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .currency-full {
        font-size: 0.85rem;
        color: #888;
        margin-left: 8px;
        font-weight: 400;
    }
    .arrow-display {
        display: flex;
        align-items: center;
        gap: 30px;
    }
    .arrow-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .arrow-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #666;
    }
    .arrow-big {
        font-size: 2.5rem;
        line-height: 1;
    }
    .bias-tag {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 12px;
        display: inline-block;
    }
    .bullish-bg { background: #2ecc71; color: white; }
    .rather-bullish-bg { background: #82e0aa; color: white; }
    .neutral-bg { background: #f39c12; color: white; }
    .rather-bearish-bg { background: #f5b7b1; color: white; }
    .bearish-bg { background: #e74c3c; color: white; }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 1.5rem 0;
    }
    .summary-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e8e8e8;
    }
    .summary-currency {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .summary-arrow {
        font-size: 2rem;
        margin: 4px 0;
    }
    .management-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .management-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e8e8e8;
    }
    .management-currency {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
    }
    @media (max-width: 768px) {
        .summary-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==================== DATA STORAGE ====================
DATA_FILE = "g8_currency_bias_data.json"

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
        'Bullish': 'bullish-bg',
        'Rather Bullish': 'rather-bullish-bg',
        'Neutral': 'neutral-bg',
        'Rather Bearish': 'rather-bearish-bg',
        'Bearish': 'bearish-bg'
    }
    return classes.get(bias, 'neutral-bg')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def initialize_bias_data():
    data = load_data()
    if not data:
        for currency in CURRENCIES:
            data[currency] = {
                '5Y': {'bias': 'Neutral', 'last_updated': datetime.now().isoformat()},
                '3M': {'bias': 'Neutral', 'last_updated': datetime.now().isoformat()}
            }
        save_data(data)
    return data

# ==================== MAIN APP ====================
def main():
    # Load data
    bias_data = initialize_bias_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="font-size: 2rem; margin: 0;">💹 G8</h1>
            <p style="color: #666; margin: 0;">Currency Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📊 Legend")
        st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
            <div style="display: flex; align-items: center; gap: 10px; padding: 2px 0;">
                <span style="font-size: 1.5rem;">⬆️</span> Bullish
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 2px 0;">
                <span style="font-size: 1.5rem;">↗️</span> Rather Bullish
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 2px 0;">
                <span style="font-size: 1.5rem;">➡️</span> Neutral
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 2px 0;">
                <span style="font-size: 1.5rem;">↘️</span> Rather Bearish
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 2px 0;">
                <span style="font-size: 1.5rem;">⬇️</span> Bearish
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        bullish = sum(1 for c in CURRENCIES if 'Bullish' in bias_data[c]['5Y']['bias'])
        bearish = sum(1 for c in CURRENCIES if 'Bearish' in bias_data[c]['5Y']['bias'])
        neutral = len(CURRENCIES) - bullish - bearish
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🟢 Bullish", bullish)
        col2.metric("🟡 Neutral", neutral)
        col3.metric("🔴 Bearish", bearish)
        
        st.markdown("---")
        st.caption(f"Data saved to: {DATA_FILE}")
    
    # Tabs
    tab1, tab2 = st.tabs(["📊 Dashboard", "⚙️ Bias Management"])
    
    # ==================== TAB 1: DASHBOARD ====================
    with tab1:
        st.markdown('<h1 class="main-header">G8 Currency Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>', unsafe_allow_html=True)
        
        # Summary Grid - All Currencies Overview
        st.markdown("### Quick Overview")
        
        cols = st.columns(4)
        for idx, currency in enumerate(CURRENCIES[:4]):
            with cols[idx]:
                bias = bias_data[currency]['5Y']['bias']
                arrow = get_arrow(bias)
                st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-currency">{currency}</div>
                    <div class="summary-arrow">{arrow}</div>
                    <div><span class="bias-tag {get_bias_class(bias)}">{bias}</span></div>
                </div>
                """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        for idx, currency in enumerate(CURRENCIES[4:]):
            with cols[idx]:
                bias = bias_data[currency]['5Y']['bias']
                arrow = get_arrow(bias)
                st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-currency">{currency}</div>
                    <div class="summary-arrow">{arrow}</div>
                    <div><span class="bias-tag {get_bias_class(bias)}">{bias}</span></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed Currency Cards
        st.markdown("### Detailed Currency View")
        
        # Currency selector for detailed view
        selected_currency = st.selectbox("Select Currency", CURRENCIES, key="currency_selector")
        
        # Display selected currency card
        currency = selected_currency
        bias_5y = bias_data[currency]['5Y']['bias']
        bias_3m = bias_data[currency]['3M']['bias']
        arrow_5y = get_arrow(bias_5y)
        arrow_3m = get_arrow(bias_3m)
        
        st.markdown(f"""
        <div class="currency-card">
            <div class="currency-header">
                <div>
                    <span class="currency-name">{currency}</span>
                    <span class="currency-full">{CURRENCY_NAMES.get(currency, '')}</span>
                </div>
                <div class="arrow-display">
                    <div class="arrow-item">
                        <span class="arrow-label">5Y Trend</span>
                        <span class="arrow-big">{arrow_5y}</span>
                        <span class="bias-tag {get_bias_class(bias_5y)}">{bias_5y}</span>
                    </div>
                    <div class="arrow-item">
                        <span class="arrow-label">3M Trend</span>
                        <span class="arrow-big">{arrow_3m}</span>
                        <span class="bias-tag {get_bias_class(bias_3m)}">{bias_3m}</span>
                    </div>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 0.8rem; color: #999;">
                Last updated: {bias_data[currency]['5Y']['last_updated'][:10]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # All currencies in a table
        with st.expander("📋 View All Currencies Summary"):
            table_data = []
            for c in CURRENCIES:
                table_data.append({
                    'Currency': c,
                    '5Y Arrow': get_arrow(bias_data[c]['5Y']['bias']),
                    '5Y Bias': bias_data[c]['5Y']['bias'],
                    '3M Arrow': get_arrow(bias_data[c]['3M']['bias']),
                    '3M Bias': bias_data[c]['3M']['bias'],
                    'Last Updated': bias_data[c]['5Y']['last_updated'][:10]
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ==================== TAB 2: BIAS MANAGEMENT ====================
    with tab2:
        st.markdown('<h1 class="main-header">⚙️ Bias Management</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Set 5-Year and 3-Month biases for each currency</p>', unsafe_allow_html=True)
        
        # Management form
        with st.form("bias_management_form"):
            st.markdown("### Update Currency Biases")
            
            updated_data = {}
            
            # Create 2 columns for better layout
            cols = st.columns(2)
            
            for idx, currency in enumerate(CURRENCIES):
                col = cols[idx % 2]
                with col:
                    st.markdown(f"**{currency} - {CURRENCY_NAMES.get(currency, '')}**")
                    
                    # Get current biases
                    current_5y = bias_data[currency]['5Y']['bias']
                    current_3m = bias_data[currency]['3M']['bias']
                    
                    # 5Y Bias dropdown
                    bias_5y = st.selectbox(
                        "5Y Trend",
                        BIAS_OPTIONS,
                        index=BIAS_OPTIONS.index(current_5y),
                        key=f"{currency}_5y_mgmt"
                    )
                    
                    # 3M Bias dropdown
                    bias_3m = st.selectbox(
                        "3M Trend",
                        BIAS_OPTIONS,
                        index=BIAS_OPTIONS.index(current_3m),
                        key=f"{currency}_3m_mgmt"
                    )
                    
                    # Store updated data
                    updated_data[currency] = {
                        '5Y': {'bias': bias_5y, 'last_updated': datetime.now().isoformat()},
                        '3M': {'bias': bias_3m, 'last_updated': datetime.now().isoformat()}
                    }
                    
                    st.markdown("---")
            
            # Submit button
            submitted = st.form_submit_button("💾 Save All Biases", use_container_width=True)
            
            if submitted:
                # Update data
                for currency in updated_data:
                    bias_data[currency]['5Y'] = updated_data[currency]['5Y']
                    bias_data[currency]['3M'] = updated_data[currency]['3M']
                
                save_data(bias_data)
                st.success("✅ All biases saved successfully!")
                st.balloons()
        
        # Display current saved biases
        st.markdown("---")
        st.markdown("### 📊 Current Saved Biases")
        
        current_data = []
        for currency in CURRENCIES:
            current_data.append({
                'Currency': currency,
                '5Y Bias': bias_data[currency]['5Y']['bias'],
                '5Y Arrow': get_arrow(bias_data[currency]['5Y']['bias']),
                '3M Bias': bias_data[currency]['3M']['bias'],
                '3M Arrow': get_arrow(bias_data[currency]['3M']['bias']),
                'Updated': bias_data[currency]['5Y']['last_updated'][:10]
            })
        
        df_current = pd.DataFrame(current_data)
        st.dataframe(df_current, use_container_width=True, hide_index=True)
        
        # Export/Import section
        with st.expander("🔧 Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Export Data"):
                    json_str = json.dumps(bias_data, indent=4)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name=f"g8_biases_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            
            with col2:
                uploaded = st.file_uploader("📥 Import JSON", type=['json'])
                if uploaded is not None:
                    try:
                        imported = json.load(uploaded)
                        save_data(imported)
                        st.success("Data imported! Refreshing...")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            if st.button("🔄 Reset All to Neutral", type="secondary"):
                for currency in CURRENCIES:
                    bias_data[currency]['5Y']['bias'] = 'Neutral'
                    bias_data[currency]['5Y']['last_updated'] = datetime.now().isoformat()
                    bias_data[currency]['3M']['bias'] = 'Neutral'
                    bias_data[currency]['3M']['last_updated'] = datetime.now().isoformat()
                save_data(bias_data)
                st.warning("All biases reset to Neutral!")
                st.rerun()

if __name__ == "__main__":
    main()