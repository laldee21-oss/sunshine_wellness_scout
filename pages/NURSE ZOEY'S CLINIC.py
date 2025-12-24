import streamlit as st
import requests
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
    st.set_page_config(page_title="Nurse Zoey Zoe – Your Health Educator | LBL Lifestyle Solutions", page_icon="🩺")

    agent_key = "zoey"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if agent_key not in st.session_state.chat_history:
        st.session_state.chat_history[agent_key] = []

    # DESIGN & STYLING (same as Nora v2.1 — with bottom-left button)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
       
        .stApp {
            background: linear-gradient(to bottom, #f5f7fa, #e0e7f0);
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
        .stMultiSelect > div > div > div,
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        .stMultiSelect > div {
            background-color: white !important;
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
        .personality-box {
            background-color: #f0f7fc;
            border: 2px solid #a0c4d8;
            border-radius: 16px;
            padding: 24px;
            margin: 30px 0;
            text-align: center;
        }
        .separator {
            margin: 35px 0;
            border-top: 1px solid #c0d8e0;
        }
        /* Back to Top Button — Bottom-Left */
        #backToTopBtn {
            position: fixed;
            bottom: 120px;
            left: 20px;
            z-index: 999;
            display: none;
            background-color: #2d6a4f;
            color: white;
            padding: 14px 18px;
            border-radius: 50px;
            border: none;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        #backToTopBtn:hover {
            background-color: #40916c;
            transform: scale(1.1);
        }
        #report-anchor, #chat-anchor {
            margin-top: 100px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Back to Top Button + Disable Chat Auto-Focus
    st.markdown("""
    <button id="backToTopBtn">↑ Back to Top</button>
    <script>
        const btn = document.getElementById('backToTopBtn');
        const checkScroll = () => {
            const scrolled = window.pageYOffset > 300 ||
                             (parent.document.body.scrollTop > 300) ||
                             (parent.document.documentElement.scrollTop > 300) ||
                             (parent.document.querySelector('section.main') && parent.document.querySelector('section.main').scrollTop > 300);
            btn.style.display = scrolled ? 'block' : 'none';
        };
        window.addEventListener('load', checkScroll);
        window.addEventListener('scroll', checkScroll);
        const mainSection = parent.document.querySelector('section.main');
        if (mainSection) mainSection.addEventListener('scroll', checkScroll);
        btn.addEventListener('click', () => {
            window.scrollTo({top: 0, behavior: 'smooth'});
            if (mainSection) mainSection.scrollTo({top: 0, behavior: 'smooth'});
        });
        checkScroll();

        // Disable auto-focus on chat input
        setTimeout(() => {
            const chatInputs = document.querySelectorAll('input[type="text"]');
            chatInputs.forEach(input => {
                if (input.placeholder && input.placeholder.includes("Ask Nurse Zoey Zoe")) {
                    input.blur();
                }
            });
        }, 500);
    </script>
    """, unsafe_allow_html=True)

    # Hero image (correct Zoey image)
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

The more you select, the more uniquely tailored your health insights and our conversation will become — like having a health educator designed just for you! 😊
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

    st.caption("🔮 Your choices will shape both your personalized health insights and all follow-up chats!")
    st.markdown("</div>", unsafe_allow_html=True)

    # BLENDED PERSONALITY PROMPT WITH GUARDRAILS AND NAME
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
    st.success("**This tool is completely free – no cost, no obligation! Your full insights will be emailed if requested. 📧**")
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

    # Form inputs (clean placeholder — replace with your actual Zoey form when ready)
    st.markdown("### Tell Nurse Zoey Zoe a little bit about you and your health 🩺")
    st.write("**Be as detailed as possible!** The more you share about your age, symptoms, labs, concerns, and goals, the better I can help. 😊")
    st.caption("💡 Tip: Upload labs, describe symptoms, or ask about prevention!")

    age = st.number_input("Your age", min_value=18, max_value=100, value=45, step=1)
    symptoms = st.text_area("Current symptoms or concerns (optional)", height=150)
    labs_upload = st.file_uploader("Upload labs or reports (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"], key="zoey_labs_upload")
    health_goals = st.multiselect("PRIMARY HEALTH GOALS 🎯", ["Longevity", "Energy & vitality", "Heart health", "Immune support", "Sleep improvement", "Stress reduction", "General wellness"])

    # Session state for persistence
    if "display_insights" not in st.session_state:
        st.session_state.display_insights = None
    if "full_insights_for_email" not in st.session_state:
        st.session_state.full_insights_for_email = None

    # GENERATE INSIGHTS
    if st.button("Get Insights 🩺", type="primary"):
        with st.spinner("Nurse Zoey Zoe is reviewing your health profile... ✨"):
            # (Your original Zoey prompt logic here — adapted to use personality prompt)
            # For now, placeholder
            core_prompt = """
### Health Insights Summary
Key takeaways from your profile.
### Preventive Recommendations
Lifestyle habits for longevity.
### When to See a Doctor
Red flags and next steps.
"""
            # ... (add your full Zoey prompt building)

            base_prompt = f"""
User name: {st.session_state.user_name or 'friend'}
Age: {age}
Symptoms: {symptoms or 'None reported'}
Health goals: {', '.join(health_goals)}
Labs uploaded: {'Yes' if labs_upload else 'No'}
"""

            try:
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": st.session_state.zoey_personality_prompt}, {"role": "user", "content": base_prompt + "\n" + core_prompt}],
                    max_tokens=2500,
                    temperature=0.7
                )
                display_insights = display_response.choices[0].message.content

                # Full version logic here...

                st.session_state.display_insights = display_insights
                # st.session_state.full_insights_for_email = full_insights

                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": f"Hey {st.session_state.get('user_name', 'friend')}! 🎉 Your personalized health insights are ready below. Feel free to ask me anything about them! 🩺"})

                st.markdown("""
                <script>
                    const reportAnchor = document.getElementById('report-anchor');
                    if (reportAnchor) {
                        reportAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                </script>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Nurse Zoey Zoe is reviewing your profile... try again soon. 🩺")
                st.caption(f"Error: {str(e)}")

    # SINGLE INSIGHTS DISPLAY
    if st.session_state.display_insights:
        st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
        st.success("Nurse Zoey Zoe's health insights for you! 🎉")
        st.markdown(st.session_state.display_insights)

        st.markdown("### Would you like me to... ❓")
        st.markdown("""
        - Explain any part in more detail? 🔍
        - Suggest preventive habits? 🌱
        - Help interpret labs? 🩸
        - Recommend when to see a doctor? 👩‍⚕️
        """)

        st.info("📧 Want the **complete version**? Fill in the email form below!")

    # EMAIL FORM
    if st.session_state.full_insights_for_email:
        st.markdown("### Get Your Full Insights Emailed (Save & Share) 📧")
        with st.form("lead_form_zoey"):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Insights")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    # (your email sending logic)
                    st.success(f"Full insights sent to {email}! Check your inbox. 🎉")
                    st.balloons()

    # CHAT SECTION
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Have a follow-up question? Chat with Nurse Zoey Zoe in the box below! 🩺✨")
    st.caption("Ask about symptoms, habits, prevention — I'm here to educate and support.")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Nurse Zoey Zoe a question... 🩺"):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Nurse Zoey Zoe is thinking... 🤔"):
            try:
                messages = [
                    {"role": "system", "content": st.session_state.zoey_personality_prompt},
                    *st.session_state.chat_history[agent_key]
                ]

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content

                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon. 🌱")

        # Scroll to chat
        st.markdown("""
        <script>
            const chatAnchor = document.getElementById('chat-anchor');
            if (chatAnchor) {
                chatAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            const main = parent.document.querySelector('section.main');
            if (main) {
                main.scrollTop = main.scrollHeight;
            }
            setTimeout(() => {
                if (chatAnchor) chatAnchor.scrollIntoView({ behavior: 'smooth' });
                if (main) main.scrollTop = main.scrollHeight;
            }, 300);
        </script>
        """, unsafe_allow_html=True)

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI ❤️</small>", unsafe_allow_html=True)

show()
