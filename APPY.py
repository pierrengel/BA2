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
if "supported_projects" not in st.session_state:
    st.session_state.supported_projects = []
if "mock_ideas" not in st.session_state:
    st.session_state.mock_ideas = [
        {"id": 1, "title": "More benches in Nordpark", "desc": "Seniors need more places to rest when walking in the north park.", "sector": "Sector 4", "tag": "Infrastructure"},
        {"id": 2, "title": "Fix streetlights on Elm St.", "desc": "It gets dangerously dark near the crosswalk after 5 PM.", "sector": "Sector 2", "tag": "Safety"}
    ]

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
       STYLE 1: THE BIG BOXES (Primary Buttons) 
       ========================================= */
    div.stButton > button[kind="primary"] {
        background-color: var(--box-bg) !important;
        color: var(--text-mint) !important;
        border: none !important;
        border-radius: 15px !important;
        
        font-size: 22px !important; 
        text-align: left !important;
        white-space: pre-wrap !important;
        font-family: 'Helvetica', sans-serif !important;
        
        width: 100% !important;
        min-height: 40vh !important; 
        padding: 40px !important;
        margin-top: 20px !important;
        
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: var(--text-mint) !important; 
        color: var(--text-dark) !important;            
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
    }
    
    div.stButton > button[kind="primary"]:hover p {
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
    
    /* Force paragraph tags inside the button to be dark blue (stops mint inheritance) */
    div.stButton > button[kind="tertiary"] p {
        color: var(--text-dark) !important; 
    }
    
    /* Hover state: Light Gray box, Dark Blue text */
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
    
    /* Safely scoped Inputs to prevent weird stretching */
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

    /* Hide default menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. GLOBAL SIDEBAR (Hardware Access)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    st.session_state.lite_mode = st.toggle("Lite Mode (Slow Internet)", value=st.session_state.lite_mode, help="Disables images and heavy media to save data.")
    st.caption("Toggle this if your connection is unstable.")

# ==========================================
# 4. DIALOGS (Modals)
# ==========================================
@st.dialog("Why do you support this?")
def support_dialog(project_id, project_title):
    st.markdown(f"**Idea:** {project_title}")
    st.write("Help the community understand the consensus behind this idea.")
    
    reason = st.radio("Select your primary reason:", ["Improves Safety", "Saves Money", "Builds Community", "Other"], label_visibility="collapsed")
    
    if st.button("Confirm Support", type="tertiary"):
        st.session_state.supported_projects.append(project_id)
        st.toast(f"Thank you! Your voice was added for '{reason}'.", icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# 5. PAGE ROUTING FUNCTIONS
# ==========================================

def home_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 5rem; margin-bottom: 20px;'>ROBIN</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 40px;'>Civic Inclusion Platform</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("COMMUNITY FEED\n\nSee what your neighbors are suggesting and vote on ideas.", type="primary"):
            navigate_to('feed')
        if st.button("MY DASHBOARD\n\nTrack your ideas, manage your identity, and meet neighbors.", type="primary"):
            navigate_to('dashboard')
            
    with col2:
        if st.button("SUBMIT AN IDEA\n\nTell the city about a problem or a new project idea.", type="primary"):
            navigate_to('submit')
        if st.button("CITY ADMIN\n\n(Staff Only) Close the feedback loop on local projects.", type="primary"):
            navigate_to('admin')


def feed_page():
    if st.button("🦇", type="secondary"):
        navigate_to('home')
        
    st.markdown("---")
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>COMMUNITY FEED</h1>", unsafe_allow_html=True)
    
    st.info("📣 **Micro-Wins:** Tom shared his ladder with Anna. | The library got 50 new books! | Streetlight on 5th repaired.", icon="✨")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("⏱️ Got 60 Seconds?")
            st.write("Help shape your neighborhood:")
            st.radio("Does the north park need more lighting?", ["Yes", "No", "Unsure"], key="poll_1")
            if st.button("Vote Instantly", type="tertiary"):
                st.toast("Vote recorded! You just shaped local policy.", icon="🎉")

    with col1:
        sort_by = st.selectbox("Sort community ideas by:", ["Needs Your Voice", "Most Popular", "Recently Added"], index=0)
        
        for idea in st.session_state.mock_ideas:
            with st.container(border=True):
                st.markdown(f"### {idea['title']}")
                st.write(idea['desc'])
                st.caption(f"✨ *Algorithm matched this because you follow [{idea['tag']}] and live in [{idea['sector']}].*")
                
                if idea['id'] in st.session_state.supported_projects:
                    st.button("✅ Supported", disabled=True, key=f"btn_disabled_{idea['id']}")
                else:
                    if st.button("🤝 Support this Idea", key=f"btn_support_{idea['id']}", type="tertiary"):
                        support_dialog(idea['id'], idea['title'])


def submit_page():
    if st.button("🦇", type="secondary"):
        navigate_to('home')
        
    st.markdown("---")
    st.warning("📡 **You are currently offline.** Your typing is automatically saved to your device.", icon="⚠️")
    
    st.markdown("<h1 style='text-align: center;'>SUBMIT AN IDEA</h1>", unsafe_allow_html=True)
    st.progress(st.session_state.wizard_step / 3.0, text=f"Step {st.session_state.wizard_step} of 3")
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center, _ = st.columns([1, 2, 1])
    
    with center:
        if st.session_state.wizard_step == 1:
            st.subheader("1. What is the problem or idea?")
            
            # --- ASSISTED MODE INTEGRATION ---
            assisted_mode = st.toggle("Assisted Mode (Step-by-step guidance)")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not assisted_mode:
                st.text_area("Description", placeholder="E.g., The sidewalk on Main St. is broken...", label_visibility="collapsed")
                st.write("**Or, record a voice message:**")
                st.audio_input("Record your voice", label_visibility="collapsed")
            else:
                st.markdown("#### What kind of project is it?")
                st.pills("Project Type", ["Quick fix", "Big idea", "Other"], label_visibility="collapsed", key="type_select")
                
                st.markdown("#### What resources do you need?")
                resources = ["Hammer", "Workspace", "Drill", "3D Printer", "Paint", "Wood", "Metal", "Soldering Iron", "Laptop"]
                st.multiselect("Resources", resources, label_visibility="collapsed", key="resource_select")
                
                st.markdown("#### Do you want to meet face to face?")
                st.pills("Meeting Preference", ["Yes", "No"], label_visibility="collapsed", key="meeting_select")
            
            # --- NAVIGATION ---
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("Next ➔", type="tertiary"):
                st.toast("System auto-tagged your description with [Infrastructure] and [Accessibility].", icon="🤖")
                st.session_state.wizard_step = 2
                st.rerun()
            if c2.button("💾 Save Draft", type="tertiary"):
                st.toast("Draft saved locally!", icon="💾")

        elif st.session_state.wizard_step == 2:
            st.subheader("2. Where is this located?")
            st.text_input("Location", placeholder="E.g., Corner of 5th and Elm", label_visibility="collapsed")
            
            if not st.session_state.lite_mode:
                st.caption("*(Interactive map would load here, disabled in Lite Mode)*")
                
            c1, c2, c3 = st.columns(3)
            if c1.button("⬅ Back", type="tertiary"):
                st.session_state.wizard_step = 1
                st.rerun()
            if c2.button("Next ➔", type="tertiary"):
                st.session_state.wizard_step = 3
                st.rerun()
            if c3.button("💾 Draft", type="tertiary"):
                st.toast("Draft saved locally!", icon="💾")

        elif st.session_state.wizard_step == 3:
            st.subheader("3. Review & Submit")
            st.info("Your idea looks great. Ready to share it with the community?")
            
            c1, c2 = st.columns(2)
            if c1.button("⬅ Back", type="tertiary"):
                st.session_state.wizard_step = 2
                st.rerun()
            if c2.button("✅ Submit", type="tertiary"):
                st.toast("Idea Submitted! You'll be notified of reviews.", icon="🎉")
                st.session_state.wizard_step = 1
                time.sleep(2)
                navigate_to('home')


def dashboard_page():
    if st.button("🦇", type="secondary"):
        navigate_to('home')
        
    st.markdown("---")
    st.markdown("<h1 style='text-align: center;'>MY DASHBOARD</h1>", unsafe_allow_html=True)
    
    st.selectbox("Currently acting on behalf of:", ["Myself", "Mrs. Schmidt (Proxy)", "Youth Center (Proxy)"])
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("My Identity & Skills")
        st.multiselect("Identity Chips:", ["Beginner", "Happy to Guide", "Rural Local", "Tech Helper", "Translator"], default=["Happy to Guide", "Rural Local"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛡️ Privacy Control Center"):
            st.toggle("Show my real name to neighbors", value=True)
            st.toggle("Allow algorithm to suggest my ideas", value=True)
            if st.button("Forget My Data & Remove", type="tertiary"):
                st.toast("Secure data removal initiated.", icon="🗑️")

    with col2:
        st.subheader("👋 Meet the Community")
        with st.container(border=True):
            st.markdown("**Sarah T.** *(Tech Helper)*")
            if st.button("Say Hello to Sarah", type="tertiary", key="h1"): st.toast("Message sent!")
        with st.container(border=True):
            st.markdown("**Elena R.** *(Translator)*")
            if st.button("Say Hello to Elena", type="tertiary", key="h2"): st.toast("Message sent!")

    st.markdown("---")
    st.subheader("My Submitted Ideas")
    with st.container(border=True):
        st.markdown("**Expand community garden operating hours**")
        st.progress(75, text="Status: City Feedback (Current)")
        st.caption("Submitted ➔ Community Review ➔ **City Feedback (Current)** ➔ Action")
        st.info("The City Parks Department is currently reviewing the budget for this proposal. Expected update: Next Tuesday.")


def admin_page():
    if st.button("🦇", type="secondary"):
        navigate_to('home')
        
    st.markdown("---")
    st.markdown("<h1 style='text-align: center;'>CITY ADMIN</h1>", unsafe_allow_html=True)
    st.write("Ensure citizens feel heard and respected.")
    
    st.subheader("⚠️ Overdue Feedback")
    st.caption("These ideas have passed community review and await official acknowledgement.")
    
    with st.container(border=True):
        st.markdown("**Idea:** Fix potholes on Route 9 *(Submitted by: David L.)*")
        st.error("Waiting for response for 4 days.")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.selectbox("Empathetic Response Template:", 
                         ["Great idea, reviewing budget now.", "Thank you, added to maintenance queue."], key="t1")
        with c2:
            st.write("") 
            if st.button("Send 1-Click Reply", type="tertiary", key="r1"):
                st.toast("Reply sent to David L.", icon="✉️")

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
