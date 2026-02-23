import streamlit as st
import time
import random

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
       STYLE 1: THE BIG SQUARES (Primary Buttons) 
       ========================================= */
       
    div.stButton > button[kind="primary"] {
        background-color: var(--box-bg) !important;
        color: var(--text-mint) !important;
        border: none !important;
        border-radius: 20px !important; /* Slightly rounder corners for squares */
        
        /* THE FIX FOR PERFECT SQUARES */
        width: 100% !important;
        aspect-ratio: 1 / 1 !important; /* Forces Height to equal Width */
        box-sizing: border-box !important;
        margin-top: 20px !important;
        padding: 35px !important;
        
        /* ALIGNMENT & OVERFLOW */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important; /* Align text to top */
        align-items: flex-start !important;
        text-align: left !important;
        white-space: pre-wrap !important;
        overflow: hidden !important; /* Hide text if it gets too long for the square */
        
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 6px 14px rgba(0,0,0,0.3) !important;
    }

    /* Target the text inside the primary buttons */
    div.stButton > button[kind="primary"] p, 
    div.stButton > button[kind="primary"] div {
        font-family: 'Helvetica', sans-serif !important;
        font-size: 28px !important; /* Large, readable font */
        font-weight: 600 !important;
        line-height: 1.3 !important;
        margin: 0 !important;
        text-align: left !important;
        color: var(--text-mint) !important;
        hyphens: auto !important; /* Break long words if needed */
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: var(--text-mint) !important; 
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.4) !important;
    }
    
    div.stButton > button[kind="primary"]:hover p,
    div.stButton > button[kind="primary"]:hover div {
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
        
        height: auto !important;
        width: auto !important;
        padding: 10px 20px !important;
        min-height: 0px !important;
        
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
        color: var(--text-dark) !important; /* Dark Blue */
        border: none !important;
        border-radius: 10px !important;
        
        font-size: 20px !important;
        font-weight: bold !important;
        
        width: 100% !important;
        height: auto !important;
        padding: 15px !important;
        min-height: 0px !important;
        margin-top: 20px !important;
    }
    
    div.stButton > button[kind="tertiary"] p {
        color: var(--text-dark) !important; 
    }
    
    div.stButton > button[kind="tertiary"]:hover {
        background-color: #e0e0e0 !important; /* Light Gray */
    }
    
    div.stButton > button[kind="tertiary"]:hover p {
        color: var(--text-dark) !important; /* Stays Dark Blue */
    }

    /* Headings & Text */
    h1, h2, h3, h4, p, label, .stMarkdown {
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
        min-height: auto !important;
    }

    /* =========================================
       FIXED HEADER & SIDEBAR TOGGLE
       ========================================= */
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
    lbl_lite_help = "Toggle this if your connection is unstable." if lang == "EN" else "Aktivieren Sie dies bei instabiler Verbindung."
    
    st.session_state.lite_mode = st.toggle(lbl_lite, value=st.session_state.lite_mode)
    st.caption(lbl_lite_help)

# Top Right Language Switcher
col_empty, col_lang = st.columns([9, 1])
with col_lang:
    selected_lang = st.selectbox("Language", ["DE", "EN"], index=0 if lang == "DE" else 1, label_visibility="collapsed")
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# Mock Ideas translated dynamically
mock_ideas = [
    {"id": 1, "title": "Mehr Bänke im Nordpark" if lang == "DE" else "More benches in Nordpark", 
     "desc": "Senioren brauchen mehr Sitzgelegenheiten beim Spazierengehen im Nordpark." if lang == "DE" else "Seniors need more places to rest when walking in the north park.", 
     "sector": "Sektor 4", "tag": "Infrastruktur" if lang == "DE" else "Infrastructure"},
    {"id": 2, "title": "Straßenlaternen reparieren (Elm St.)" if lang == "DE" else "Fix streetlights on Elm St.", 
     "desc": "Nach 17 Uhr wird es am Zebrastreifen gefährlich dunkel." if lang == "DE" else "It gets dangerously dark near the crosswalk after 5 PM.", 
     "sector": "Sektor 2", "tag": "Sicherheit" if lang == "DE" else "Safety"}
]

