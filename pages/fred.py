import streamlit as st
import requests
from openai import OpenAI

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def fetch_pexels_image(neighborhood="", location_hint="", theme_hints=""):
    if not PEXELS_API_KEY:
        return None
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search"
    queries = []
    if neighborhood and location_hint:
        queries.append(f"{neighborhood} {location_hint} neighborhood homes landscape nature aerial view")
    if neighborhood:
        queries.append(f"{neighborhood} residential homes nature")
    if location_hint:
        queries.append(f"{location_hint} city skyline landscape homes nature")
        queries.append(f"{location_hint} scenic view aerial")
    if theme_hints:
        queries.append(f"{location_hint or 'USA'} {theme_hints} landscape nature")
    queries.append("wellness home nature landscape sunset")

    seen_urls = set()
    for query in queries:
        params = {"query": query, "per_page": 3, "orientation": "landscape"}
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for photo in data.get("photos", []):
                    img_url = photo["src"]["large2x"]
                    if img_url not in seen_urls:
                        seen_urls.add(img_url)
                        return img_url
        except:
            continue
    return None

def add_images_to_report(report_text, location_hint="", client_needs=""):
    lines = report_text.split('\n')
    enhanced_lines = []
    in_top_5 = False
    seen_urls = set()
    lower_needs = client_needs.lower()
    theme_hints = ""
    if any(word in lower_needs for word in ["beach", "ocean", "tampa", "florida", "coast"]):
        theme_hints = "beach ocean sunset palm trees waterfront"
    elif any(word in lower_needs for word in ["mountain", "asheville", "colorado", "hike", "trail", "cabins"]):
        theme_hints = "mountains cabins forest autumn nature scenic"
    elif any(word in lower_needs for word in ["lake", "waterfront"]):
        theme_hints = "lake waterfront homes nature"

    for line in lines:
        enhanced_lines.append(line)
        if "Top 5 Neighborhoods" in line or "Top 5 Suburbs" in line:
            in_top_5 = True
        if in_top_5 and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            parts = line.split('-', 1)
            if len(parts) > 1:
                name_part = parts[0].strip()[2:].strip()
                img_url = fetch_pexels_image(name_part, location_hint, theme_hints)
                if img_url and img_url not in seen_urls:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"![{name_part} – Beautiful homes and scenery]({img_url})")
                    enhanced_lines.append("")
                    seen_urls.add(img_url)
    return '\n'.join(enhanced_lines)

def show():
    st.markdown("""
    <style>
        /* Same styling as other agents */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        .stApp { background: linear-gradient(to bottom, #f5f7fa, #e0e7f0); color: #1e3a2f; font-family: 'Inter', sans-serif; }
        h1, h2, h3 { font-family: 'Playfair Display', serif; color: #2d6a4f; font-weight: 600; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: white !important; color: #1e3a2f !important; border: 2px solid #a0c4d8 !important; border-radius: 10px !important; padding: 12px !important; }
        .stButton>button { background-color: #2d6a4f; color: white; border-radius: 12px; font-weight: 600; }
        .stButton>button:hover { background-color: #40916c; }
        img { border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<script>window.scrollTo(0, 0); const mainSection = window.parent.document.querySelector('section.main'); if (mainSection) mainSection.scrollTop = 0;</script>", unsafe_allow_html=True)

    if st.button("← Back to Team", key="fred_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg_J1J8SDEAY-unsplash.jpg", caption="Your Keys Await – Welcome to your longevity lifestyle")

    st.markdown("### 🏡 Hello! I'm Fred – Your Wellness Home Scout")
    st.write("I'm here to help you find or create a home environment that actively supports your health, recovery, and longevity — anywhere in the U.S.")
    st.warning("**Important**: I am not a licensed real estate agent. My recommendations are general wellness education based on research and trends. Always consult a licensed professional for real estate decisions.")
    st.success("**This tool is completely free – no cost, no obligation! Your full report will be emailed if requested.**")

    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="fred_name_input")
    if user_name:
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = "there"

    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        - Find quiet neighborhoods with trails near Tampa
        - Suggest homes with gym space under $600k
        - Compare walkability in Asheville vs Sarasota
        - Modify my current home for aging in place
        """)

    st.markdown("### Tell Fred a little bit about you and your dream wellness home")
    client_needs = st.text_area("Share your story – the more details, the better!", height=280, key="fred_needs")

    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000, key="fred_budget")
    with col2:
        location = st.text_input("Preferred state or area", value="", key="fred_location")

    location_hint = location.strip() if location else "wellness community USA"

    report_sections = st.multiselect("Add optional sections:", [
        "Wellness/Outdoor Highlights", "Cost of Living & Financial Breakdown",
        "Healthcare Access & Longevity Metrics", "Community & Social Wellness",
        "Climate & Seasonal Wellness Tips", "Transportation & Daily Convenience",
        "Future-Proofing for Aging in Place", "Sample Daily Wellness Routine in This Area",
        "Top Property Recommendations"
    ], default=["Wellness/Outdoor Highlights", "Cost of Living & Financial Breakdown", "Healthcare Access & Longevity Metrics"], key="fred_sections")

    if st.button("🔍 GENERATE MY REPORT", type="primary", key="fred_generate"):
        if not client_needs.strip():
            st.warning("Please share your story so Fred can help!")
        else:
            with st.spinner("Fred is crafting your report..."):
                # Core prompt logic here (you already have this in your original)
                # For brevity, placeholder — replace with your full prompt
                base_prompt = f"User: {st.session_state.user_name}\nNeeds: {client_needs}\nBudget: ${budget}\nLocation: {location}\nSections: {', '.join(report_sections)}"
                # Call API twice: display (short) + full (long)
                # Then use add_images_to_report()
                # Example placeholder:
                display_report = "Sample report..."  # Replace with actual API call
                full_report = "Full detailed report..."  # Replace
                display_with_images = add_images_to_report(display_report, location_hint, client_needs)
                full_with_images = add_images_to_report(full_report, location_hint, client_needs)

                st.success("Fred found your perfect matches!")
                st.markdown(display_with_images)
                st.session_state.full_report_for_email = full_with_images
                st.info("📧 Want the complete version? Fill in email below!")

    # Email form and chat — same pattern as others (add if needed)

    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Powered by Grok (xAI)</small>", unsafe_allow_html=True)

# Note: You can expand Fred's generation logic later using the same pattern as Greg/Nora/Zoey
