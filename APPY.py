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
if "submission_type" not in st.session_state:
    st.session_state.submission_type = "resources" # Default
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
        # Submit Button now routes to the choice page
        lbl_submit = "**IDEE EINREICHEN**\n\nMelden Sie ein Problem oder eine Idee." if lang == "DE" else "**SUBMIT AN IDEA**\n\nReport a problem or share an idea."
        if st.button(lbl_submit, type="primary"): navigate_to('submit_choice')
            
        lbl_how = "**WIE ES FUNKTIONIERT**\n\nSo sorgt der Algorithmus für Fairness." if lang == "DE" else "**HOW IT WORKS**\n\nHow our algorithm ensures fairness."
        if st.button(lbl_how, type="primary"): navigate_to('how_it_works')
        
    with col3:
        lbl_success = "**ERFOLGSGESCHICHTEN**\n\nPositive Veränderungen in der Nachbarschaft." if lang == "DE" else "**SUCCESS STORIES**\n\nPositive impact in the neighborhood."
        if st.button(lbl_success, type="primary"): navigate_to('success')

        lbl_admin = "**STADTVERWALTUNG**\n\n(Nur Personal) Feedback-Schleife schließen." if lang == "DE" else "**CITY ADMIN**\n\n(Staff Only) Close the feedback loop."
        if st.button(lbl_admin, type="primary"): navigate_to('admin')


def submit_choice_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
    st.markdown("---")
    
    title = "Welche Art von Unterstützung benötigen Sie?" if lang == "DE" else "What kind of support do you need?"
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1><br><br>", unsafe_allow_html=True)
    
    _, col1, col2, _ = st.columns([1, 2, 2, 1])
    
    with col1:
        lbl_fin = "**FINANZIELLE HILFE**\n\nBeantragen Sie Mikrostipendien oder Gemeindefinanzierung." if lang == "DE" else "**FINANCIAL HELP**\n\nApply for micro-grants or community funding."
        if st.button(lbl_fin, type="primary"):
            st.session_state.submission_type = "financial"
            st.session_state.wizard_step = 1
            navigate_to('submit')
            
    with col2:
        lbl_res = "**RESSOURCEN & HILFE**\n\nFinden Sie Werkzeuge, Freiwillige oder Platz für Ihr Projekt." if lang == "DE" else "**RESOURCES & HELP**\n\nFind tools, volunteers, or space for your project."
        if st.button(lbl_res, type="primary"):
            st.session_state.submission_type = "resources"
            st.session_state.wizard_step = 1
            navigate_to('submit')


