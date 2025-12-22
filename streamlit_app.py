import streamlit as st
import streamlit_analytics2 as analytics

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
# TOP NAVIGATION BAR (SHARED ACROSS ALL PAGES)
# ===================================================
def show_top_navigation():
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        if st.button("🏡 Home", use_container_width=True, key="nav_home"):
            navigate_to("home")
    with cols[1]:
        if st.button("🏠 Fred", use_container_width=True, key="nav_fred"):
            navigate_to("fred")
    with cols[2]:
        if st.button("💪 Greg", use_container_width=True, key="nav_greg"):
            navigate_to("greg")
    with cols[3]:
        if st.button("🩺 Zoey", use_container_width=True, key="nav_zoey"):
            navigate_to("zoey")
    with cols[4]:
        if st.button("🥗 Nora", use_container_width=True, key="nav_nora"):
            navigate_to("nora")
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# ===================================================
# START ANALYTICS TRACKING
# ===================================================
with analytics.track():
    # Always show top navigation first
    show_top_navigation()

    # ===================================================
    # HOME PAGE
    # ===================================================
    if st.session_state.current_page == "home":
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
          
            .stApp {
                background: linear-gradient(to bottom, #f5f7fa, #e0e7f0);
                color: #1e3a2f;
                font-family: 'Inter', sans-serif;
            }
            h1, h2, h3, .main-header {
                font-family: 'Playfair Display', serif;
                color: #2d6a4f;
                font-weight: 600;
            }
            /* ... (rest of your original CSS unchanged) */
            .stButton>button {
                background-color: #2d6a4f;
                color: white;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1.1rem;
                height: 3.5em;
                width: 100%;
                border: none;
                box-shadow: 0 4px 8px rgba(45, 106, 79, 0.2);
            }
            .stButton>button:hover {
                background-color: #40916c;
            }
            img {
                border-radius: 16px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            }
        </style>
        """, unsafe_allow_html=True)
        # ... (ALL your original home page content exactly as before)
        # Just note: all home page buttons now use navigate_to() — already did!

        # Example (your existing button code is fine, just shown for context):
        if st.button("Talk to Fred →", key="fred_home"):
            navigate_to("fred")
        # ... same for others

        # Footer unchanged
        st.markdown("---")
        st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

    # ===================================================
    # AGENT PAGES (IMPORTS UNCHANGED)
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
