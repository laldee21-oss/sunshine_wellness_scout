import streamlit as st
import requests
from openai import OpenAI
import re

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

MODEL_NAME = "grok-4-1-fast-reasoning"

# CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
    .chat-container { margin-top: 3rem; padding: 1.5rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .user-message { background: #ea580c; color: white; padding: 12px; border-radius: 15px; margin: 8px 0; text-align: right; max-width: 80%; margin-left: auto; }
    .assistant-message { background: #f0f0f0; color: #0c4a6e; padding: 12px; border-radius: 15px; margin: 8px 0; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# Back to Team
if st.button("← Back to Team"):
    st.session_state.selected_agent = None
    st.session_state.chat_history = {}
    st.rerun()

# Auto-scroll to interaction
st.markdown("<div id='agent-interaction'></div>", unsafe_allow_html=True)
st.markdown("""
<script>
    const element = document.getElementById('agent-interaction');
    if (element) element.scrollIntoView({ behavior: 'smooth', block: 'start' });
</script>
""", unsafe_allow_html=True)

# Hero image
st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", use_column_width=True, caption="Your Keys Await – Welcome to your longevity lifestyle")

st.markdown("### 🏡 FRED – Your Wellness Home Scout")
st.success("**This tool is completely free – no cost, no obligation! You will receive the full personalized report below and via email.**")
st.write("The perfect home that supports your lifestyle awaits — anywhere in the U.S.!")

client_needs = st.text_area("DESCRIBE YOUR DREAM WELLNESS NEEDS IN DETAIL. LET FRED DO THE REST!!!", height=220,
                            placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
with col2:
    location = st.text_input("Preferred state or area (e.g., North Carolina, Asheville, Tampa FL)", value="")

st.markdown("### Refine Your Report (Optional)")
report_sections = st.multiselect(
    "Select sections to include:",
    ["Introduction summary", "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)",
     "Top 5 Must-Have Home Features", "Wellness/Outdoor Highlights"],
    default=["Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)", "Top 5 Must-Have Home Features", "Wellness/Outdoor Highlights"]
)

if st.button("🔍 GENERATE MY REPORT", type="primary"):
    if not client_needs.strip():
        st.warning("Please describe your lifestyle needs above!")
    else:
        with st.spinner("Fred is crafting your personalized report..."):
            sections_prompt = ""
            if "Introduction summary" in report_sections:
                sections_prompt += "### Introduction\n5-6 sentences introducing how well their needs match the area and budget.\n\n"
            if "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)" in report_sections:
                sections_prompt += "### Top 5 Neighborhoods/Suburbs and Why They Fit\n1. [Neighborhood] - [5-8 sentences] [Fun facts: 3-5 sentences]\n(repeat 2-5)\n\n"
            if "Top 5 Must-Have Home Features" in report_sections:
                sections_prompt += "### Top 5 Must-Have Home Features\n1. [Feature] - [5-8 sentences]\n(repeat 2-5)\n\n"
            if "Wellness/Outdoor Highlights" in report_sections:
                sections_prompt += "### Wellness/Outdoor Highlights\n6-10 sentences on trails, parks, etc.\n\n"

            full_prompt = f"""
            Client description: {client_needs}
            Budget: ${budget:,}
            Location: {location or 'wellness-friendly U.S. areas'}
            You are Fred, professional wellness real estate advisor.
            Follow this exact structure only:
            {sections_prompt}
            Professional, clear tone. No extra commentary.
            """

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Fred, a professional real estate advisor."},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                full_report = response.choices[0].message.content
                st.success("Fred found your perfect matches! Here's your personalized report:")
                st.markdown(full_report)

                # Add report to chat history so follow-ups remember it
                if "fred" not in st.session_state.chat_history:
                    st.session_state.chat_history["fred"] = []
                st.session_state.chat_history["fred"].append({"role": "assistant", "content": f"Here's your full wellness home report:\n\n{full_report}"})

                # Email form
                st.markdown("### Get Your Full Report Emailed")
                with st.form("lead_form", clear_on_submit=True):
                    name = st.text_input("Your Name")
                    email = st.text_input("Email (required)", placeholder="you@example.com")
                    phone = st.text_input("Phone (optional)")
                    submitted = st.form_submit_button("📧 Send My Full Report")
                    if submitted:
                        if not email:
                            st.error("Email is required!")
                        else:
                            data = {
                                "from": "reports@lbllifestyle.com",
                                "to": [email],
                                "cc": [YOUR_EMAIL],
                                "subject": f"{name or 'Client'}'s LBL Wellness Home Report",
                                "text": f"Hi {name or 'there'},\n\nThank you for using LBL Lifestyle Solutions.\n\nHere's your report:\n\n{full_report}\n\nBest,\nFred & LBL Team"
                            }
                            headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                            try:
                                resp = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                                if resp.status_code == 200:
                                    st.success(f"Report sent to {email}!")
                                    st.balloons()
                                else:
                                    st.error(f"Failed: {resp.text}")
                            except Exception as e:
                                st.error(str(e))
            except Exception as e:
                st.error("Fred is busy... try again soon.")
                st.caption(f"Error: {e}")

# Chat Box
st.markdown("### Have a follow-up question? Chat with me!")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if "fred" not in st.session_state.chat_history:
    st.session_state.chat_history["fred"] = []

for msg in st.session_state.chat_history["fred"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Ask Fred a question..."):
    st.session_state.chat_history["fred"].append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States."},
                    *st.session_state.chat_history["fred"]
                ],
                max_tokens=800,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history["fred"].append({"role": "assistant", "content": reply})
            st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Trouble connecting. Try again.")
            st.caption(f"Error: {e}")

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
