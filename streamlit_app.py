import streamlit as st

# ===================================================
# SESSION STATE INITIALIZATION
# ===================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "fred": [],
        "greg": [],
        "zoey": [],
        "nora": []
    }

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if st.session_state.current_page not in ["home", "fred", "greg", "zoey", "nora"]:
    st.session_state.current_page = "home"

def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()

# ===================================================
# NEW PROFESSIONAL CSS + FONTS
# ===================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa, #e6f0fa);
        color: #1e3a2f;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, .main-header {
        font-family: 'Playfair Display', serif;
        color: #2d6a4f;
        font-weight: 600;
    }
    .tagline {
        font-size: 2rem;
        color: #40916c;
        font-style: italic;
    }
    .stButton>button {
        background-color: #2d6a4f;
        color: white;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        height: 3.5em;
        border: none;
        box-shadow: 0 4px 8px rgba(45, 106, 79, 0.2);
    }
    .stButton>button:hover {
        background-color: #40916c;
    }
    .stSuccess, .stInfo {
        background-color: #d8f0e6;
        border-left: 5px solid #40916c;
    }
    .stWarning {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    img {
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .agent-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #2d6a4f;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================
# HOME PAGE
# ===================================================

if st.session_state.current_page == "home":
    st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)

    st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", caption="Your Longevity Blueprint")

    st.markdown("<h2>How It Works – 3 Simple Steps</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; font-size: 1.4rem; line-height: 1.9; max-width: 900px; margin: auto;'>
    1. **Choose Your Agent** – Click one of the team members below to get started.<br><br>
    2. **Get Personalized Guidance** – Fill out the form or chat — your agent will create a custom report or plan just for you.<br><br>
    3. **Build Your Longevity Lifestyle** – Save your reports, come back anytime, and unlock more agents as you go!<br><br>
    Ready to live better longer? 👇 Pick an agent below!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### MEET THE LIFESTYLE TEAM")
    st.markdown("<p style='text-align:center; color:#1e3a2f; font-size:1.2rem;'>Click an agent to begin your longevity journey</p>", unsafe_allow_html=True)

    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
        st.markdown("<div style='font-size: 1.1rem; line-height: 1.6;'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused advisor helping you find or create a home that supports your longevity lifestyle — anywhere in the U.S.</div>", unsafe_allow_html=True)
        if st.button("Talk to Fred →", key="fred_home"):
            navigate_to("fred")

    with cols[1]:
        st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
        st.markdown("<div style='font-size: 1.1rem; line-height: 1.6;'>*YOUR PERSONAL TRAINER* <br>A motivated coach building sustainable strength, mobility, and endurance routines tailored to your goals.</div>", unsafe_allow_html=True)
        if st.button("Talk to Greg →", key="greg_home"):
            navigate_to("greg")

    with cols[2]:
        st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
        st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
        st.markdown("<div style='font-size: 1.1rem; line-height: 1.6;'>*YOUR HEALTH EDUCATOR* <br>A compassionate guide helping you understand labs, symptoms, and preventive wellness habits.</div>", unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe →", key="zoey_home"):
            navigate_to("zoey")

    with cols[3]:
        st.markdown("<div class='agent-name'>NORA</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/cJqPm9BP/pexels-tessy-agbonome-521343232-18252407.jpg", width=200)
        st.markdown("<div style='font-size: 1.1rem; line-height: 1.6;'>*YOUR NUTRITION COACH* <br>Personalized, sustainable eating plans focused on joy, balance, and long-term health.</div>", unsafe_allow_html=True)
        if st.button("Talk to Nora →", key="nora_home"):
            navigate_to("nora")

    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

# ===================================================
# AGENT PAGES
# ===================================================

elif st.session_state.current_page == "fred":
    import pages.fred as fred_page
    fred_page.show()

elif st.session_state.current_page == "greg":
    import pages.greg as greg_page
    greg_page.show()

elif st.session_state.current_page == "zoey":
    import pages.nurse_zoey_zoe as zoey_page
    zoey_page.show()

elif st.session_state.current_page == "nora":
    import pages.nora as nora_page
    nora_page.show()
