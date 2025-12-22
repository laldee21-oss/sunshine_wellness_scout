import streamlit as st
import requests
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # HIGH-CONTRAST PROFESSIONAL DESIGN
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
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
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

    # Scroll to top
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
        const mainSection = window.parent.document.querySelector('section.main');
        if (mainSection) mainSection.scrollTop = 0;
    </script>
    """, unsafe_allow_html=True)

    # Back button - UNIQUE KEY
    if st.button("← Back to Team", key="greg_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", caption="Greatness Awaits – Welcome to your longevity lifestyle")

    # Welcome & Disclaimer
    st.markdown("### 💪 HI!!! I'M GREG – Your Awesome Personal Trainer. GET SOME!!!!")
    st.write("I'm a motivated gym rat helping you build strength, endurance, and longevity. Let's get started by building you a personalized workout routine.")
    st.warning("**Important**: I am not a certified personal trainer or medical professional. My suggestions are general wellness education. Always consult a qualified trainer or doctor before starting a new exercise program.")
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested.**")

    # Name Input - UNIQUE KEY
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="greg_name_input")
    if user_name:
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = "there"

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        - Build a 3-day home workout for busy parents
        - Create a plan for beginners with bad knees
        - Add mobility work to my current routine
        - Design a program for better sleep and energy
        """)

    st.markdown("### Tell Greg a little bit about you and your fitness goals")
    st.caption("💡 Tip: Include age, injuries, equipment, days per week, and what motivates you!")

    age = st.number_input("Your age", min_value=18, max_value=100, value=45, step=1, key="greg_age")
    fitness_level = st.selectbox("CURRENT FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"], key="greg_fitness_level")
    goals = st.multiselect("PRIMARY GOALS", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"], key="greg_goals")
    equipment = st.multiselect("AVAILABLE EQUIPMENT", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"], key="greg_equipment")
    injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional)", placeholder="Example: Bad knee from old injury, avoid high-impact", key="greg_injuries")
    days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN", 1, 7, 4, key="greg_days")
    session_length = st.selectbox("PREFERRED SESSION LENGTH", ["20-30 minutes", "30-45 minutes", "45-60 minutes"], key="greg_session_length")

    plan_sections = st.multiselect(
        "Add optional sections:",
        ["Nutrition Guidelines", "Recovery & Mobility Tips", "Motivation & Habit Building", "Cardio Integration", "Home vs Gym Variations", "Scaling for Travel", "Long-Term Progression (12 weeks)"],
        default=["Nutrition Guidelines", "Recovery & Mobility Tips"],
        key="greg_sections"
    )

    if st.button("Generate My Custom Workout Plan", type="primary", key="greg_generate"):
        with st.spinner("Greg is building your plan..."):
            core_prompt = """
### Weekly Workout Plan
Create a full 7-day schedule with the specified training days and rest/recovery days.
Include warm-up, main workout (exercises, sets, reps, rest), cool-down/stretch.
### Progression Tips
How to advance safely over 4-8 weeks.
"""
            optional_prompt = ""
            if "Nutrition Guidelines" in plan_sections: optional_prompt += "### Nutrition Guidelines\nSimple, sustainable eating tips.\n\n"
            if "Recovery & Mobility Tips" in plan_sections: optional_prompt += "### Recovery & Mobility Tips\nSleep, stretching, foam rolling.\n\n"
            if "Motivation & Habit Building" in plan_sections: optional_prompt += "### Motivation & Habit Building\nMindset and consistency tips.\n\n"
            if "Cardio Integration" in plan_sections: optional_prompt += "### Cardio Integration\nSafe ways to add cardio.\n\n"
            if "Home vs Gym Variations" in plan_sections: optional_prompt += "### Home vs Gym Variations\nModifications for equipment.\n\n"
            if "Scaling for Travel" in plan_sections: optional_prompt += "### Scaling for Travel\nBodyweight-only options.\n\n"
            if "Long-Term Progression (12 weeks)" in plan_sections: optional_prompt += "### Long-Term Progression (12 weeks)\nPhase 2 and 3 ideas.\n\n"

            full_plan_prompt = core_prompt + optional_prompt + """
### Nutrition Guidelines
### Recovery & Mobility Tips
### Motivation & Habit Building
### Cardio Integration
### Home vs Gym Variations
### Scaling for Travel
### Long-Term Progression (12 weeks)
"""

            base_prompt = f"""
User name: {st.session_state.user_name}
Age: {age}
Fitness level: {fitness_level}
Goals: {', '.join(goals)}
Equipment: {', '.join(equipment) or 'Bodyweight only'}
Injuries: {injuries or 'None'}
Training {days_per_week} days/week, {session_length} sessions
You are Greg, an energetic, motivating personal trainer focused on sustainable strength and longevity for people over 40.
Be encouraging but realistic, emphasize form and safety.
"""

            try:
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Greg, motivating personal trainer."}, {"role": "user", "content": base_prompt + core_prompt + optional_prompt}],
                    max_tokens=2500,
                    temperature=0.7
