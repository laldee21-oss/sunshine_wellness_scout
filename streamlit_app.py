import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "fred"

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Florida-themed CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffecd2, #fcb69f);
        color: #0c4a6e;
    }
    .main-header { font-size: 3rem; color: #ea580c; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .tagline { font-size: 1.8rem; color: #166534; text-align: center; font-style: italic; margin-bottom: 2rem; }
    .agent-card { text-align: center; padding: 1.5rem; border-radius: 15px; background: rgba(255,255,255,0.9); box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 10px; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3em; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

# Hero image (your favorite biker sunset)
st.image("https://www.floridarambler.com/wp-content/uploads/2023/04/shark-valley-biker-everglades.jpg", use_column_width=True, caption="Your Florida Longevity Lifestyle – Active Trails at Sunset")

# === Meet Your LBL Wellness Team ===
st.markdown("### Meet Your LBL Wellness Team")

cols = st.columns(2)

with cols[0]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://thumbs.dreamstime.com/b/cartoon-realtor-presenting-colorful-house-model-style-stands-facing-forward-white-background-wearing-dark-blue-suit-393019561.jpg", width=150)  # Fred #4
    st.markdown("**Fred**")
    st.markdown("*Wellness Home Scout*  \nProfessional goal-focused realtor")
    if st.button("Talk to Fred", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://www.shutterstock.com/image-vector/man-struggling-lift-heavy-barbell-260nw-2699957111.jpg", width=150)  # Greg #0
    st.markdown("**Greg**")
    st.markdown("*Personal Trainer*  \nMotivated gym rat")
    if st.button("Talk to Greg", key="greg", use_container_width=True):
        st.session_state.selected_agent = "greg"
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# === Agent Content ===
if st.session_state.selected_agent == "fred":
    st.markdown("### 🏡 Fred – Your Wellness Home Scout")
    st.success("**This tool is completely free – no cost, no obligation!**")
    st.write("Find the perfect Florida home that supports trails, natural light, home gym space, and active living.")

    # Group fitness image
    st.image("https://thebiostation.com/wp-content/uploads/2023/06/outdoor-group-exercise-class-scaled.jpg", use_column_width=True, caption="Community wellness – part of your Florida longevity lifestyle")

    # (rest of Fred's code - inputs, Grok call, teaser, form - same as before)

elif st.session_state.selected_agent == "greg":
    st.markdown("### 💪 Greg – Your Personal Trainer")
    st.write("Motivated gym rat helping you build strength, endurance, and longevity.")

    # (rest of Greg's code - inputs, Grok plan - same as before)

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
