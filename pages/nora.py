import streamlit as st
import requests
from openai import OpenAI

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
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

    st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)

    if st.button("← Back to Team", key="nora_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    st.image("https://i.postimg.cc/cJqPm9BP/pexels-tessy-agbonome-521343232-18252407.jpg", caption="Fuel Your Longevity")

    st.markdown("### 🥗 HI! I'M NORA – Your Nutrition Coach for Longevity")
    st.success("**This tool is completely free – no cost, no obligation!**")
    st.write("I help you build sustainable, delicious eating habits that fit your life — focusing on balance, joy, and long-term health.")
    st.warning("**Important**: I am not a registered dietitian. This is general wellness education. Consult a professional for medical conditions.")

    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="nora_name_input")
    if user_name:
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = "there"

    with st.expander("💡 Quick Start Ideas"):
        st.markdown("""
        - Create a 7-day plan with $100 grocery budget
        - Build meals around my 40/30/30 macros
        - Suggest snacks that won't spike blood sugar
        - Make family-friendly Mediterranean recipes
        """)

    st.markdown("### Tell Nora a little bit about you and your eating habits")
    age = st.number_input("Your age", min_value=18, max_value=100, value=45, key="nora_age")
    goals = st.multiselect("PRIMARY NUTRITION GOALS", ["Longevity/anti-aging", "Energy & vitality", "Heart health", "Weight management", "Gut health", "Brain health", "Muscle maintenance", "General wellness"], key="nora_goals")

    dietary_options = ["Mediterranean", "Plant-based", "Omnivore", "Pescatarian", "Keto", "Low-carb", "No restrictions"]
    selected_dietary = st.multiselect("DIETARY PREFERENCES", dietary_options, default=["No restrictions"], key="nora_dietary")

    allergies = st.text_area("ALLERGIES OR INTOLERANCES? (optional)", key="nora_allergies")
    budget_level = st.selectbox("WEEKLY GROCERY BUDGET LEVEL", ["Budget-conscious", "Moderate", "Premium/organic focus"], key="nora_budget")
    cooking_time = st.selectbox("TIME AVAILABLE FOR COOKING", ["<20 min/meal", "20–40 min/meal", "40+ min/meal (love cooking)"], key="nora_cooking")
    meals_per_day = st.slider("MEALS PER DAY YOU WANT PLANS FOR", 2, 5, 3, key="nora_meals")
    macro_input = st.text_input("Optional: Daily Macro Targets (e.g., 40/30/30)", placeholder="Leave blank for balanced", key="nora_macros")

    greg_plan_file = st.file_uploader("Optional: Upload Greg's workout plan", type=["txt", "pdf", "png", "jpg", "jpeg"], key="nora_greg_upload")
    greg_plan_text = ""
    if greg_plan_file:
        try:
            greg_plan_text = greg_plan_file.read().decode("utf-8")
        except:
            greg_plan_text = "[Greg's plan uploaded]"

    plan_sections = st.multiselect("Add optional sections:", [
        "Blue Zones Focus", "Supplement Education (general)", "Meal Prep Strategies",
        "Eating Out Tips", "Hydration & Beverage Guide", "Seasonal/Longevity Food Focus",
        "Family-Friendly Adaptations"
    ], default=["Meal Prep Strategies"], key="nora_sections")

    if st.button("Generate My Custom Meal Plan", type="primary", key="nora_generate"):
        with st.spinner("Nora is crafting your plan..."):
            core_prompt = """
### Weekly Meal Plan
7-day plan with specified meals/day. Include portion guidance and variety.
### Grocery List
Organized by category.
### Longevity Nutrition Principles
Key habits and why they matter.
"""
            optional_prompt = ""
            if "Blue Zones Focus" in plan_sections: optional_prompt += "### Blue Zones Focus\nTips and recipes.\n\n"
            if "Supplement Education (general)" in plan_sections: optional_prompt += "### Supplement Education (general)\nOverview — consult doctor.\n\n"
            if "Meal Prep Strategies" in plan_sections: optional_prompt += "### Meal Prep Strategies\nTime-saving tips.\n\n"
            if "Eating Out Tips" in plan_sections: optional_prompt += "### Eating Out Tips\nHealthy choices.\n\n"
            if "Hydration & Beverage Guide" in plan_sections: optional_prompt += "### Hydration & Beverage Guide\nBest drinks.\n\n"
            if "Seasonal/Longevity Food Focus" in plan_sections: optional_prompt += "### Seasonal/Longevity Food Focus\nCurrent best foods.\n\n"
            if "Family-Friendly Adaptations" in plan_sections: optional_prompt += "### Family-Friendly Adaptations\nAdjustments for family.\n\n"

            full_plan_prompt = core_prompt + optional_prompt + """
### Blue Zones Focus
### Supplement Education (general)
### Meal Prep Strategies
### Eating Out Tips
### Hydration & Beverage Guide
### Seasonal/Longevity Food Focus
### Family-Friendly Adaptations
"""

            base_prompt = f"""
User name: {st.session_state.user_name}
Age: {age}
Goals: {', '.join(goals)}
Dietary: {', '.join(selected_dietary)}
Macros: {macro_input or 'Balanced'}
Allergies: {allergies or 'None'}
Budget: {budget_level}
Cooking time: {cooking_time}
Greg's plan: {greg_plan_text or 'None'}
You are Nora, warm, evidence-based nutrition coach. Focus on joy, flavor, and sustainability.
"""

            try:
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nora, warm nutrition coach."}, {"role": "user", "content": base_prompt + core_prompt + optional_prompt}],
                    max_tokens=2500,
                    temperature=0.7
                )
                display_plan = display_response.choices[0].message.content

                full_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nora, warm nutrition coach."}, {"role": "user", "content": base_prompt + full_plan_prompt}],
                    max_tokens=3500,
                    temperature=0.7
                )
                full_plan = full_response.choices[0].message.content

                st.success("Nora's custom nutrition plan for you!")
                st.markdown(display_plan)
                st.session_state.full_plan_for_email = full_plan
                st.info("📧 Want the complete version? Fill in email below!")
            except Exception as e:
                st.error("Nora is in the kitchen... try again.")

    if "full_plan_for_email" in st.session_state:
        st.markdown("### Get Your Full Plan Emailed")
        with st.form("lead_form_nora", clear_on_submit=True):
            name = st.text_input("Your Name", key="nora_email_name")
            email = st.text_input("Email (required)", key="nora_email")
            phone = st.text_input("Phone (optional)", key="nora_phone")
            submitted = st.form_submit_button("📧 Send My Full Plan")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    plan_to_send = st.session_state.full_plan_for_email
                    email_body = f"""Hi {st.session_state.user_name},
Thank you for exploring nutrition with Nora!
Here's your COMPLETE longevity meal plan:
{plan_to_send}
Enjoy every bite!
Best,
Nora & the LBL Team"""
                    data = {"from": "reports@lbllifestyle.com", "to": [email], "cc": [YOUR_EMAIL], "subject": "Your LBL Nutrition Plan", "text": email_body}
                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Sent to {email}!")
                            st.balloons()
                            del st.session_state.full_plan_for_email
                    except Exception as e:
                        st.error("Send error.")

    st.markdown("### Have a follow-up question? Chat with Nora! 🥗")
    for msg in st.session_state.chat_history.get("nora", []):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask Nora...", key="nora_chat_input"):
        st.session_state.chat_history.setdefault("nora", []).append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Nora is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nora, warm nutrition coach."}] + st.session_state.chat_history["nora"],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["nora"].append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.write(reply)
            except Exception as e:
                st.error("Connection issue.")

    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Powered by Grok (xAI)</small>", unsafe_allow_html=True)

show()
