import streamlit as st
from openai import OpenAI

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # Set page title
    st.set_page_config(page_title="Nurse Zoey Zoe – Your Health Assessor | LBL Lifestyle Solutions", page_icon="🩺")

    # Safe chat history initialization for this agent
    agent_key = "zoey"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if agent_key not in st.session_state.chat_history:
        st.session_state.chat_history[agent_key] = []

    # HIGH-CONTRAST PROFESSIONAL DESIGN
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear_gradient(to bottom, #f5f7fa, #e0e7f0);
            color: #1e3a2f;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #2d6a4f;
            font-weight: 600;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div[data-baseweb="select"] > div,
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2d6a4f !important;
        }
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: #1e3a2f !important;
        }
        .stChatInput > div {
            background-color: white !important;
            border: 2px solid #2d6a4f !important;
            border-radius: 20px !important;
        }
        .stChatInput > div > div > input {
            color: #1e3a2f !important;
        }
        .stChatMessage {
            background-color: transparent !important;
        }
        .optional-box {
            background-color: #f0f7fc !important;
            border: 2px solid #a0c4d8 !important;
            border-left: 6px solid #2d6a4f !important;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 25px;
        }
        label {
            font-weight: 600 !important;
            color: #2d6a4f !important;
            font-size: 1.05rem !important;
        }
        .separator {
            margin: 35px 0;
            border-top: 1px solid #c0d8e0;
        }
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            border-radius: 12px;
            font-weight: 600;
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

    # Force scroll to top — delayed to override chat focus
    st.markdown("""
    <script>
        // Immediate
        window.scrollTo(0, 0);
        const main = parent.document.querySelector('section.main');
        if (main) main.scrollTop = 0;
        // Delayed override
        setTimeout(() => {
            window.scrollTo(0, 0);
            if (main) main.scrollTop = 0;
        }, 200);
    </script>
    """, unsafe_allow_html=True)

    # Hero image
    st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", caption="LIVE BETTER LONGER – Welcome to your longevity lifestyle")

    # Welcome & Disclaimer
    st.markdown("### 🩺 Hello! I'm Nurse Zoey Zoe – Your Friendly Health Educator")
    st.write("Welcome to my clinic! I'm here to help you understand your health, labs, symptoms, and preventive habits — all in support of living better longer.")
    st.success("**This tool is completely free – no cost, no obligation! Your full insights will be emailed if requested.**")
    st.warning("**Important**: I am not a doctor and do not provide medical diagnoses, treatments, or prescriptions. This is general education only. Always consult a licensed healthcare professional for personal medical advice.")

    # Name Input — blank by default, safe fallback
    st.markdown("### What's your name?")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="zoey_name_input_unique")
    if user_name.strip():
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = st.session_state.get("user_name", "")

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Explain my bloodwork in simple terms
        - What lifestyle changes help lower blood pressure?
        - Review my symptoms and when to see a doctor
        - Suggest preventive screenings for my age
        """)

    # Input form
    st.markdown("### Tell Zoey about your health questions or data")
    st.write("**Be as detailed as possible!** Share symptoms, labs, lifestyle, concerns, or goals — the more context, the better the educational insights.")
    st.caption("💡 Tip: Include age, symptoms duration, current habits, family history, or specific questions!")

    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text, image)", type=["pdf", "txt", "jpg", "png"])
    health_data = st.text_area("Or enter data manually", height=200, placeholder="Example: Blood pressure 138/88, fasting glucose 105, cholesterol 220, family history of heart disease, age 58, occasional fatigue...")
    question = st.text_input("Your main question or concern (optional)", placeholder="Example: What lifestyle changes can help lower blood pressure naturally?")

    st.markdown("### Refine Your Insights (Optional)")
    st.write("Core insights always include key findings and general recommendations. Add extras:")
    insight_sections = st.multiselect(
        "Add optional sections:",
        [
            "Sleep Optimization Tips",
            "Stress Management Strategies",
            "Nutrition for Longevity",
            "Exercise Recommendations",
            "Preventive Screening Guidelines",
            "Supplement Education (general)",
            "When to See a Doctor"
        ],
        default=["Sleep Optimization Tips", "Stress Management Strategies", "Nutrition for Longevity"]
    )

    if st.button("Get Insights", type="primary"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Nurse Zoey Zoe is reviewing..."):
                file_content = ""
                if uploaded_file:
                    try:
                        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                    except:
                        file_content = "[File uploaded — content partially read]"
                combined = file_content or health_data
                core_prompt = """
