import streamlit as st
import time

# ==========================================
# PAGE CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(page_title="ROBIN | Civic Inclusion", page_icon="🐦", layout="centered")

# Initialize Session State Variables
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "draft_saved" not in st.session_state:
    st.session_state.draft_saved = False
if "lite_mode" not in st.session_state:
    st.session_state.lite_mode = False
if "supported_projects" not in st.session_state:
    st.session_state.supported_projects = []
if "mock_ideas" not in st.session_state:
    st.session_state.mock_ideas = [
        {"id": 1, "title": "More benches in Nordpark", "desc": "Seniors need more places to rest when walking in the north park.", "sector": "Sector 4", "tag": "Infrastructure"},
        {"id": 2, "title": "Fix streetlights on Elm St.", "desc": "It gets dangerously dark near the crosswalk after 5 PM.", "sector": "Sector 2", "tag": "Safety"}
    ]

# ==========================================
# DIALOGS (Modals)
# ==========================================
@st.dialog("Why do you support this?")
def support_dialog(project_id, project_title):
    st.write(f"**Idea:** {project_title}")
    st.write("Help the community understand the consensus behind this idea.")
    
    # Deliberative Consensus Options
    reason = st.pills("Select your primary reason:", ["Improves Safety", "Saves Money", "Builds Community", "Other"])
    
    if st.button("Confirm Support", type="primary"):
        st.session_state.supported_projects.append(project_id)
        st.toast(f"Thank you! Your voice was added for '{reason}'.", icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# SIDEBAR NAVIGATION & HARDWARE ACCESS
# ==========================================
with st.sidebar:
    st.title("🐦 ROBIN")
    st.caption("Civic Inclusion Platform")
    st.divider()
    
    # 1. Hardware & Access: Lite Mode Toggle
    st.session_state.lite_mode = st.toggle("Lite Mode (Slow Internet)", value=st.session_state.lite_mode, help="Disables images and heavy media to save data.")
    
    st.subheader("Navigation")
    page = st.radio("Go to:", ["Home Feed", "Submit an Idea", "My Dashboard", "City Admin"], label_visibility="collapsed")

# ==========================================
# PAGE 1: HOME FEED (Power Dynamics & Time Poverty)
# ==========================================
if page == "Home Feed":
    st.header("Community Feed")
    
    # 4. Power Dynamics: Micro-Wins Ticker
    st.info("📣 **Micro-Wins:** Tom just shared his ladder with Anna. | The library received 50 new books! | Streetlight on 5th Ave repaired yesterday.", icon="✨")
    
    # 5. Time Poverty: Micro-Participation Poll
    with st.container(border=True):
        st.subheader("⏱️ Got 60 Seconds?")
        st.write("Help shape your neighborhood quickly:")
        poll_response = st.radio("Does the north park need more lighting?", ["Yes, it feels unsafe", "No, it's fine", "Unsure / I don't go there"], horizontal=True)
        if st.button("Submit Vote"):
            st.toast("Vote recorded! You just helped shape local policy.", icon="🎉")
            
    st.divider()
    
    # 4. Power Dynamics: Equity-Weighted Feed
    sort_by = st.selectbox("Sort community ideas by:", ["Needs Your Voice", "Most Popular", "Recently Added"], index=0, help="We prioritize ideas that need diverse perspectives.")
    
    st.subheader(f"Ideas — {sort_by}")
    
    for idea in st.session_state.mock_ideas:
        with st.container(border=True):
            st.markdown(f"### {idea['title']}")
            st.write(idea['desc'])
            
            # 4. Power Dynamics: XAI Labels
            st.caption(f"✨ **Suggested because you follow [{idea['tag']}] and live in [{idea['sector']}].**", 
                       help="Our equity algorithm surfaces ideas relevant to your location and interests to ensure diverse neighborhood representation.")
            
            if idea['id'] in st.session_state.supported_projects:
                st.button("✅ You supported this idea", disabled=True, key=f"btn_disabled_{idea['id']}")
            else:
                # 4. Power Dynamics: Deliberative Consensus Button
                if st.button("🤝 Support this Idea", key=f"btn_support_{idea['id']}"):
                    support_dialog(idea['id'], idea['title'])

# ==========================================
# PAGE 2: SUBMIT AN IDEA (Self-Efficacy & Hardware)
# ==========================================
elif page == "Submit an Idea":
    # 1. Hardware & Access: Offline Banner
    st.warning("📡 **You are currently offline.** Your typing is automatically saved to your device. We will upload it when you reconnect.", icon="⚠️")
    
    st.header("Share an Idea or Problem")
    st.progress(st.session_state.wizard_step / 3.0, text=f"Step {st.session_state.wizard_step} of 3")
    
    # 6. Self-Efficacy: Scaffolded Wizard UI & Asynchronous Design
    if st.session_state.wizard_step == 1:
        st.subheader("What is the problem or idea?")
        problem_desc = st.text_area("Describe it in your own words:", placeholder="E.g., The sidewalk on Main St. is broken and hard for wheelchairs...")
        
        # 6. Self-Efficacy: Multi-Modal Voice Input
        st.write("**Or, record a voice message:**")
        audio_val = st.audio_input("Record your voice")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        if col1.button("Next ➔", type="primary"):
            # 6. Self-Efficacy: Vernacular Mapping via Toast
            st.toast("System auto-tagged your description with [Infrastructure] and [Accessibility].", icon="🤖")
            st.session_state.wizard_step = 2
            st.rerun()
        if col3.button("💾 Save Draft for Later", key="draft_1"):
            st.toast("Draft saved locally!", icon="💾")

    elif st.session_state.wizard_step == 2:
        st.subheader("Where is this located?")
        location = st.text_input("Enter a street, landmark, or park name:", placeholder="E.g., Corner of 5th and Elm")
        
        # 1. Hardware & Access: Lite mode check for maps
        if not st.session_state.lite_mode:
            st.caption("*(Interactive map would load here, but it is disabled in Lite Mode)*")
            
        col1, col2, col3 = st.columns([1, 1, 2])
        if col1.button("Next ➔", type="primary"):
            st.session_state.wizard_step = 3
            st.rerun()
        if col2.button("⬅ Back"):
            st.session_state.wizard_step = 1
            st.rerun()
        if col3.button("💾 Save Draft for Later", key="draft_2"):
            st.toast("Draft saved locally!", icon="💾")

    elif st.session_state.wizard_step == 3:
        st.subheader("Review & Submit")
        st.info("Your idea looks great. Ready to share it with the community?")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        if col1.button("✅ Submit to Community", type="primary"):
            st.toast("Idea Submitted! You'll be notified when people review it.", icon="🎉")
            st.session_state.wizard_step = 1  # Reset
            time.sleep(2)
            st.rerun()
        if col2.button("⬅ Back"):
            st.session_state.wizard_step = 2
            st.rerun()
        if col3.button("💾 Save Draft for Later", key="draft_3"):
            st.toast("Draft saved locally!", icon="💾")

# ==========================================
# PAGE 3: MY DASHBOARD (Identity & Relational)
# ==========================================
elif page == "My Dashboard":
    st.header("My Neighborhood Profile")
    
    # 2. Social Proxy
    st.selectbox("Currently acting on behalf of:", ["Myself", "Mrs. Schmidt (Proxy)", "Local Youth Center (Proxy)"], help="Switch profiles if you are helping someone else submit feedback.")
    st.divider()
    
    # 3. Identity Friction: Mentorship Badges
    st.subheader("My Identity & Skills")
    badges = st.multiselect("Select Identity Chips to show how you participate:", 
                            ["Beginner", "Happy to Guide", "Rural Local", "Tech Helper", "Translator", "Long-time Resident"],
                            default=["Happy to Guide", "Rural Local"])
    
    # 2. Relational Onboarding: Meet the Community
    st.subheader("👋 Meet the Community")
    st.write("Connect with neighbors who share your interests.")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            if not st.session_state.lite_mode: st.markdown("👤") # Placeholder avatar
            st.markdown("**Sarah T.**\n*(Tech Helper)*")
            if st.button("Say Hello", key="hello_1", use_container_width=True): st.toast("Message sent to Sarah T.!")
    with c2:
        with st.container(border=True):
            if not st.session_state.lite_mode: st.markdown("👤")
            st.markdown("**Marcus J.**\n*(Local Business)*")
            if st.button("Say Hello", key="hello_2", use_container_width=True): st.toast("Message sent to Marcus J.!")
    with c3:
        with st.container(border=True):
            if not st.session_state.lite_mode: st.markdown("👤")
            st.markdown("**Elena R.**\n*(Translator)*")
            if st.button("Say Hello", key="hello_3", use_container_width=True): st.toast("Message sent to Elena R.!")

    st.divider()

    # 7. The Feedback Void: Pizza Tracker
    st.subheader("My Submitted Ideas")
    with st.container(border=True):
        st.markdown("**Expand community garden operating hours**")
        # Step 3 out of 4 is active
        st.progress(75, text="Status: City Feedback (Current)")
        st.caption("Submitted ➔ Community Review ➔ **City Feedback (Current)** ➔ Action")
        st.info("The City Parks Department is currently reviewing the budget for this proposal. Expected update: Next Tuesday.")

    st.divider()
    
    # 3. Identity Friction: Data Sovereignty
    with st.expander("🛡️ Privacy Control Center"):
        st.write("You own your data. Choose how you want to be seen.")
        st.toggle("Show my real name to verified neighbors", value=True)
        st.toggle("Allow algorithm to suggest my ideas to others", value=True)
        st.divider()
        st.warning("Danger Zone")
        if st.button("Forget My Data & Remove from Algorithm", type="primary"):
            st.toast("Action logged: Initiating secure data removal protocol.", icon="🗑️")

# ==========================================
# PAGE 4: CITY ADMIN (The Feedback Void)
# ==========================================
elif page == "City Admin":
    st.header("Admin Dashboard: Closing the Feedback Loop")
    st.write("Ensure citizens feel heard and respected.")
    
    # 7. The Feedback Void: Mandated Micro-Responses
    st.subheader("⚠️ Overdue Feedback")
    st.caption("These citizen ideas have passed community review and are awaiting official acknowledgement.")
    
    # Mock Admin Task 1
    with st.container(border=True):
        st.markdown("**Idea:** Fix potholes on Route 9 (Submitted by: David L.)")
        st.markdown("*Waiting for response for 4 days.*")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            template1 = st.selectbox("Select Empathetic Response Template:", 
                                     ["Great idea, reviewing budget now.", 
                                      "Thank you for reporting, we've added this to the maintenance queue.", 
                                      "We hear you. We are currently gathering more data on this issue."], 
                                     key="admin_sel_1")
        with col2:
            st.write("") # Spacing
            st.write("")
            if st.button("Send 1-Click Reply", type="primary", key="admin_btn_1"):
                st.toast(f"Reply sent to David L.: '{template1}'", icon="✉️")

    # Mock Admin Task 2
    with st.container(border=True):
        st.markdown("**Idea:** New crosswalk near the elementary school (Submitted by: Proxy - Mrs. Schmidt)")
        st.markdown("*Waiting for response for 6 days.*")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            template2 = st.selectbox("Select Empathetic Response Template:", 
                                     ["We hear you. We are currently gathering more data on this issue.",
                                      "Great idea, reviewing budget now.", 
                                      "Thank you for reporting, we've added this to the maintenance queue."], 
                                     key="admin_sel_2")
        with col2:
            st.write("") 
            st.write("")
            if st.button("Send 1-Click Reply", type="primary", key="admin_btn_2"):
                st.toast(f"Reply sent to Mrs. Schmidt: '{template2}'", icon="✉️")
