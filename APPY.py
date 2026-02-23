import streamlit as st
import time

# ==========================================
# 1. CONFIGURATION & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="ROBIN", layout="wide", page_icon="🐦")

# Initialize routing and state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "lite_mode" not in st.session_state:
    st.session_state.lite_mode = False
if "lang" not in st.session_state:
    st.session_state.lang = "DE"
if "supported_projects" not in st.session_state:
    st.session_state.supported_projects = []

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 2. CUSTOM CSS & THEMING
# ==========================================
st.markdown("""
    <style>
    /* Global Variables */
    :root {
        --app-bg: #1b263b;         /* Lighter Dark Blue (Background) */
        --box-bg: #0d1b2a;         /* Deep Dark Blue (Box Normal) */
        --text-mint: #76c8b9;      /* Dimmer Mint (Text Normal / Box Hover) */
        --text-dark: #0d1b2a;      /* Deep Dark Blue (Text Hover) */
    }

    /* Main App Background */
    .stApp {
        background-color: var(--app-bg);
        color: var(--text-mint);
    }

    /* =========================================
       STYLE 1: THE PERFECT SQUARES (Primary Buttons) 
       ========================================= */
       
    /* Center the buttons within their columns */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button[kind="primary"] {
        background-color: var(--box-bg) !important;
        color: var(--text-mint) !important;
        border: none !important;
        border-radius: 20px !important;
        
        /* STRICT ABSOLUTE SIZING - EXACT SQUARES */
        width: 350px !important;
        height: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
        min-height: 350px !important;
        max-height: 350px !important;
        
        padding: 30px !important;
        margin-bottom: 20px !important;
        box-sizing: border-box !important;
        
        /* TEXT ALIGNMENT */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important; 
        align-items: flex-start !important;
        text-align: left !important;
        white-space: pre-wrap !important;
        overflow: hidden !important; 
        
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 6px 14px rgba(0,0,0,0.3) !important;
    }

    /* Target the base Description text */
    div.stButton > button[kind="primary"] p {
        font-family: 'Helvetica', sans-serif !important;
        font-size: 20px !important; /* Description is smaller */
        font-weight: 400 !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        color: var(--text-mint) !important;
    }

    /* Target the Bold Title text (Split into two lines) */
    div.stButton > button[kind="primary"] strong {
        font-size: 32px !important; /* Title is massive */
        font-weight: 900 !important;
        display: block !important;  /* Forces the line break */
        margin-bottom: 15px !important; /* Space between title and description */
        color: var(--text-mint) !important;
        line-height: 1.2 !important;
    }

    /* Hover Effects */
    div.stButton > button[kind="primary"]:hover {
        background-color: var(--text-mint) !important; 
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.4) !important;
    }
    
    div.stButton > button[kind="primary"]:hover p,
    div.stButton > button[kind="primary"]:hover strong {
        color: var(--text-dark) !important;
    }

    /* =========================================
       STYLE 2: THE BACK BUTTON (Secondary Buttons) 
       ========================================= */
    div.stButton > button[kind="secondary"] {
        background-color: var(--text-mint) !important; 
        border: none !important;
        border-radius: 12px !important;
        color: transparent !important;  
        text-shadow: 0 0 0 var(--text-dark) !important; 
        font-size: 50px !important;
        line-height: 50px !important;
        padding: 10px 20px !important;
        transition: transform 0.2s ease !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        transform: scale(1.1) !important; 
        background-color: #e0e0e0 !important; /* Light Gray */
    }

    /* =========================================
       STYLE 3: THE MINT BOXES (Tertiary Buttons) 
       ========================================= */
    div.stButton > button[kind="tertiary"] {
        background-color: var(--text-mint) !important;
        color: var(--text-dark) !important; 
        border: none !important;
        border-radius: 10px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 15px !important;
        margin-top: 20px !important;
    }
    div.stButton > button[kind="tertiary"] p { color: var(--text-dark) !important; }
    div.stButton > button[kind="tertiary"]:hover { background-color: #e0e0e0 !important; }
    div.stButton > button[kind="tertiary"]:hover p { color: var(--text-dark) !important; }

    /* Headings & Text */
    h1, h2, h3, h4, label, .stMarkdown {
        color: var(--text-mint) !important;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Safely scoped Inputs */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background-color: var(--box-bg) !important;
        color: var(--text-mint) !important;
        border: 2px solid var(--text-mint) !important;
        border-radius: 10px !important;
    }

    /* Fixed Header */
    footer {visibility: hidden;}
    header {background-color: var(--app-bg) !important;}
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. GLOBAL UI ELEMENTS (Sidebar & Language)
# ==========================================
lang = st.session_state.lang

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Settings</h2>" if lang == "EN" else "<h2 style='text-align: center;'>⚙️ Einstellungen</h2>", unsafe_allow_html=True)
    lbl_lite = "Lite Mode (Slow Internet)" if lang == "EN" else "Lite-Modus (Langsames Internet)"
    st.session_state.lite_mode = st.toggle(lbl_lite, value=st.session_state.lite_mode)

# Top Right Language Switcher
col_empty, col_lang = st.columns([9, 1])
with col_lang:
    selected_lang = st.selectbox("Language", ["DE", "EN"], index=0 if lang == "DE" else 1, label_visibility="collapsed")
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# Mock Ideas
mock_ideas = [
    {"id": 1, "title": "Mehr Bänke im Nordpark" if lang == "DE" else "More benches in Nordpark", "desc": "Senioren brauchen mehr Sitzgelegenheiten." if lang == "DE" else "Seniors need more places to rest.", "sector": "Sektor 4", "tag": "Infrastruktur" if lang == "DE" else "Infrastructure"},
    {"id": 2, "title": "Straßenlaternen reparieren" if lang == "DE" else "Fix streetlights", "desc": "Nach 17 Uhr wird es dunkel." if lang == "DE" else "It gets dangerously dark.", "sector": "Sektor 2", "tag": "Sicherheit" if lang == "DE" else "Safety"}
]

# ==========================================
# 4. DIALOGS (Modals)
# ==========================================
dlg_title = "Warum unterstützen Sie das?" if lang == "DE" else "Why do you support this?"
@st.dialog(dlg_title)
def support_dialog(project_id, project_title):
    st.write("Grund auswählen:" if lang == "DE" else "Select your primary reason:")
    opts = ["Erhöht die Sicherheit", "Spart Geld", "Fördert die Gemeinschaft", "Sonstiges"] if lang == "DE" else ["Improves Safety", "Saves Money", "Builds Community", "Other"]
    reason = st.radio("Grund", opts, label_visibility="collapsed")
    
    if st.button("Bestätigen" if lang == "DE" else "Confirm Support", type="tertiary"):
        st.session_state.supported_projects.append(project_id)
        st.toast("Stimme gezählt!" if lang == "DE" else "Voice added!", icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# 5. PAGE ROUTING FUNCTIONS
# ==========================================

def home_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 6rem; margin-bottom: 40px;'>ROBIN</h1>", unsafe_allow_html=True)
    
    # 3 Columns for a balanced 2x3 grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lbl_feed = "**COMMUNITY-FEED**\n\nSehen Sie, was Ihre Nachbarn vorschlagen." if lang == "DE" else "**COMMUNITY FEED**\n\nSee what neighbors are suggesting."
        if st.button(lbl_feed, type="primary"): navigate_to('feed')
            
        lbl_dash = "**MEIN DASHBOARD**\n\nVerwalten Sie Ihre Ideen und Ihr Profil." if lang == "DE" else "**MY DASHBOARD**\n\nManage your ideas and profile."
        if st.button(lbl_dash, type="primary"): navigate_to('dashboard')

    with col2:
        lbl_submit = "**IDEE EINREICHEN**\n\nMelden Sie ein Problem oder eine Idee." if lang == "DE" else "**SUBMIT AN IDEA**\n\nReport a problem or share an idea."
        if st.button(lbl_submit, type="primary"): navigate_to('submit')
            
        lbl_how = "**WIE ES FUNKTIONIERT**\n\nSo sorgt der Algorithmus für Fairness." if lang == "DE" else "**HOW IT WORKS**\n\nHow our algorithm ensures fairness."
        if st.button(lbl_how, type="primary"): navigate_to('how_it_works')
        
    with col3:
        lbl_success = "**ERFOLGSGESCHICHTEN**\n\nPositive Veränderungen in der Nachbarschaft." if lang == "DE" else "**SUCCESS STORIES**\n\nPositive impact in the neighborhood."
        if st.button(lbl_success, type="primary"): navigate_to('success')

        lbl_admin = "**STADTVERWALTUNG**\n\n(Nur Personal) Feedback-Schleife schließen." if lang == "DE" else "**CITY ADMIN**\n\n(Staff Only) Close the feedback loop."
        if st.button(lbl_admin, type="primary"): navigate_to('admin')

def feed_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{'COMMUNITY-FEED' if lang == 'DE' else 'COMMUNITY FEED'}</h1>", unsafe_allow_html=True)
    st.info("📣 **Mikro-Erfolge:** Tom hat seine Leiter mit Anna geteilt." if lang == "DE" else "📣 **Micro-Wins:** Tom shared his ladder with Anna.", icon="✨")
    
    for idea in mock_ideas:
        with st.container(border=True):
            st.markdown(f"### {idea['title']}")
            st.write(idea['desc'])
            if idea['id'] in st.session_state.supported_projects:
                st.button("✅ Unterstützt" if lang == "DE" else "✅ Supported", disabled=True, key=f"btn_disabled_{idea['id']}")
            else:
                if st.button("🤝 Idee unterstützen" if lang == "DE" else "🤝 Support this Idea", key=f"btn_support_{idea['id']}", type="tertiary"):
                    support_dialog(idea['id'], idea['title'])

def submit_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'IDEE EINREICHEN' if lang == 'DE' else 'SUBMIT AN IDEA'}</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.wizard_step / 3.0)
    
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.session_state.wizard_step == 1:
            st.subheader("1. Was ist das Problem?" if lang == "DE" else "1. What is the problem?")
            st.text_area("Beschreibung", placeholder="Hier schreiben..." if lang == "DE" else "Type here...", label_visibility="collapsed")
            if st.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                st.session_state.wizard_step = 2
                st.rerun()
        elif st.session_state.wizard_step == 2:
            st.subheader("2. Wo befindet sich das?" if lang == "DE" else "2. Where is this located?")
            st.text_input("Ort", placeholder="Z.B. Nordpark" if lang == "DE" else "E.g. North Park", label_visibility="collapsed")
            if st.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                st.session_state.wizard_step = 3
                st.rerun()
        elif st.session_state.wizard_step == 3:
            st.subheader("3. Überprüfen & Einreichen" if lang == "DE" else "3. Review & Submit")
            if st.button("✅ Einreichen" if lang == "DE" else "✅ Submit", type="tertiary"):
                st.toast("Erfolgreich eingereicht!" if lang == "DE" else "Successfully submitted!", icon="🎉")
                st.session_state.wizard_step = 1
                time.sleep(1)
                navigate_to('home')

def dashboard_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'MEIN DASHBOARD' if lang == 'DE' else 'MY DASHBOARD'}</h1>", unsafe_allow_html=True)
    st.write("Profil und Privatsphäre Einstellungen" if lang == "DE" else "Profile and Privacy settings")

def admin_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'STADTVERWALTUNG' if lang == 'DE' else 'CITY ADMIN'}</h1>", unsafe_allow_html=True)

def how_it_works_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'WIE ES FUNKTIONIERT' if lang == 'DE' else 'HOW IT WORKS'}</h1>", unsafe_allow_html=True)

def success_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown(f"<h1 style='text-align: center;'>{'ERFOLGSGESCHICHTEN' if lang == 'DE' else 'SUCCESS STORIES'}</h1>", unsafe_allow_html=True)

# ==========================================
# 6. MAIN CONTROLLER
# ==========================================
if st.session_state.page == 'home': home_page()
elif st.session_state.page == 'feed': feed_page()
elif st.session_state.page == 'submit': submit_page()
elif st.session_state.page == 'dashboard': dashboard_page()
elif st.session_state.page == 'admin': admin_page()
elif st.session_state.page == 'how_it_works': how_it_works_page()
elif st.session_state.page == 'success': success_page()