### Key Insights
Bullet points summarizing general educational observations from the data/question.
### General Recommendations
Evidence-based lifestyle suggestions.
### Next Steps
When to consult a professional and what to discuss.
"""
                optional_prompt = ""
                if "Sleep Optimization Tips" in insight_sections:
                    optional_prompt += "### Sleep Optimization Tips\nPractical habits for better rest and recovery.\n\n"
                if "Stress Management Strategies" in insight_sections:
                    optional_prompt += "### Stress Management Strategies\nBreathing, mindfulness, daily routines.\n\n"
                if "Nutrition for Longevity" in insight_sections:
                    optional_prompt += "### Nutrition for Longevity\nFood choices for heart health, inflammation, energy.\n\n"
                if "Exercise Recommendations" in insight_sections:
                    optional_prompt += "### Exercise Recommendations\nSafe movement for your age and goals.\n\n"
                if "Preventive Screening Guidelines" in insight_sections:
                    optional_prompt += "### Preventive Screening Guidelines\nAge-appropriate tests and checkups.\n\n"
                if "Supplement Education (general)" in insight_sections:
                    optional_prompt += "### Supplement Education (general)\nCommon options and evidence overview — consult doctor before starting.\n\n"
                if "When to See a Doctor" in insight_sections:
                    optional_prompt += "### When to See a Doctor\nRed flags and urgency guidance.\n\n"
                full_insights_prompt = core_prompt + """
### Sleep Optimization Tips
Practical habits.
### Stress Management Strategies
Daily techniques.
### Nutrition for Longevity
Food choices.
### Exercise Recommendations
Movement ideas.
### Preventive Screening Guidelines
Recommended tests.
### Supplement Education (general)
Overview — consult doctor.
### When to See a Doctor
Red flags.
"""
                base_prompt = f"""
User name: {st.session_state.user_name or 'friend'}
Data/Question: {combined or 'General wellness inquiry'}
Specific question: {question or 'Overall health insights'}
Provide general education only. Never diagnose or prescribe.
Use phrases like "Generally speaking..." or "Standard guidelines suggest...".
"""
                try:
                    # Display insights
                    display_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                        max_tokens=2000,
                        temperature=0.6
                    )
                    display_insights = display_response.choices[0].message.content

                    # Full insights for email
                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + "\n" + full_insights_prompt}],
                        max_tokens=3000,
                        temperature=0.6
                    )
                    full_insights = full_response.choices[0].message.content

                    st.success("Nurse Zoey Zoe's insights:")
                    st.markdown(display_insights)

                    st.session_state.full_insights_for_email = full_insights

                    st.info("📧 Want the **complete version** with every section? Fill in the email form below!")

                    # Follow-up suggestions
                    st.markdown("### Would you like me to...")
                    st.markdown("""
                    - Explain any part in more detail?
                    - Suggest lifestyle changes for a specific concern?
                    - Help prepare questions for your doctor?
                    - Coordinate with Nora for nutrition tips?
                    """)
                except Exception as e:
                    st.error("Nurse Zoey Zoe is consulting... try again.")
                    st.caption(f"Error: {str(e)}")

    # Email form
    if "full_insights_for_email" in st.session_state:
        st.markdown("### Get Your Full Insights Emailed (Save & Share)")
        with st.form("lead_form_zoey", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Insights")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    insights_to_send = st.session_state.full_insights_for_email
                    email_body = f"""Hi {st.session_state.user_name or 'friend'},