# ==========================================
# 4. DIALOGS (Modals)
# ==========================================
dlg_title = "Warum unterstützen Sie das?" if lang == "DE" else "Why do you support this?"
@st.dialog(dlg_title)
def support_dialog(project_id, project_title):
    st.markdown(f"**{'Idee' if lang == 'DE' else 'Idea'}:** {project_title}")
    st.write("Helfen Sie der Community zu verstehen, warum diese Idee wichtig ist." if lang == "DE" else "Help the community understand the consensus behind this idea.")
    
    opts = ["Erhöht die Sicherheit", "Spart Geld", "Fördert die Gemeinschaft", "Sonstiges"] if lang == "DE" else ["Improves Safety", "Saves Money", "Builds Community", "Other"]
    reason = st.radio("Grund auswählen:" if lang == "DE" else "Select your primary reason:", opts, label_visibility="collapsed")
    
    btn_text = "Unterstützung bestätigen" if lang == "DE" else "Confirm Support"
    if st.button(btn_text, type="tertiary"):
        st.session_state.supported_projects.append(project_id)
        msg = f"Danke! Ihre Stimme für '{reason}' wurde gezählt." if lang == "DE" else f"Thank you! Your voice was added for '{reason}'."
        st.toast(msg, icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# 5. PAGE ROUTING FUNCTIONS
# ==========================================

def home_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 6rem; margin-bottom: 40px;'>ROBIN</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Box 1
        lbl_feed = "COMMUNITY-\nFEED\n\nSehen Sie, was Ihre Nachbarn vorschlagen." if lang == "DE" else "COMMUNITY\nFEED\n\nSee what neighbors are suggesting."
        if st.button(lbl_feed, type="primary"): navigate_to('feed')
            
        # Box 2
        lbl_dash = "MEIN\nDASHBOARD\n\nVerwalten Sie Ihre Ideen und Ihr Profil." if lang == "DE" else "MY\nDASHBOARD\n\nManage your ideas and profile."
        if st.button(lbl_dash, type="primary"): navigate_to('dashboard')
            
        # Box 3
        lbl_admin = "STADT-\nVERWALTUNG\n\n(Nur Personal) Feedback-Schleife schließen." if lang == "DE" else "CITY\nADMIN\n\n(Staff Only) Close the feedback loop."
        if st.button(lbl_admin, type="primary"): navigate_to('admin')

    with col2:
        # Box 4
        lbl_submit = "IDEE\nEINREICHEN\n\nMelden Sie ein Problem oder eine Idee." if lang == "DE" else "SUBMIT\nAN IDEA\n\nReport a problem or share an idea."
        if st.button(lbl_submit, type="primary"): navigate_to('submit')
            
        # Box 5
        lbl_how = "WIE ES\nFUNKTIONIERT\n\nSo sorgt der Algorithmus für Fairness." if lang == "DE" else "HOW IT\nWORKS\n\nHow our algorithm ensures fairness."
        if st.button(lbl_how, type="primary"): navigate_to('how_it_works')
        
        # Box 6
        lbl_success = "ERFOLGS-\nGESCHICHTEN\n\nPositive Veränderungen in der Nachbarschaft." if lang == "DE" else "SUCCESS\nSTORIES\n\nPositive impact in the neighborhood."
        if st.button(lbl_success, type="primary"): navigate_to('success')


def feed_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{'COMMUNITY-FEED' if lang == 'DE' else 'COMMUNITY FEED'}</h1>", unsafe_allow_html=True)
    
    st.info("📣 **Mikro-Erfolge:** Tom hat seine Leiter mit Anna geteilt. | Die Bibliothek hat 50 neue Bücher! | Straßenlaterne repariert." if lang == "DE" else "📣 **Micro-Wins:** Tom shared his ladder with Anna. | The library got 50 new books! | Streetlight repaired.", icon="✨")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("⏱️ 60 Sekunden Zeit?" if lang == "DE" else "⏱️ Got 60 Seconds?")
            st.write("Helfen Sie Ihrer Nachbarschaft:" if lang == "DE" else "Help shape your neighborhood:")
            opts = ["Ja", "Nein", "Unsicher"] if lang == "DE" else ["Yes", "No", "Unsure"]
            q = "Braucht der Nordpark mehr Beleuchtung?" if lang == "DE" else "Does the north park need more lighting?"
            st.radio(q, opts, key="poll_1")
            if st.button("Jetzt abstimmen" if lang == "DE" else "Vote Instantly", type="tertiary"):
                st.toast("Abstimmung gespeichert!" if lang == "DE" else "Vote recorded!", icon="🎉")

    with col1:
        sort_opts = ["Braucht Ihre Stimme", "Beliebteste", "Kürzlich hinzugefügt"] if lang == "DE" else ["Needs Your Voice", "Most Popular", "Recently Added"]
        st.selectbox("Ideen sortieren nach:" if lang == "DE" else "Sort community ideas by:", sort_opts, index=0)
        
        for idea in mock_ideas:
            with st.container(border=True):
                st.markdown(f"### {idea['title']}")
                st.write(idea['desc'])
                st.caption(f"✨ *Algorithmus-Empfehlung, weil Sie [{idea['tag']}] folgen und in [{idea['sector']}] leben.*" if lang == "DE" else f"✨ *Algorithm matched this because you follow [{idea['tag']}] and live in [{idea['sector']}].*")
                
                if idea['id'] in st.session_state.supported_projects:
                    st.button("✅ Unterstützt" if lang == "DE" else "✅ Supported", disabled=True, key=f"btn_disabled_{idea['id']}")
                else:
                    if st.button("🤝 Idee unterstützen" if lang == "DE" else "🤝 Support this Idea", key=f"btn_support_{idea['id']}", type="tertiary"):
                        support_dialog(idea['id'], idea['title'])


def submit_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.warning("📡 **Sie sind offline.** Ihre Eingaben werden auf dem Gerät gespeichert." if lang == "DE" else "📡 **You are offline.** Your typing is automatically saved to your device.", icon="⚠️")
    
    st.markdown(f"<h1 style='text-align: center;'>{'IDEE EINREICHEN' if lang == 'DE' else 'SUBMIT AN IDEA'}</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.wizard_step / 3.0, text=f"Schritt {st.session_state.wizard_step} von 3" if lang == "DE" else f"Step {st.session_state.wizard_step} of 3")
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center, _ = st.columns([1, 2, 1])
    
    with center:
        if st.session_state.wizard_step == 1:
            st.subheader("1. Was ist das Problem oder die Idee?" if lang == "DE" else "1. What is the problem or idea?")
            
            assisted_mode = st.toggle("Assistenz-Modus (Schritt-für-Schritt)" if lang == "DE" else "Assisted Mode (Step-by-step guidance)")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not assisted_mode:
                p_text = "Z.B. Der Bürgersteig auf der Hauptstraße ist kaputt..." if lang == "DE" else "E.g., The sidewalk on Main St. is broken..."
                st.text_area("Beschreibung", placeholder=p_text, label_visibility="collapsed")
                st.write("**Oder sprechen Sie eine Nachricht ein:**" if lang == "DE" else "**Or, record a voice message:**")
                st.audio_input("Sprachaufnahme" if lang == "DE" else "Record your voice", label_visibility="collapsed")
            else:
                st.markdown("#### Um welche Art von Projekt handelt es sich?" if lang == "DE" else "#### What kind of project is it?")
                t_opts = ["Schnelle Lösung", "Große Idee", "Sonstiges"] if lang == "DE" else ["Quick fix", "Big idea", "Other"]
                st.pills("Typ", t_opts, label_visibility="collapsed", key="type_select")
                
                st.markdown("#### Welche Ressourcen benötigen Sie?" if lang == "DE" else "#### What resources do you need?")
                r_opts = ["Hammer", "Arbeitsplatz", "Bohrmaschine", "3D-Drucker", "Farbe", "Holz", "Metall", "Lötkolben", "Laptop"] if lang == "DE" else ["Hammer", "Workspace", "Drill", "3D Printer", "Paint", "Wood", "Metal", "Soldering Iron", "Laptop"]
                st.multiselect("Ressourcen", r_opts, label_visibility="collapsed", key="resource_select")
                
                st.markdown("#### Möchten Sie sich persönlich treffen?" if lang == "DE" else "#### Do you want to meet face to face?")
                st.pills("Treffen", ["Ja", "Nein"] if lang == "DE" else ["Yes", "No"], label_visibility="collapsed", key="meeting_select")
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("Weiter ➔" if lang == "DE" else "Next ➔", type="tertiary"):
                st.toast("System hat Tags hinzugefügt: [Infrastruktur] [Barrierefreiheit]" if lang == "DE" else "Auto-tagged: [Infrastructure] [Accessibility]", icon="🤖")
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


def dashboard_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.markdown(f"<h1 style='text-align: center;'>{'MEIN DASHBOARD' if lang == 'DE' else 'MY DASHBOARD'}</h1>", unsafe_allow_html=True)
    
    opts = ["Ich selbst", "Frau Schmidt (Vertretung)", "Jugendzentrum (Vertretung)"] if lang == "DE" else ["Myself", "Mrs. Schmidt (Proxy)", "Youth Center (Proxy)"]
    st.selectbox("Derzeit handelnd im Namen von:" if lang == "DE" else "Currently acting on behalf of:", opts)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Identität & Fähigkeiten" if lang == "DE" else "My Identity & Skills")
        chips = ["Anfänger", "Helfe gerne", "Einheimischer", "Technik-Helfer", "Übersetzer"] if lang == "DE" else ["Beginner", "Happy to Guide", "Rural Local", "Tech Helper", "Translator"]
        def_chips = ["Helfe gerne", "Einheimischer"] if lang == "DE" else ["Happy to Guide", "Rural Local"]
        st.multiselect("Identitäts-Chips:" if lang == "DE" else "Identity Chips:", chips, default=def_chips)
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛡️ Datenschutz-Kontrollzentrum" if lang == "DE" else "🛡️ Privacy Control Center"):
            st.toggle("Echten Namen für Nachbarn anzeigen" if lang == "DE" else "Show my real name to neighbors", value=True)
            st.toggle("Erlaube Algorithmus, meine Ideen vorzuschlagen" if lang == "DE" else "Allow algorithm to suggest my ideas", value=True)
            if st.button("Meine Daten vergessen & Löschen" if lang == "DE" else "Forget My Data & Remove", type="tertiary"):
                st.toast("Sicheres Löschen initiiert." if lang == "DE" else "Secure removal initiated.", icon="🗑️")

    with col2:
        st.subheader("👋 Community treffen" if lang == "DE" else "👋 Meet the Community")
        with st.container(border=True):
            st.markdown(f"**Sarah T.** *({'Technik-Helfer' if lang == 'DE' else 'Tech Helper'})*")
            if st.button("Hallo sagen zu Sarah" if lang == "DE" else "Say Hello to Sarah", type="tertiary", key="h1"): st.toast("Gesendet!" if lang == "DE" else "Sent!")
        with st.container(border=True):
            st.markdown(f"**Elena R.** *({'Übersetzer' if lang == 'DE' else 'Translator'})*")
            if st.button("Hallo sagen zu Elena" if lang == "DE" else "Say Hello to Elena", type="tertiary", key="h2"): st.toast("Gesendet!" if lang == "DE" else "Sent!")

    st.markdown("---")
    st.subheader("Meine eingereichten Ideen" if lang == "DE" else "My Submitted Ideas")
    with st.container(border=True):
        st.markdown("**Öffnungszeiten des Gemeinschaftsgartens verlängern**" if lang == "DE" else "**Expand community garden operating hours**")
        p_text = "Status: Feedback der Stadt (Aktuell)" if lang == "DE" else "Status: City Feedback (Current)"
        st.progress(75, text=p_text)
        st.caption("Eingereicht ➔ Community Review ➔ **Feedback der Stadt (Aktuell)** ➔ Aktion" if lang == "DE" else "Submitted ➔ Community Review ➔ **City Feedback (Current)** ➔ Action")
        st.info("Das städtische Grünflächenamt prüft derzeit das Budget für diesen Vorschlag. Erwartetes Update: Nächsten Dienstag." if lang == "DE" else "The City Parks Department is currently reviewing the budget. Expected update: Next Tuesday.")


def admin_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.markdown(f"<h1 style='text-align: center;'>{'STADTVERWALTUNG' if lang == 'DE' else 'CITY ADMIN'}</h1>", unsafe_allow_html=True)
    st.write("Stellen Sie sicher, dass Bürger sich gehört und respektiert fühlen." if lang == "DE" else "Ensure citizens feel heard and respected.")
    
    st.subheader("⚠️ Überfälliges Feedback" if lang == "DE" else "⚠️ Overdue Feedback")
    st.caption("Diese Ideen haben das Community-Review bestanden und warten auf offizielle Bestätigung." if lang == "DE" else "These ideas await official acknowledgement.")
    
    with st.container(border=True):
        st.markdown("**Idee:** Schlaglöcher auf Route 9 reparieren *(Von: David L.)*" if lang == "DE" else "**Idea:** Fix potholes on Route 9 *(By: David L.)*")
        st.error("Wartet seit 4 Tagen auf Antwort." if lang == "DE" else "Waiting for response for 4 days.")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            opts = ["Tolle Idee, wir prüfen das Budget.", "Danke, zur Wartungsliste hinzugefügt."] if lang == "DE" else ["Great idea, reviewing budget now.", "Thank you, added to maintenance queue."]
            st.selectbox("Empathische Antwort-Vorlage:" if lang == "DE" else "Empathetic Response Template:", opts, key="t1")
        with c2:
            st.write("") 
            if st.button("1-Klick-Antwort senden" if lang == "DE" else "Send 1-Click Reply", type="tertiary", key="r1"):
                st.toast("Antwort gesendet an David L." if lang == "DE" else "Reply sent to David L.", icon="✉️")


def how_it_works_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.markdown(f"<h1 style='text-align: center;'>{'WIE ES FUNKTIONIERT' if lang == 'DE' else 'HOW IT WORKS'}</h1>", unsafe_allow_html=True)
    
    if lang == "DE":
        st.write("ROBIN ist so konzipiert, dass alle Stimmen in unserer Stadt gleichermaßen gehört werden. Hier ist, wie unser Algorithmus und unsere Plattform Sie schützen:")
        
        st.subheader("⚖️ 1. Der Gerechtigkeits-Algorithmus (Equity-Weighted Feed)")
        st.write("Ideen werden nicht nur danach sortiert, wer die meisten Freunde hat. Unser Algorithmus hebt gezielt Vorschläge aus Vierteln hervor, die historisch weniger Aufmerksamkeit erhalten haben, oder Projekte, die noch vielfältige Perspektiven (wie von Senioren oder Jugendlichen) benötigen.")
        
        st.subheader("🌐 2. Barrierefreiheit & Offline-Modus")
        st.write("Nicht jeder hat schnelles Internet. Sie können den **Lite-Modus** in den Einstellungen aktivieren, um Daten zu sparen. Falls Sie die Verbindung verlieren, speichert die App Ihre Eingaben sicher auf Ihrem Gerät und synchronisiert sie später.")
        
        st.subheader("🛡️ 3. Datensouveränität")
        st.write("Sie besitzen Ihre Daten. Im *Datenschutz-Kontrollzentrum* auf Ihrem Dashboard können Sie jederzeit auf den roten Knopf drücken, um Ihre Daten vollständig aus dem System und dem Empfehlungsalgorithmus zu löschen.")
    else:
        st.write("ROBIN is designed to ensure all voices in our city are heard equally. Here is how our algorithm and platform protect you:")
        
        st.subheader("⚖️ 1. The Equity-Weighted Feed")
        st.write("Ideas are not just sorted by who has the most friends. Our algorithm deliberately highlights proposals from neighborhoods that have historically received less attention, or projects that still need diverse perspectives (like from seniors or youth).")
        
        st.subheader("🌐 2. Accessibility & Offline Mode")
        st.write("Not everyone has fast internet. You can activate **Lite Mode** in the settings to save data. If you lose connection, the app securely saves your typing to your device and syncs it later.")
        
        st.subheader("🛡️ 3. Data Sovereignty")
        st.write("You own your data. In the *Privacy Control Center* on your dashboard, you can hit the red button at any time to completely erase your data from the system and the recommendation algorithm.")


def success_page():
    if st.button("🦇", type="secondary"): navigate_to('home')
        
    st.markdown("---")
    st.markdown(f"<h1 style='text-align: center;'>{'ERFOLGSGESCHICHTEN' if lang == 'DE' else 'SUCCESS STORIES'}</h1>", unsafe_allow_html=True)
    
    if lang == "DE":
        st.write("Hier sind einige Beispiele, wie Nachbarn ROBIN genutzt haben, um echte Verbesserungen in unserer Stadt zu bewirken:")
        
        with st.container(border=True):
            st.subheader("🌳 Gemeinschaftsgarten gerettet")
            st.write("Dank 150 Unterstützern auf der Plattform hat die Stadtregierung die Finanzierung für den Erhalt des Gartens in Sektor 3 gesichert.")
            
        with st.container(border=True):
            st.subheader("🚸 Neuer Zebrastreifen an der Grundschule")
            st.write("Eine von einer Vertretung (Proxy) eingereichte Idee führte zu einem sichereren Schulweg für über 200 Kinder.")
            
        with st.container(border=True):
            st.subheader("💡 Mehr Beleuchtung im Nordpark")
            st.write("Eine schnelle 60-Sekunden-Umfrage zeigte, dass sich Anwohner unwohl fühlten. Letzte Woche wurden 5 neue Laternen installiert.")
    else:
        st.write("Here are some examples of how neighbors have used ROBIN to make real improvements in our city:")
        
        with st.container(border=True):
            st.subheader("🌳 Community Garden Saved")
            st.write("Thanks to 150 supporters on the platform, the city government secured funding to maintain the garden in Sector 3.")
            
        with st.container(border=True):
            st.subheader("🚸 New Crosswalk near the Elementary School")
            st.write("An idea submitted by a proxy representative led to a safer school route for over 200 children.")
            
        with st.container(border=True):
            st.subheader("💡 Better Lighting in the North Park")
            st.write("A quick 60-second poll revealed residents felt unsafe. Last week, 5 new streetlights were successfully installed.")

# ==========================================
# 6. MAIN CONTROLLER
# ==========================================
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'feed':
    feed_page()
elif st.session_state.page == 'submit':
    submit_page()
elif st.session_state.page == 'dashboard':
    dashboard_page()
elif st.session_state.page == 'admin':
    admin_page()
elif st.session_state.page == 'how_it_works':
    how_it_works_page()
elif st.session_state.page == 'success':
    success_page()
