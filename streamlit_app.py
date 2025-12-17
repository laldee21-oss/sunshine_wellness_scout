import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""

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
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Hero: Florida sunset beach with pier & palms
st.image("https://thumbs.dreamstime.com/b/tropical-sunset-beach-scene-pier-palm-trees-vibrant-colors-serene-water-rocky-shore-ai-generated-356600072.jpg", use_column_width=True, caption="Welcome to Your Florida Longevity Lifestyle")

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

st.success("**This tool is completely free – no cost, no obligation!**")
st.write("Discover Florida homes designed for active living, natural light, trails, and home wellness spaces.")

# Outdoor wellness trail image
st.image("https://oversee.us/wp-content/uploads/2025/07/FITNESS-RECREATION-IN-MIRAMAR-BEACH.jpg", use_column_width=True, caption="Year-round trails and outdoor fitness in the Sunshine State")

# Inputs...
client_needs = st.text_area("Describe your dream wellness/active home in Florida", height=220, placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
with col2:
    location = st.text_input("Preferred area in Florida", value="Tampa Bay, St. Petersburg, Clearwater, Brandon")

if st.button("🔍 Show Me Free Teaser Matches", type="primary"):
    # (Same Grok call and teaser logic as before – omitted for brevity, copy from previous version)
    # ... [keep your full_prompt, response, teaser building here] ...

    # Modern wellness home image (the vibe you loved!)
    st.image("https://photos.prod.cirrussystem.net/1345/87b5b2578644499ae245ac9c09fe3c1c/2565310842.jpeg", use_column_width=True, caption="Modern Florida homes with pools, light, and space for your longevity lifestyle")

    # Lead capture form (same as before)

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Real estate recommendations powered by AI • Not affiliated with any brokerage</small>", unsafe_allow_html=True)