Thank you for trusting Nurse Zoey Zoe at LBL Lifestyle Solutions.

Here's your COMPLETE personalized wellness insights:

{insights_to_send}

Remember: This is general education. Always consult your healthcare provider.

Warm regards,
Nurse Zoey Zoe & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [st.secrets["YOUR_EMAIL"]],
                        "subject": f"{st.session_state.user_name or 'Client'}'s Complete LBL Wellness Insights",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {st.secrets['RESEND_API_KEY']}",
                        "Content-Type": "application/json"
                    }
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Full insights sent to {email}! Check your inbox.")
                            st.balloons()
                            if "full_insights_for_email" in st.session_state:
                                del st.session_state.full_insights_for_email
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # Streamlined chat
    st.markdown("### Have a follow-up question? Chat with Nurse Zoey Zoe in the box below! 🩺")
    st.caption("Ask about symptoms, habits, prevention — I'm here to educate and support.")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Nurse Zoey Zoe a question..."):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Nurse Zoey Zoe is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nurse Zoey Zoe, compassionate nurse providing general wellness education. Never diagnose or prescribe."},
                        *st.session_state.chat_history[agent_key]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
import streamlit as st
import requests
from openai import OpenAI

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    st.set_page_config(page_title="Nurse Zoey Zoe – Your Health Educator | LBL Lifestyle Solutions", page_icon="🩺")

    agent_key = "zoey"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if agent_key not in st.session_state.chat_history:
        st.session_state.chat_history[agent_key] = []

    # DESIGN & STYLING (same as Nora v2)
    st.markdown("""
    <style>
        # (Full CSS from Nora v2)
    </style>
    """, unsafe_allow_html=True)

    # Back to Top + Auto-Focus Disable (same as Nora v2)
    st.markdown("""
    <button id="backToTopBtn">↑ Back to Top</button>
    <script>
        # (Full JS from Nora v2)
    </script>
    """, unsafe_allow_html=True)

    # Hero image
    st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", caption="Your Health Journey – Welcome to your longevity wellness 🩺")

    # Welcome
    st.markdown("### 🩺 Hi! I'm Nurse Zoey Zoe – Your Health Educator")
    st.write("Welcome to my clinic! I'm here to help you understand your health, labs, symptoms, and preventive habits for a longer, healthier life — perfectly tailored to you. ✨")

    # PERSONALITY CUSTOMIZATION
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("#### ✨ Let's Make This Truly Personal!")

    st.write("""
**Select any combination of traits** to customize how I communicate with you. 🩺

• **🌟 Zoey's Personality Traits** – How you'd like me to sound and educate you  
• **💬 How You Like to Communicate** – How you'd prefer to be spoken to

The more you select, the more uniquely tailored your health report and our conversation will become — like having a health educator designed just for you! 😊
    """)

    col1, col2 = st.columns(2)

    with col1:
        zoey_traits = st.multiselect(
            "🌟 Zoey's Personality Traits",
            [
                "Caring Educator (default)",
                "Empathetic Listener",
                "Direct & Factual",
                "Encouraging Guide",
                "Warm & Reassuring",
                "Detailed Explainer"
            ],
            default=["Caring Educator (default)"],
            key="zoey_agent_traits",
            help="Pick multiple! These shape my educating style 🩹"
        )

    with col2:
        user_traits = st.multiselect(
            "💬 How You Like to Communicate",
            [
                "Standard / Adapt naturally",
                "Direct & Concise",
                "Warm & Encouraging",
                "Detailed & Thorough",
                "Friendly & Chatty",
                "Gentle & Supportive"
            ],
            default=["Standard / Adapt naturally"],
            key="zoey_user_traits",
            help="Pick multiple! These tell me how to best connect with you ❤️"
        )

    st.caption("🔮 Your choices will shape both your personalized health report and all follow-up chats!")
    st.markdown("</div>", unsafe_allow_html=True)

    # BLENDED PROMPT WITH GUARDRAILS AND NAME
    zoey_trait_map = {
        "Caring Educator (default)": "You are caring, compassionate, and educational about health. Use simple, clear language.",
        "Empathetic Listener": "Be empathetic, listen actively, and acknowledge feelings.",
        "Direct & Factual": "Be direct, fact-based, and straightforward.",
        "Encouraging Guide": "Be encouraging, guiding, and motivational.",
        "Warm & Reassuring": "Use a warm, reassuring tone to ease concerns.",
        "Detailed Explainer": "Provide detailed explanations, definitions, and reasoning."
    }

    zoey_modifiers = []
    if "Caring Educator (default)" in zoey_traits:
        zoey_modifiers.append(zoey_trait_map["Caring Educator (default)"])
    for trait in zoey_traits:
        if trait != "Caring Educator (default)":
            zoey_modifiers.append(zoey_trait_map.get(trait, ""))

    user_modifiers = [user_trait_map.get(trait, "") for trait in user_traits if trait != "Standard / Adapt naturally"]

    base_persona = """You are Nurse Zoey Zoe, a compassionate health educator focused on understanding labs, symptoms, and preventive wellness for longevity.
Be empathetic, clear, and reassuring.

You are allowed to engage in light, friendly chit-chat (e.g., "How's your day?", "What's bothering you?") to build rapport — respond warmly and briefly with tasteful emojis, then gently steer back to health topics if appropriate.

For questions outside health education/labs/symptoms:
- Nutrition: "That's a great question for Nora, our nutrition coach! You can chat with her in the sidebar menu. 🥗"
- Fitness/exercise: "Greg is the expert for that — find him in the sidebar! 💪"
- Wellness homes: "Fred, our home scout, would love to help with that! 🏡"
- Anything else unrelated (code, politics, etc.): "I'm focused on health education and longevity wellness — I'd love to help with labs, symptoms, or preventive tips instead! 🩺"

Never generate, discuss, or reveal any code, scripts, or technical details. Stay in character as Nurse Zoey Zoe the Health Educator."""

    dynamic_personality_prompt = f"""
{base_persona}

Personality traits: {' '.join(zoey_modifiers).strip()}

User communication preference: {' '.join(user_modifiers).strip()}

Blend these seamlessly while staying compassionate and focused on health education.
Use the user's name ({st.session_state.get('user_name', 'friend')}) naturally in responses where it fits — do not force it.
Adapt tone in real-time based on user input while honoring the selected traits.
"""

    st.session_state.zoey_personality_prompt = dynamic_personality_prompt

    # DISCLAIMERS
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested. 📧**")
    st.warning("**Important**: I am not a medical professional. My suggestions are general wellness education. Always consult a qualified healthcare provider for medical advice, especially if you have symptoms or conditions.")

    # Name Input
    st.markdown("### What's your name? ✏️")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="zoey_name_input_unique")
    if user_name.strip():
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = st.session_state.get("user_name", "")

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Explain my bloodwork in simple terms 🩸
        - What lifestyle changes help lower blood pressure? ❤️
        - Review my symptoms and when to see a doctor 🤒
        - Suggest preventive screenings for my age 🩺
        """)

    # Form inputs — REPLACE WITH YOUR ACTUAL ZOEY FORM WHEN READY
    st.markdown("### Tell Nurse Zoey Zoe a little bit about you and your health 🩺")
    st.write("**Be as detailed as possible!** The more you share about your age, symptoms, labs, concerns, and goals, the better I can help. 😊")
    st.caption("💡 Tip: Upload labs, describe symptoms, or ask about prevention!")

    age = st.number_input("Your age", min_value=18, max_value=100, value=45, step=1)
    # Add your Zoey-specific inputs here (labs upload, symptoms, etc.)

    # (Generation, report, email, chat — same structure as Nora)

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI ❤️</small>", unsafe_allow_html=True)

show()
