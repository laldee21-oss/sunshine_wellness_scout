import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}  # {agent: [{"role": "user/assistant", "content": "..."}]}

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# CSS (same as before)
st.markdown("""
<style>
    /* ... your existing CSS ... */
    .chat-message { padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
    .user-message { background: #ea580c; color: white; text-align: right; }
    .assistant-message { background: #f0f0f0; color: #0c4a6e; }
</style>
""", unsafe_allow_html=True)

# Header & Hero (same)
st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)
st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", use_column_width=True, caption="Your Longevity Blueprint")

# Motivating section (same)
# ... (your motivation text)

# Team selection (same)
# ... (your 3-column agent cards)

st.markdown("---")

# === Agent Content with Chat ===
MODEL_NAME = "grok-4-1-fast-reasoning"

def get_agent_system_prompt(agent):
    if agent == "fred":
        return "You are Fred, a professional, goal-focused real estate advisor specializing in wellness homes across the U.S. Answer only real estate, location, neighborhood, cost of living, safety, healthcare, commute, schools, culture, and lifestyle questions. If asked about workouts, nutrition, or health conditions, say: 'That's a great question! Greg (Fitness) or Nurse Zoey Zoe (Health) can help with that — go talk to them!' Keep responses concise, friendly, and helpful."
    elif agent == "greg":
        return "You are Greg, a motivated, encouraging personal trainer. Answer only workout, fitness, strength, endurance, and exercise questions. If asked about homes or health conditions, say: 'Great question! Fred can help with homes, and Nurse Zoey Zoe with health insights — head over to them!' Be energetic and supportive."
    elif agent == "zoey":
        return "You are Nurse Zoey Zoe, a compassionate, caring nurse providing general wellness education. Answer general health, wellness, and lifestyle questions. Never diagnose. If asked about workouts or homes, say: 'That's perfect for Greg (Fitness) or Fred (Home Scout) — they'll give you tailored advice!' Be warm and reassuring."

if st.session_state.selected_agent:
    agent = st.session_state.selected_agent
    st.markdown(f"### Chat with {agent.capitalize() if agent != 'zoey' else 'Nurse Zoey Zoe'}")

    # Initialize chat history for this agent
    if agent not in st.session_state.chat_history:
        st.session_state.chat_history[agent] = []

    # Display chat history
    for msg in st.session_state.chat_history[agent]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-message user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input(f"Ask {agent.capitalize() if agent != 'zoey' else 'Nurse Zoey Zoe'} a question...")
    if user_input:
        # Add user message
        st.session_state.chat_history[agent].append({"role": "user", "content": user_input})
        st.markdown(f"<div class='chat-message user-message'>{user_input}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": get_agent_system_prompt(agent)},
                        *st.session_state.chat_history[agent]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                assistant_reply = response.choices[0].message.content
                st.session_state.chat_history[agent].append({"role": "assistant", "content": assistant_reply})
                st.markdown(f"<div class='chat-message assistant-message'>{assistant_reply}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Sorry, I'm having trouble thinking right now. Try again soon!")

    # Keep existing agent logic (Fred report, Greg plan, Zoey insights) above or below chat as preferred

# Keep your existing Fred/Greg/Zoey report generation code here (above or below chat)

# Footer
st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
