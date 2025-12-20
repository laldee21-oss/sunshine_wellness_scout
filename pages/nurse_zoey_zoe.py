import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["XAI_API_KEY"],
    base_url="https://api.x.ai/v1"
)

def show():
    st.title("🩺 Nurse Zoey Zoe – Health Advisor")

    st.markdown("Have a follow-up question? Chat with me!")

    # System prompt - Zoey's personality
    system_prompt = {
        "role": "system",
        "content": (
            "You are Nurse Zoey Zoe, a compassionate, evidence-based registered nurse and health educator. "
            "You provide clear, accurate, practical advice on preventive care, symptom understanding, "
            "sleep, stress management, nutrition basics, longevity habits, and when to see a doctor. "
            "You never diagnose or prescribe — you educate and empower. "
            "You're warm, patient, and focused on sustainable wellness for lifelong health."
        )
    }

    for message in st.session_state.chat_history["zoey"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Zoey about sleep, stress, symptoms, prevention, healthy habits..."):
        st.session_state.chat_history["zoey"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Zoey is preparing thoughtful advice..."):
                messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history["zoey"]
                ]

                response = client.chat.completions.create(
                    model="grok-4-1-fast-reasoning",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=False
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.chat_history["zoey"].append({"role": "assistant", "content": reply})

    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

show()
