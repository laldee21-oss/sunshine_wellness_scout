import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["XAI_API_KEY"],
    base_url="https://api.x.ai/v1"
)

def show():
    st.title("💪 Greg – Fitness Coach")

    st.markdown("Have a follow-up question? Chat with me!")

    # System prompt - Greg's personality
    system_prompt = {
        "role": "system",
        "content": (
            "You are Greg, an energetic, supportive, and knowledgeable Fitness Coach. "
            "You help people over 40 build sustainable strength, mobility, balance, and energy — "
            "especially for an active Florida lifestyle. You create practical workout plans using "
            "bodyweight, minimal equipment, or home gyms. You're motivating but realistic, "
            "emphasizing form, recovery, progression, and enjoyment. You never push extreme diets or fads."
        )
    }

    for message in st.session_state.chat_history["greg"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Greg about workouts, strength, mobility, recovery, home routines..."):
        st.session_state.chat_history["greg"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Greg is designing your plan..."):
                messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history["greg"]
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

        st.session_state.chat_history["greg"].append({"role": "assistant", "content": reply})

    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

show()
