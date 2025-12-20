import streamlit as st
from openai import OpenAI

# xAI API Client
client = OpenAI(
    api_key=st.secrets["XAI_API_KEY"],
    base_url="https://api.x.ai/v1"
)

def show():
    st.title("🛋️ Fred – Wellness Home Scout")

    st.markdown("Have a follow-up question? Chat with me!")

    # System prompt - Fred's personality
    system_prompt = {
        "role": "system",
        "content": (
            "You are Fred, a warm, practical, and insightful Wellness Home Scout. "
            "You specialize in helping people create living spaces that promote calm, recovery, "
            "natural light, air quality, ergonomics, and longevity. You give specific, actionable advice "
            "about layout, furniture, plants, lighting, decluttering, and Florida-friendly home features. "
            "You're encouraging, non-judgmental, and focused on realistic improvements."
        )
    }

    # Display chat history
    for message in st.session_state.chat_history["fred"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask Fred about your home environment, sleep sanctuary, lighting, plants, decluttering..."):
        # Append user message
        st.session_state.chat_history["fred"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Fred is thinking about your space..."):
                messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history["fred"]
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

        # Append assistant reply
        st.session_state.chat_history["fred"].append({"role": "assistant", "content": reply})

    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

# Required for import in main
show()
