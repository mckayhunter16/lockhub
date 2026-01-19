# -*- coding: utf-8 -*-
"""
LockHub - Garrett's Lock Tracker
A Streamlit app with that sweet 90s internet aesthetic.
"""

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="🔒 LockHub 🔒",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 90s RETRO CSS
# ============================================================================

st.markdown('<meta charset="UTF-8">', unsafe_allow_html=True)

st.markdown("""
<style>
    /* Import a retro font */
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=DotGothic16&display=swap');
    
    /* Main background - classic tiled look */
    .stApp {
        background-color: #008080;
        background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23006666' fill-opacity='0.4'%3E%3Cpath d='M0 0h20v20H0V0zm20 20h20v20H20V20z'/%3E%3C/g%3E%3C/svg%3E");
    }
    
    /* Mobile-first main container */
    .main .block-container {
        padding-top: 0.5rem;
        max-width: 100%;
        background-color: #c0c0c0;
        border: 3px outset #ffffff;
        box-shadow: 3px 3px 0px #000000;
        margin: 10px auto;
        padding: 10px;
    }
    
    /* Retro header - DotGothic16 - Mobile first */
    .retro-header {
        font-family: 'DotGothic16', sans-serif;
        font-size: 1.8rem;
        text-align: center;
        color: #000080;
        text-shadow: 2px 2px #ffff00;
        padding: 10px;
        background: linear-gradient(180deg, #ffff00 0%, #ff8c00 100%);
        border: 3px outset #ffffff;
        margin-bottom: 10px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    
    /* Desktop header */
    @media (min-width: 768px) {
        .retro-header {
            font-size: 3rem;
            padding: 15px;
            letter-spacing: 3px;
        }
        
        .main .block-container {
            padding-top: 1rem;
            max-width: 1000px;
            padding: 20px;
            margin: 20px auto;
            box-shadow: 5px 5px 0px #000000;
        }
    }
    
    .retro-subheader {
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        text-align: center;
        color: #000000;
        background-color: #ffff00;
        padding: 5px;
        border: 2px inset #808080;
        margin-bottom: 20px;
    }
    
    /* Marquee effect */
    .marquee {
        background-color: #000080;
        color: #00ff00;
        font-family: 'VT323', monospace;
        font-size: 1rem;
        padding: 8px;
        border: 2px inset #808080;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    @media (min-width: 768px) {
        .marquee {
            font-size: 1.2rem;
        }
    }
    
    .marquee span {
        display: inline-block;
        animation: marquee 35s linear infinite;
        white-space: nowrap;
        padding-left: 0%;
    }
    
    @keyframes marquee {
        0% { transform: translateX(20%); }
        100% { transform: translateX(-66%); }
    }
    
    /* Stat boxes - Mobile first */
    .stat-box {
        background-color: #c0c0c0;
        border: 3px outset #ffffff;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .stat-box h2 {
        font-family: 'VT323', monospace;
        font-size: 2.2rem;
        margin: 0;
        color: #000080;
    }
    
    .stat-box p {
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        margin: 5px 0 0 0;
        color: #000000;
    }
    
    .stat-box small {
        font-family: 'VT323', monospace;
        margin-top: 5px;
        font-size: 0.8rem;
        color: #000000;
    }
    
    @media (min-width: 768px) {
        .stat-box {
            padding: 15px;
            min-height: 120px;
        }
        
        .stat-box h2 {
            font-size: 2.8rem;
        }
        
        .stat-box p {
            font-size: 1.2rem;
        }
        
        .stat-box small {
            font-size: 0.85rem;
        }
    }
    
    .stat-box.win {
        background-color: #00ff00;
    }
    
    .stat-box.win h2, .stat-box.win p, .stat-box.win small {
        color: #003300;
    }
    
    .stat-box.lose {
        background-color: #ff0000;
    }
    
    .stat-box.lose h2, .stat-box.lose p, .stat-box.lose small {
        color: #ffffff;
    }
    
    /* Section headers - Mobile first */
    .section-header {
        font-family: 'Press Start 2P', cursive;
        font-size: 0.6rem;
        background: linear-gradient(90deg, #000080 0%, #0000ff 100%);
        color: #ffffff;
        padding: 8px 10px;
        border: 2px outset #ffffff;
        margin: 15px 0 10px 0;
    }
    
    @media (min-width: 768px) {
        .section-header {
            font-size: 0.9rem;
            padding: 8px 15px;
            margin: 20px 0 10px 0;
        }
    }
    
    /* Retro buttons */
    .stButton > button {
        font-family: 'VT323', monospace !important;
        font-size: 1.1rem !important;
        background-color: #c0c0c0 !important;
        border: 3px outset #ffffff !important;
        color: #000000 !important;
        padding: 8px 15px !important;
        cursor: pointer !important;
        box-shadow: 2px 2px 0px #000000 !important;
        width: 100% !important;
    }
    
    @media (min-width: 768px) {
        .stButton > button {
            font-size: 1.2rem !important;
            padding: 10px 20px !important;
        }
    }
    
    .stButton > button:hover {
        background-color: #a0a0a0 !important;
    }
    
    .stButton > button:active {
        border: 3px inset #ffffff !important;
        box-shadow: none !important;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        font-family: 'VT323', monospace !important;
        font-size: 1rem !important;
        background-color: #ffffff !important;
        border: 2px inset #808080 !important;
    }
    
    @media (min-width: 768px) {
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div {
            font-size: 1.1rem !important;
        }
    }
    
    /* Tabs - retro folder style - Mobile first */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: #c0c0c0;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'VT323', monospace;
        font-size: 0.9rem;
        background-color: #c0c0c0;
        border: 2px outset #ffffff;
        border-bottom: none;
        padding: 8px 12px;
        color: #000000;
    }
    
    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 1.1rem;
            padding: 10px 20px;
        }
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border: 2px inset #808080;
        border-bottom: 2px solid #ffffff;
    }
    
    /* Table styling */
    .stDataFrame {
        border: 3px inset #808080;
    }
    
    /* Lock entry styling - Mobile first */
    .lock-entry {
        background-color: #ffffff;
        border: 2px inset #808080;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'VT323', monospace;
        font-size: 1rem;
        color: #000000;
    }
    
    @media (min-width: 768px) {
        .lock-entry {
            padding: 15px;
            font-size: 1.1rem;
        }
    }
    
    .lock-entry strong {
        color: #000080;
    }
    
    .lock-entry span {
        color: #000000;
    }
    
    /* Sidebar retro styling - Hidden on mobile by default */
    [data-testid="stSidebar"] {
        background-color: #808080;
        border-right: 3px outset #ffffff;
    }
    
    [data-testid="stSidebar"] .block-container {
        background-color: #c0c0c0;
        border: 2px inset #808080;
        padding: 10px;
        margin: 10px;
    }
    
    /* Guestbook style info boxes - Mobile first */
    .info-box {
        background-color: #ffffcc;
        border: 2px solid #000000;
        padding: 8px;
        font-family: 'VT323', monospace;
        font-size: 1rem;
        margin: 8px 0;
        color: #000000;
    }
    
    .info-box b, .info-box strong {
        color: #000000;
    }
    
    @media (min-width: 768px) {
        .info-box {
            padding: 10px;
            font-size: 1.1rem;
            margin: 10px 0;
        }
    }
    
    /* Red divider */
    .red-divider {
        height: 5px;
        background: #ff0000;
        margin: 10px 0;
    }
    
    @media (min-width: 768px) {
        .red-divider {
            margin: 15px 0;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Mobile column override - stack stats vertically */
    @media (max-width: 767px) {
        [data-testid="column"] {
            width: 50% !important;
            flex: 0 0 50% !important;
            min-width: 50% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONSTANTS
# ============================================================================

CONFIDENCE_LEVELS = [
    "Fuck It, I'm Bored",
    "Feeling Good",
    "You're Welcome for the Free Money"
]

BET_TYPES = ["Spread", "Moneyline", "Over/Under"]

PROV1_PRICE = 4.75
LABATT_BLUE_PRICE = 0.95

GLOCK_PASSWORD = "glock"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_gsheet_connection():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

def load_locks_data(conn):
    try:
        df = conn.read(worksheet="Locks", usecols=list(range(11)), ttl=5)
        if df is None or df.empty:
            return pd.DataFrame(columns=[
                'id', 'game', 'bet_type', 'pick', 'confidence', 
                'status', 'result', 'created_at', 'settled_at', 'notes', 'odds'
            ])
        # Ensure odds column exists
        if 'odds' not in df.columns:
            df['odds'] = None
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=[
            'id', 'game', 'bet_type', 'pick', 'confidence', 
            'status', 'result', 'created_at', 'settled_at', 'notes', 'odds'
        ])

def save_lock(conn, lock_data):
    try:
        existing_df = load_locks_data(conn)
        new_id = 1 if existing_df.empty else int(existing_df['id'].max()) + 1
        lock_data['id'] = new_id
        new_row = pd.DataFrame([lock_data])
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        conn.update(worksheet="Locks", data=updated_df)
        return True
    except Exception as e:
        st.error(f"Error saving lock: {e}")
        return False

def update_locks(conn, df):
    try:
        conn.update(worksheet="Locks", data=df)
        return True
    except Exception as e:
        st.error(f"Error updating locks: {e}")
        return False

def calculate_streak(df):
    settled = df[df['result'].isin(['Win', 'Loss'])].copy()
    if settled.empty:
        return 0
    settled = settled.sort_values('settled_at', ascending=False)
    streak = 0
    for _, row in settled.iterrows():
        if row['result'] == 'Win':
            streak += 1
        else:
            break
    return streak

def calculate_fade_index(df):
    """Calculate profit from fading every lock at $10, using actual odds."""
    settled = df[df['result'].isin(['Win', 'Loss', 'Push'])]
    if settled.empty:
        return 0.0
    profit = 0.0
    for _, row in settled.iterrows():
        # Get odds, default to -110 if not specified
        odds = row.get('odds')
        try:
            odds = int(float(odds)) if pd.notna(odds) and odds != '' else -110
        except:
            odds = -110
        
        if row['result'] == 'Loss':
            # Garrett lost, so fading wins
            # Calculate winnings based on the opposite side (assume same odds)
            if odds < 0:
                # If Garrett bet favorite at -110, fading wins $9.09 on $10
                profit += 10 * (100 / abs(odds))
            else:
                # If Garrett bet underdog at +150, fading (favorite) wins less
                profit += 10 * (100 / (odds + 100)) if odds > 0 else 9.09
        elif row['result'] == 'Win':
            # Garrett won, so fading loses the $10 bet
            profit -= 10.00
    return profit

def convert_to_units(amount):
    return {
        'prov1_balls': amount / PROV1_PRICE,
        'labatt_blues': amount / LABATT_BLUE_PRICE
    }

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header - clickable to reload
st.markdown('''
<a href="." target="_self" style="text-decoration: none;">
    <div class="retro-header">🔒 LOCKHUB 🔒</div>
</a>
''', unsafe_allow_html=True)

# Marquee
st.markdown("""
<div class="marquee">
    <span>★ The official home of G Locks. Past performance does not guarantee future results. Good luck, degenerate! ★ The official home of G Locks. Past performance does not guarantee future results. Good luck, degenerate! ★ The official home of G Locks. Past performance does not guarantee future results. Good luck, degenerate! ★</span>
</div>
""", unsafe_allow_html=True)

conn = get_gsheet_connection()

if conn is None:
    st.error("⚠️ DATABASE CONNECTION ERROR - Please refresh page")
    st.stop()

df = load_locks_data(conn)

# Stats
st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

pending_locks = len(df[df['status'] == 'Active'])
settled_locks = len(df[df['result'].isin(['Win', 'Loss', 'Push'])])
wins = len(df[df['result'] == 'Win'])
losses = len(df[df['result'] == 'Loss'])
pushes = len(df[df['result'] == 'Push'])
win_rate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
streak = calculate_streak(df)
fade_index = calculate_fade_index(df)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <h2>{pending_locks}</h2>
        <p>PENDING</p>
        <h2>{settled_locks}</h2>
        <p>SETTLED</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    box_class = "win" if win_rate >= 50 else "lose"
    st.markdown(f"""
    <div class="stat-box {box_class}">
        <h2>{win_rate:.1f}%</h2>
        <p>WIN PERCENTAGE</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <h2>{streak}</h2>
        <p>WIN STREAK</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fade_class = "win" if fade_index > 0 else "lose"
    st.markdown(f"""
    <div class="stat-box {fade_class}">
        <h2>${fade_index:+.2f}</h2>
        <p>FADE INDEX</p>
        <small>How much you'd pocket if you faded every G Lock ($10/bet)</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 ACTIVE", "🏛️ VAULT", "💰 CONVERTER", "🔐 ENTRY", "📸 SHARE"])

# ----------------------------------------------------------------------------
# TAB 1: ACTIVE LOCKS
# ----------------------------------------------------------------------------

with tab1:
    st.markdown('<div class="section-header">📋 ACTIVE LOCKS</div>', unsafe_allow_html=True)
    
    active_locks = df[df['status'] == 'Active']
    
    if active_locks.empty:
        st.markdown("""
        <div class="info-box">
            <center>
            <br>
            😴 No active locks right now... 😴<br>
            <small>Garrett must be conserving his energy</small>
            <br><br>
            </center>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, lock in active_locks.iterrows():
            st.markdown(f"""
            <div class="lock-entry">
                <strong>🏈 GAME:</strong> {lock['game']}<br>
                <strong>🎯 PICK:</strong> {lock['pick']}<br>
                <strong>📊 TYPE:</strong> {lock['bet_type']}<br>
                <strong>💪 CONFIDENCE:</strong> {lock['confidence']}<br>
                <strong>⏳ STATUS:</strong> <span style="color: #cc6600; font-weight: bold;">PENDING...</span>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB 2: THE VAULT
# ----------------------------------------------------------------------------

with tab2:
    st.markdown('<div class="section-header">🏛️ THE VAULT - Historical Records</div>', unsafe_allow_html=True)
    
    settled_locks = df[df['result'].isin(['Win', 'Loss', 'Push'])]
    
    if settled_locks.empty:
        st.markdown("""
        <div class="info-box">
            <center>
            <br>
            📭 The Vault is empty! 📭<br>
            <small>No locks have been settled yet</small>
            <br><br>
            </center>
        </div>
        """, unsafe_allow_html=True)
    else:
        settled_locks = settled_locks.sort_values('settled_at', ascending=False)
        
        for _, lock in settled_locks.iterrows():
            if lock['result'] == 'Win':
                result_color = "#006600"
                border_color = "#00cc00"
                result_text = "✅ WIN ✅"
            elif lock['result'] == 'Loss':
                result_color = "#cc0000"
                border_color = "#ff0000"
                result_text = "❌ LOSS ❌"
            else:
                result_color = "#cc9900"
                border_color = "#ffcc00"
                result_text = "🤷 PUSH 🤷"
            
            st.markdown(f"""
            <div class="lock-entry" style="border-left: 5px solid {border_color};">
                <strong>🏈 GAME:</strong> {lock['game']}<br>
                <strong>🎯 PICK:</strong> {lock['pick']}<br>
                <strong>📊 TYPE:</strong> {lock['bet_type']}<br>
                <strong>💪 CONFIDENCE:</strong> {lock['confidence']}<br>
                <strong>🏆 RESULT:</strong> <span style="color: {result_color}; font-weight: bold;">{result_text}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Stats by confidence
        st.markdown('<div class="section-header">📊 PERFORMANCE BY CONFIDENCE</div>', unsafe_allow_html=True)
        
        for level in CONFIDENCE_LEVELS:
            level_locks = settled_locks[settled_locks['confidence'] == level]
            if not level_locks.empty:
                level_wins = len(level_locks[level_locks['result'] == 'Win'])
                level_losses = len(level_locks[level_locks['result'] == 'Loss'])
                level_total = level_wins + level_losses
                level_pct = (level_wins / level_total * 100) if level_total > 0 else 0
                
                emoji = "🤷" if level == "Fuck It, I'm Bored" else ("😎" if level == "Feeling Good" else "💰")
                st.markdown(f"""
                <div class="info-box">
                    {emoji} <b>{level}</b>: {level_wins}W - {level_losses}L ({level_pct:.1f}%)
                </div>
                """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB 5: SHARE STATS
# ----------------------------------------------------------------------------

with tab5:
    st.markdown('<div class="section-header">📸 SHARE STATS</div>', unsafe_allow_html=True)
    
    # Determine colors based on fade index
    fade_bg = "#00ff00" if fade_index > 0 else "#ff0000"
    fade_text = "#003300" if fade_index > 0 else "#ffffff"
    
    # Generate the share card HTML with inline styles on single lines
    st.markdown(f'''<div style="background: linear-gradient(135deg, #008080 0%, #004040 100%); border: 4px outset #ffffff; padding: 20px; max-width: 400px; margin: 20px auto; box-shadow: 5px 5px 0px #000000;">
<div style="background: linear-gradient(180deg, #ffff00 0%, #ff8c00 100%); border: 3px outset #ffffff; padding: 10px; text-align: center; margin-bottom: 15px;">
<span style="font-family: DotGothic16, sans-serif; font-size: 1.5rem; color: #000080; text-shadow: 1px 1px #ffff00;">🔒 LOCKHUB 🔒</span>
</div>
<div style="background-color: #c0c0c0; border: 3px outset #ffffff; padding: 15px; margin-bottom: 10px; text-align: center;">
<div style="font-family: VT323, monospace; font-size: 2.5rem; color: #000080;">{win_rate:.1f}%</div>
<div style="font-family: VT323, monospace; font-size: 1rem; color: #000000;">WIN PERCENTAGE</div>
</div>
<div style="background-color: #c0c0c0; border: 3px outset #ffffff; padding: 15px; margin-bottom: 10px; text-align: center;">
<div style="font-family: VT323, monospace; font-size: 2.5rem; color: #000080;">{streak} 🔥</div>
<div style="font-family: VT323, monospace; font-size: 1rem; color: #000000;">WIN STREAK</div>
</div>
<div style="background-color: {fade_bg}; border: 3px outset #ffffff; padding: 15px; text-align: center;">
<div style="font-family: VT323, monospace; font-size: 2.5rem; color: {fade_text};">${fade_index:+.2f}</div>
<div style="font-family: VT323, monospace; font-size: 1rem; color: {fade_text};">FADE INDEX</div>
</div>
<div style="text-align: center; margin-top: 15px; font-family: VT323, monospace; font-size: 0.9rem; color: #00ff00;">{wins}W - {losses}L - {pushes}P</div>
</div>''', unsafe_allow_html=True)
    
    st.markdown('''<div style="font-family: VT323, monospace; font-size: 1.1rem; text-align: center; margin: 20px 0; color: #000000;">📱 To share: Screenshot this card and send it!</div>''', unsafe_allow_html=True)
    
    # Text version for easy copying
    share_text = f"""🔒 LOCKHUB STATS 🔒
Win %: {win_rate:.1f}%
Win Streak: {streak} 🔥
Fade Index: ${fade_index:+.2f}
Record: {wins}W - {losses}L - {pushes}P"""
    
    st.markdown('<div class="section-header">📋 COPY TEXT VERSION</div>', unsafe_allow_html=True)
    
    st.code(share_text, language=None)
    
    st.markdown('''<div class="info-box"><center>👆 Click the copy icon on the text box above to copy stats to clipboard!</center></div>''', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB 4: GLOCK ENTRY
# ----------------------------------------------------------------------------

with tab4:
    st.markdown('<div class="section-header">🔐 LOCK ENTRY</div>', unsafe_allow_html=True)
    
    if 'glock_authenticated' not in st.session_state:
        st.session_state['glock_authenticated'] = False
    
    if not st.session_state['glock_authenticated']:
        st.markdown("""
        <div class="info-box" style="background-color: #ffcccc;">
            <center>
            ⚠️ <b>RESTRICTED</b> ⚠️
            </center>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Enter the sacred password:", type="password")
        if st.button("🔓 UNLOCK"):
            if password == GLOCK_PASSWORD:
                st.session_state['glock_authenticated'] = True
                st.rerun()
            else:
                st.markdown("""
                <div class="info-box" style="background-color: #ff0000; color: #ffffff;">
                    <center>❌ ACCESS DENIED ❌<br>Nice try, freeloader!</center>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box" style="background-color: #ccffcc;">
            <center>✅ <b>ACCESS GRANTED</b> ✅<br>Welcome back, king! 👑</center>
        </div>
        """, unsafe_allow_html=True)
        
        # New Lock Entry
        st.markdown('<div class="section-header">➕ ADD NEW LOCK</div>', unsafe_allow_html=True)
        
        with st.form("lock_entry_form", clear_on_submit=True):
            game = st.text_input("🏈 Game", placeholder="e.g., Eagles @ Cowboys")
            
            col1, col2 = st.columns(2)
            with col1:
                bet_type = st.selectbox("📊 Bet Type", options=BET_TYPES)
            with col2:
                confidence = st.selectbox("💪 Confidence", options=CONFIDENCE_LEVELS)
            
            pick = st.text_input("🎯 The Pick", placeholder="e.g., Eagles -6.5 or Over 45.5")
            odds = st.text_input("📈 Odds", placeholder="e.g., -110 or +150")
            notes = st.text_area("📝 Notes (Optional)", placeholder="Any reasoning? Or just vibes?", max_chars=500)
            
            submitted = st.form_submit_button("🔒 LOCK IT IN 🔒")
            
            if submitted:
                if not game or not pick:
                    st.error("⚠️ Game and Pick are required!")
                else:
                    lock_data = {
                        'game': game,
                        'bet_type': bet_type,
                        'pick': pick,
                        'confidence': confidence,
                        'status': 'Active',
                        'result': None,
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'settled_at': None,
                        'notes': notes,
                        'odds': odds if odds else '-110'
                    }
                    
                    if save_lock(conn, lock_data):
                        st.success("🎉 LOCK SUBMITTED! 🎉")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save. Try again.")
        
        # Edit Locks
        st.markdown('<div class="section-header">✏️ EDIT LOCK</div>', unsafe_allow_html=True)
        
        active_for_edit = df[df['status'] == 'Active']
        
        if active_for_edit.empty:
            st.markdown("""
            <div class="info-box">
                <center>No active locks to edit.</center>
            </div>
            """, unsafe_allow_html=True)
        else:
            edit_options = {f"{row['game']} - {row['pick']}": row['id'] for _, row in active_for_edit.iterrows()}
            
            selected_edit_lock = st.selectbox("Select Lock to Edit", options=list(edit_options.keys()), key="edit_select")
            
            # Get the current lock data
            edit_lock_id = edit_options[selected_edit_lock]
            current_lock = df[df['id'] == edit_lock_id].iloc[0]
            
            with st.form("edit_lock_form"):
                edit_game = st.text_input("🏈 Game", value=current_lock['game'], key="edit_game")
                
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    current_bet_type_idx = BET_TYPES.index(current_lock['bet_type']) if current_lock['bet_type'] in BET_TYPES else 0
                    edit_bet_type = st.selectbox("📊 Bet Type", options=BET_TYPES, index=current_bet_type_idx, key="edit_bet_type")
                with edit_col2:
                    current_confidence_idx = CONFIDENCE_LEVELS.index(current_lock['confidence']) if current_lock['confidence'] in CONFIDENCE_LEVELS else 0
                    edit_confidence = st.selectbox("💪 Confidence", options=CONFIDENCE_LEVELS, index=current_confidence_idx, key="edit_confidence")
                
                edit_pick = st.text_input("🎯 The Pick", value=current_lock['pick'], key="edit_pick")
                current_odds = current_lock['odds'] if pd.notna(current_lock.get('odds')) else "-110"
                edit_odds = st.text_input("📈 Odds", value=str(current_odds), key="edit_odds")
                edit_notes = st.text_area("📝 Notes (Optional)", value=current_lock['notes'] if pd.notna(current_lock['notes']) else "", key="edit_notes")
                
                edit_submitted = st.form_submit_button("✏️ UPDATE LOCK")
                
                if edit_submitted:
                    if not edit_game or not edit_pick:
                        st.error("⚠️ Game and Pick are required!")
                    else:
                        idx = df[df['id'] == edit_lock_id].index[0]
                        df.at[idx, 'game'] = edit_game
                        df.at[idx, 'bet_type'] = edit_bet_type
                        df.at[idx, 'pick'] = edit_pick
                        df.at[idx, 'confidence'] = edit_confidence
                        df.at[idx, 'odds'] = edit_odds if edit_odds else '-110'
                        df.at[idx, 'notes'] = edit_notes
                        
                        if update_locks(conn, df):
                            st.success("✅ Lock updated!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update. Try again.")
            
            # Delete Lock option
            if st.button("🗑️ DELETE THIS LOCK", key="delete_lock"):
                idx = df[df['id'] == edit_lock_id].index[0]
                df = df.drop(idx)
                if update_locks(conn, df):
                    st.success("🗑️ Lock deleted!")
                    st.rerun()
        
        # Settle Locks
        st.markdown('<div class="section-header">⚖️ SETTLE LOCKS</div>', unsafe_allow_html=True)
        
        active_for_settle = df[df['status'] == 'Active']
        
        if active_for_settle.empty:
            st.markdown("""
            <div class="info-box">
                <center>No active locks to settle.</center>
            </div>
            """, unsafe_allow_html=True)
        else:
            settle_options = {f"{row['game']} - {row['pick']}": row['id'] for _, row in active_for_settle.iterrows()}
            
            selected_lock = st.selectbox("Select Lock", options=list(settle_options.keys()))
            result = st.radio("Result", options=['Win', 'Loss', 'Push'], horizontal=True)
            
            if st.button("⚖️ SETTLE LOCK"):
                lock_id = settle_options[selected_lock]
                idx = df[df['id'] == lock_id].index[0]
                df.at[idx, 'result'] = result
                df.at[idx, 'status'] = 'Settled'
                df.at[idx, 'settled_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if update_locks(conn, df):
                    emoji = "🎉" if result == 'Win' else ("😢" if result == 'Loss' else "🤷")
                    st.success(f"{emoji} Lock settled as {result}!")
                    st.rerun()
        
        # Edit Settled Locks
        st.markdown('<div class="section-header">📝 EDIT SETTLED LOCKS</div>', unsafe_allow_html=True)
        
        settled_for_edit = df[df['status'] == 'Settled']
        
        if settled_for_edit.empty:
            st.markdown("""
            <div class="info-box">
                <center>No settled locks to edit.</center>
            </div>
            """, unsafe_allow_html=True)
        else:
            settled_edit_options = {f"{row['game']} - {row['pick']} ({row['result']})": row['id'] for _, row in settled_for_edit.iterrows()}
            
            selected_settled_lock = st.selectbox("Select Settled Lock to Edit", options=list(settled_edit_options.keys()), key="settled_edit_select")
            
            # Get the current settled lock data
            settled_lock_id = settled_edit_options[selected_settled_lock]
            current_settled_lock = df[df['id'] == settled_lock_id].iloc[0]
            
            with st.form("edit_settled_lock_form"):
                settled_edit_game = st.text_input("🏈 Game", value=current_settled_lock['game'], key="settled_edit_game")
                
                settled_col1, settled_col2 = st.columns(2)
                with settled_col1:
                    current_settled_bet_type_idx = BET_TYPES.index(current_settled_lock['bet_type']) if current_settled_lock['bet_type'] in BET_TYPES else 0
                    settled_edit_bet_type = st.selectbox("📊 Bet Type", options=BET_TYPES, index=current_settled_bet_type_idx, key="settled_edit_bet_type")
                with settled_col2:
                    current_settled_confidence_idx = CONFIDENCE_LEVELS.index(current_settled_lock['confidence']) if current_settled_lock['confidence'] in CONFIDENCE_LEVELS else 0
                    settled_edit_confidence = st.selectbox("💪 Confidence", options=CONFIDENCE_LEVELS, index=current_settled_confidence_idx, key="settled_edit_confidence")
                
                settled_edit_pick = st.text_input("🎯 The Pick", value=current_settled_lock['pick'], key="settled_edit_pick")
                current_settled_odds = current_settled_lock['odds'] if pd.notna(current_settled_lock.get('odds')) else "-110"
                settled_edit_odds = st.text_input("📈 Odds", value=str(current_settled_odds), key="settled_edit_odds")
                
                # Result dropdown
                result_options = ['Win', 'Loss', 'Push']
                current_result_idx = result_options.index(current_settled_lock['result']) if current_settled_lock['result'] in result_options else 0
                settled_edit_result = st.selectbox("🏆 Result", options=result_options, index=current_result_idx, key="settled_edit_result")
                
                settled_edit_notes = st.text_area("📝 Notes (Optional)", value=current_settled_lock['notes'] if pd.notna(current_settled_lock['notes']) else "", key="settled_edit_notes")
                
                settled_edit_submitted = st.form_submit_button("✏️ UPDATE SETTLED LOCK")
                
                if settled_edit_submitted:
                    if not settled_edit_game or not settled_edit_pick:
                        st.error("⚠️ Game and Pick are required!")
                    else:
                        idx = df[df['id'] == settled_lock_id].index[0]
                        df.at[idx, 'game'] = settled_edit_game
                        df.at[idx, 'bet_type'] = settled_edit_bet_type
                        df.at[idx, 'pick'] = settled_edit_pick
                        df.at[idx, 'confidence'] = settled_edit_confidence
                        df.at[idx, 'odds'] = settled_edit_odds if settled_edit_odds else '-110'
                        df.at[idx, 'result'] = settled_edit_result
                        df.at[idx, 'notes'] = settled_edit_notes
                        
                        if update_locks(conn, df):
                            st.success("✅ Settled lock updated!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update. Try again.")
            
            # Delete Settled Lock option
            if st.button("🗑️ DELETE THIS SETTLED LOCK", key="delete_settled_lock"):
                idx = df[df['id'] == settled_lock_id].index[0]
                df = df.drop(idx)
                if update_locks(conn, df):
                    st.success("🗑️ Settled lock deleted!")
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔒 LOCK SCREEN"):
            st.session_state['glock_authenticated'] = False
            st.rerun()

# ----------------------------------------------------------------------------
# TAB 3: DEGENERATE CONVERTER
# ----------------------------------------------------------------------------

with tab3:
    st.markdown('<div class="section-header">💰 DEGENERATE UNIT CONVERSIONS</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin: 15px 0; color: #000000;">
    How much did you win/lose from your G Lock?
    </div>
    """, unsafe_allow_html=True)
    
    amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0, label_visibility="collapsed")
    
    if amount > 0:
        conversions = convert_to_units(amount)
        
        # Display conversions in a 2-column grid on mobile
        conv_col1, conv_col2 = st.columns(2)
        
        with conv_col1:
            st.markdown(f"""
            <div class="info-box">
                <center>
                <b>🏌️ ProV1s</b><br>
                <span style="font-size: 1.8rem; color: #006600;">{conversions['prov1_balls']:.1f}</span><br>
                <small style="color: #000000;">@ $4.75 each</small>
                </center>
            </div>
            """, unsafe_allow_html=True)
        
        with conv_col2:
            st.markdown(f"""
            <div class="info-box">
                <center>
                <b>🍺 Labatt Blues</b><br>
                <span style="font-size: 1.8rem; color: #000066;">{conversions['labatt_blues']:.1f}</span><br>
                <small style="color: #000000;">@ $0.95 each</small>
                </center>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# LIVE ODDS SECTION (Below Tabs)
# ============================================================================

st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📊 LIVE ODDS</div>', unsafe_allow_html=True)

# Embed CapperTek vertical odds widget
st.components.v1.iframe(
    src="https://cappertek.com/xAjaxEventsCarouselX.asp?ref=widget",
    height=410,
    scrolling=True
)

st.markdown("""
<div style="font-family: 'VT323', monospace; font-size: 0.9rem; margin-top: 10px; color: #666666; text-align: center;">
Odds provided by CapperTek
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-family: 'Comic Sans MS', cursive; font-size: 0.8rem; color: #000000; margin-top: 15px;">
    <p>🔒 LockHub v2.0 🔒</p>
    <p>© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