def submit_page():
    if st.button("🦇", type="secondary"): navigate_to('submit_choice')
    
    st.markdown("---")
    st.warning("📡 **Sie sind offline.** Ihre Eingaben werden auf dem Gerät gespeichert." if lang == "DE" else "📡 **You are offline.** Your typing is automatically saved to your device.", icon="⚠️")
    
    st.markdown(f"<h1 style='text-align: center;'>{'IDEE EINREICHEN' if lang == 'DE' else 'SUBMIT AN IDEA'}</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.wizard_step / 3.0)
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center, _ = st.columns([1, 2, 1])
    
    with center:
        if st.session_state.wizard_step == 1:
            st.subheader("1. Was ist das Problem oder die Idee?" if lang == "DE" else "1. What is the problem or idea?")
            
            # --- ASSISTED MODE RESTORED ---
            assisted_mode = st.toggle("Assistenz-Modus (Schritt-für-Schritt)" if lang == "DE" else "Assisted Mode (Step-by-step guidance)", value=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not assisted_mode:
                p_text = "Z.B. Der Bürgersteig auf der Hauptstraße ist kaputt..." if lang == "DE" else "E.g., The sidewalk on Main St. is broken..."
                st.text_area("Beschreibung", placeholder=p_text, label_visibility="collapsed", key="ta_desc")
                st.write("**Oder sprechen Sie eine Nachricht ein:**" if lang == "DE" else "**Or, record a voice message:**")
                st.audio_input("Sprachaufnahme" if lang == "DE" else "Record your voice", label_visibility="collapsed")
            else:
                # DYNAMIC ASSISTED MODE BASED ON ROUTE SELECTION
                if st.session_state.submission_type == "financial":
                    st.markdown("#### Geschätztes benötigtes Budget:" if lang == "DE" else "#### Estimated Budget Needed:")
                    b_opts = ["Bis zu 50€", "50€ - 200€", "200€ - 500€", "Mehr als 500€"] if lang == "DE" else ["Up to 50€", "50€ - 200€", "200€ - 500€", "Over 500€"]
                    st.selectbox("Budget", b_opts, label_visibility="collapsed", key="fin_budget")
                    
                    st.markdown("#### Art der Finanzierung:" if lang == "DE" else "#### Type of Funding:")
                    f_opts = ["Mikrozuschuss", "Spenden", "Stadtbudget"] if lang == "DE" else ["Micro-grant", "Donations", "City Budget"]
                    st.pills("Finanzierungstyp", f_opts, label_visibility="collapsed", key="fin_type")
                    
                    st.markdown("#### Projektphase:" if lang == "DE" else "#### Project Phase:")
                    p_opts = ["Nur eine Idee", "In Planung", "Startklar"] if lang == "DE" else ["Just an idea", "Planning", "Ready to start"]
                    st.pills("Phase", p_opts, label_visibility="collapsed", key="fin_phase")

                else: # "resources" default
                    st.markdown("#### Um welche Art von Projekt handelt es sich?" if lang == "DE" else "#### What kind of project is it?")
                    t_opts = ["Schnelle Lösung", "Große Idee", "Sonstiges"] if lang == "DE" else ["Quick fix", "Big idea", "Other"]
                    st.pills("Typ", t_opts, label_visibility="collapsed", key="res_type")
                    
                    st.markdown("#### Welche Ressourcen benötigen Sie?" if lang == "DE" else "#### What resources do you need?")
                    r_opts = ["Hammer", "Arbeitsplatz", "Bohrmaschine", "3D-Drucker", "Farbe", "Holz", "Metall", "Lötkolben", "Laptop"] if lang == "DE" else ["Hammer", "Workspace", "Drill", "3D Printer", "Paint", "Wood", "Metal", "Soldering Iron", "Laptop"]
                    st.multiselect("Ressourcen", r_opts, label_visibility="collapsed", key="res_items")
                    
                    st.markdown("#### Möchten Sie sich persönlich treffen?" if lang == "DE" else "#### Do you want to meet face to face?")
                    st.pills("Treffen", ["Ja", "Nein"] if lang == "DE" else ["Yes", "No"], label_visibility="collapsed", key="res_meet")
            
            # --- NAVIGATION ---
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                st.session_state.wizard_step = 2
                st.rerun()
            if c2.button("💾 Entwurf speichern" if lang == "DE" else "💾 Save Draft", type="tertiary"):
                st.toast("Entwurf lokal gespeichert!" if lang == "DE" else "Draft saved locally!", icon="💾")

        elif st.session_state.wizard_step == 2:
            st.subheader("2. Wo befindet sich das?" if lang == "DE" else "2. Where is this located?")
            st.text_input("Ort", placeholder="Z.B. Ecke 5. Straße und Elm" if lang == "DE" else "E.g., Corner of 5th and Elm", label_visibility="collapsed")
            
            if not st.session_state.lite_mode:
                st.caption("*(Interaktive Karte würde hier laden, im Lite-Modus deaktiviert)*" if lang == "DE" else "*(Interactive map disabled in Lite Mode)*")
                
            c1, c2, c3 = st.columns(3)
            if c1.button("⬅ Zurück" if lang == "DE" else "⬅ Back", type="tertiary"):
                st.session_state.wizard_step = 1
                st.rerun()
            if c2.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                st.session_state.wizard_step = 3
                st.rerun()
            if c3.button("💾 Entwurf" if lang == "DE" else "💾 Draft", type="tertiary"):
                st.toast("Gespeichert!" if lang == "DE" else "Saved!", icon="💾")

        elif st.session_state.wizard_step == 3:
            st.subheader("3. Überprüfen & Einreichen" if lang == "DE" else "3. Review & Submit")
            st.info("Ihre Idee sieht gut aus. Bereit, sie mit der Community zu teilen?" if lang == "DE" else "Idea looks great. Ready to share?")
            
            c1, c2 = st.columns(2)
            if c1.button("⬅ Zurück" if lang == "DE" else "⬅ Back", type="tertiary"):
                st.session_state.wizard_step = 2
                st.rerun()
            if c2.button("✅ Einreichen" if lang == "DE" else "✅ Submit", type="tertiary"):
                st.toast("Idee eingereicht! Sie werden bei Neuigkeiten benachrichtigt." if lang == "DE" else "Idea Submitted! You'll be notified.", icon="🎉")
                st.session_state.wizard_step = 1
                time.sleep(2)
                navigate_to('home')


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
elif st.session_state.page == 'submit_choice': submit_choice_page()
elif st.session_state.page == 'feed': feed_page()
elif st.session_state.page == 'submit': submit_page()
elif st.session_state.page == 'dashboard': dashboard_page()
elif st.session_state.page == 'admin': admin_page()
elif st.session_state.page == 'how_it_works': how_it_works_page()
elif st.session_state.page == 'success': success_page()
